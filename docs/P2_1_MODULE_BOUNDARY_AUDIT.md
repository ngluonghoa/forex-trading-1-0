# P2.1 — Forex Module Boundary & Dependency Audit (DESIGN ONLY)
Date: 2026-11-07 | Status: PROPOSED / REVIEW ONLY | Scope: targeted source audit, no functional change
Project: Forex Trading 1.0, private GitHub repo
Source reference: main 2a78ac532702ee543f064ccf7c57f9c4e941dc58
Original executable baseline: M2/P0.10 PR #28 7f0904eefad9afe3da7bbaab522d8c59b6847c9e
Canonical design: native 02_FOREX_MASTER_SPEC v0.11 §26; canonical governance: native 00_MASTER_HANDOFF v0.38 §48; QA §68.
IMPORTANT: This proposal DOES NOT supersede any canonical document, and DOES NOT restore withdrawn M2/P0.11–P0.14 code.

## 1. Decision and scope
Approved direction: preserve Forex-specific domain and architecture; adopt strong engineering practices from Swing Trading only where genuinely compatible. Review module boundaries before changing Python behavior. This audit examines 10 named Forex source files plus three relevant test files, not the entire 46-file source/test tree. All findings below are scoped to the inspected files. No real FX feed, licensed storage, broker or Backtest is authorized.

## 2. Observed dependency edges on current main
| Module | Direct internal imports | Responsibility observed |
| --- | --- | --- |
| model.py | — | Direction, Horizon, ActionIntent, SignalStage, zone/signal domain types |
| quotes.py | model | UTC validation and BID/ASK indicative quote model |
| market_data.py | quotes | Observations, candle keys, first-known/revision/quality guards |
| source_qualification.py | market_data, quotes | Source capability/rights claims and read-only quality checks |
| cache_core.py | market_data, quotes | CachePartition, CandleSnapshot, delta plan/reconciliation |
| cache_storage_review.py | cache_core, quotes, source_qualification | Durable-store policy review and synthetic generation manifests |
| synthetic_scan_workload.py | cache_core, market_data, quotes | Synthetic 5-minute workload and stream reports |
| scan_selection.py | cache_core, quotes, synthetic_scan_workload | ScanMode/ScanSelection selection AND synthetic scan dispatch |
| synthetic_drive_cache_staging.py | cache_core, cache_storage_review, market_data, quotes, scan_selection | In-memory cache store AND mixed-scope fixture orchestration |
| synthetic_drive_receipt_validation.py | — | Offline validation of actual tiny Drive synthetic smoke receipts (no network calls) |

Observed shortest dependency chain:
- quotes -> model
- market_data -> quotes
- cache_core -> market_data + quotes
- synthetic_scan_workload -> cache_core
- scan_selection -> synthetic_scan_workload
- synthetic_drive_cache_staging -> scan_selection -> synthetic_scan_workload

Note: arrows in this section mean "imports", not data flow. No cycle was observed among these inspected edges. There is no evidence here that all other modules are cycle-free.

## 3. Findings
**P2.1-F01 — Selection domain coupled to synthetic tests (target for first refactor).**
ScanMode, ScanSelection and plan_scan_selection are useful for both fixture testing and a future real scan orchestrator; however, their present home scan_selection.py also imports SyntheticScanFixture, SyntheticSweepReport and run_synthetic_five_minute_sweep. Consequently a future production component importing the public selection contract would transitively import synthetic workload code. This is an architectural dependency concern, not a confirmed bug or operational failure.

**P2.1-F02 — Synthetic storage mixed with orchestration (separate later refactor).**
SyntheticDriveCacheStaging handles in-memory chunk state and validation; the same module hosts run_mixed_scope_synthetic_drive_scan, which knows about selection and fixture sweep semantics. These responsibilities can be separated later. Do not combine F01/F02 in one change; preserve public imports and tests.

**P2.1-F03 — Current data-quality isolation is worth keeping.**
CandleSnapshot/CachePartition in cache_core.py enforce pair/provider/product/side/timeframe/version isolation, close/verified coverage and as-of constraints. MarketBar/Observation and source claims remain distinct; self-reported quality and head IDs do not grant real rights. Keep unchanged unless independently justified.

