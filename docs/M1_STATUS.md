# Forex M1 status: independent GitHub repo foundation

## Proven engineering results (2026-11-07, Asia/Ho_Chi_Minh)

Private repo: https://github.com/ngluonghoa/forex-trading-1-0, owner `ngluonghoa`, default branch `main`. Swing project untouched; MOCHI optional/offline, M15001 NOT AUTHORIZED.

- Source PR #1: https://github.com/ngluonghoa/forex-trading-1-0/pull/1
- Failed branch Actions first attempt 42267350324 — Python 3.11/3.12 catalog type-name NameError. Root cause repaired in commit `a94a16f7c05caa4a77b3ea1d5426a9154aee080a`.
- Successful FINAL PR Actions https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42267449139 — Python 3.11: 41/41 synthetic tests PASS; Python 3.12: 41/41 synthetic tests PASS. Compileall PASS both.
- PR #1 squash merged main SHA `59c7ebf1f7fb99d817c6a702944acadaf9c33fd7`. Main README and merged commit inspected.
- **Post-merge MAIN GitHub Actions CI:** NOT INDEPENDENTLY VERIFIED (PR-focused connector run lookup). Do not claim main CI passed.
- Full extracted-text Drive 00/02 snapshots added in a separate docs branch, with exact-match source readback. See [snapshot manifest](HANDOFF_SNAPSHOT_MANIFEST.md); main snapshot merge/CI requires separate verification.

## M1 scope that exists
Typed frozen Python DTOs, 18 design labels/15 entry candidate classification, four action-intents/quote sides, UTC first-known and quality guards, display status vocab, pipeline stages, full-profile fingerprint and READ-ONLY rollback compatibility preview. Neither `assess_rollback()` nor `can_publish_full_analysis()` grants market/trade eligibility.

## Not yet implemented or tested
Actual calibrated B2/S2 or other zone predicates, licensed historical FX BID/ASK coverage and revisions, real entry/exit/SL/TP/cost/financing fill simulator, real Backtest and OOS/walk-forward, persistent cache/runtime/backup restore drill, full formal FX-VR-01..20 and TEST-TPX-01..32, branch protection/ruleset, production release tag or LKG.

**Next:** verify main post-merge CI and docs PR main readback; extend temporal and source-quality contract with synthetic tests, pin and review dependency/action supply chain, configure branch controls if GitHub plan supports, then qualify data source M2 before starting trading-detector M3.
