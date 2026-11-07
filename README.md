# Forex Trading 1.0

**M1/M2 read-only reference — synthetic engineering only, NO operational market data cache.** This repo is separate from Swing Trading 1.8, FX 2.0, CK 2.0 and Scanner.

## Engineering model
- **GitHub private repo**: canonical code, small PRs, commit history and GitHub Actions CI.
- **Google Drive**: canonical Master Spec, Master Handoff and decision / QA records.
- **ChatGPT Python**: disposable analysis/test environment, not a persistence or live-trading host.
- **MOCHI**: optional, separately approved data/cache/backup helper; it is NOT required for PR/CI.
- **M15001-FG-3**: NOT authorized for Forex project work.

## Canonical documents
- [00 Master Handoff v0.33, latest §43](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit)
- [02 Master Spec v0.12](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit)
- [04 Zone taxonomy v0.5](https://docs.google.com/document/d/1iMDKhYjJj9c3WbRMLbMywBuEkDdTuF_eR9lc7rNzU-c/edit)
- [06 QA](https://docs.google.com/document/d/19CGNHVw1QqnTifmtf1Xu5bst0IAbEWLhQlgOoVzfYZg/edit)
- [10 Version / Release / Rollback policy](https://docs.google.com/document/d/19z5m73GJgCu5AYCfio0JJGWHbcPJMwm___djxSq-GtA/edit)

## Full-text source snapshots
- [00 Master Handoff v0.33](docs/source-snapshots/00_MASTER_HANDOFF.txt) and [02 Master Spec v0.12](docs/source-snapshots/02_MASTER_SPEC.txt) are **point-in-time text snapshots**, not authoritative editable copies. See [revision/verification manifest](docs/HANDOFF_SNAPSHOT_MANIFEST.md).

## What exists
- Typed immutable quote, timestamp, catalog, signal-state and version-profile contracts.
- 18 **design labels**: 7 LONG entry candidates, 8 SHORT entry candidates, B7 watch-only, S3/S8 EXIT_LONG_WARNING_ONLY.
- FX-B9 remains *RESEARCH_ONLY*; **not** a live rule or 19th approved label.
- Eight pipeline step identifiers; fail-closed source quality and directional quote-side selector.
- M1/P0.1 immutable source observations / versioned BID/ASK/MID bars and as-of revisions; M1/P0.2 calendar/DST and source-session claims; M1/P0.3 byte-pinned **synthetic** TZif and two-stream BID/ASK metadata consistency. These are read-only safeguards, not executable signals, licensed data or actual broker fills. [Evidence](docs/M1_STATUS.md).

## Source qualification (M2/P0.1, research only)
- [Documented candidate survey and licensing gates](docs/M2_P01_SOURCE_RIGHTS_REVIEW.md) for OANDA, Dukascopy/JForex, Twelve Data. No qualified vendor selected, no account-license approval or real BID/ASK ingestion, and no right to run a market Backtest. Source rights claims cannot self-authorize.

## Forex Smart Incremental Cache (M2/P0.2, synthetic reference)
- [Cache architecture and five-minute incremental plan](docs/M2_P02_FOREX_SMART_INCREMENTAL_CACHE.md). Namespaced by broker product/provider/pair/BID-ASK-MID/TF/calendar/revision, immutable closed candles, bounded-range delta plan and late correction reconciliation.
- Explicit L1–L5 dependency invalidation, source/quality/review gates and synthetic EMA append/revision parity; **no background polling, source connector, durable cache, licensed historical storage or speed benchmark**.
- [Decision DEC-FX-020](https://docs.google.com/document/d/1rZdd9tMfT98wH7oDvWlV-0n7EQvvIoUx1T6M79Gb0d8/edit), latest [02 Spec v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit).

## M2/P0.3 — Synthetic source adapter and storage proposal only
- [Source/provider contract & storage review](docs/M2_P03_PROVIDER_DELTA_AND_STORAGE_REVIEW.md): staged OANDA-v20-shaped BID/ASK M1/M5/M15/M30/H1 closed candles, bounded range, UTC/nanosecond precision checks, overlap append/revision/unchanged; no real API calls or provider rights.
- Proposed durable storage controls and metadata-only generation/hash chain; **no approved persistent cache or host**, no automatic on-demand scan speed metrics. [PR #13](https://github.com/ngluonghoa/forex-trading-1-0/pull/13), [verified main CI 42325743265](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42325743265): 275/275 synthetic tests per Python 3.11/3.12.

## M2/P0.4 — Synthetic 20-pair repeat-scan counters and source custody
- [Synthetic benchmark/first-seen custody design](docs/M2_P04_SYNTHETIC_SWEEP_AND_CUSTODY.md), [PR #15](https://github.com/ngluonghoa/forex-trading-1-0/pull/15), [main CI 42327843231](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42327843231) **310/310 synthetic tests per Python 3.11/3.12**.
- Fixture-only 20 fake pair IDs × 2 sides × 5 TF = 200 partitions; counterfactual 1640 full rows vs 120 hypothetical delta rows **if** 160 streams' upstream head tokens can be trusted. These are NOT real source API bytes/latency/calls or proof of 5min automatic polling.
- Causal receipt chain separates untrusted vendor event-time claims from first-seen-by-us UTC; older silent correction outside overlap remains a production blind spot pending approved vendor revision/deep reconciliation.

## M2/P0.5 — Account-specific data retention and storage review
- [Rights-by-purpose & storage location checklist](docs/M2_P05_ACCOUNT_RIGHTS_STORAGE_REVIEW.md), [PR #17](https://github.com/ngluonghoa/forex-trading-1-0/pull/17), [verified main CI 42329604319](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42329604319): **349/349 synthetic tests per Python 3.11/3.12**.
- Evaluates **claims only**: account/product/jurisdiction, purpose-specific historical API, raw retention/cache/indicator/replay/Backtest, expiry/revocation and candidate encrypted residency; no real-data rights automatically granted, no host chosen or data fetched.

## M2/P0.6 — Synthetic rights invalidation and atomic recovery guards
- [Design/negative-path receipt](docs/M2_P06_SYNTHETIC_RIGHTS_AND_RECOVERY.md), [PR #19](https://github.com/ngluonghoa/forex-trading-1-0/pull/19), [verified main CI 42334368272](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42334368272): **374/374 synthetic tests per Python 3.11/3.12**.
- Scoped opaque partition fingerprint L1-L5 invalidation proposal for observed revocation/expiry; future-known notices do not retroactively become observed vendor events. Crash-stage/commit-marker checks reject torn pointer, corrupt parent and claimed rollback floor.
- **NO active cache IO or restore**: commit pointers/generation floors are untrusted fixture claims; no approved account rights, independent vendor feed, persistent encrypted host or real HTTP five-minute performance.

## M2/P0.7 — Single / custom / all scope selector (synthetic reference)
- [Approved scan-mode selection and isolation contract](docs/M2_P07_SELECTABLE_SCAN_MODES.md). A pure typed selector supports exactly one pair, 2–19 custom pairs, or all 20 from a caller-provided approved catalog.
- `run_selected_synthetic_scan` reuses the SAME existing cache/sweep core and excludes unselected pairs before delta planning: 1 selected pair = 10 BID/ASK × 5 timeframe fixture streams, not 200. No cross-pair cache eviction, no network source request or production GUI was added.
- Source/vendor authorization, durable cache, actual 5-minute polling, live price scan, measured API performance, detectors and trades remain NOT IMPLEMENTED/NOT APPROVED.

## M2/P0.8 — Google Drive staging choice and mixed-scope cache reuse (synthetic only)
- **User-selected destination**: Google Drive. [Staging/cache folder and contract](docs/M2_P08_GOOGLE_DRIVE_STAGING_AND_MIXED_SCAN_CACHE.md). Empty staging folder created inside the Forex project Drive; no real price data, credentials, or persistent cache files uploaded.
- `synthetic_drive_cache_staging.py`: in-memory model of immutable chunk/manifests with checksums, stale-writer/crash/corruption negative paths; uses the prior L1 delta planner to run **5→20→1→20** chosen-pair scans. Existing partitions retain history; only missing 15 are bootstrapped on expansion. **ZERO real Google Drive/API calls, no live storage adapter**.
- Real vendor cache permission, encryption/key/ACL/region, Drive file I/O/atomicity, 5-minute real source/Drive benchmark and L2–L5 runtime remain unverified/unimplemented. Google Drive is a storage destination, **not** an always-on scanner.

## M2/P0.9 — Google Drive v3 synthetic blob wire protocol
- [Drive v3 multipart/list/readback synthetic-only contract](docs/M2_P09_GOOGLE_DRIVE_BLOB_WIRE_CONTRACT.md) adds a binary file request builder and **injected fake transport**. An immutable synthetic chunk is deduplicated by opaque partition SHA256 + content SHA256, uploaded in fake Drive wire form, checked against metadata and independently read back and hashed.
- Tests include mixed **5→20→1→20** file-level reuse, ambiguous 503/429, duplicate filename/pagination, tamper/missing/wrong parent, size and digest corruption. **No live Drive REST token/network requests or files have been made by this module.**
- Cloud storage operations, OAuth transport, safe concurrent multi-file commits, approved client-side encryption/rights and actual persistent production Forex cache are still pending.

## M2/P0.10 — Real Google Drive connector smoke, synthetic files only

- [Actual Google Drive connector chunk + manifest readback receipt](docs/M2_P10_REAL_DRIVE_SYNTHETIC_CONNECTOR_SMOKE.md). **Two real small synthetic text files** uploaded to existing staging folders with the connected Google Drive account: 141-byte TESTPAIR00 chunk + 439-byte manifest. Raw download verified byte-for-byte SHA256 matching exported originals and correct manifest reference. Temporary source Google Docs deleted.
- New offline `synthetic_drive_receipt_validation.py` and regression tests validate the copied connector evidence, folder IDs, content-address names, manifest pointers, MIME, checksums and data-rights fail-closed flags. The validator itself does **not** call Drive; the previously implemented Python Drive wire port remains injected FAKE TRANSPORT, not authenticated real IO.
- **No actual real FX candles were uploaded.** Cloud file smoke is not a transactional, encrypted, always-on or licensed Smart Cache and does not establish quota/latency at 5-minute 20-pair workload scale. Provider licensing, client-side keys/ACL/region, active manifest CAS/lease/rollback witness and restart recovery remain gates.

## M2/P0.11 — AES-256-GCM sealed synthetic cache and fail-closed recovery
- [Synthetic AES-256-GCM generation, witness and recovery design](docs/M2_P11_AEAD_SYNTHETIC_RECOVERY_AND_WITNESS.md): 256-bit key supplied at runtime, fresh random 12-byte nonce, authenticated partition/generation/parent/key reference, immutable sealed chunk + generation manifest, explicit stale-writer and tamper rejection.
- **Only an IN-MEMORY simulated Drive store and IN-MEMORY separate witness.** The demo detects staged crashes, broken pointer/witness, rollback and reopens the same memory state using a different session object. Neither is an authenticated Drive client, durable OS-restart exercise, external anti-rollback witness or distributed CAS.
- Pins the synthetic security test dependency in `requirements-security-synthetic.txt`. Never place a real secret key in GitHub, Google Docs or a raw cache manifest. The earlier two actual connected Google Drive smoke files are **not encrypted by this milestone**. No real FX quotes, provider cache rights, licensed feed or trading.

## M2/P0.13 — Actual Google Drive connector encrypted synthetic smoke

- [Real Drive AES-GCM synthetic chunk and manifest receipt](docs/M2_P13_REAL_DRIVE_ENCRYPTED_SYNTHETIC_SMOKE.md). Connected Google Drive plugin uploaded a real **753-byte sealed TESTPAIR00 synthetic envelope** and a **644-byte manifest** into their proper staging folders, then raw downloaded both; exact byte SHA256, GCM authentication/decryption and manifest references verified.
- **The 256-bit key is an intentionally PUBLIC test key**, not a production secret. This test proves the encryption/decryption data path and cloud file integrity only, **not confidentiality, authenticated cloud writer fencing, long-term key custody, real FX source entitlement, 5-minute 20-pair performance or encrypted production cache**. Temporary Docs were deleted after export; the two test files remain in staging.
- New offline `synthetic_cloud_aead_receipt.py` and regression tests reconstruct actual byte/hash fixtures and reject tampering, bad manifest, wrong key/parent and forbidden release claims. CI does not contact Google Drive or any provider.

## M2/P0.12 + P0.13 — weekly sub-window cache, encrypted fake Drive smoke and FX execution fixture

The cross-project approved engineering standard keeps Forex independent from Vietnam stock trading and preserves native FX BID/ASK, DST, spread/swap and broker semantics. [PR #31](https://github.com/ngluonghoa/forex-trading-1-0/pull/31) added in-memory immutable **weekly sub-windows inside each pair/product/side/TF** partition; new/revised fake week regenerates only one week's mock object. [PR #32](https://github.com/ngluonghoa/forex-trading-1-0/pull/32) independently tested actual connected Google Drive upload/download of a **753-byte encrypted synthetic TESTPAIR00 envelope + 644-byte manifest using an intentionally PUBLIC TEST KEY**. It proves integrity/readback but NOT confidentiality, production encryption/key custody, vendor data entitlements or operational Cache. [PR #33](https://github.com/ngluonghoa/forex-trading-1-0/pull/33) added independent synthetic FX execution-cost reference: LONG ASK→BID, SHORT BID→ASK, net quote-currency PnL after explicit commission/slippage/signed swap; same-bar stop+target => AMBIGUOUS, no invented fill. Main [GitHub Actions 42363465304](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42363465304) **539/539 PASS each Python 3.11/3.12**, with all three independent workstreams merged. Latest native 00 Handoff v0.33 §43 includes complete canonical Spec v0.12 §27. No full historic Backtest, trade ledger, verified broker execution, licensed market-price cache, protected KMS/remote witness or live trading.

## What does NOT exist
No executable detector predicates, no calibrated thresholds, no trade eligibility engine, no brokerage connectivity, no licensed FX price feed, no validated broker fill/SL/TP execution simulator (synthetic-only cost/ambiguity references exist), no historical Backtest, no OOS or paper validation, and no active/LKG production release. M1 CI tests only synthetic software invariants.

## Running synthetic tests
Requires Python 3.11+ (GitHub Actions uses Python 3.11 and 3.12). Synthetic security milestone additionally requires `python -m pip install -r requirements-security-synthetic.txt` (`cryptography==50.0.2`).

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
```

Design and provenance controls are in `docs/`. Never commit credentials, broker orders, real licensed price bars or private user data.