**P2.1-F04 — Existing Drive test boundary is explicit.**
synthetic_drive_receipt_validation.py validates copied synthetic files offline. It neither implements Google Drive authenticated persistence nor vendor rights/KMS/CAS/actual five-minute savings. Do not promote smoke validation to production storage.

## 4. Proposed future small PR A — selection contract isolation
**New path (proposal, not created):** src/forex_trading/scan_contract.py
- Move unchanged ScanMode, ScanSelection and plan_scan_selection into scan_contract.py.
- Import only Python standard library modules in the new module; do not import synthetic workload, cache, vendor or broker dependencies.
- Retain scan_selection.py as a compatibility shim: re-export the same names, keep SelectedSyntheticScanReport and run_selected_synthetic_scan there.
- Leave synthetic_drive_cache_staging.py and existing imports unchanged for this PR. Preserve class identity through re-export, avoiding two competing enum/dataclass types.
- No changes to pair catalog rules or scope: SINGLE=1, CUSTOM=2..19, ALL=20 from caller-supplied catalog; fail closed on malformed/duplicate/unknown pairs.
- No change to external IO flags, source rights, BID/ASK side requirements, or fixture APIs.

**Acceptance for PR A:**
1. Old import paths still work and refer to the one canonical types/functions.
2. scan_contract.py has no import/path dependency on synthetic_scan_workload, cache_core, Google Drive or network/provider code.
3. Existing tests/test_scan_selection.py, tests/test_synthetic_drive_cache_staging.py and all repository tests remain passing.
4. New contract import/compatibility/corner-case tests, both Python 3.11 and 3.12; baseline is 448 existing tests per interpreter, not a forecast of the new total.
5. Identical results for SINGLE/CUSTOM/ALL, including 5→20→1→20 reuse and fail-closed incomplete BID/ASK; no change in external data requests (currently zero) or active snapshot data.
6. Compare new PR against M2/P0.10 source baseline: only approved new/relocated contract, compatibility imports and new tests may differ; no reintroduction of withdrawn PR #29–#37 code.
7. Run independent PR CI and postmerge main CI before claiming merged acceptance. Do NOT label this as complete merely because this design PR is merged.

**Rollback of future PR A:** Revert only PR A via reviewed GitHub PR after confirming no downstream importers/new schema dependency. No changes to data, manifests, migrations, Drive objects, signal rules or approved business catalog are expected.

## 5. Proposed future small PR B — synthetic cache store/orchestrator split
Only after PR A is verified: retain SyntheticDriveCacheStaging, SyntheticChunk and manifest validation in store module; relocate run_mixed_scope_synthetic_drive_scan and MixedScanResult to a synthetic-only orchestrator. Keep legacy imports as re-exports. Verify exact 5→20→1→20 fixture equivalence, stale writer/crash/quarantine behavior, and zero real IO. Must be its own independently reversible PR.

## 6. Non-goals and safety gates
- No implementation of segmented weekly cache, AES-GCM, real KMS, distributed CAS or off-host monotonic witness in P2.1.
- No live provider calls, true Drive raw-file storage adapter, scheduler, real trading, historical Backtest or OOS.
- No changes to active Master Spec v0.11, approved 18 labels (15 entry candidates), four LONG and SHORT display states, eight-stage pipeline, TP/Exit policy or 1/custom/20 scan modes.
- Design proposals are not substitute permissions for Forex-specific source retention/BID/ASK/cost data.
- FX repo only; no changes to Swing Trading, CK, FX 2.0, Scanner or Mac devices.
- A docs-only draft PR is the deliverable here. Do not merge a feature, rewrite Git history or silently move original M2/P0.10 source.

## 7. Completion criteria for P2.1 design review
- [x] Record observed module edges from current main and identify coupling with concrete paths.
- [x] Identify interfaces to preserve and propose the smallest reversible change.
- [x] Specify acceptance tests, non-goals and rollback boundary.
- [ ] Review/accept this plan as a design artifact.
- [ ] Implement future PR A (NOT STARTED).
- [ ] Verify future PR A CI and baseline behavior (NOT STARTED).
- [ ] Consider future PR B only after PR A success.
