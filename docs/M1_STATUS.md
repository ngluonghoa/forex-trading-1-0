# Forex M1 Implementation / Evidence Register

**Scope:** M1 repository foundation (NOT a release; not a trading strategy).

## Evidence distinctions
- Repository must be verified PRIVATE in owner `ngluonghoa`, independent of Swing.
- This feature branch adds Python 3.11+ modular immutable domain contracts and synthetic tests.
- GitHub Actions workflow proposes a Python 3.11/3.12 matrix with compileall and unittest.
- **TEST STATUS: NOT_RUN until CI run is observed**. A workflow file or declared tests are not a PASS.
- No external runtime, licensed raw quote, broker position, historical Backtest, OOS, signal effectiveness, or active/LKG profile.

## M1 Acceptance Checklist
- [x] User created independent private GitHub repository.
- [x] Feature branch / scope governed by reviewed PR policy.
- [x] Read-only immutable domain/quote/catalog/profile/pipeline contract code authored.
- [ ] Branch GitHub CI verified PASS for both supported Python versions.
- [ ] PR accepted and main merge SHA / post-merge CI verified.
- [ ] Rule/parameter contract static checks and source qualification are future gates.
- [ ] End-to-end typed component architecture, negative cases, full state rollback drill, LKG: NOT DONE.

## History / host boundary
M15001-FG-3 was not approved and its prior prototype was explicitly removed. None of that local code or its test evidence is reused here. MOCHI offline does not block GitHub code/CI. Do not use M15001 as fallback.

Source: [Forex Handoff, latest §26](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit).
