"""M2/P0.12 reproducible byte fixtures from REAL Google Drive synthetic readback.

All bytes are harmless encrypted TESTPAIR00 with a PUBLIC TEST KEY from M2/P0.11.
These are local regression tests; CI does not contact Google Drive or any vendor.
"""
from dataclasses import replace
from hashlib import sha256
from json import dumps
import unittest

from forex_trading.synthetic_cloud_aead_receipt import (
    PARTITION, FIXTURE, verify_real_drive_encrypted_synthetic_receipt,
)
from forex_trading.synthetic_drive_receipt_validation import ObservedDriveFile
from forex_trading.synthetic_sealed_cache import (
    SealedSyntheticChunk, _envelope_digest,
)

KEY = bytes(range(32))  # INTENTIONALLY PUBLIC TEST KEY, never a real secret.
CHUNK_FOLDER = "1mE7Zx29kDjyN8DYfvZn4HYx-OIoYaScw"
MANIFEST_FOLDER = "1OPBHzq5sPNV9ohqlsfi_I5e35ve1qvkD"
CHUNK_ID = "1IfzBILWfo6dAPHBIdvPpY52QQ3XVsDaR"
MANIFEST_ID = "1Be06jBxGDpjeKHpzJdA0XMLHoY4I7lCF"
CIPHERTEXT = (
    "44482d0408645bffd0ec4d25f0317facc4c365390507d1bd2b74c8877859299a"
    "97bd4f17ffd86b46c43f07000d38279a4fcb04a5a6ddd21c63b167da4241151"
    "283c37568762ccb7bb38703053063b42f18c1ac8ba81ea27001fd10acef0379ca"
    "c8cf16f548efbb42ad39e7e44fe78ee56a6a97611bb78435ab395702"
)
SEAL = {
    "ciphertext_with_tag_hex": CIPHERTEXT,
    "envelope_sha256": "82fcbab6691d56dd958f550b44d0a0646c6eae3499c425449203f542c8eb2807",
    "generation": 1,
    "key_ref": "TESTKEY-01",
    "nonce_hex": "96fd291b97d4ba29395784a8",
    "partition": PARTITION,
    "previous_manifest_sha256": None,
}
CHUNK = {
    "chunk": SEAL, "plaintext_sha256":
    "32f7b9d4e5ea3ddae25c74bb4bb8f679ee76959241c04dfbb4b6af53aee1fe3a",
    "real_fx_data": False,
    "schema": "FX_SYNTHETIC_AEAD_FILE_V1",
    "synthetic_only": True, "test_key_public": True,
}
MANIFEST = {
    "chunk_drive_file_id": CHUNK_ID,
    "chunk_envelope_sha256": SEAL["envelope_sha256"],
    "chunk_exported_sha256":
    "80e77881ce0ed5f65ab243915282900b79c5bb99a67cef221a3c3c0a1d7805f0",
    "chunk_exported_size_bytes": 753,
    "generation": 1, "key_ref": "TESTKEY-01",
    "no_distributed_cas": True,
    "no_external_rollback_witness": True,
    "pair": "TESTPAIR00",
    "plain_sha256": CHUNK["plaintext_sha256"],
    "real_fx_data": False,
    "schema": "FX_SYNTHETIC_AEAD_DRIVE_MANIFEST_V1",
    "source_rights_verified": False,
    "synthetic_only": True,
    "test_key_public": True,
    "trade_allowed": False,
}


def raw(obj):
    # Observed from Google Docs -> text/plain export: UTF-8 BOM + canonical JSON.
    return b"\xef\xbb\xbf" + dumps(
        obj, separators=(",", ":"), sort_keys=True,
    ).encode("ascii")


def changed(obj: ObservedDriveFile, updated: bytes, prefix: str):
    return replace(
        obj, body=updated, file_name=prefix + sha256(updated).hexdigest()[:16] + ".txt",
    )


def inputs():
    cb, mb = raw(CHUNK), raw(MANIFEST)
    c = ObservedDriveFile(
        CHUNK_ID, CHUNK_FOLDER, "fxsynthetic-m2p12-aead-"
        + sha256(cb).hexdigest()[:16] + ".txt", "text/plain", cb,
    )
    m = ObservedDriveFile(
        MANIFEST_ID, MANIFEST_FOLDER, "fxsynthetic-m2p12-aead-manifest-"
        + sha256(mb).hexdigest()[:16] + ".txt", "text/plain", mb,
    )
    return c, m


