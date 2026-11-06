# Forex M1 status — GitHub main / M1/P0.2 source-calendar and DST contracts

**Current implementation checkpoint:** 2026-11-07 (Asia/Ho_Chi_Minh), 00 Google Drive Master Handoff v0.19 §29. Private repo `ngluonghoa/forex-trading-1-0` (not Swing). GitHub is canonical code and CI; MOCHI optional, NOT used; M15001 NOT AUTHORIZED.

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
No true entitlement/vendor source verification, independent TZDB/calendar attestation, licensed historical BID/ASK, strategy predicates B2/S2 or other executable zone detectors, feed costs/fill/SL/TP, Backtest/OOS, runtime/cache, actual operational rollback or LKG. `FX-DC-01..08`, `FX-VR-01..20` and `TEST-TPX-01..32` formal test sets are not declared PASS merely because 97 synthetic tests pass. GitHub main currently reported protected=false; manual PR/CI governance is used but an enforced review rule is NOT verified (private repo ruleset plan limitations).

## Documentation policy
Canonical editable 00_MASTER_HANDOFF v0.19 §29 and 02_MASTER_SPEC v0.8 are on Google Drive. GitHub `docs/source-snapshots/` is **point-in-time extracted text**, not native Google Docs formatting nor real-time sync. [Revision manifest](HANDOFF_SNAPSHOT_MANIFEST.md) tracks source versions and equality checks. Current docs PR merges and main verification require independent receipts; it cannot certify user source rights.
