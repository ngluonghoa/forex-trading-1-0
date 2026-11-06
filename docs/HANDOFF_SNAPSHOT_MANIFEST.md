# Google Drive canonical snapshot manifest — Forex Trading 1.0

**Snapshot taken:** 2026-11-07 (Asia/Ho_Chi_Minh). **Status:** full extracted text in GitHub branch, exact-content readback verified BEFORE merge. This is NOT a second editable business-spec source.

## Native source -> point-in-time extracted-text copy

| Source | Drive source document / revision | Repo snapshot | Verification |
| --- | --- | --- | --- |
| 00 Master Handoff v0.17, latest §27 | [Google Doc](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit) revision `AHj4eMRmQlyA38TaPP6UAFdNVRpeNvMTybRtI61cmk7uOggYp0OtgNDA-8_hOGgFeVUwatU9orngdvwS83yZ5jYY-71LEpnpA0Qsp419O9-T` | [Full text](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `44b5c05567f8406ef2d92e0b03576556e208506b` | 454 paragraphs; 110396 characters; EXACT_MATCH verified by independent GitHub fetch vs live Drive get_document_text |
| 02 Master Spec v0.8 | [Google Doc](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit) revision `AHj4eMT09W-jwTk1I4SBqcULN-RGKVl0C8ziS8-Neore1LAQSn7SAN6kBCZIRV2NwMo68SJNZXORA2wu6gPJMmIGZLtlIdjnA15opGW3C6j_` | [Full text](source-snapshots/02_MASTER_SPEC.txt), Git blob `9ac2b35bc086d9993a66dc464bfe0d46e121c064` | 247 paragraphs; 50785 characters; EXACT_MATCH verified by independent GitHub fetch vs live Drive get_document_text |

**Comparison method:** `(get_document_text.paragraphs.map(p=>p.text).join("\n") + "\n") === fetch_file.content`. This verifies **plain extracted text**; does not claim a native Docs layout/tables/chips/formatting parity. Both source documents remain canonical on Google Drive. Any later source edit changes the current authority and requires a new snapshot; this artifact is a frozen revision, never an automatic two-way synchronization.

**Governance:** Neither an exact doc snapshot nor synthetic CI establishes rights to market-data retention, validated detector performance, OOS robustness or live trading. M15001 remains prohibited; MOCHI is optional and was not used.
