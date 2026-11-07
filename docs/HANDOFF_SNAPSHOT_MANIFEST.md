# Forex Trading 1.0 — exact active-source restoration and controlled native snapshots

**Audit date:** 2026-11-07 (Asia/Ho_Chi_Minh). **ACTIVE code baseline M2/P0.10** — original merged source/docs commit `7f0904eefad9afe3da7bbaab522d8c59b6847c9e`, source-era original Handoff **v0.30 §40**. The **current editable Handoff v0.38 §48** documents later rollback operations and deep audit only; it does **not** imply later source milestone. **ACTIVE normative 02 Master Spec v0.11 §26** is RESTORED character-exact to the source-era baseline. Historical v0.12 §27 is archived in old Handoff §43 and Git revisions, **not normative**.

## GitHub source and QA

- Source rollback [PR #43](https://github.com/ngluonghoa/forex-trading-1-0/pull/43) + prior #39/#41 reverted the later M2/P0.11–M2/P0.14 prototype modules, tests, dependency file and test-only CI installer. [Docs PR #44](https://github.com/ngluonghoa/forex-trading-1-0/pull/44) documented code baseline before the later Master Spec gap was found.
- **47/47 Git blob SHAs identical** for files under `src/`, `tests/`, `.github/` and `requirements*` at original `7f0904eefad9afe3da7bbaab522d8c59b6847c9e` versus audited main `8adc7278cebe5244a725bcb277a3e75a963bf63b`; 46 source+test files and the original single CI workflow. No active M2/P0.11 AES-GCM, weekly-segment prototype or synthetic fill simulator, and no third-party cryptography dependency.
- [Independent GitHub main Actions 42375920559](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42375920559) completed SUCCESS at audited SHA; **448/448 synthetic tests PASS per Python 3.11 and 3.12**. Latest documentation updates only; rerun CI and exact tree comparison after the docs PR merges.
- Prior feature branches, archived snapshot branches and merged PRs are deliberately retained as historical evidence, NOT active deployments; GitHub had zero open PRs and no releases at audit.

## Canonical native Google Docs ↔ complete GitHub snapshot text

| Native editable source | GitHub immutable text snapshot | Exact native text parity |
| --- | --- | --- |
| [00_MASTER_HANDOFF **v0.38 §48**](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), native revision `AHj4eMRVi8_YCbIKY9U9LSd8yTAx1-Q1CTv36LyGm8oOnbc62V7OJ-NMx6f6hyqoMghi_bNEkOw6p8OHob7ODUJOo5AfA6ej77biaIgAjlS0` | [Entire 00 Handoff](source-snapshots/00_MASTER_HANDOFF.txt) · blob `6d1b4ac428241e30461e2cbf174d51c3aa6e6bd5` | **1682 paragraphs · 454528 characters · EXACT** |
| [02_MASTER_SPEC **v0.11 §26**](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), native revision `AHj4eMS8gMntscY_hO6GQMfmS0SWgRCO7pW7ockHZV4_jrppz9VbGvi-Q38vLPWwHIWbdiiyzmOAnjT4PtfYQgBqWcYFbEegOA84DUkPA6iC` | [Entire 02 Spec](source-snapshots/02_MASTER_SPEC.txt) · blob `024d1f2c0d0997230e0ae97bfcf60d3880c39832` | **273 paragraphs · 63846 characters · EXACT original M2/P0.10** |

Comparison contract: `get_document_text.paragraphs.map(p => p.text).join("\n") + "\n" === GitHub fetched file content`. This tests all extracted text as of the indicated native revisions, not Google Docs rich formatting or continuous real-time synchronization. Version history and old complete v0.12 remain recoverable. Updates must use controlled branch/PR, protected CI and postmerge exact readback; Github is the code authority and native Docs the current editable design authority.

## Google Drive cache files — active vs quarantine

- Active synthetic staging `01_IMMUTABLE_CHUNKS__STAGING`: only original M2/P0.10 **141-byte** file `1HgjhwKJW2JzuO_OL8ODl45GdsW9bGv3h`. Active synthetic staging `00_MANIFESTS_AND_INDEX__STAGING`: only original M2/P0.10 **439-byte** manifest `1j7yevV6EgH7fyKj5uok5iOqrF1dGBegK`.
- `02_AUDIT_AND_QUARANTINE__STAGING`: later PR #32 fabricated encrypted TEST-only **753-byte** chunk `1IfzBILWfo6dAPHBIdvPpY52QQ3XVsDaR` and **644-byte** manifest `1Be06jBxGDpjeKHpzJdA0XMLHoY4I7lCF`, preserved but NOT active.
- Original decision ledger 01 v0.14 and business docs 03–05/07–10 predate source-era checkpoint; preserved. 00/06 document later audit chronology intentionally retained. See [deep audit](FOREX_ROLLBACK_DEEP_AUDIT_20261107.md) and [source rollback audit](FOREX_FOURTH_MILESTONE_REWIND_20261107.md).

**FROZEN:** no licensed native FX BID/ASK data cache, production encrypted Drive storage, trusted KMS/witness/lease/CAS, operational five-minute scanner, strategy Backtest/OOS, real broker orders or active release. Do not resurrect removed code or v0.12 §27 design from historical branches without new explicit user approval and a single Forex development conversation.
