# Forex Trading 1.0 — Canonical Google Drive extracted-text snapshot manifest

**Captured:** 2026-11-07 (Asia/Ho_Chi_Minh), after user-approved DEC-FX-020 Forex Smart Incremental Cache design and GitHub source PR #11. Google Drive controls editable functional Spec/Handoff; GitHub controls code, CI and frozen text snapshots. Source text was independently reread and compared with GitHub branch files exactly. PR main readback requires separate verification after merge.

| Source Google Doc | Frozen GitHub text copy | Verified text |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.22 §32](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), revision `AHj4eMRd26YpW_Fcfvy4P5BezzeBIzY9PzPb-VzH3FRiUNkQXjo6TmZGO35FFS0Y_PfahOrrDRkgxn71i7wc_Fc7bjiAPg4Ghf_q0RVuO48g` | [00 full Handoff](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `3b7cabdd3e76878fc6bca6a146951306ab9fc144` | **753 paragraphs / 189693 characters, EXACT_MATCH on branch** |
| [02_MASTER_SPEC v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), revision `AHj4eMTTg_rR-7qLQ9U70xibVMbckC13Z0ILEWzvqX6tmqDAr2dhUbn46zN90S1f12j3pd5czKLidxFreme3y_E1V_nDmALyDV9CkBO0kZsv` | [02 full Spec](source-snapshots/02_MASTER_SPEC.txt), Git blob `5751412eefa0590d210f8adf3302c26b4a83b764` | **260 paragraphs / 56797 characters, EXACT_MATCH on branch** |

Exact comparison method: `(Google_Drive.get_document_text.paragraphs.map(p=>p.text).join("\n") + "\n") === GitHub.fetch_file.content` per document after commit. This is **extracted text**, not faithful Google Docs native layout/chips/tables or an automatic 2-way sync. Handoff §32 contains a verified complete embedded v0.9 Spec text; historical §21 v0.8 Spec copy remains preserved, but v0.9 §24 supersedes cache implementation detail. A later Drive change requires a new controlled snapshot.

## Code evidence and runtime boundary

- Decision: [01 Migration Register v0.12 §22 DEC-FX-020](https://docs.google.com/document/d/1rZdd9tMfT98wH7oDvWlV-0n7EQvvIoUx1T6M79Gb0d8/edit).
- [Forex cache PR #11](https://github.com/ngluonghoa/forex-trading-1-0/pull/11), squash main SHA `caf0df610aeb5dd5b8e9e6ef01f41d5827f29e32`.
- [PR GitHub CI 42323752852](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42323752852) and [main CI 42323816487](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42323816487): Python 3.11 and Python 3.12 each **224/224 synthetic unit tests PASS**.
- `cache_core.py`, `cache_dependency.py`, `cache_indicators.py` implement **pure in-memory synthetic reference only**, not any approved real vendor download, persistent store, signed head/rights, 5-minute task scheduler or production scanner. No actual gains in download speed or 20-pair runtime measured. No live broker activity; no M15001; MOCHI only optional with separate approvals.
