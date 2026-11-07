# M2/P0.13 — Real Google Drive encrypted synthetic chunk and manifest readback

**2026-11-07 (Asia/Ho_Chi_Minh).** Continued the user-approved Google Drive Smart Cache storage choice (DEC-FX-022) and the M2/P0.11 in-memory AES-256-GCM reference. **A real encrypted, harmless TESTPAIR00 fixture was uploaded to and downloaded from Google Drive through the connected Drive plugin.** This is not an operational Forex price-data cache and does not constitute approved encryption key custody.

## Actual Google Drive operation and immutable fixture evidence

| Verified staging object | Drive link and parent folder | Raw exported bytes / SHA-256 |
| --- | --- | --- |
| [AES-256-GCM synthetic JSON envelope](https://drive.google.com/file/d/1IfzBILWfo6dAPHBIdvPpY52QQ3XVsDaR/view) | `01_IMMUTABLE_CHUNKS__STAGING`, folder `1mE7Zx29kDjyN8DYfvZn4HYx-OIoYaScw` | **753 bytes** / `80e77881ce0ed5f65ab243915282900b79c5bb99a67cef221a3c3c0a1d7805f0` |
| [Manifest for that encrypted chunk](https://drive.google.com/file/d/1Be06jBxGDpjeKHpzJdA0XMLHoY4I7lCF/view) | `00_MANIFESTS_AND_INDEX__STAGING`, folder `1OPBHzq5sPNV9ohqlsfi_I5e35ve1qvkD` | **644 bytes** / `7686d6600288e8a433776e84c0f565aee733b08d22c2bb975078a11c08a4f373` |

- Used `cryptography` AESGCM on **108 bytes of exclusively invented TESTPAIR00 fixture text** `FX_SYNTHETIC_CACHE_V1` with a freshly generated 12-byte nonce, SHA256 partition identifier, generation 1, parent null and AAD binding schema/partition/generation/parent/key reference.
- **CRITICAL KEY LIMITATION:** Encryption/decryption used **bytes(range(32)) — an intentionally PUBLIC TEST KEY already declared in the synthetic unit tests. Anyone with the public test key can decrypt this fixture.** This proves correct cryptographic formatting/authentication and a working cloud byte path, NOT confidential storage or real key custody. No confidential key was created, exported or stored in Drive/Docs/GitHub.
- For the existing connector's `file_uri` upload route, placed only the AES-GCM ciphertext envelope JSON in a temporary Google Doc, exported as text/plain, uploaded that exported ordinary file into the staging chunk folder and independently read it back via the actual connected Drive plugin. Export added UTF-8 BOM (3 bytes) to the 750-byte canonical source JSON. The manifest was similarly exported from a second temporary Google Doc as a 644-byte ordinary text file (641-byte canonical JSON + BOM). **Google Docs export is a temporary proof-of-connectivity bridge, not a recommended production binary cache transport.**
- Locally compared each downloaded raw file byte-for-byte against its corresponding exported source; both raw SHA256 hashes matched. Parsed downloaded ciphertext envelope and manifest; verified strict ID/byte-size/file digest, AES-GCM envelope SHA256 `82fcbab6691d56dd958f550b44d0a0646c6eae3499c425449203f542c8eb2807`, AAD, GCM tag and decrypted SHA256 `32f7b9d4e5ea3ddae25c74bb4bb8f679ee76959241c04dfbb4b6af53aee1fe3a` of exactly 108 synthetic bytes.
- Both temporary source Google Docs were **permanently deleted** after verified upload/download; the immutable encrypted test chunk and its manifest were retained in the two staging folders. No customer account, credential, broker quote, real price bar, FX market feed or user-identifying data was included.

## Reproducible automated checks in the repo

- `src/forex_trading/synthetic_cloud_aead_receipt.py` is a **strict offline validator**, not an authenticated Drive client. It uses existing `ObservedDriveFile` and the prior AES-GCM/manifest code; rejects invalid file hashes/names, body encoding, folder/ID/MIME, duplicate JSON keys, incorrect pair/AAD/generation/parent/key ID, invalid ciphertext/tag/wrong key, forged manifest ref/SHA/size, and unapproved source-entitlement/trading or external-witness claims.
- `tests/test_synthetic_cloud_aead_receipt.py` reconstructs the observed exact **753-byte/644-byte files** from fixed public-test ciphertext and known metadata. Negative tests prove fail-closed behavior without Google Drive or a vendor HTTP call. CI on Python 3.11/3.12 with pinned cryptography. **These unit tests are not equivalent to additional live Drive uploads or measured throughput**.
- For the earlier 5→20→1→20 optimization, unchanged selected partitions still avoid unnecessary synthetic writes in M2/P0.8/M2/P0.9/M2/P0.11 tests. The live Drive test this time is **one test pair only**, and does not benchmark real 5-minute cross-scope Drive/vendor load.

## Release gates remain BLOCKED

**No real data confidentiality** (public fixed test key), external/independent KMS or durable key custody, key rotation/revocation/recovery, ACL/region/security review, true conditional publication / cross-process lock / multi-file transaction, independent trusted monotonic anti-rollback witness, OS restart recovery drill, actual production 5→20→1→20 Google Drive and provider API call/byte/latency measurements, source-specific historical native BID/ASK cache/derived retention/replay/backtest permission and expiry policy, complete L2–L5 indicators/detectors/backtest/OOS or real broker trading.

Drive's storage and a SHA256 checksum prove neither third-party historical FX price licensing nor confidentiality, rollback resistance, market source authenticity, concurrency safety or future availability. This remains **M2/P0.13 SYNTHETIC_ENCRYPTED_DRIVE_CONNECTOR_SMOKE_PASS** only. No MOCHI, M15001, VPS or paid host used. Next: properly designed independent key custody and write fencing, and a true binary streaming Drive adapter before any production price-data storage.
