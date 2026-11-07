# Forex Trading 1.0 — exact native Google Docs snapshot after three-milestone rollback

**2026-11-07 (Asia/Ho_Chi_Minh).** Canonical native Google Drive documents are editable sources of truth; GitHub files are complete, immutable-by-commit text snapshots. Following user-requested rollback, current code/tests have **48/48 exact blob SHA parity** with M2/P0.11 `aa411515d837e59664cf4a9fdfbe1a3caf7ab5e2`, established by [PR #41](https://github.com/ngluonghoa/forex-trading-1-0/pull/41) main `eaceb402e90d13482dcaddd160fc20da490551da`, independently [472/472 tests per Python 3.11/3.12](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42373765837). This document records **exact text parity**, not any real price cache or trading permission.

| Current canonical native source | Exact GitHub text snapshot | Verification |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.36 §46](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), native revision `AHj4eMRCz_c2NF4FRD7Tp11cK7PWzjTkJ3C22Xu5zY6GJrWWN3QORBgUcdg2NY4LSiD0bs0IxNT_EiAG6478nvn2UzvvBDj2GKfzsWYoeOZb` | [Complete 00 text](source-snapshots/00_MASTER_HANDOFF.txt), blob `463846dd760f2cc57020b615fb7a559c5a8fd8a4` | **1669 native paragraphs, 446981 characters, EXACT** |
| [02_MASTER_SPEC v0.12 §27](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), native revision `AHj4eMTL7kS5K871aHwX9dTZX7iedryIt7Gd3PC-5YcZbzR-mNeUabvI9Nwx4qscjpDVjQMYQOR6jkvSG0eh5nTlhDTWslr10KnCCBSuehuz` | [Complete 02 text](source-snapshots/02_MASTER_SPEC.txt), blob `1b7b5946ef637826b5d52805267eaedff9d3624d` | **281 native paragraphs, 68912 characters, EXACT** |

**Exact comparison contract:** `Google_Drive.get_document_text.paragraphs.map(p=>p.text).join("\\n")+"\\n" === GitHub.fetch_file.content`. It verifies extracted paragraph text, **not rich Docs formatting, chips, source permissions or continuous synchronization**. Canonical Spec v0.12 at Handoff §43 is previously approved **design only**; all references to #31/#32/#33/#37 as active implementation are SUPERSEDED by §46. Historical Handoff v0.35 §45 rollback and before are retained as audit, not current NEXT.

## Scope and safety

- Prior selective rollback [#39](https://github.com/ngluonghoa/forex-trading-1-0/pull/39) removed standalone #31/#33; complete user-requested three-milestone rollback [#41](https://github.com/ngluonghoa/forex-trading-1-0/pull/41) removed remaining #32/#37. Pre-rollback archive branch `archive/forex-pre-three-milestone-rewind-20261107` stores SHA `b47bfd09936e252bc1b6b93b2ab401597d9f11d9`; historical PRs remain recoverable.
- [Rollback evidence](FOREX_THREE_MILESTONE_REWIND_20261107.md) includes moved synthetic TESTPAIR00 Drive files to Audit & Quarantine without deletion; older #27 smoke preserved. No real Forex historical prices uploaded or broker trades.
- No more Forex engineering until user explicitly resumes in one chosen chat. All real vendor entitlement, protected key custody, production Drive cache, Backtest/OOS, and trading release gates remain BLOCKED.
