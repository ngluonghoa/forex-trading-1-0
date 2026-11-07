# Forex Trading 1.0 — controlled Google Drive extracted-text snapshot manifest

**Captured:** 2026-11-07 (Asia/Ho_Chi_Minh), after M2/P0.6 synthetic rights-to-cache invalidation and atomic recovery PR #19. Canonical editable Handoff/Spec remain Google Docs; canonical code/CI and frozen text snapshots remain private GitHub. This PR checks full extracted-text equality against native Docs and leaves the business Spec unchanged.

| Native canonical Google Doc | Frozen GitHub extracted TEXT | Comparison |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.26 §36](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), native revision `AHj4eMQxydBZu6xkV1c6_ub_4wWHG4zzR6O4nP5Ghw-zdojroYVhx2GeXlm_qTFLTDsrNKS3uxtZUV5Lu7riqO9BUF_KAODnx6UuMO3KD220` | [00 full Handoff](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `4efec28b381a268e6944f0c5ff9f03a70237c7dd` | **777 paragraphs, 208656 characters, EXACT_MATCH on docs branch** |
| [02_MASTER_SPEC v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), native revision `AHj4eMTTg_rR-7qLQ9U70xibVMbckC13Z0ILEWzvqX6tmqDAr2dhUbn46zN90S1f12j3pd5czKLidxFreme3y_E1V_nDmALyDV9CkBO0kZsv` | [02 full Spec](source-snapshots/02_MASTER_SPEC.txt), Git blob `5751412eefa0590d210f8adf3302c26b4a83b764` | **260 paragraphs, 56797 characters, EXACT_MATCH on docs branch; unchanged** |

Extraction equality is `(Google_Drive.get_document_text.paragraphs.map(p=>p.text).join("\n")+"\n") === GitHub.fetch_file.content`. It compares **text only**, not native Docs styling/chips/layout or continuous synchronization. Handoff §32 contains full v0.9 Spec; older v0.8 text at §21 is historical.

## M2/P0.6 engineering evidence and nonclaims

- [PR #19](https://github.com/ngluonghoa/forex-trading-1-0/pull/19) merged source main `5211ef2131cdaf4bef78b4629e46107f2626f2dc`, [PR CI 42334294778](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42334294778) and independent [main CI 42334368272](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42334368272), each **374/374 synthetic tests per Python 3.11/3.12**. Baseline 349→374 (+25 tests).
- Rights review now models invalidation of specified opaque cache partitions and L1–L5 on actual-known expiry/revocation; fail-closed on denied/unknown evidence; no retrospective first-known leak. Simulated metadata recovery rejects torn pointers, bad checksums/parents and rollback-floor claims. No vendor authenticity, trusted external anchor, disk recovery or actual encryption demonstrated.
- [DEC-FX-020](https://docs.google.com/document/d/1rZdd9tMfT98wH7oDvWlV-0n7EQvvIoUx1T6M79Gb0d8/edit) / [02 Spec v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit) business design unchanged; 18 labels, four states each direction, FX-B9 research-only.
- All vendor/account-specific license, storage host/rights and external retention verification are OPEN. No licensed data, encrypted production cache, real 5-minute 20-pair HTTP speed metric, Backtest/OOS, broker trading, MOCHI, M15001, paid resources or production/LKG release. GitHub main branch protection not enforced; approvals/CI governed manually.
