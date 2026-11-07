# M2/P0.11 — AES-256-GCM sealed cache, synthetic cross-session recovery, witness protocol

**Scope:** incremental engineering step following M2/P0.10's successful *real Google Drive connector* synthetic text-file readback. The **new AES-256-GCM implementation is real cryptography operating on synthetic bytes IN MEMORY**, **not a Google Drive cloud encryption or production persistence deployment**. Do not imply the new encrypted objects were written to Google Drive: the previously uploaded 141-byte chunk and 439-byte manifest were unencrypted test text and remain separate.

## What was implemented

- `src/forex_trading/synthetic_sealed_cache.py`: uses `cryptography.hazmat.primitives.ciphers.aead.AESGCM`, 256-bit key supplied at runtime, random 96-bit nonce for each new sealed generation, full authentication tag, and authenticated additional data binding opaque partition SHA256, generation, parent manifest digest, schema and opaque key reference.
- Immutable content-addressed encrypted envelopes: SHA256 of sealed envelope, plaintext SHA256 verified after authenticated decryption, per-partition generation manifest digest and complete ancestry validation. The secret **key is never stored in the manifest, envelope or GitHub**; a deliberately public fake test key is used only by unit tests.
- `SyntheticUntrustedDriveStore`: IN-MEMORY test double for immutable encrypted objects/manifest history/active pointer. `SyntheticSeparateWitness`: a **different IN-MEMORY object**, simulating external monotonic generation witness. Real independent, authenticated, durable, non-rollback witness does not exist.
- `SyntheticSealedCacheSession`: validates complete active chain and decrypts sealed fixture on each read; compares active pointer against witness claim before reading or committing. Rejects a stale writer, missing/tampered chunks/manifests, wrong key, wrong partition/generation/parent/key reference, rolled-back active pointer and partial publication. The in-process compare-and-advance is **not an inter-process/distributed atomic CAS** or true Drive lease.
- Simulates two crash windows: after immutable staging but before pointer (orphan remains but previous generation readable), and after pointer publish but before witness advancement (fail closed, explicitly **not** automatic recovery). A new session object with the same in-memory store, witness and injected key successfully re-reads cache; this is **not a process-restart/cloud recovery drill**.
- Synthetic `5 → 20 → 1 → 20` scope sequence with four session objects creates 20 initial per-pair sealed objects, reuses unchanged valid objects and causes no re-encryption/reupload for repeated unchanged payloads. This test is independent of the prior 200-stream BID/ASK/5-TF L1 oracle; does not claim full indicator L2–L5 parity.
- Dependency explicitly pinned `cryptography==50.0.2` for this reference milestone, with Python 3.11/3.12 GitHub Actions installing from `requirements-security-synthetic.txt`. Pinning does not itself prove supply-chain security or production suitability.

## Security semantics and nonclaims

Authenticated additional data binds encrypted payload to **partition/generation/parent/key ID**. Tampered ciphertext, nonce, key or AAD must fail before emitting plaintext. A SHA256 digest alone does not provide authentication; AES-GCM authentication does, **provided the secret key is protected**.

The program only accepts inputs carrying synthetic marker `FX_SYNTHETIC_CACHE_V1` with bounded length. This marker is merely an accidental-misuse guard; malicious code could insert such a marker ahead of real FX data. No source rights are inferred from markers, cache success, source credentials or approvals to use Google Drive for general storage.

The witness model is only an analogy: it is mutable and is lost between OS processes. An attacker with control over both simulated witness and Drive objects could forge or roll back both together. The simulated in-process writer check cannot stop conflicting processes sharing Google Drive. The two-write publish/witness window fails closed; it is NOT transactional and there is no production remediation/rollback implementation. Retention, audit evidence, emergency key loss, rotation/revocation, ACL/residency and re-encryption flows require separate review.

**Actual Google Drive raw-file transfer status:** earlier M2/P0.10 smoke 141-byte synthetic plaintext chunk + 439-byte synthetic manifest really uploaded/downloaded and re-read in a later chat; both SHA256 match. This milestone has **ZERO actual Drive encrypted blob uploads and ZERO real provider requests**, no throughput or 5-minute latency measurement, no real FX candle cache.

## Unmet release gates (BLOCKED)

Vendor account/product/region-specific permission to download/store historical native BID/ASK, retain raw/derived data, backtest/replay, TTL/revocation and correction audit; approved client-side key custody/external KMS, encryption-at-rest threat model, residency/permissions; authenticated cloud adapter for immutable bytes (no Docs export as binary pipeline); real distributed writer fencing + conditional pointer + trusted independent antirollback anchor; process/device restart and key-recovery drill; actual Drive/vendor API 5→20→1→20 calls/bytes/latency/quotas; complete L2–L5 indicators/detectors and Backtest/OOS; no broker orders or ACTIVE/LKG.

## Future milestone

Design a properly independent monotonic witness, strict single-writer coordination and keyed recovery, then implement/test a real Google Drive encrypted synthetic blob upload (only after security/ACL and key custody are approved). Do not store secret keys in GitHub/Docs/Drive manifests/logs. Preserve DEC-FX-020/021/022 and all existing Forex UI and signal taxonomy decisions.
