# Forex Trading 1.0

**M1 foundation — READ-ONLY / SYNTHETIC ENGINEERING ONLY.** This repo is separate from Swing Trading 1.8, FX 2.0, CK 2.0 and Scanner.

## Engineering model
- **GitHub private repo**: canonical code, small PRs, commit history and GitHub Actions CI.
- **Google Drive**: canonical Master Spec, Master Handoff and decision / QA records.
- **ChatGPT Python**: disposable analysis/test environment, not a persistence or live-trading host.
- **MOCHI**: optional, separately approved data/cache/backup helper; it is NOT required for PR/CI.
- **M15001-FG-3**: NOT authorized for Forex project work.

## Canonical documents
- [00 Master Handoff v0.18, latest §28](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit)
- [02 Master Spec v0.8](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit)
- [04 Zone taxonomy v0.5](https://docs.google.com/document/d/1iMDKhYjJj9c3WbRMLbMywBuEkDdTuF_eR9lc7rNzU-c/edit)
- [06 QA](https://docs.google.com/document/d/19CGNHVw1QqnTifmtf1Xu5bst0IAbEWLhQlgOoVzfYZg/edit)
- [10 Version / Release / Rollback policy](https://docs.google.com/document/d/19z5m73GJgCu5AYCfio0JJGWHbcPJMwm___djxSq-GtA/edit)

## Full-text source snapshots
- [00 Master Handoff v0.18](docs/source-snapshots/00_MASTER_HANDOFF.txt) and [02 Master Spec v0.8](docs/source-snapshots/02_MASTER_SPEC.txt) are **point-in-time text snapshots**, not authoritative editable copies. See [revision/verification manifest](docs/HANDOFF_SNAPSHOT_MANIFEST.md).

## What exists
- Typed immutable quote, timestamp, catalog, signal-state and version-profile contracts.
- 18 **design labels**: 7 LONG entry candidates, 8 SHORT entry candidates, B7 watch-only, S3/S8 EXIT_LONG_WARNING_ONLY.
- FX-B9 remains *RESEARCH_ONLY*; **not** a live rule or 19th approved label.
- Eight pipeline step identifiers; fail-closed source quality and directional quote-side selector.
- M1/P0.1 immutable source observations and versioned BID/ASK/MID bar keys with CLOSED/coverage/quality/first-known and as-of revision guards; M5 is only a conditional early input, not confirmation. [Evidence](docs/M1_STATUS.md).

## What does NOT exist
No executable detector predicates, no calibrated thresholds, no trade eligibility engine, no brokerage connectivity, no licensed FX price feed, no bid/ask fill/SL/TP simulator, no historical Backtest, no OOS or paper validation, and no active/LKG production release. M1 CI tests only synthetic software invariants.

## Running synthetic tests
Requires Python 3.11+ (GitHub Actions uses Python 3.11 and 3.12). No third-party runtime dependencies.

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
```

Design and provenance controls are in `docs/`. Never commit credentials, broker orders, real licensed price bars or private user data.
