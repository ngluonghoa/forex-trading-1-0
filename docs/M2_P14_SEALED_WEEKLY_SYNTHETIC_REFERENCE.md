# M2/P0.14 — Synthetic sealed weekly chunk integration (read-only)

**Status: engineering reference only; NOT a licensed, authenticated or production Google Drive Forex cache.**

This milestone bridges the independent M2/P0.12 weekly immutable window design and M2/P0.11 AES-256-GCM primitive. It does **not** repurpose Google Docs exports as an authenticated binary cloud transport, nor create a durable source-data store.

## Implemented

- `src/forex_trading/synthetic_sealed_weekly_store.py` provides canonical ASCII-JSON serialization of each synthetic weekly BID/ASK window with full source observation metadata, revision, first-known timestamp, UTC start/end, Decimal OHLC and closed/complete/verified status.
- Every serialized plaintext starts with the existing `FX_SYNTHETIC_CACHE_V1` magic and includes its partition SHA256 and Monday-UTC **storage** bucket. It is encrypted by the existing AES-256-GCM helper with runtime-supplied 256-bit key, fresh nonce and authenticated generation/parent/key-reference context.
- Immutable week refs use SHA256 of **the complete serialized plaintext**, not the earlier in-memory `CandleSnapshot.fingerprint`. This is an intentional new wire-encoding identity: do not mix the two ref namespaces or claim unchanged compatibility without explicit migration tests.
- A simulated in-memory store retains unchanged encrypted weekly chunks across fake generations, stages only changed-week objects, and emits a new partition generation manifest only if week content changes. Repeated full snapshot -> 0 new chunk, 0 new manifest. A corrected old week or a new week -> 1 changed chunk in simple fixtures.
- Reopen selectively decrypts only requested week windows. Authenticated ciphertext, expected partition, key reference, UTC bucket, plaintext SHA, canonical bytes, complete bar count and typed `CandleSnapshot` are all checked. Wrong key/tag, tamper, wrong partition/ref, stale head, false generation floor and unverified week deletion fail closed.
- Simulated stage crash leaves an unreferenced orphan; a clean retry verifies and reuses the orphan, then publishes a manifest. There is no claim of atomic remote publish; all states remain IN MEMORY.

## Hard boundaries

This module rejects anything outside explicit `TEST-*` provider, `*-fake` pair, `NO-RIGHTS` partition and `ONLY_SYNTHETIC`/`NO_REAL_LICENSE` observation markers. These **caller labels are not independent proof of origin** and cannot certify real licensed quotes. The key in regression tests is publicly known `bytes(range(32))`, demonstrating authentication correctness but **no confidentiality against anyone with the test key**.

`FXWindowManifest` pointer and its generation are ordinary untrusted in-memory claims: there is no actual authenticated independent monotonic witness, distributed compare-and-swap, lease, key-management service, cloud ACL, storage tenancy/location, real Drive API IO, cold OS restart test or production backup. Weekly UTC buckets do not imply provider trading-session calendars, market weekends, rollover or DST.

No real provider source, native historical BID/ASK rights, 5-minute scheduler, 5→20→1→20 measured Drive/vendor traffic, L2–L5 production cache, full historical Backtest/OOS, detector activation or real trading is introduced. All source-rights, data freshness/correction, encryption key custody, vendor contract, and release gates remain HARD FALSE. Forex design labels, entry/exit states and TP policies are unchanged.

## Acceptance tests

`tests/test_synthetic_sealed_weekly_store.py` checks initial 3-week encryption and typed roundtrip; unchanged zero writes; one-week append, new-week append and late correction; one-week selection; pair/BID-ASK isolation; wrong key/key reference; envelope tamper; stale/rollback pins; lost week rejection; staged crash/orphan retry; corruption block; fake source/rights gates; future-known guard; no live Drive or trading claim.

Run `PYTHONPATH=src python -m unittest discover -s tests` after installing pinned `requirements-security-synthetic.txt`. CI must pass Python 3.11 and 3.12 before any merge.

## Next after passing CI

A separate scoped milestone should define a real provider-rights-approved, *authenticated binary* Google Drive connector with safe retries/readback, then externally anchored monotonic witness and distributed fencing before any production deployment. Keep all cache tests with fake data until account-specific historical native BID/ASK caching/replay/Backtest rights are independently verified. Independently work on the purged/embargoed FX event-time Backtest split; no performance claims until OOS evidence.
