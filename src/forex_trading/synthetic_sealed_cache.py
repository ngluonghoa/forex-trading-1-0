"""M2/P0.11: synthetic-only AES-256-GCM cache and recovery reference.

This is REAL authenticated encryption of FAKE fixtures, but ONLY in memory.
There is no Drive adapter, trusted/independent durable witness, KMS, source
license, multi-host CAS, real FX price bars or trading permission. Even a
passing test cannot approve live source-data storage or rollback protection.
"""
from dataclasses import dataclass
from hashlib import sha256
from json import dumps
from re import fullmatch
from secrets import token_bytes

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b"FX_SYNTHETIC_CACHE_V1\n"
SCHEMA = "FX_SYNTHETIC_AEAD_V1"
MAX_BYTES = 128 * 1024


def _hash(value: bytes) -> str:
    return sha256(value).hexdigest()


def _json(value: dict) -> bytes:
    return dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")


def _part(partition: str) -> None:
    if not isinstance(partition, str) or not fullmatch(r"[a-f0-9]{64}", partition):
        raise ValueError("INVALID_PARTITION_FINGERPRINT")


def _digest(value: str | None, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str) or not fullmatch(r"[a-f0-9]{64}", value):
        raise ValueError("INVALID_MANIFEST_DIGEST")


def _key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) != 32:
        raise ValueError("AES256_KEY_MUST_BE_32_BYTES")


def _key_ref(key_ref: str) -> None:
    if not isinstance(key_ref, str) or not fullmatch(r"[A-Za-z0-9_-]{6,64}", key_ref):
        raise ValueError("INVALID_OPAQUE_KEY_REFERENCE")


def _aad(partition: str, generation: int, previous: str | None, key_ref: str) -> bytes:
    return _json({"schema": SCHEMA, "partition": partition,
                  "generation": generation, "previous": previous,
                  "key_ref": key_ref})


@dataclass(frozen=True, slots=True)
class SealedSyntheticChunk:
    partition: str
    generation: int
    previous_manifest_sha256: str | None
    key_ref: str
    nonce: bytes
    ciphertext_with_tag: bytes
    envelope_sha256: str


def _envelope_digest(chunk: SealedSyntheticChunk) -> str:
    return _hash(_json({
        "aad": _aad(chunk.partition, chunk.generation,
                    chunk.previous_manifest_sha256, chunk.key_ref).decode("ascii"),
        "nonce": chunk.nonce.hex(),
        "ciphertext_with_tag": chunk.ciphertext_with_tag.hex(),
    }))


def seal_synthetic_fixture(
    payload: bytes, *, key: bytes, partition: str, generation: int,
    previous_manifest_sha256: str | None, key_ref: str,
) -> SealedSyntheticChunk:
    _key(key)
    _part(partition)
    _digest(previous_manifest_sha256, nullable=True)
    _key_ref(key_ref)
    if type(generation) is not int or generation < 1:
        raise ValueError("GENERATION_MUST_BE_POSITIVE")
    if (not isinstance(payload, bytes) or len(payload) <= len(MAGIC)
            or len(payload) > MAX_BYTES or not payload.startswith(MAGIC)):
        raise ValueError("SYNTHETIC_FIXTURE_ONLY")
    nonce = token_bytes(12)
    ct = AESGCM(key).encrypt(nonce, payload,
                             _aad(partition, generation,
                                  previous_manifest_sha256, key_ref))
    draft = SealedSyntheticChunk(partition, generation,
                                 previous_manifest_sha256, key_ref,
                                 nonce, ct, "")
    return SealedSyntheticChunk(partition, generation,
                                previous_manifest_sha256, key_ref,
                                nonce, ct, _envelope_digest(draft))


