# Forex Trading 1.0 — exact active-source restoration and controlled native snapshots

**Audit date:** 2026-11-08 (Asia/Ho_Chi_Minh). **CURRENT GOVERNANCE: P2.2 REVIEW COMPLETE, SOURCE: P2.1-A+B.** Documentation PR #52 merged main `fb62ba24d87ba1024ac9ccda285554f504dea284` (no source changes). Latest reviewed Python source remains PR #50 `238de5454187c2312e885d45dbcae6107e25818f` after PR #48 `e8cf43830fd6f7086f4366a43363d3eabb2d99f4`. Historical immutable M2/P0.10 rollback SHA `7f0904eefad9afe3da7bbaab522d8c59b6847c9e`. Native Handoff **v0.41 §51**, QA **v0.56 §71**, normative Master Spec 02 **v0.11 §26** (unchanged). Exactly seven intentional P2.1 source/test paths differ from the historical rollback, but no src/test change occurred under P2.2 docs PR #52. Historical QA 47/47 blob parity remains a source-era audit, not a current main claim.
## GitHub source and QA

- Source rollback [PR #43](https://github.com/ngluonghoa/forex-trading-1-0/pull/43) + prior #39/#41 reverted the later M2/P0.11–M2/P0.14 prototype modules, tests, dependency file and test-only CI installer. [Docs PR #44](https://github.com/ngluonghoa/forex-trading-1-0/pull/44) documented code baseline before the later Master Spec gap was found.
- **47/47 Git blob SHAs identical** for files under `src/`, `tests/`, `.github/` and `requirements*` at original `7f0904eefad9afe3da7bbaab522d8c59b6847c9e` versus audited main `8adc7278cebe5244a725bcb277a3e75a963bf63b`; 46 source+test files and the original single CI workflow. No active M2/P0.11 AES-GCM, weekly-segment prototype or synthetic fill simulator, and no third-party cryptography dependency.
- [Independent GitHub main Actions 42375920559](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42375920559) completed SUCCESS at audited SHA; **448/448 synthetic tests PASS per Python 3.11 and 3.12**. Latest documentation updates only; rerun CI and exact tree comparison after the docs PR merges.
- Prior feature branches, archived snapshot branches and merged PRs are deliberately retained as historical evidence, NOT active deployments; GitHub had zero open PRs and no releases at audit.

## Canonical native Google Docs ↔ complete GitHub snapshot text

| Native editable source | GitHub immutable text snapshot | Exact native text parity |
| --- | --- | --- |
| [00_MASTER_HANDOFF **v0.41 §51**](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), native revision `AHj4eMQHHiRwE3uLAzeowMs2S8EV7uIkK5fZLP1MWaL6ACH7yN9SNLMFbcFAap0NU40VSMhZ5SqXRjaGnkeLeyhPGlwZaM0RCqHPgrdC5jxy` | [Entire 00 Handoff](source-snapshots/00_MASTER_HANDOFF.txt) · blob `37f1788acfa7f6a16a8a9c81ed4d29285c22e6b6` | **1711 paragraphs · 467167 characters · EXACT after P2.2 review** |
| [02_MASTER_SPEC **v0.11 §26**](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), native revision `AHj4eMS8gMntscY_hO6GQMfmS0SWgRCO7pW7ockHZV4_jrppz9VbGvi-Q38vLPWwHIWbdiiyzmOAnjT4PtfYQgBqWcYFbEegOA84DUkPA6iC` | [Entire 02 Spec](source-snapshots/02_MASTER_SPEC.txt) · blob `024d1f2c0d0997230e0ae97bfcf60d3880c39832` | **273 paragraphs · 63846 characters · EXACT original M2/P0.10** |

Comparison contract: `get_document_text.paragraphs.map(p => p.text).join("\n") + "\n" === GitHub fetched file content`. This tests all extracted text as of the indicated native revisions, not Google Docs rich formatting or continuous real-time synchronization. Version history and old complete v0.12 remain recoverable. Updates must use controlled branch/PR, protected CI and postmerge exact readback; Github is the code authority and native Docs the current editable design authority.

## Google Drive cache files — active vs quarantine

- Active synthetic staging `01_IMMUTABLE_CHUNKS__STAGING`: only original M2/P0.10 **141-byte** file `1HgjhwKJW2JzuO_OL8ODl45GdsW9bGv3h`. Active synthetic staging `00_MANIFESTS_AND_INDEX__STAGING`: only original M2/P0.10 **439-byte** manifest `1j7yevV6EgH7fyKj5uok5iOqrF1dGBegK`.
- `02_AUDIT_AND_QUARANTINE__STAGING`: later PR #32 fabricated encrypted TEST-only **753-byte** chunk `1IfzBILWfo6dAPHBIdvPpY52QQ3XVsDaR` and **644-byte** manifest `1Be06jBxGDpjeKHpzJdA0XMLHoY4I7lCF`, preserved but NOT active.
- Original decision ledger 01 v0.14 and business docs 03–05/07–10 predate source-era checkpoint; preserved. 00/06 document later audit chronology intentionally retained. See [deep audit](FOREX_ROLLBACK_DEEP_AUDIT_20261107.md) and [source rollback audit](FOREX_FOURTH_MILESTONE_REWIND_20261107.md).

**PRODUCTION BLOCKED:** no licensed native FX BID/ASK data cache, production encrypted Drive storage, trusted KMS/witness/lease/CAS, operational five-minute scanner, strategy Backtest/OOS, real broker orders or active release. Source engineering has resumed only through reviewed P2.1 PR #48; do not resurrect removed code or normative v0.12 §27 from historical branches without new approval.


## P2.1 verified addendum — post-safe-rollback version distinction

- Current native Google Drive QA [v0.54 §69](https://docs.google.com/document/d/19CGNHVw1QqnTifmtf1Xu5bst0IAbEWLhQlgOoVzfYZg/edit) revision `AHj4eMQ5ZAt3EDwPPCJOz97bNfM_C0vakYBpujW89Oh9_E5lx6AggrEx9CVjIBOwYo7iY0ZMQ6gvtUDDvOgdrk_7F-p87qJCRieWKd37iqYI`, 634 paragraphs, 207534 extracted characters; Drive QA is authoritative and is not replicated as a second normative spec.
- GitHub [source PR #48](https://github.com/ngluonghoa/forex-trading-1-0/pull/48) merged as `e8cf43830fd6f7086f4366a43363d3eabb2d99f4` with exactly three source/test paths: `src/forex_trading/scan_contract.py` added, `scan_selection.py` legacy re-export, `tests/test_scan_contract_boundary.py` with six tests. PR Actions [42391199891](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42391199891) PASS **454/454 per Python 3.11 and 3.12** from downloaded job logs.
- GitHub [design audit PR #47](https://github.com/ngluonghoa/forex-trading-1-0/pull/47) merged as `09523533451d21274b187a987c1cf590e486dabb`; CI [42391405011](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42391405011) PASS **454/454 per Python version**. The audit doc is `docs/P2_1_MODULE_BOUNDARY_AUDIT.md`.
- Current source is **not** 47/47 blob identical to original M2/P0.10 because three approved P2.1 files now differ; rollback SHA `7f0904e` and previous audits are retained. No vendor IO/retention, production cache, detector/backtest or broker actions were activated.
- A docs-only branch publishes Handoff v0.39 snapshot. Exact text contract is `get_document_text.paragraphs.map(p => p.text).join("\n") + "\n" === GitHub snapshot`. Native Handoff revision `AHj4eMSsm-vJvCpsoJSDFtzPmPeAF-g1gooicLKHafL99yhSVlh_k0H00Wibnu-vcTHdUeE8zbYKEmVdqAf5xRrV3AEA1eD_JViCVLnOEVy4`; `1691` paragraphs, `458539` characters. Postmerge main CI for new source has not been independently verified; keep this gate OPEN rather than infer it from PR CI.


## P2.1-B independent evidence and current native QA (§70)

- Native QA [v0.55 §70](https://docs.google.com/document/d/19CGNHVw1QqnTifmtf1Xu5bst0IAbEWLhQlgOoVzfYZg/edit) revision `AHj4eMQGOaujQ0WtnWhbZYS0x64LuV2_fVAePe_bZywqUZJFJkb36fea0BtRgbGtF1Ut_jvGZsBZY4_APnYc83ifxXM0ijA7l9eDngOngjDG`, 643 paragraphs / 210936 extracted characters; QA is canonical on Drive, not a replacement for Master Spec.
- [Source PR #50](https://github.com/ngluonghoa/forex-trading-1-0/pull/50) merged `238de5454187c2312e885d45dbcae6107e25818f`; **exactly four source/test paths**: new store, new orchestrator, compatibility shim, seven new tests. [Actions run 42392919832](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42392919832) SUCCESS with Python 3.11 **461/461 tests OK** and Python 3.12 **461/461 tests OK** from independently inspected logs.
- Code relocation was mechanically checked against previous original source for four exact functional blocks: cache action/chunk, store class, result dataclass and runner function. New package imports remain synthetic-only; no licensed source requests, authenticated Drive cache, persistent KMS/CAS, trading or Backtest authorization.
- This Handoff snapshot is exact extracted paragraph text at native revision `AHj4eMT7pj8Iah1uOUKapCCKyqXenOmUDazl9JsCbcs50clzTFVffNOV3qBCu2kwvqRbWE2OydwqERfeTUzmKogmWgq_I1SLIhEBrUxIK-Ub`: 1701 paragraphs / 462680 characters, plus final newline; blob `017d2fb4c16011618ced415923801edfc728bedb`. Native 02 Master Spec remains unchanged. Independent postmerge MAIN-push CI has not been observed; avoid conflating PR CI with main CI.


## P2.2 read-only data contract review evidence (2026-11-08)

- [P2.2 docs PR #52](https://github.com/ngluonghoa/forex-trading-1-0/pull/52) MERGED main `fb62ba24d87ba1024ac9ccda285554f504dea284` from baseline `941e2ef775e03ef77b1ce76fed32a3e0a38f2959`. Single added file [P2.2 Forex data contract review](P2_2_FOREX_DATA_CONTRACT_INTERFACE_REVIEW.md), 8 findings, 5 future reviewable code gates. No source/test/CI/config changes.
- Independent PR GitHub Actions [42394635779](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42394635779) SUCCESS, downloaded job logs: 461/461 tests PASS Python 3.11 and 461/461 PASS Python 3.12, the unchanged P2.1-A+B suite.
- Native QA [v0.56 §71](https://docs.google.com/document/d/19CGNHVw1QqnTifmtf1Xu5bst0IAbEWLhQlgOoVzfYZg/edit), revision `AHj4eMSp4nmZaZQZJlgejPFAnl82g40ohk6xbNWE2TLLE-Z45RpzeSM7va18N4QDpW5Xdtv4UN7su9Xi5eSKteIWvGKrAHEkN-HdrWMLOpkF`, 652 paragraphs and 214949 characters extracted; remains canonical on Drive rather than replicated as a second normative spec.
- Native Handoff revision `AHj4eMQHHiRwE3uLAzeowMs2S8EV7uIkK5fZLP1MWaL6ACH7yN9SNLMFbcFAap0NU40VSMhZ5SqXRjaGnkeLeyhPGlwZaM0RCqHPgrdC5jxy`: 1711 paragraphs / 467167 characters, plus final newline. Exact Unicode source text equals this branch's GitHub snapshot at blob `37f1788acfa7f6a16a8a9c81ed4d29285c22e6b6`.
- P2.2-A additive stream/product binding contract is proposed but NOT STARTED; source/release claims remain synthetic/unverified. Source PR #50 and seven intentional source/test paths remain unchanged. Independent postmerge main push CI not verified by available connector.
