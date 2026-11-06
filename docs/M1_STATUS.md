# Forex M1 — Verified GitHub engineering checkpoint (2026-11-07)

## Source authority and project boundary
- Canonical editable Handoff: [Google Drive 00 v0.18 §28](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit); business rules: [02 Master Spec v0.8](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit).
- Code owner: [private GitHub Forex repo](https://github.com/ngluonghoa/forex-trading-1-0), separate from Swing Trading. MOCHI optional and NOT used; M15001 expressly prohibited.

## Actual code + CI evidence
| Milestone | PR / merge | PR Actions | Main Actions |
| --- | --- | --- | --- |
| M1 bootstrap / read-only DTOs | [#1](https://github.com/ngluonghoa/forex-trading-1-0/pull/1), `59c7ebf1f7fb99d817c6a702944acadaf9c33fd7` | [42267449139](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42267449139) PASS 41/41 each Python 3.11/3.12 | [42267577979](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42267577979) SUCCESS, both versions |
| Full 00/02 text snapshot | [#2](https://github.com/ngluonghoa/forex-trading-1-0/pull/2), `7dfd70b1c7651ca41b20b132e331515a7592e4d1` | [42268428672](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42268428672) PASS | [42268493022](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42268493022) SUCCESS, both versions |
| M1/P0.1 market bar first-known/revision gates | [#3](https://github.com/ngluonghoa/forex-trading-1-0/pull/3), `de6cc28a998ef60d7bcb041c0e091cfd543bda41` | [42269509799](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42269509799) PASS **68/68 each Python 3.11/3.12** | [42269624491](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42269624491) PASS **68/68 each Python 3.11/3.12** |

All tests are **synthetic** with read-only typed fixtures. They do not constitute market performance tests, broker/license validation or full formal FX-DC/FX-VR acceptance.

## Implemented, not operational
1. Immutable typed enums / frozen DTOs for LONG/SHORT, four action intents, stage and display status, 18 design labels: 7 entry LONG + 8 entry SHORT + B7 watch + S3/S8 protective; research-only FX-B9 excluded.
2. Four direction-correct indicative bid/ask mappings, UTC event / first-known / source quality and age fail-closed controls; no broker orders.
3. 8 named pipeline stages and version-profile SHA256 identity / conservative rollback preview (no actual rollback/release).
4. M1/P0.1 Observation source lineage and SHA256 shape; MarketBarKey time range/calendar/side; OHLC Decimal validation; OPEN/CLOSED, COVERAGE, QUALITY dimensions; no future-correction lookahead; only closed complete quality-checked M15 technical input and explicitly gated M5 early branch. MID never a fill, quality is not a license. **No confirmed signal / trade authorization** emitted.

## Not ready
- Source entitlement, historical tick/M1/M5/M15 BID/ASK validation (including coverage/revision, UTC/DST/rollover, provider rights to store/derive/backtest), validated venue calendar.
- Quantitative/causal B2 LONG/S2 SHORT or other detector rules, dedup, risk/economically feasible entry/SL/TP, simulator and common-core replay.
- Backtest with costs, untouched OOS, full FX-DC-01..08, FX-VR-01..20, TEST-TPX-01..32 acceptance, persistent cache, actual release/LKG or operational rollback drill.
- GitHub branch enforcement: integration read of branch protection returned 403; private rulesets reported GitHub Pro/public requirement. Repo remains PRIVATE; manual PR+CI is observed, automated enforcement NOT VERIFIED.
- Latest Docs Handoff v0.18 point-in-time snapshot is staged on a docs PR, not canonical editable truth and must be independently checked after merge.

**Next:** close latest docs snapshot PR with CI and main exact readback; strengthen source clock DST/calendar and as-of negative/equivalence tests, then M2 source-rights qualification before M3 calibrated detector and M4 real Backtest.
