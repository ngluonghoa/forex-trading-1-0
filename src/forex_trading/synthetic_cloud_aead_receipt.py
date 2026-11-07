"""M2/P0.13: offline verification of a REAL Drive connector AES-GCM test readback.

The two source artifacts were uploaded/downloaded via the connected Google
Drive app, NOT through this module. Both were harmless synthetic TESTPAIR00.
A PUBLIC test key is used: authentication and byte-path proof, NOT secrecy.
No independent metadata attestation, production key custody, provider license,
distributed CAS, source feed or cloud recovery is implied.
"""
from dataclasses import dataclass
from hashlib import sha256
from json import loads
from re import fullmatch

from .synthetic_drive_receipt_validation import ObservedDriveFile
from .synthetic_sealed_cache import (
    SealedSyntheticChunk, _envelope_digest, unseal_synthetic_fixture,
)

FILE_SCHEMA = "FX_SYNTHETIC_AEAD_FILE_V1"
MANIFEST_SCHEMA = "FX_SYNTHETIC_AEAD_DRIVE_MANIFEST_V1"
FIXTURE = (
    b"FX_SYNTHETIC_CACHE_V1\n"
    b"fixture_id=M2P12_REAL_DRIVE_ENCRYPTED_SMOKE\n"
    b"instrument=TESTPAIR00\n"
    b"no_market_data=true\n"
)
PARTITION = sha256(b"TESTPAIR00").hexdigest()
MAX_FILE_BYTES = 16 * 1024


@dataclass(frozen=True, slots=True)
class DriveEncryptedSyntheticReceipt:
    chunk_file_sha256: str
    manifest_file_sha256: str
    chunk_size_bytes: int
    manifest_size_bytes: int
    fixture_integrity_verified: bool = True
    test_key_is_public: bool = True
    real_data_confidentiality_proven: bool = False
    actual_drive_calls_from_validator: int = 0
    live_fx_cache_permitted: bool = False
    multi_file_transaction_proven: bool = False
    external_antirollback_proven: bool = False
    may_trade: bool = False


def _fail(code: str):
    raise ValueError(code)


def _json(blob: bytes, label: str) -> dict:
    if (not isinstance(blob, bytes) or len(blob) > MAX_FILE_BYTES
            or not blob.startswith(b"\xef\xbb\xbf{")):
        _fail(label + "_NOT_APPROVED_GOOGLE_DOCS_EXPORT_BYTES")
    def pairs(items):
        result = {}
        for key, val in items:
            if key in result:
                _fail("DUPLICATE_JSON_FIELD")
            result[key] = val
        return result
    try:
        obj = loads(blob.decode("utf-8-sig"), object_pairs_hook=pairs)
    except (UnicodeError, ValueError) as exc:
        _fail(label + "_JSON_INVALID:" + str(exc))
    if not isinstance(obj, dict):
        _fail(label + "_NOT_OBJECT")
    return obj


def _file(file: ObservedDriveFile, folder: str, name_prefix: str) -> str:
    if not isinstance(file, ObservedDriveFile):
        raise TypeError("TYPED_DRIVE_OBSERVATION_REQUIRED")
    if (not isinstance(folder, str) or
            not fullmatch(r"[A-Za-z0-9_-]{10,128}", folder)):
        _fail("INVALID_EXPECTED_FOLDER")
    if file.folder_id != folder:
        _fail("DRIVE_FOLDER_MISMATCH")
    if (not isinstance(file.file_id, str)
            or not fullmatch(r"[A-Za-z0-9_-]{10,128}", file.file_id)):
        _fail("INVALID_DRIVE_FILE_ID")
    if file.mime_type != "text/plain":
        _fail("DRIVE_SMOKE_MIME_MISMATCH")
    if not isinstance(file.body, bytes) or not 10 <= len(file.body) <= MAX_FILE_BYTES:
        _fail("INVALID_BOUNDED_FILE_BYTES")
    digest = sha256(file.body).hexdigest()
    if file.file_name != name_prefix + digest[:16] + ".txt":
        _fail("CONTENT_ADDRESS_FILENAME_MISMATCH")
    return digest


def _hex(value: object, length: int | None = None) -> bytes:
    if not isinstance(value, str) or len(value) % 2:
        _fail("INVALID_HEX")
    if length is not None and len(value) != length * 2:
        _fail("INVALID_HEX_LENGTH")
    try:
        return bytes.fromhex(value)
    except ValueError as exc:
        _fail("INVALID_HEX:" + str(exc))


