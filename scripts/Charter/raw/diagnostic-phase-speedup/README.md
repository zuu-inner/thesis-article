# Charter raw data — diagnostic-phase-speedup

Access-pattern boundaries A (full materialization), B (partial projection), C (selective traversal): per-document speedup with 95% CI, both sites, primary runs only.

- Source: `article\data\csv\evidence-ledger.csv` (sha256 `800218af02b4fdc3…`)
- Estimand: S = T_V8/T_ZE; ratio of round-level medians over 15 paired rounds; paired bootstrap B=10000, seed=20261117, percentile 95% CI
- Runs: server-lanjut-20261116060843-8a1324b, server-lanjut-20261116060900-8a1324b, server-lanjut-20261116060915-8a1324b, zuu-20261115071747-6d87bf3, zuu-20261115075332-6d87bf3, zuu-20261115080838-6d87bf3
- Regenerate: `python article/scripts/Ledger/export_charter_raw.py`
- Chart: `python article/scripts/Charter/main.py` (Stage 6)
