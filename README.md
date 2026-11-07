# Forex Trading 1.0

**M1/M2 read-only reference — synthetic engineering only, NO operational market data cache.** This repo is separate from Swing Trading 1.8, FX 2.0, CK 2.0 and Scanner.

## Engineering model
- **GitHub private repo**: canonical code, small PRs, commit history and GitHub Actions CI.
- **Google Drive**: canonical Master Spec, Master Handoff and decision / QA records.
- **ChatGPT Python**: disposable analysis/test environment, not a persistence or live-trading host.
- **MOCHI**: optional, separately approved data/cache/backup helper; it is NOT required for PR/CI.
- **M15001-FG-3**: NOT authorized for Forex project work.

## Canonical documents
- [00 Master Handoff v0.24, latest §34](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit)
- [02 Master Spec v0.9](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit)
- [04 Zone taxonomy v0.5](https://docs.google.com/document/d/1iMDKhYjJj9c3WbRMLbMywBuEkDdTuF_eR9lc7rNzU-c/edit)
- [06 QA](https://docs.google.com/document/d/19CGNHVw1QqnTifmtf1Xu5bst0IAbEWLhQlgOoVzfYZg/edit)
- [10 Version / Release / Rollback policy](https://docs.google.com/document/d/19z5m73GJgCu5AYCfio0JJGWHbcPJMwm___djxSq-GtA/edit)

## Full-text source snapshots
- [00 Master Handoff v0.22](docs/source-snapshots/00_MASTER_HANDOFF.txt) and [02 Master Spec v0.9](docs/source-snapshots/02_MASTER_SPEC.txt) are **point-in-time text snapshots**, not authoritative editable copies. See [revision/verification manifest](docs/HANDOFF_SNAPSHOT_MANIFEST.md).

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

## What does NOT exist
No executable detector predicates, no calibrated thresholds, no trade eligibility engine, no brokerage connectivity, no licensed FX price feed, no bid/ask fill/SL/TP simulator, no historical Backtest, no OOS or paper validation, and no active/LKG production release. M1 CI tests only synthetic software invariants.

## Running synthetic tests
Requires Python 3.11+ (GitHub Actions uses Python 3.11 and 3.12). No third-party runtime dependencies.

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
```

Design and provenance controls are in `docs/`. Never commit credentials, broker orders, real licensed price bars or private user data.