def unseal_synthetic_fixture(
    chunk: SealedSyntheticChunk, *, key: bytes, partition: str,
    generation: int, previous_manifest_sha256: str | None,
    key_ref: str,
) -> bytes:
    if not isinstance(chunk, SealedSyntheticChunk):
        raise TypeError("SEALED_SYNTHETIC_CHUNK_REQUIRED")
    _key(key)
    _part(partition)
    _digest(previous_manifest_sha256, nullable=True)
    _key_ref(key_ref)
    if (chunk.partition != partition or chunk.generation != generation
            or chunk.previous_manifest_sha256 != previous_manifest_sha256
            or chunk.key_ref != key_ref):
        raise ValueError("AUTHENTICATED_CONTEXT_MISMATCH")
    if (not isinstance(chunk.nonce, bytes) or len(chunk.nonce) != 12
            or not isinstance(chunk.ciphertext_with_tag, bytes)
            or len(chunk.ciphertext_with_tag) < 17
            or chunk.envelope_sha256 != _envelope_digest(chunk)):
        raise ValueError("SEALED_ENVELOPE_CORRUPT")
    try:
        plaintext = AESGCM(key).decrypt(
            chunk.nonce, chunk.ciphertext_with_tag,
            _aad(partition, generation, previous_manifest_sha256, key_ref),
        )
    except InvalidTag as exc:
        raise ValueError("AEAD_AUTHENTICATION_FAILED") from exc
    if (not plaintext.startswith(MAGIC) or len(plaintext) <= len(MAGIC)
            or len(plaintext) > MAX_BYTES):
        raise ValueError("DECRYPTED_FIXTURE_NOT_APPROVED")
    return plaintext


@dataclass(frozen=True, slots=True)
class SealedManifest:
    partition: str
    generation: int
    previous_manifest_sha256: str | None
    envelope_sha256: str
    plaintext_sha256: str
    key_ref: str
    manifest_sha256: str


def _manifest_digest(manifest: SealedManifest) -> str:
    return _hash(_json({"schema": SCHEMA, "partition": manifest.partition,
                        "generation": manifest.generation,
                        "previous": manifest.previous_manifest_sha256,
                        "envelope_sha256": manifest.envelope_sha256,
                        "plaintext_sha256": manifest.plaintext_sha256,
                        "key_ref": manifest.key_ref}))


class SyntheticUntrustedDriveStore:
    """An in-memory stand-in for immutable Drive objects + active pointers."""
    def __init__(self):
        self.chunks: dict[str, SealedSyntheticChunk] = {}
        self.manifests: dict[str, SealedManifest] = {}
        self.active: dict[str, str] = {}
        self.chunk_writes = 0


class SyntheticSeparateWitness:
    """In-memory stand-in for an independent *trusted* durable witness.

    In production this state MUST live outside Drive in independently
    authenticated/monotonic infrastructure; this memory object is not proof.
    """
    def __init__(self):
        self.claims: dict[str, tuple[int, str]] = {}

    def compare_and_advance(self, partition: str, expected: str | None,
                            generation: int, next_digest: str) -> None:
        current = self.claims.get(partition)
        if ((current[1] if current else None) != expected
                or generation != (current[0] + 1 if current else 1)):
            raise ValueError("SIMULATED_WITNESS_STALE_GENERATION")
        self.claims[partition] = generation, next_digest


