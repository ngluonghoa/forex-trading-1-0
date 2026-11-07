"""M2/P0.11 synthetic AES-GCM and memory-only witness/restart acceptance."""
from dataclasses import replace
from hashlib import sha256
import unittest

from forex_trading.synthetic_sealed_cache import (
    MAGIC, MAX_BYTES, SyntheticSeparateWitness, SyntheticSealedCacheSession,
    SyntheticUntrustedDriveStore, _envelope_digest, _manifest_digest,
    seal_synthetic_fixture, unseal_synthetic_fixture,
)

# Non-secret public TEST-ONLY constant. NEVER re-use in any real cache.
TEST_KEY = bytes(range(32))
KEY_REF = "TESTKEY-01"


def part(pair):
    return sha256(pair.encode("ascii")).hexdigest()


def fake(pair):
    return MAGIC + ("FAKE-PAIR-" + pair).encode("ascii")


def session(store=None, witness=None, *, key=TEST_KEY):
    return SyntheticSealedCacheSession(
        store if store is not None else SyntheticUntrustedDriveStore(),
        witness if witness is not None else SyntheticSeparateWitness(),
        key=key, key_ref=KEY_REF,
    )


def encrypt(pair="TESTPAIR00"):
    return seal_synthetic_fixture(
        fake(pair), key=TEST_KEY, partition=part(pair), generation=1,
        previous_manifest_sha256=None, key_ref=KEY_REF,
    )


def decrypt(blob, pair="TESTPAIR00", **overrides):
    options = dict(key=TEST_KEY, partition=part(pair), generation=1,
                   previous_manifest_sha256=None, key_ref=KEY_REF)
    options.update(overrides)
    return unseal_synthetic_fixture(blob, **options)


