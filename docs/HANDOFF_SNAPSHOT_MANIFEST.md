# Forex Trading 1.0 — controlled full-text snapshot manifest

**Captured:** 2026-11-07 (Asia/Ho_Chi_Minh), after M1/P0.3 PR #7. **State:** independently verified exact extracted-text equality on this source branch; verify again after docs PR merge to `main`. Google Drive remains canonical for editable requirements and Handoff. GitHub is canonical only for versioned code and frozen snapshot evidence.

| Native Drive canonical source / source revision | GitHub snapshot (plain extracted text) | Captured result |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.20 §30](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), revision `AHj4eMTab9_2VMqS0qh1G22YZHDVWoDkAmlx6ZRb8x6yGsD_rNZKY_0qHqdMjmsvB5l3N5okmktgmwblV3G2Rf2sLBjuiRZq-LtFi_uaoNoF` | [00_MASTER_HANDOFF.txt](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `70ad4e13e4b6b46b0eef78fa72bdbaf4311fe4b1` | **477 paragraphs, 123707 characters; EXACT_MATCH on PR branch** |
| [02_MASTER_SPEC v0.8](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), revision `AHj4eMT09W-jwTk1I4SBqcULN-RGKVl0C8ziS8-Neore1LAQSn7SAN6kBCZIRV2NwMo68SJNZXORA2wu6gPJMmIGZLtlIdjnA15opGW3C6j_` | [02_MASTER_SPEC.txt](source-snapshots/02_MASTER_SPEC.txt), Git blob `9ac2b35bc086d9993a66dc464bfe0d46e121c064` | **247 paragraphs, 50785 characters; EXACT_MATCH on PR branch** |

**Exact-text comparison contract:** `(get_document_text.paragraphs.map(p => p.text).join("\n") + "\n") === GitHub.fetch_file.content`, checked separately for both documents. Comparison covers extracted plain text, not Google Docs visual layout, tables, chips or formatting. This is NOT automatic bidirectional sync; a new edited Drive revision needs a new controlled snapshot PR. Git blob SHA and Google Docs revision identify point-in-time text custody, not vendor market data entitlement or approved trading software.

**Code receipt:** [M1/P0.3 PR #7](https://github.com/ngluonghoa/forex-trading-1-0/pull/7) main merge `556b904124f378a8b8e1a78590b4d634d22ae16b`, [PR CI 42274337404](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42274337404) and [main CI 42274433483](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42274433483) both 133/133 synthetic unit tests per Python 3.11 and 3.12, SUCCESS. SHA-256 pin of *synthetic TZif bytes* does not constitute authentic tzdb vendor provenance or a real licensed BID/ASK source.

**Host boundaries:** no M15001. MOCHI optional/not used. No licensed data was accessed or persisted in this artifact.
