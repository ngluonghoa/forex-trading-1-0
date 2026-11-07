# Forex Trading 1.0 — Canonical Google Drive extracted-text snapshot manifest

**Captured:** 2026-11-07 (Asia/Ho_Chi_Minh), after synthetic-only M2/P0.3 PR #13 and controlled Handoff v0.23 §33 update. Google Drive is authoritative for editable Spec/Handoff; GitHub is authoritative for code, CI and point-in-time frozen extracted-text copies. Independent exact branch readback was performed for both Docs. Separate main verification is required after this docs PR merges.

| Canonical Google Doc source | GitHub extracted text file | Exact source comparison |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.23 §33](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), revision `AHj4eMRekn4ni-3w2d8OY06aaA5u_ssSdIoNAO7eRvHKO3Ot8wq3-6YwQvrxvNXVRXS39YC5S0gSFClSlFnOIGrkvYbLUF2eay41zIw85NPG` | [00 full Handoff](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `cee6c5e4264f3bfdcfe857bef64848b3f66758fe` | **759 paragraphs / 194205 characters, EXACT_MATCH on docs branch** |
| [02_MASTER_SPEC v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), revision `AHj4eMTTg_rR-7qLQ9U70xibVMbckC13Z0ILEWzvqX6tmqDAr2dhUbn46zN90S1f12j3pd5czKLidxFreme3y_E1V_nDmALyDV9CkBO0kZsv` | [02 full Spec](source-snapshots/02_MASTER_SPEC.txt), Git blob `5751412eefa0590d210f8adf3302c26b4a83b764` | **260 paragraphs / 56797 characters, EXACT_MATCH on docs branch** |

Exact comparison method: `(Google_Drive.get_document_text.paragraphs.map(p=>p.text).join("\n")+"\n") === GitHub.fetch_file.content` for both sources. This proves extracted **plain text** equality only, not native Google Docs formatting, embedded chips/layout or live two-way sync. Native 00 Handoff v0.23 includes complete 02 Spec v0.9 text inside §32; older §21 v0.8 is historical.

## Code and QA receipts

- Approved Forex-specific five-layer Smart Incremental Cache: [DEC-FX-020 register](https://docs.google.com/document/d/1rZdd9tMfT98wH7oDvWlV-0n7EQvvIoUx1T6M79Gb0d8/edit), [Spec v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit).
- [Cache pure-core PR #11](https://github.com/ngluonghoa/forex-trading-1-0/pull/11), main SHA `caf0df610aeb5dd5b8e9e6ef01f41d5827f29e32`, [main CI 42323816487](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42323816487): 224/224 synthetic PASS per Python 3.11 and 3.12.
- [Synthetic BID/ASK delta+storage review PR #13](https://github.com/ngluonghoa/forex-trading-1-0/pull/13), main SHA `1f46b7e1df871609a19e53c8369cce5819f4eb70`. First PR CI 42325628149 FAILED one schema-message test; fixed before merge (commit `87e907f89347f3dc342d24cce23982c8a78d290a`). Final [PR CI 42325690593](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42325690593) and postmerge [main CI 42325743265](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42325743265): **275/275 synthetic PASS per Python 3.11 and 3.12**.
- `provider_delta_contract.py` strictly parses synthetic OANDA-v20-shaped BID/ASK overlap deltas; `cache_storage_review.py` enforces read-only storage proposal, and metadata-only generation checksum chain. No OANDA account, real source revision, raw data storage, authenticated vendor rights or benchmarks.
- **No 5-minute production poll, real historical BID/ASK source, encrypted durable cache, actual disk restart/rollback recovery, complete indicator/zone engine, Backtest/OOS, broker orders or active/LKG release.** No unauthorized M15001. MOCHI remains optional and untouched; no paid service.
