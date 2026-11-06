# Google Drive canonical snapshot manifest — Forex Trading 1.0

**Snapshot taken:** 2026-11-07 (Asia/Ho_Chi_Minh). **Status:** full extracted point-in-time text, exact-content readback verified on source branch; latest v0.19 main readback pending docs PR merge. This is NOT a second editable business-spec source.

## Native source -> point-in-time extracted-text copy

| Source | Drive source document / revision | Repo snapshot | Verification |
| --- | --- | --- | --- |
| 00 Master Handoff v0.17, latest §27 | [Google Doc](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit) revision `AHj4eMQPZR9LjMf1LVTRtzLAbyLz-SOyvzD63FSLX1P3DqOkcR5Ywwx_fn_iVGRsORHyF6PVGL6LzMoKufxdggLAQZNYgYps4l4JHVrAMdvk` | [Full text](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `bc330284b7e4b4df6ffd2b562718bacb03793ecb` | 470 paragraphs; 119354 characters; EXACT_MATCH verified by independent GitHub fetch vs live Drive get_document_text |
| 02 Master Spec v0.8 | [Google Doc](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit) revision `AHj4eMT09W-jwTk1I4SBqcULN-RGKVl0C8ziS8-Neore1LAQSn7SAN6kBCZIRV2NwMo68SJNZXORA2wu6gPJMmIGZLtlIdjnA15opGW3C6j_` | [Full text](source-snapshots/02_MASTER_SPEC.txt), Git blob `9ac2b35bc086d9993a66dc464bfe0d46e121c064` | 247 paragraphs; 50785 characters; EXACT_MATCH verified by independent GitHub fetch vs live Drive get_document_text |

**Comparison method:** `(get_document_text.paragraphs.map(p=>p.text).join("\n") + "\n") === fetch_file.content`. This verifies **plain extracted text**; does not claim a native Docs layout/tables/chips/formatting parity. Both source documents remain canonical on Google Drive. Any later source edit changes the current authority and requires a new snapshot; this artifact is a frozen revision, never an automatic two-way synchronization.

**Governance:** Neither an exact doc snapshot nor synthetic CI establishes rights to market-data retention, validated detector performance, OOS robustness or live trading. M15001 remains prohibited; MOCHI is optional and was not used.
