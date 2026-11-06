# Source-of-truth and text-snapshot policy

- Canonical **Google Drive Handoff v0.21 §31**: https://docs.google.com/document/d/1_F8yvAw5uBj25J5g7OUhhKyBgO2aO65qPtme4yHHgAE/edit
- Canonical **Google Drive Master Spec v0.8**: https://docs.google.com/document/d/1k5vidJ5mPjCFCDYxuzJ29DSfOaBicZUzXLOX4jtscy4/edit
- Snapshots in GitHub: [00 text](source-snapshots/00_MASTER_HANDOFF.txt) and [02 text](source-snapshots/02_MASTER_SPEC.txt).
- Provenance, source revisions and exact-text comparison: [HANDOFF_SNAPSHOT_MANIFEST](HANDOFF_SNAPSHOT_MANIFEST.md).

Google Drive remains canonical for editable policy/functional contract. These are frozen, extracted-text snapshots for repeatable engineer handoff, verified on their originating branch against the then-current Drive text. Native Docs visual layout/controls are NOT copied. A future Drive edit does not retroactively update a GitHub snapshot; publish a new PR and exact-match receipt. GitHub is canonical for code.
