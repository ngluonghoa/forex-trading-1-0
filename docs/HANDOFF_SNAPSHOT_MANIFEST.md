# Forex Trading 1.0 — authoritative source snapshots after extra rollback (2026-11-07)

## ACTIVE checkpoint: M2/P0.10 source = original Handoff v0.30 §40

The user's latest instruction is to roll back **one more Forex milestone** after the earlier three-milestone rewind. Current **executable code, tests, CI and dependency configuration** are back to original M2/P0.10 (commit `7f0904eefad9afe3da7bbaab522d8c59b6847c9e`, original Handoff v0.30 §40). The editable **Google Drive Handoff has advanced to v0.37 §47 solely to record the rollback**, and its §47 supersedes previous §46. The native 02 Master Spec remains at **v0.12 §27 — approved DESIGN, not evidence that withdrawn source features remain implemented**.

- Source rollback [PR #43](https://github.com/ngluonghoa/forex-trading-1-0/pull/43) merged main `a68d9015781469156ac0339483bf4bc1d893ce84`.
- Exact recursive GitHub tree verification against the original M2/P0.10 commit: **47/47 blob SHAs identical under `src/`, `tests/`, `.github/` and `requirements*` (46 code/test files)**. No third-party cryptography install or M2/P0.11 AES-GCM module remains. PR [CI 42375323936](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42375323936) and independent postmerge [main CI 42375384660](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42375384660) BOTH SUCCESS, **448/448 tests PASS on each Python 3.11 and 3.12**.
- Pre-extra-rollback current main snapshot branch `archive/forex-before-extra-m2-p10-rewind-20261107` at SHA `67e7b3a0d73fa1600c7c762827974bcc19ed07c2`; historical PR #29/#30 and earlier PR #31/#32/#33/#37 preserved for future audit; no force-push or history destruction.

## Controlled native-doc to GitHub exact extracted-text equivalence

| Native editable source | Frozen full GitHub text snapshot | Verified equality |
| --- | --- | --- |
| [00 Master Handoff **v0.37 §47**](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), native revision `AHj4eMTWbM-qWqzgmo6a-Lx8p6UQoILitf763jFjWRk3CTZ3PzgmgYpRGGBBsYjopmauTLXaTz4bQKv3O4-dIqivZj79gdmeL1bokdYGMQfm` | [Entire 00 source text](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `7c76e90813a33fdbdb49736c1cf2e377a1a2dde9` | **1676 native paragraphs, 450374 characters, EXACT** |
| [02 Master Spec **v0.12 §27**](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), native revision `AHj4eMTL7kS5K871aHwX9dTZX7iedryIt7Gd3PC-5YcZbzR-mNeUabvI9Nwx4qscjpDVjQMYQOR6jkvSG0eh5nTlhDTWslr10KnCCBSuehuz` | [Entire 02 source text](source-snapshots/02_MASTER_SPEC.txt), Git blob `1b7b5946ef637826b5d52805267eaedff9d3624d` | **281 native paragraphs, 68912 characters, EXACT** |

**Comparison algorithm:** `nativeDoc.paragraphs.map(p => p.text).join("\\n") + "\\n" === githubFetchedFullFileContent`. The check proves a point-in-time copy of **all extracted text**, not native Google Docs formatting or an always-on sync. Native Google Docs is the source of truth for document editing; GitHub `main` is the source of truth for code. Snapshot verification must be repeated after any future native edit.

## Historical context and frozen project state

- [Current extra-rollback audit](FOREX_FOURTH_MILESTONE_REWIND_20261107.md) and [earlier three-milestone rollback](FOREX_THREE_MILESTONE_REWIND_20261107.md). Earlier Handoff §46/QA §64 are previous states, **not active source**.
- M2/P0.10 synthetic Google Drive connector smoke **141B chunk + 439B manifest** from PR #27 remains preserved. Later #32 fabricated encrypted TESTPAIR00 files (753B + 644B) remain in the audit/quarantine Drive folder, not active cache; no deletion.
- No real licensed Forex BID/ASK price cache, 5-minute operational scanner, production key store, rollback witness, authorized Backtest/OOS or brokerage activity. All production gates **BLOCKED**; no implementation until user explicitly resumes in ONE chosen Forex conversation.
