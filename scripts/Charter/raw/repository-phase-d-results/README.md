# Charter raw data — repository-phase-d-results

Repository-boundary speedups (Phase D): warmed Mongo-cache canonical-bytes path vs file-store path, both sites. CI includes 1 for the file-store rows (negative result retained).

- Source: `article\data\csv\evidence-ledger.csv` (sha256 `800218af02b4fdc3…`)
- Estimand: S = T_V8/T_ZE; ratio of round-level medians over 15 paired rounds; paired bootstrap B=10000, seed=20261117, percentile 95% CI
- Runs: server-lanjut-20261116060933-8a1324b, zuu-20261115080840-6d87bf3
- Regenerate: `python article/scripts/Ledger/export_charter_raw.py`
- Chart: `python article/scripts/Charter/main.py` (Stage 6)