def verify_real_drive_encrypted_synthetic_receipt(
    chunk: ObservedDriveFile,
    manifest: ObservedDriveFile,
    *,
    chunk_folder: str,
    manifest_folder: str,
    public_test_key: bytes,
) -> DriveEncryptedSyntheticReceipt:
    """Validate copied REAL connector bytes + manifest with PUBLIC TEST KEY.

    Reads no network or Drive resources itself. Caller observations are not
    independent server-side proofs. Only TESTPAIR00 fixed synthetic plaintext
    is accepted. The public key deliberately provides NO confidentiality.
    """
    if chunk_folder == manifest_folder:
        _fail("CHUNK_MANIFEST_FOLDERS_MUST_BE_DISTINCT")
    chunk_digest = _file(chunk, chunk_folder, "fxsynthetic-m2p12-aead-")
    manifest_digest = _file(
        manifest, manifest_folder, "fxsynthetic-m2p12-aead-manifest-"
    )
    if chunk.file_id == manifest.file_id:
        _fail("SAME_CHUNK_MANIFEST_FILE_ID")
    p, m = _json(chunk.body, "CHUNK"), _json(manifest.body, "MANIFEST")
    if set(p) != {
        "schema", "synthetic_only", "real_fx_data", "test_key_public",
        "chunk", "plaintext_sha256",
    }:
        _fail("CHUNK_FIELDS_UNEXPECTED")
    if (p["schema"] != FILE_SCHEMA or p["synthetic_only"] is not True
            or p["real_fx_data"] is not False
            or p["test_key_public"] is not True):
        _fail("NOT_APPROVED_TEST_KEY_CHUNK")
    c = p["chunk"]
    if not isinstance(c, dict) or set(c) != {
        "partition", "generation", "previous_manifest_sha256",
        "key_ref", "nonce_hex", "ciphertext_with_tag_hex", "envelope_sha256",
    }:
        _fail("SEALED_CHUNK_FIELDS_UNEXPECTED")
    if (c["partition"] != PARTITION or
            type(c["generation"]) is not int or c["generation"] != 1 or
            c["previous_manifest_sha256"] is not None or
            c["key_ref"] != "TESTKEY-01"):
        _fail("UNAPPROVED_SEALED_CHUNK_CONTEXT")
    nonce = _hex(c["nonce_hex"], 12)
    ciphertext = _hex(c["ciphertext_with_tag_hex"])
    digest_bytes = _hex(c["envelope_sha256"], 32)
    if len(ciphertext) <= 16:
        _fail("EMPTY_ENCRYPTED_FIXTURE")
    sealed = SealedSyntheticChunk(
        c["partition"], 1, None, c["key_ref"], nonce, ciphertext,
        digest_bytes.hex(),
    )
    if _envelope_digest(sealed) != sealed.envelope_sha256:
        _fail("SEALED_CHUNK_CONTENT_ADDRESS_MISMATCH")
    plaintext = unseal_synthetic_fixture(
        sealed, key=public_test_key, partition=PARTITION,
        generation=1, previous_manifest_sha256=None, key_ref="TESTKEY-01",
    )
    if (plaintext != FIXTURE or
            sha256(plaintext).hexdigest() != p["plaintext_sha256"]):
        _fail("SYNTHETIC_PLAINTEXT_DOES_NOT_MATCH")
    if set(m) != {
        "schema", "synthetic_only", "real_fx_data", "test_key_public",
        "trade_allowed", "source_rights_verified", "no_distributed_cas",
        "no_external_rollback_witness", "pair", "generation", "key_ref",
        "chunk_drive_file_id", "chunk_exported_size_bytes",
        "chunk_exported_sha256", "chunk_envelope_sha256", "plain_sha256",
    }:
        _fail("MANIFEST_FIELDS_UNEXPECTED")
    if (m["schema"] != MANIFEST_SCHEMA
            or m["synthetic_only"] is not True
            or m["real_fx_data"] is not False
            or m["test_key_public"] is not True
            or m["trade_allowed"] is not False
            or m["source_rights_verified"] is not False
            or m["no_distributed_cas"] is not True
            or m["no_external_rollback_witness"] is not True
            or m["pair"] != "TESTPAIR00"
            or type(m["generation"]) is not int or m["generation"] != 1
            or m["key_ref"] != "TESTKEY-01"):
        _fail("MANIFEST_FALSE_RELEASE_CLAIM")
    if (m["chunk_drive_file_id"] != chunk.file_id
            or type(m["chunk_exported_size_bytes"]) is not int
            or m["chunk_exported_size_bytes"] != len(chunk.body)
            or m["chunk_exported_sha256"] != chunk_digest
            or m["chunk_envelope_sha256"] != sealed.envelope_sha256
            or m["plain_sha256"] != sha256(plaintext).hexdigest()):
        _fail("MANIFEST_REFERENCE_INTEGRITY_MISMATCH")
    return DriveEncryptedSyntheticReceipt(
        chunk_digest, manifest_digest, len(chunk.body), len(manifest.body),
    )