class SyntheticSealedCacheSession:
    """Single-process staging/commit/reopen algorithm with fail-closed gaps.

    The 'CAS' here is a plain memory dict comparison, NOT Google Drive CAS.
    The separate witness here is also an in-memory mock, NOT a trust anchor.
    """
    def __init__(self, store: SyntheticUntrustedDriveStore,
                 witness: SyntheticSeparateWitness, *,
                 key: bytes, key_ref: str):
        if not isinstance(store, SyntheticUntrustedDriveStore):
            raise TypeError("TYPED_SYNTHETIC_DRIVE_STORE_REQUIRED")
        if not isinstance(witness, SyntheticSeparateWitness):
            raise TypeError("TYPED_SYNTHETIC_WITNESS_REQUIRED")
        _key(key)
        _key_ref(key_ref)
        self.store = store
        self.witness = witness
        self._key = key
        self.key_ref = key_ref

    def read(self, partition: str) -> tuple[bytes, str] | None:
        _part(partition)
        pointer = self.store.active.get(partition)
        trusted_claim = self.witness.claims.get(partition)
        if pointer is None and trusted_claim is None:
            return None
        if (pointer is None or trusted_claim is None
                or pointer != trusted_claim[1]):
            raise ValueError("SIMULATED_WITNESS_POINTER_DIVERGED")
        visited: set[str] = set()
        cursor = pointer
        expected_generation = trusted_claim[0]
        current_plaintext = None
        while cursor is not None:
            if cursor in visited:
                raise ValueError("MANIFEST_CHAIN_CYCLE")
            visited.add(cursor)
            manifest = self.store.manifests.get(cursor)
            if (not isinstance(manifest, SealedManifest)
                    or _manifest_digest(manifest) != cursor
                    or manifest.manifest_sha256 != cursor
                    or manifest.partition != partition
                    or manifest.generation != expected_generation
                    or manifest.key_ref != self.key_ref):
                raise ValueError("SIMULATED_MANIFEST_CHAIN_CORRUPT")
            sealed = self.store.chunks.get(manifest.envelope_sha256)
            if sealed is None:
                raise ValueError("SIMULATED_ENCRYPTED_CHUNK_MISSING")
            plaintext = unseal_synthetic_fixture(
                sealed, key=self._key, partition=partition,
                generation=manifest.generation,
                previous_manifest_sha256=manifest.previous_manifest_sha256,
                key_ref=manifest.key_ref,
            )
            if (sealed.envelope_sha256 != manifest.envelope_sha256
                    or _hash(plaintext) != manifest.plaintext_sha256):
                raise ValueError("SIMULATED_MANIFEST_CHUNK_MISMATCH")
            if current_plaintext is None:
                current_plaintext = plaintext
            cursor = manifest.previous_manifest_sha256
            expected_generation -= 1
            if (cursor is None) != (expected_generation == 0):
                raise ValueError("SIMULATED_MANIFEST_SEQUENCE_GAP")
        return current_plaintext, pointer

    def commit(self, partition: str, payload: bytes, *,
               expected_manifest_sha256: str | None,
               failpoint: str | None = None) -> str:
        _part(partition)
        _digest(expected_manifest_sha256, nullable=True)
        if failpoint not in (None, "after_stage", "after_publish_before_witness"):
            raise ValueError("UNKNOWN_SYNTHETIC_CRASH_POINT")
        observed_pointer = self.store.active.get(partition)
        witness = self.witness.claims.get(partition)
        if ((witness[1] if witness else None) != observed_pointer):
            raise ValueError("SIMULATED_WITNESS_POINTER_DIVERGED")
        if observed_pointer != expected_manifest_sha256:
            raise ValueError("SIMULATED_STALE_WRITER_REJECTED")
        previous = self.read(partition)
        if previous is not None and previous[0] == payload:
            return previous[1]  # unchanged snapshot -> no upload/new manifest
        generation = (witness[0] + 1) if witness else 1
        sealed = seal_synthetic_fixture(
            payload, key=self._key, partition=partition, generation=generation,
            previous_manifest_sha256=expected_manifest_sha256,
            key_ref=self.key_ref,
        )
        draft = SealedManifest(partition, generation, expected_manifest_sha256,
                               sealed.envelope_sha256, _hash(payload), self.key_ref, "")
        manifest = SealedManifest(partition, generation, expected_manifest_sha256,
                                  sealed.envelope_sha256, _hash(payload), self.key_ref,
                                  _manifest_digest(draft))
        if sealed.envelope_sha256 not in self.store.chunks:
            self.store.chunks[sealed.envelope_sha256] = sealed
            self.store.chunk_writes += 1
        self.store.manifests[manifest.manifest_sha256] = manifest
        if failpoint == "after_stage":
            raise RuntimeError("SIMULATED_CRASH_AFTER_STAGE")
        # Local-only pointer check; no distributed / Drive atomicity guarantee.
        if self.store.active.get(partition) != expected_manifest_sha256:
            raise ValueError("SIMULATED_STALE_WRITER_REJECTED")
        self.store.active[partition] = manifest.manifest_sha256
        if failpoint == "after_publish_before_witness":
            raise RuntimeError("SIMULATED_CRASH_AFTER_POINTER_PUBLISH")
        self.witness.compare_and_advance(
            partition, expected_manifest_sha256, generation,
            manifest.manifest_sha256,
        )
        return manifest.manifest_sha256