def validate(c=None, m=None, *, key=KEY, chunk_folder=CHUNK_FOLDER,
             manifest_folder=MANIFEST_FOLDER):
    first, second = inputs()
    return verify_real_drive_encrypted_synthetic_receipt(
        c if c is not None else first, m if m is not None else second,
        chunk_folder=chunk_folder, manifest_folder=manifest_folder,
        public_test_key=key,
    )


def mutate_chunk(**kwargs):
    c, _ = inputs()
    payload = dict(CHUNK)
    payload.update(kwargs)
    return changed(c, raw(payload), "fxsynthetic-m2p12-aead-")


def mutate_seal(**kwargs):
    c, _ = inputs()
    payload = dict(CHUNK)
    payload["chunk"] = {**SEAL, **kwargs}
    return changed(c, raw(payload), "fxsynthetic-m2p12-aead-")


def mutate_manifest(**kwargs):
    _, m = inputs()
    return changed(m, raw({**MANIFEST, **kwargs}),
                   "fxsynthetic-m2p12-aead-manifest-")


class EncryptedRealConnectorReceiptTests(unittest.TestCase):
    def test_exact_real_downloaded_byte_digests(self):
        c, m = inputs()
        self.assertEqual(len(c.body), 753)
        self.assertEqual(len(m.body), 644)
        self.assertEqual(sha256(c.body).hexdigest(),
                         "80e77881ce0ed5f65ab243915282900b79c5bb99a67cef221a3c3c0a1d7805f0")
        self.assertEqual(sha256(m.body).hexdigest(),
                         "7686d6600288e8a433776e84c0f565aee733b08d22c2bb975078a11c08a4f373")
        self.assertEqual(len(FIXTURE), 108)

    def test_provenance_passes_synthetic_only_no_security_or_trading_claim(self):
        receipt = validate()
        self.assertTrue(receipt.fixture_integrity_verified)
        self.assertTrue(receipt.test_key_is_public)
        self.assertFalse(receipt.real_data_confidentiality_proven)
        self.assertFalse(receipt.live_fx_cache_permitted)
        self.assertFalse(receipt.multi_file_transaction_proven)
        self.assertFalse(receipt.external_antirollback_proven)
        self.assertFalse(receipt.may_trade)
        self.assertEqual(receipt.actual_drive_calls_from_validator, 0)

    def test_wrong_key_fails_aead(self):
        with self.assertRaisesRegex(ValueError, "AEAD_AUTHENTICATION_FAILED"):
            validate(key=b"Z" * 32)

    def test_bad_key_length_fails(self):
        with self.assertRaisesRegex(ValueError, "AES256_KEY"):
            validate(key=b"bad")

    def test_changed_ciphertext_even_with_matching_content_address_fails(self):
        mutated_hex = CIPHERTEXT[:-2] + (
            "ff" if CIPHERTEXT[-2:] != "ff" else "00"
        )
        sealed = replace(
            SealedSyntheticChunk(PARTITION, 1, None, "TESTKEY-01",
                                 bytes.fromhex(SEAL["nonce_hex"]),
                                 bytes.fromhex(mutated_hex), ""),
            envelope_sha256="",
        )
        rec = mutate_seal(
            ciphertext_with_tag_hex=mutated_hex,
            envelope_sha256=_envelope_digest(sealed),
        )
        with self.assertRaisesRegex(ValueError, "AEAD_AUTHENTICATION_FAILED"):
            validate(c=rec)

    def test_changed_nonce_and_stale_envelope_hash_fails(self):
        with self.assertRaisesRegex(ValueError, "SEALED_CHUNK_CONTENT_ADDRESS"):
            validate(c=mutate_seal(nonce_hex="00" * 12))

    def test_wrong_partition_context_rejected(self):
        with self.assertRaisesRegex(ValueError, "UNAPPROVED_SEALED_CHUNK_CONTEXT"):
            validate(c=mutate_seal(partition="f" * 64))

    def test_generation_rollback_or_spoofing_rejected(self):
        for value in (0, 2, True):
            with self.subTest(generation=value), self.assertRaisesRegex(
                ValueError, "UNAPPROVED_SEALED_CHUNK_CONTEXT"
            ):
                validate(c=mutate_seal(generation=value))

    def test_change_parent_or_key_ref_rejected(self):
        for change in ({"previous_manifest_sha256": "f" * 64},
                       {"key_ref": "OTHERKEY"}):
            with self.subTest(change=change), self.assertRaisesRegex(
                ValueError, "UNAPPROVED_SEALED_CHUNK_CONTEXT"
            ):
                validate(c=mutate_seal(**change))

    def test_chunk_content_address_filename_mismatch_rejected(self):
        c, _ = inputs()
        with self.assertRaisesRegex(ValueError, "CONTENT_ADDRESS_FILENAME_MISMATCH"):
            validate(c=replace(c, body=c.body + b" "))

    def test_manifest_content_address_filename_mismatch_rejected(self):
        _, m = inputs()
        with self.assertRaisesRegex(ValueError, "CONTENT_ADDRESS_FILENAME_MISMATCH"):
            validate(m=replace(m, body=m.body + b" "))

    def test_manifest_wrong_chunk_sha_or_id_or_size_fails(self):
        for change in (
            {"chunk_exported_sha256": "0" * 64},
            {"chunk_drive_file_id": "SOME_OTHER_FILE_ID"},
            {"chunk_exported_size_bytes": 752},
            {"chunk_exported_size_bytes": True},
            {"chunk_envelope_sha256": "f" * 64},
            {"plain_sha256": "e" * 64},
        ):
            with self.subTest(change=change), self.assertRaisesRegex(
                ValueError, "MANIFEST_REFERENCE_INTEGRITY_MISMATCH"
            ):
                validate(m=mutate_manifest(**change))

    def test_false_rights_or_release_claims_rejected(self):
        for change in (
            {"source_rights_verified": True},
            {"no_distributed_cas": False},
            {"no_external_rollback_witness": False},
            {"trade_allowed": True},
            {"real_fx_data": True},
            {"synthetic_only": False},
            {"test_key_public": False},
            {"pair": "EURUSD"},
        ):
            with self.subTest(change=change), self.assertRaisesRegex(
                ValueError, "MANIFEST_FALSE_RELEASE_CLAIM"
            ):
                validate(m=mutate_manifest(**change))

    def test_wrong_folders_fail_closed(self):
        c, m = inputs()
        with self.assertRaisesRegex(ValueError, "DRIVE_FOLDER_MISMATCH"):
            validate(c=replace(c, folder_id=MANIFEST_FOLDER))
        with self.assertRaisesRegex(ValueError, "DRIVE_FOLDER_MISMATCH"):
            validate(m=replace(m, folder_id=CHUNK_FOLDER))

    def test_same_folder_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "FOLDERS_MUST_BE_DISTINCT"):
            validate(manifest_folder=CHUNK_FOLDER)

    def test_duplicate_file_id_is_rejected(self):
        _, m = inputs()
        with self.assertRaisesRegex(ValueError, "SAME_CHUNK_MANIFEST_FILE_ID"):
            validate(m=replace(m, file_id=CHUNK_ID))

    def test_missing_bom_malformed_or_large_file_rejected(self):
        c, _ = inputs()
        samples = (
            (c.body[3:], "NOT_APPROVED_GOOGLE_DOCS_EXPORT_BYTES"),
            (b"not-json", "INVALID_BOUNDED_FILE_BYTES"),
            (b"\xef\xbb\xbf{" + b"x" * 20000, "INVALID_BOUNDED_FILE_BYTES"),
        )
        for b, reason in samples:
            bad = changed(c, b, "fxsynthetic-m2p12-aead-")
            with self.subTest(size=len(b)), self.assertRaisesRegex(ValueError, reason):
                validate(c=bad)

    def test_extra_chunk_or_manifest_fields_rejected(self):
        c = mutate_chunk(unexpected="evil")
        with self.assertRaisesRegex(ValueError, "CHUNK_FIELDS_UNEXPECTED"):
            validate(c=c)
        m = mutate_manifest(unexpected="evil")
        with self.assertRaisesRegex(ValueError, "MANIFEST_FIELDS_UNEXPECTED"):
            validate(m=m)

    def test_duplicate_json_keys_rejected(self):
        _, m = inputs()
        raw_bytes = b"\xef\xbb\xbf" + m.body[3:-1] + b',"pair":"EURUSD"}'
        bad = changed(m, raw_bytes, "fxsynthetic-m2p12-aead-manifest-")
        with self.assertRaisesRegex(ValueError, "DUPLICATE_JSON_FIELD"):
            validate(m=bad)

    def test_wrong_chunk_flag_rejected(self):
        for change in (
            {"synthetic_only": False},
            {"real_fx_data": True},
            {"test_key_public": False},
        ):
            with self.subTest(change=change), self.assertRaisesRegex(
                ValueError, "NOT_APPROVED_TEST_KEY_CHUNK"
            ):
                validate(c=mutate_chunk(**change))


if __name__ == "__main__":
    unittest.main()
