# Forex Trading 1.0 — canonical Drive text snapshot manifest

**Captured:** 2026-11-07 (Asia/Ho_Chi_Minh) after M2/P0.1 source qualification code PR #9. Branch exact-text verification completed; main post-merge readback to be verified separately. Google Drive is canonical for editable Handoff and business Spec; GitHub is canonical for code and these frozen point-in-time extracted TEXT copies.

| Native Drive canonical source / revision | GitHub extracted TEXT | Comparison |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.21 §31](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), revision `AHj4eMR4-Qpi0ZSQnG6cKfz5lGm9VOOBLzVlF_47YJX1qRbaKdrz4836IgX_iQfg7Tx0k08fPClnRh9KuTWzhcPYSMjETnR69LJ5lhXsomrm` | [00 full Handoff](source-snapshots/00_MASTER_HANDOFF.txt), blob `8ab9a10c37fc4289f97f635021e457ee61d439f9` | **484 paragraphs, 128963 characters; EXACT_MATCH in docs branch** |
| [02_MASTER_SPEC v0.8](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), revision `AHj4eMT09W-jwTk1I4SBqcULN-RGKVl0C8ziS8-Neore1LAQSn7SAN6kBCZIRV2NwMo68SJNZXORA2wu6gPJMmIGZLtlIdjnA15opGW3C6j_` | [02 full Spec](source-snapshots/02_MASTER_SPEC.txt), blob `9ac2b35bc086d9993a66dc464bfe0d46e121c064` | **247 paragraphs, 50785 characters; EXACT_MATCH in docs branch** |

**Comparison:** `(get_document_text.paragraphs.map(p=>p.text).join("\n") + "\n") === GitHub.fetch_file.content` on independent native Google Docs read vs GitHub branch read. This verifies *extracted plain text*, not native Google Docs formatting/chips/tables/visual layout. No automatic two-way sync; subsequent Drive changes require another snapshot PR.

**M2 source rights code receipt:** [PR #9](https://github.com/ngluonghoa/forex-trading-1-0/pull/9) merged `0345a9f7d158de1d04148ee9ac7b317a214b27a3`; [PR CI run 42277238158](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42277238158) and [main CI run 42277351212](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42277351212) SUCCESS, Python 3.11/3.12 **167/167 synthetic unit tests each**. None of these are real provider entitlement, verified BID/ASK history, broker execution or financial Backtest proof.

**Restrictions:** no M15001, MOCHI optional, no real licensed source data stored, no paid service or live trading.
