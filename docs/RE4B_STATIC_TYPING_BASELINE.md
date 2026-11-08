# RE4b — Static quality and strict typing of stable Forex contracts

**Scope:** new additive CI gates only, RE4b first slice. No runtime source changes, indicator changes, cache migration, broker operation, release, release tag, LKG, data vendor access or master business spec edits. Propose one small PR on top of RE4a Handoff-sync PR #63.

## Baseline and gate design

- Keep the same `python-unittest` job identity, Python 3.11/3.12 matrix, 528 existing synthetic tests and artifact parity smoke checks.
- Preserve prior pinned Ruff v0.13.0 critical checks `E9,F63,F7,F82` over `src tests tools`; add blocking `E4,E7` error classes on the same full tree.
- Apply complete Pyflakes `F` in strict blocking mode to five self-contained, already typed foundational contracts: `model.py`, `pipeline.py`, `scan_contract.py`, `versioning.py`, `release_readiness.py`.
- Run pinned mypy 1.18.2 `--strict` on exactly the five contracts above under Python 3.11 semantics. Includes static analysis of dependencies actually imported; never use `--ignore-missing-imports`, `--follow-imports=skip`, `--disable-error-code` or global `# type: ignore` in CI to manufacture passing evidence.
- Intentional legacy re-export and module shims (especially `synthetic_drive_cache_staging.py`) have not been migrated to full `F` or strict mypy yet. Broader full-project lint, type coverage, formatting, tests/tool typing and security scanning remain OPEN, not implicitly PASS.
- Pinned type/lint tools are installed in CI only; they are **not production dependencies**, do not change `pyproject.toml`, and cannot publish/activate Forex trades.

## Evidence and failure handling

GitHub Actions PR and postmerge main logs must independently show the exact strict-type and Ruff commands PASS in each Python job, baseline unittests PASS and twice-built wheel SHA parity. If either job fails, do not merge; inspect source/CI diagnostics and make an isolated reviewed fix, never globally suppress errors or edit unrelated domain logic. For a clean revert, revert this PR's CI and this audit doc without touching stateful caches, broker state, previously merged RE4a, or historical M2/P0.10 rollback archive.

**STATUS: PROPOSED / CI NOT YET OBSERVED WHEN WRITTEN.** Google Drive 00 Handoff v0.45 §55, 06 QA v0.60 §75 and 10 Release Standard v1.5 §17 remain current until independently verified PR results and canonical document updates.
