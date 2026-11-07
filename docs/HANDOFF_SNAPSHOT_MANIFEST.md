# Forex Trading 1.0 — controlled Google Drive extracted-text snapshot manifest

**Captured:** 2026-11-07 (Asia/Ho_Chi_Minh), after M2/P0.4 synthetic 20-pair sweep and causal receipt custody PR #15. Editable Handoff/Spec are canonical on Google Drive; code/CI and these frozen point-in-time extracted-text copies are on PRIVATE GitHub. Independently reread and confirmed exact full-text equality on this docs branch; verify main again following docs PR merge.

| Native canonical Google Doc | Frozen GitHub extracted TEXT | Comparison |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.24 §34](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), revision `AHj4eMRaPbOkFqEaYKvJRP_5pxSo8SgXx9lTyjWaTZLKZCtoj6F0G8d_eqP1Kr12558cXEK0sEQdXlFoVX01YAQL6OcLz197Uw6Mg0OgBJNj` | [00 full Handoff](source-snapshots/00_MASTER_HANDOFF.txt), blob `a209cfa1bcaacefba09114430a71e0af9fa5871b` | **765 paragraphs, 198973 characters, EXACT_MATCH on docs branch** |
| [02_MASTER_SPEC v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), revision `AHj4eMTTg_rR-7qLQ9U70xibVMbckC13Z0ILEWzvqX6tmqDAr2dhUbn46zN90S1f12j3pd5czKLidxFreme3y_E1V_nDmALyDV9CkBO0kZsv` | [02 full Spec](source-snapshots/02_MASTER_SPEC.txt), blob `5751412eefa0590d210f8adf3302c26b4a83b764` | **260 paragraphs, 56797 characters, EXACT_MATCH on docs branch** |

**Exact comparison:** `(Google_Drive.get_document_text.paragraphs.map(p=>p.text).join("\n")+"\n") === GitHub.fetch_file.content` for each full document. This proves extracted **plain text** equality, not native Google Docs formatting/chips or two-way automatic sync. 00 Handoff §32 contains all extracted-text current 02 Spec v0.9; old §21 v0.8 snapshot is preserved for historical continuity. Source revisions are point-in-time evidence.

## Code and CI evidence

- User-approved Forex Smart Cache DEC-FX-020, current [02 Master Spec v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), isolated from Swing Trading.
- [PR #15](https://github.com/ngluonghoa/forex-trading-1-0/pull/15) main merge `336c87bebd1af2752211ac8da4fc86be3316c30c`: synthetic 20-pair × BID/ASK × M5/M15/H1/H4/D1 repeat-scan workload and first-seen causal source custody. [PR CI 42327775902](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42327775902) and [main CI 42327843231](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42327843231): Python 3.11/3.12 each **310/310 synthetic unit tests PASS**.
- Fixture-only 1640 counterfactual full-history candle rows vs 120 synthetic delta rows with **caller-claimed** unchanged head tokens; 200 partitions, 40 bounded plans. *Not* measured provider API calls/bytes, real latency, entitlement or actual 5-min cache speedup; no licensed BID/ASK prices, validated vendor revision feed, authenticated head, approved storage or broker order.
- `source_custody` local hash-chain and as-of first-seen guard is NOT a signed vendor evidence stream or external immutable anchor. A correction older than overlap may remain invisible in production.
- No actual HTTP source, persistent encrypted data store, restart/rollback drill, active scanner/Backtest/OOS/production release/LKG. No use of M15001, MOCHI or paid services.
