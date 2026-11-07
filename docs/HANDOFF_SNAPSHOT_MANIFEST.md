# Forex Trading 1.0 — controlled Google Drive extracted-text snapshot manifest

**Captured:** 2026-11-07 (Asia/Ho_Chi_Minh), after M2/P0.5 account source rights and durable cache review PR #17. Editable Handoff/Spec are canonical on Google Drive; code/CI and frozen plain-text point-in-time snapshots are on PRIVATE GitHub. Independently reread and compared full text on this docs PR branch; main equality to be independently checked after merge.

| Native canonical Google Doc | Frozen GitHub extracted TEXT | Comparison |
| --- | --- | --- |
| [00_MASTER_HANDOFF v0.25 §35](https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit), revision `AHj4eMTfRJ9yq_bHGl822OZzMqV6S8JZ38qdVNxYw5U9DMcox_SD5EaG2xzX5x0yUbqwRLa2TPKHsRegM78GDAbnw49ANxsBce4xTjS1aC83` | [00 full Handoff](source-snapshots/00_MASTER_HANDOFF.txt), Git blob `09cfd2dc6f6cd4e154fc59ed075a75cb2e87096b` | **772 paragraphs, 204990 characters, EXACT_MATCH on docs branch** |
| [02_MASTER_SPEC v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit), revision `AHj4eMTTg_rR-7qLQ9U70xibVMbckC13Z0ILEWzvqX6tmqDAr2dhUbn46zN90S1f12j3pd5czKLidxFreme3y_E1V_nDmALyDV9CkBO0kZsv` | [02 full Spec](source-snapshots/02_MASTER_SPEC.txt), Git blob `5751412eefa0590d210f8adf3302c26b4a83b764` | **260 paragraphs, 56797 characters, EXACT_MATCH on docs branch** |

Exact comparison: `(Google_Drive.get_document_text.paragraphs.map(p=>p.text).join("\n")+"\n") === GitHub.fetch_file.content`. This verifies extracted TEXT only, not original Google Docs formatting/chips/tables or an automatic two-way sync. The full v0.9 functional Spec remains embedded in Handoff §32; historical v0.8 copy remains in §21.

## Engineering and rights evidence

- [DEC-FX-020](https://docs.google.com/document/d/1rZdd9tMfT98wH7oDvWlV-0n7EQvvIoUx1T6M79Gb0d8/edit) approved Forex-specific Smart Cache design; [Spec v0.9 §24](https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit) remains unchanged.
- [PR #17](https://github.com/ngluonghoa/forex-trading-1-0/pull/17) account-rights/storage **paperwork reviewer**, merged main `9dc612e99f168f42d4afc9fa10e0b5b9d8e80b4f`, [PR CI 42329544166](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42329544166) and [main CI 42329604319](https://github.com/ngluonghoa/forex-trading-1-0/actions/runs/42329604319): Python 3.11 and 3.12 each **349/349 synthetic tests PASS**.
- Synthetic account/product/jurisdiction rights by purpose, retention maximum, region, derived-indicator rights, contract/revocation timeline, encrypted-storage control claims and expiry/suspension review. No independent vendor rights attestation, storage approval, paid resources, secrets, host use or real source IO.
- User goal of on-demand 5-minute incremental 20-pair cache remains NOT OPERATIONAL: no approved native historical BID/ASK account feed, durable cache host, actual data rights, provider revision authenticity, cross-session persistence, measured HTTP bytes/calls, real Backtest/OOS or live trading.
- No M15001 or MOCHI use. GitHub main `protected=false`; review/CI protocol currently manual, not branch-protection enforced.