class SyntheticAeadAndRecoveryTests(unittest.TestCase):
    def test_aes256_roundtrip_and_ciphertext_does_not_contain_plaintext(self):
        sealed = encrypt()
        self.assertEqual(len(sealed.nonce), 12)
        self.assertNotIn(fake("TESTPAIR00"), sealed.ciphertext_with_tag)
        self.assertEqual(decrypt(sealed), fake("TESTPAIR00"))

    def test_fresh_encryptions_use_different_random_nonces(self):
        self.assertNotEqual(encrypt().nonce, encrypt().nonce)

    def test_wrong_32byte_key_fails_authentication(self):
        with self.assertRaisesRegex(ValueError, "AEAD_AUTHENTICATION_FAILED"):
            decrypt(encrypt(), key=b"X" * 32)

    def test_context_binding_rejects_other_pair_generation_parent_and_keyref(self):
        blob = encrypt()
        changes = (
            {"partition": part("TESTPAIR01")},
            {"generation": 2},
            {"previous_manifest_sha256": "a" * 64},
            {"key_ref": "OTHERKEY"},
        )
        for change in changes:
            with self.subTest(change=change), self.assertRaisesRegex(
                ValueError, "AUTHENTICATED_CONTEXT_MISMATCH"
            ):
                decrypt(blob, **change)

    def test_ciphertext_change_detected_even_if_plain_hash_recomputed(self):
        blob = encrypt()
        mutated = replace(
            blob, ciphertext_with_tag=blob.ciphertext_with_tag[:-1]
            + bytes([blob.ciphertext_with_tag[-1] ^ 1])
        )
        with self.assertRaisesRegex(ValueError, "SEALED_ENVELOPE_CORRUPT"):
            decrypt(mutated)
        mutated = replace(mutated, envelope_sha256=_envelope_digest(mutated))
        with self.assertRaisesRegex(ValueError, "AEAD_AUTHENTICATION_FAILED"):
            decrypt(mutated)

    def test_nonce_change_detected(self):
        blob = encrypt()
        bad = replace(blob, nonce=b"\x00" * 12)
        with self.assertRaisesRegex(ValueError, "SEALED_ENVELOPE_CORRUPT"):
            decrypt(bad)
        bad = replace(bad, envelope_sha256=_envelope_digest(bad))
        with self.assertRaisesRegex(ValueError, "AEAD_AUTHENTICATION_FAILED"):
            decrypt(bad)

    def test_bad_length_key_rejected(self):
        with self.assertRaisesRegex(ValueError, "AES256_KEY"):
            decrypt(encrypt(), key=b"bad")

    def test_real_fx_without_fixture_marker_rejected(self):
        with self.assertRaisesRegex(ValueError, "SYNTHETIC_FIXTURE_ONLY"):
            seal_synthetic_fixture(
                b"EURUSD ask=1.1", key=TEST_KEY,
                partition=part("TESTPAIR00"), generation=1,
                previous_manifest_sha256=None, key_ref=KEY_REF,
            )

    def test_empty_and_oversized_fake_payloads_rejected(self):
        for data in (MAGIC, MAGIC + b"X" * MAX_BYTES):
            with self.subTest(size=len(data)), self.assertRaisesRegex(
                ValueError, "SYNTHETIC_FIXTURE_ONLY"
            ):
                seal_synthetic_fixture(
                    data, key=TEST_KEY, partition=part("TESTPAIR00"),
                    generation=1, previous_manifest_sha256=None, key_ref=KEY_REF,
                )

    def test_invalid_partition_and_key_ref_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_PARTITION"):
            decrypt(encrypt(), partition="EURUSD")
        with self.assertRaisesRegex(ValueError, "INVALID_OPAQUE_KEY_REFERENCE"):
            decrypt(encrypt(), key_ref="bad")

    def test_reopen_with_new_session_uses_existing_encrypted_generation(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        first = session(store, witness)
        dig = first.commit(part("TESTPAIR00"), fake("TESTPAIR00"),
                           expected_manifest_sha256=None)
        later = session(store, witness)
        self.assertEqual(later.read(part("TESTPAIR00")),
                         (fake("TESTPAIR00"), dig))
        self.assertEqual(later.commit(part("TESTPAIR00"), fake("TESTPAIR00"),
                                      expected_manifest_sha256=dig), dig)
        self.assertEqual(store.chunk_writes, 1)

    def test_two_generations_and_stale_writer_are_fenced_locally(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        first = session(store, witness)
        p = part("TESTPAIR00")
        a = first.commit(p, fake("TESTPAIR00"), expected_manifest_sha256=None)
        b = session(store, witness).commit(
            p, fake("TESTPAIR01"), expected_manifest_sha256=a
        )
        with self.assertRaisesRegex(ValueError, "SIMULATED_STALE_WRITER"):
            first.commit(p, fake("TESTPAIR02"), expected_manifest_sha256=a)
        self.assertEqual(session(store, witness).read(p),
                         (fake("TESTPAIR01"), b))
        self.assertEqual(witness.claims[p][0], 2)

    def test_crash_after_stage_leaves_orphan_without_pointer_promotion(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        p = part("TESTPAIR00")
        a = s.commit(p, fake("TESTPAIR00"), expected_manifest_sha256=None)
        with self.assertRaisesRegex(RuntimeError, "CRASH_AFTER_STAGE"):
            s.commit(p, fake("TESTPAIR01"),
                     expected_manifest_sha256=a, failpoint="after_stage")
        self.assertEqual(store.chunk_writes, 2)
        self.assertEqual(session(store, witness).read(p),
                         (fake("TESTPAIR00"), a))

    def test_crash_between_pointer_and_witness_fails_closed_on_reopen(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        p = part("TESTPAIR00")
        a = s.commit(p, fake("TESTPAIR00"), expected_manifest_sha256=None)
        with self.assertRaisesRegex(RuntimeError, "CRASH_AFTER_POINTER_PUBLISH"):
            s.commit(p, fake("TESTPAIR01"), expected_manifest_sha256=a,
                     failpoint="after_publish_before_witness")
        with self.assertRaisesRegex(ValueError, "WITNESS_POINTER_DIVERGED"):
            session(store, witness).read(p)

    def test_rollback_pointer_to_old_generation_rejected_by_witness(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        p = part("TESTPAIR00")
        a = s.commit(p, fake("TESTPAIR00"), expected_manifest_sha256=None)
        s.commit(p, fake("TESTPAIR01"), expected_manifest_sha256=a)
        store.active[p] = a
        with self.assertRaisesRegex(ValueError, "WITNESS_POINTER_DIVERGED"):
            s.read(p)

    def test_missing_pointer_with_existing_witness_fails(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        p = part("TESTPAIR00")
        s.commit(p, fake("TESTPAIR00"), expected_manifest_sha256=None)
        store.active.pop(p)
        with self.assertRaisesRegex(ValueError, "WITNESS_POINTER_DIVERGED"):
            s.read(p)

    def test_missing_encrypted_chunk_detected(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        p = part("TESTPAIR00")
        digest = s.commit(p, fake("TESTPAIR00"),
                          expected_manifest_sha256=None)
        store.chunks.pop(store.manifests[digest].envelope_sha256)
        with self.assertRaisesRegex(ValueError, "ENCRYPTED_CHUNK_MISSING"):
            s.read(p)

    def test_missing_or_modified_manifest_detected(self):
        for remove in (True, False):
            store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
            s = session(store, witness)
            p = part("TESTPAIR00")
            digest = s.commit(p, fake("TESTPAIR00"),
                              expected_manifest_sha256=None)
            if remove:
                store.manifests.pop(digest)
            else:
                store.manifests[digest] = replace(
                    store.manifests[digest], plaintext_sha256="f" * 64
                )
            with self.subTest(remove=remove), self.assertRaisesRegex(
                ValueError, "MANIFEST_CHAIN_CORRUPT"
            ):
                s.read(p)

    def test_missing_ancestor_chunk_detected_even_when_latest_chunk_valid(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        p = part("TESTPAIR00")
        a = s.commit(p, fake("TESTPAIR00"), expected_manifest_sha256=None)
        s.commit(p, fake("TESTPAIR01"), expected_manifest_sha256=a)
        store.chunks.pop(store.manifests[a].envelope_sha256)
        with self.assertRaisesRegex(ValueError, "ENCRYPTED_CHUNK_MISSING"):
            s.read(p)

    def test_wrong_reopen_key_fails_closed(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        p = part("TESTPAIR00")
        session(store, witness).commit(p, fake("TESTPAIR00"),
                                       expected_manifest_sha256=None)
        with self.assertRaisesRegex(ValueError, "AEAD_AUTHENTICATION_FAILED"):
            session(store, witness, key=b"Y" * 32).read(p)

    def test_two_independent_pair_partitions_do_not_overwrite_each_other(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        a, b = part("TESTPAIR00"), part("TESTPAIR01")
        digest_a = s.commit(a, fake("TESTPAIR00"), expected_manifest_sha256=None)
        s.commit(b, fake("TESTPAIR01"), expected_manifest_sha256=None)
        self.assertEqual(s.read(a), (fake("TESTPAIR00"), digest_a))
        self.assertEqual(store.chunk_writes, 2)

    def test_5_to_20_to_1_to_20_fake_cross_session_scope_preserves_all(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        names = ["TESTPAIR%02d" % i for i in range(20)]
        first = session(store, witness)
        for n in names[:5]:
            first.commit(part(n), fake(n), expected_manifest_sha256=None)
        self.assertEqual(store.chunk_writes, 5)
        second = session(store, witness)
        for n in names:
            p = part(n)
            existing = second.read(p)
            second.commit(p, fake(n),
                          expected_manifest_sha256=existing[1] if existing else None)
        self.assertEqual(store.chunk_writes, 20)
        third = session(store, witness)
        n = names[3]
        p = part(n)
        third.commit(p, fake(n), expected_manifest_sha256=third.read(p)[1])
        fourth = session(store, witness)
        for n in names:
            p = part(n)
            fourth.commit(p, fake(n), expected_manifest_sha256=fourth.read(p)[1])
        self.assertEqual(store.chunk_writes, 20)
        self.assertEqual(len(store.active), 20)
        self.assertEqual(fourth.read(part(names[19]))[0], fake(names[19]))

    def test_source_never_stores_plaintext_keys_in_manifest(self):
        store, witness = SyntheticUntrustedDriveStore(), SyntheticSeparateWitness()
        s = session(store, witness)
        p = part("TESTPAIR00")
        digest = s.commit(p, fake("TESTPAIR00"), expected_manifest_sha256=None)
        manifest = store.manifests[digest]
        self.assertFalse(hasattr(manifest, "key"))
        self.assertEqual(manifest.key_ref, KEY_REF)
        self.assertNotIn(fake("TESTPAIR00"),
                         store.chunks[manifest.envelope_sha256].ciphertext_with_tag)

    def test_invalid_failpoint_rejected(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_SYNTHETIC_CRASH_POINT"):
            session().commit(part("TESTPAIR00"), fake("TESTPAIR00"),
                             expected_manifest_sha256=None, failpoint="erase_everything")


if __name__ == "__main__":
    unittest.main()
