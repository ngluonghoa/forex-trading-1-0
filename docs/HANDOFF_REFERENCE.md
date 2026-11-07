# Source-of-truth and text-snapshot policy

- Canonical **Google Drive Handoff v0.40 §50 (LATEST P2.1-B store-orchestrator PR #50; P2.1-A §49, historical rollback M2/P0.10 §48/§40; normative Spec v0.11 unchanged)**: https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit
- Canonical **Google Drive Master Spec v0.11 §26 (active, EXACT original M2/P0.10 content)**: https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit
- Canonical Google Drive QA v0.55 §70: https://docs.google.com/document/d/19CGNHVw1QqnTifmtf1Xu5bst0IAbEWLhQlgOoVzfYZg/edit
- Snapshots in GitHub: [00 text](source-snapshots/00_MASTER_HANDOFF.txt) and [02 text](source-snapshots/02_MASTER_SPEC.txt).
- Provenance, source revisions and exact-text comparison: [HANDOFF_SNAPSHOT_MANIFEST](HANDOFF_SNAPSHOT_MANIFEST.md).

Google Drive remains canonical for editable policy/functional contract. These are frozen, extracted-text snapshots for repeatable engineer handoff, verified on their originating branch against the then-current Drive text. Native Docs visual layout/controls are NOT copied. A future Drive edit does not retroactively update a GitHub snapshot; publish a new PR and exact-match receipt. GitHub is canonical for code.

Previous P2.1-A code PR #48 merged e8cf43830fd6f7086f4366a43363d3eabb2d99f4; docs audit PR #47 merged 09523533451d21274b187a987c1cf590e486dabb. Old 47/47 exact-to-M2/P0.10 source equality is HISTORICAL ONLY after this three-file refactor. Latest QA §69 is authoritative for test evidence; PR CI 454/454 each Python 3.11/3.12, independent postmerge MAIN CI not verified at handoff publication.

P2.1-B source PR #50 https://github.com/ngluonghoa/forex-trading-1-0/pull/50 merged code SHA 238de5454187c2312e885d45dbcae6107e25818f, with four file changes (store, orchestrator, compatibility reexports, seven new tests). GitHub Actions run 42392919832 Python 3.11 + 3.12 verified 461/461 each. Original M2/P0.10 baseline remains archival rollback SHA 7f0904e. Canonical QA §70 specifies postmerge main CI limitation.
