# Forex M1–M2 status — read-only source, incremental cache, rights and storage contracts

**Current implementation checkpoint:** 2026-11-07 (Asia/Ho_Chi_Minh), 00 Google Drive Master Handoff v0.26 §36. Private repo `ngluonghoa/forex-trading-1-0` (not Swing). GitHub is canonical code and CI; MOCHI optional, NOT used; M15001 NOT AUTHORIZED.

| Code/document checkpoint | Merge SHA | PR CI observed | Main CI observed |
| --- | --- | --- | --- |
| [#1 typed read-only foundation](https://github.com/ngluonghoa/forex-trading-1-0/pull/1) | `59c7ebf1f7fb99d817c6a702944acadaf9c33fd7` | [42267449139](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42267449139) 41/41 Python 3.11/3.12 | [42267577979](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42267577979) PASS |
| [#2 first complete Drive 00/02 extracted-text snapshot](https://github.com/ngluonghoa/forex-trading-1-0/pull/2) | `7dfd70b1c7651ca41b20b132e331515a7592e4d1` | [42268428672](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42268428672) PASS | [42268493022](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42268493022) PASS |
| [#3 typed source/first-known/as-of bar](https://github.com/ngluonghoa/forex-trading-1-0/pull/3) | `de6cc28a998ef60d7bcb041c0e091cfd543bda41` | [42269509799](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42269509799) 68/68 each | [42269624491](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42269624491) 68/68 each |
| [#4 Drive Handoff v0.18 extracted-text revision](https://github.com/ngluonghoa/forex-trading-1-0/pull/4) | `7f3c06d5238946929e1293654a8c0f3b4891c5b8` | [42270304500](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42270304500) PASS | [42270368924](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42270368924) 68/68 each |
| [#5 provider-declared DST and session calendar](https://github.com/ngluonghoa/forex-trading-1-0/pull/5) | `ea5d85a2568f39c110e1f54de7105e7919023f06` | [42271838611](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42271838611) **97/97 each 3.11/3.12** | [42271977850](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42271977850) **97/97 each 3.11/3.12** |

## Implemented, read-only only
- Typed immutable classes for 18 approved design zone labels/15 entry candidates, four display phases per direction, four intents, 8 pipeline stage IDs, bid/ask indicative quote sides, UTC/first-known and quality fail-closed gates, incomplete source and no-trade reasons, immutable execution profile fingerprint + **synthetic** rollback compatibility PREVIEW.
- M1/P0.1: Observation & MarketBar, source/price side/version, closed-complete quality and as-of revision guards, M15 closed base; M5 early conditional only; MID never executable.
- M1/P0.2: provider-specified calendar and IANA DST wall clock conversion (nonexistent gap rejects, overlap fold required), source session with first-known/versioned evidence, explicit D1 rollover (DST 25-hour valid when provider policy permits), W1 fails until provider week policy, overlap detection. A *calendar metadata pass* does NOT independently validate vendor time, bar quality, source license or broker permission.
- GitHub Actions pinned to official checked commits `actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09` (v5) and `actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1` (v6). TZDB contents and Python patch versions not fully locked.

## Missing gates
No true entitlement/vendor source verification, independent TZDB/calendar attestation, licensed historical BID/ASK, strategy predicates B2/S2 or other executable zone detectors, feed costs/fill/SL/TP, Backtest/OOS, actual persistent cache/runtime or operational rollback/LKG. `FX-DC-01..08`, `FX-VR-01..20` and `TEST-TPX-01..32` formal test sets are not declared PASS merely because 97 synthetic tests pass. GitHub main currently reported protected=false; manual PR/CI governance is used but an enforced review rule is NOT verified (private repo ruleset plan limitations).


## M1/P0.3 — TZif byte pin and BID/ASK source coherence (2026-11-07)
- GitHub [PR #7](https://github.com/ngluonghoa/forex-trading-1-0/pull/7) source SHA `f466b491c4183236b1faa0d355f3c89646203ec9` squash merged `main` SHA `556b904124f378a8b8e1a78590b4d634d22ae16b`.
- Actual GitHub Actions [PR 42274337404](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42274337404) and [MAIN 42274433483](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42274433483) completed SUCCESS: Python 3.11 **133/133**, Python 3.12 **133/133** synthetic unittest PASS per run, compileall successful.
- Added typed `TzifArtifact` SHA-256 integrity and `ZoneInfo.from_file` exact pinned **synthetic** TZif bytes, as-of and DST-gap/overlap reject gates; local bytes are NOT an official tzdb release nor authenticated provider policy. Added `BidAskSourceManifest` and `assess_bid_ask_side_pair` for provider, source-side, calendar, interval, revision and first-known checks.
- No independent vendor-source rights, official timezone signature/production tzdb lock, tick-align BID/ASK fills, financial Backtest/OOS, detector, release or LKG. A declared dataset hash is not independently verified without actual source bytes/rights. `permission_to_trade` is always false.
- New controlled source snapshot: Google Drive 00 Master Handoff v0.20 §30 (see [manifest](HANDOFF_SNAPSHOT_MANIFEST.md)); 02 Master Spec remains v0.8 unchanged. Docs PR main merge/CI must be checked separately.


## M2/P0.1 — Source data rights and public capability (2026-11-07)
- Code [PR #9](https://github.com/ngluonghoa/forex-trading-1-0/pull/9), source commit `ca9c06a6f94a1b7828303ca4a1c0251cf77b004d`, main merge `0345a9f7d158de1d04148ee9ac7b317a214b27a3`. Public documentation and policy evidence in [M2_P01_SOURCE_RIGHTS_REVIEW](M2_P01_SOURCE_RIGHTS_REVIEW.md).
- [PR CI 42277238158](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42277238158) and [main CI 42277351212](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42277351212): **167/167 synthetic tests per Python 3.11 and 3.12, PASS**, compileall PASS.
- `PublicCapabilityClaim` distinguishes historical native 2-sided BID+ASK from generic OHLC or snapshots and requires M1/M5/M15 plus timestamps/account-price basis. `UseRightsClaim` tracks access, storage, derivatives, replay, backtest, cache (redistribution independent) and blocks missing/denied/expired/future/unproved account grants.
- `assess_source_for_m2_review` can mark supplied CLAIM records ready for external legal/account review. `vendor_entitlement_independently_verified`, `may_ingest_real_data`, `may_cache_or_store_real_data`, `may_run_real_backtest` **always False**. No actual vendor account contract, license, native BID/ASK historical source, source sample/revision or real market Backtest has been validated.
- Official technical candidate documentation: OANDA v20 historical BID/ASK candle support but historical/account-price mismatch warning, Dukascopy historical ticks/bar side, Twelve Data Forex generic OHLC with native two-sided historical price support not independently established. API connection/quota does NOT imply retention or backtest rights.
- **M2 verdict: PUBLIC_CAPABILITY_RESEARCH_ONLY / RIGHTS_AND_NATIVE_BIDASK_NOT_QUALIFIED**. Do not promote vendor or indicator/detector to ready, no data retrieval/storage, no real trading.

## M2/P0.2 — Forex Smart Incremental Cache (2026-11-07)
- [GitHub PR #11](https://github.com/ngluonghoa/forex-trading-1-0/pull/11) merged `caf0df610aeb5dd5b8e9e6ef01f41d5827f29e32`.
- PR CI [42323752852](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42323752852) and postmerge main CI [42323816487](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42323816487) each Python 3.11 and 3.12 **224/224 synthetic tests PASS**.
- `cache_core`: versioned partition/closed-bar snapshots, bounded source delta plan with source-head claims not authenticated, immutable APPEND/REVISE/NO_CHANGE reconciliation, first-dirty UTC, no in-place rewrite or silent eviction.
- `cache_dependency`: selective L1–L5 invalidate by explicit dependencies, digest includes algorithm+params/input lineage, audit rerun required despite reuse.
- `cache_indicators`: experimental Decimal EMA full vs append/revision parity only. Other indicators, native data adapters, retention-rights, durable storage/restart/recovery, automatic 5-minute checks and real performance SLO remain **NOT IMPLEMENTED/NOT VERIFIED**.
- Forex Master Spec **v0.9 §24**, Migration Register v0.12 §22 DEC-FX-020, Handoff v0.25 §35 including full v0.9 Spec copy. Source/snapshot exact match to be verified after docs PR merge.

## M2/P0.3 — Synthetic-only bounded provider fixture and storage review (2026-11-07)
- [PR #13](https://github.com/ngluonghoa/forex-trading-1-0/pull/13) merged main SHA `1f46b7e1df871609a19e53c8369cce5819f4eb70`. First PR CI 42325628149 failed exactly one schema-classification negative test; fixed before merge. Final [PR CI 42325690593](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42325690593) and [main CI 42325743265](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42325743265) each **275/275 synthetic tests on Python 3.11 and 3.12**.
- `provider_delta_contract.py` validates OANDA-v20-shaped synthetic BID and ASK complete n-sided OHLC, UTC/range and overlap append/correction, no network or cache rights. H4/D1/W1 provider session alignment not enabled until verified.
- `cache_storage_review.py` evaluates encryption/atomic/retention/backup/append-only/revocation claims; its checksum generation chain is METADATA ONLY. No real IO, host/runtime selection or trusted source authorization, no real 5-minute scans/backtests.
- Real-data source terms, source correctness, persistent storage restart & rollback, 20-pair performance and full indicator parity remain OPEN. [M2/P0.3 design](M2_P03_PROVIDER_DELTA_AND_STORAGE_REVIEW.md).

## M2/P0.4 — 20-pair synthetic repeat scans and source custody (2026-11-07)
- [PR #15](https://github.com/ngluonghoa/forex-trading-1-0/pull/15) main merge `336c87bebd1af2752211ac8da4fc86be3316c30c`, [PR CI 42327775902](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42327775902) and [main CI 42327843231](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42327843231) **310/310 synthetic unit tests on each Python 3.11 and 3.12**.
- `synthetic_scan_workload`: 20 fake pair identifiers × BID+ASK × 5 TF = 200 partitions. 1640 full-row counterfactual vs 120 synthetic bounded rows in a claimed unchanged-head scenario; 40 planned bounded windows; no real API calls/bytes/time/rights measured. No authenticated provider HEAD; correction outside overlap flagged by test-only full oracle, not detectable in real runtime without genuine source changes/reconciliation.
- `synthetic_source_custody`: first-seen local UTC, as-of replay guard, ordinal/parent-hash receipt checks; no independent vendor attestation or external immutable anchoring.
- 02 Spec remains v0.9 §24 (DEC-FX-020), 00 Handoff v0.25 §35. Production storage, active five-minute scanner, source license, source-specific candles/calendar, real benchmark, full L2–L5 runtime and Backtest/OOS remain NOT VERIFIED/NOT IMPLEMENTED.


## M2/P0.5 — Account rights + storage eligibility review (2026-11-07)
- [PR #17](https://github.com/ngluonghoa/forex-trading-1-0/pull/17) merged `9dc612e99f168f42d4afc9fa10e0b5b9d8e80b4f`; [PR CI 42329544166](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42329544166), [main CI 42329604319](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42329604319) each Python 3.11/3.12 **349/349 synthetic PASS**.
- [Source legal/storage checklist](M2_P05_ACCOUNT_RIGHTS_STORAGE_REVIEW.md), `src/forex_trading/account_data_review.py` (no provider/network/cache IO) reviews opaque nonsecret account/product/jurisdiction and contract timeline, use rights individually, retention limit, separate derived-data retention, allowed storage residency, proposed encrypted-store controls and expiry/revocation; positive applicant claims mean **ready only for independent review**. All `may_*` real market-data operations are FALSE.
- Neither OANDA/Twelve Data/Dukascopy account rights nor permanent data retention, selected host, real 5-minute active cache, source price correctness, actual 20-pair benchmark, source revision audit, full indicator/parity or Backtest/OOS are verified. MOCHI optional only, not used; M15001 prohibited.

## Documentation policy
Canonical editable 00_MASTER_HANDOFF v0.23 §33 and 02_MASTER_SPEC v0.9 §24 remain on Google Drive. GitHub `docs/source-snapshots/` is **point-in-time extracted text**, not native Google Docs formatting nor real-time sync. [Revision manifest](HANDOFF_SNAPSHOT_MANIFEST.md) tracks source versions and equality checks. Current docs PR merges and main verification require independent receipts; it cannot certify user source rights.


## M2/P0.6 — Rights invalidation and atomic crash-window synthetic reference (2026-11-07)
- [PR #19](https://github.com/ngluonghoa/forex-trading-1-0/pull/19) source head `5c4c22477ba57ed7173b01ed616aed0900b15de2`, squash merged main `5211ef2131cdaf4bef78b4629e46107f2626f2dc`. [PR CI 42334294778](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42334294778) PASS and independent [main CI 42334368272](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42334368272) PASS; Python 3.11 and Python 3.12 **374/374 synthetic tests each** (+25).
- [Pure code and negative-path contract](M2_P06_SYNTHETIC_RIGHTS_AND_RECOVERY.md) models expiration/revocation source review -> targeted L1-L5 invalidation; distinct retroactive notice effective clock and local first-seen clock; simulated staged/committed generation with checksum/parent/pointer/rollback-floor checks. A caller-controlled pointer/floor is not a trusted external anchor.
- No live licensed bars, vendor contract, host, persistent storage, scheduled actual API poll, 20-pair measured bytes/calls/latency, Backtest/OOS or broker order. No real-data permissions granted. No MOCHI/M15001 use; Spec v0.9 business logic unchanged.
