# Charter raw data — http-endpoint-phase-e-results

HTTP endpoint speedups (Phase E, GET /rekap): two dev-device runs and one server run, reported separately (no pooling).

- Source: `article\data\csv\evidence-ledger.csv` (sha256 `800218af02b4fdc3…`)
- Estimand: S = T_V8/T_ZE; ratio of round-level medians over 15 paired rounds; paired bootstrap B=10000, seed=20261117, percentile 95% CI
- Runs: server-lanjut-20261117003513-530f751, zuu-20261116101458-8556513, zuu-20261117000112-6979e3f
- Regenerate: `python article/scripts/Ledger/export_charter_raw.py`
- Chart: `python article/scripts/Charter/main.py` (Stage 6)
