#!/usr/bin/env python3
"""Export article/scripts/Charter/raw/<slug>/{data.csv,provenance.json,README.md}
from the validated evidence ledger (article/data/csv/evidence-ledger.csv).

Read-only w.r.t. the ledger: this script derives chart input data from the
ledger rows (primary evidence only) and writes them into the Charter raw
directories. Deterministic; the date below is a constant, not a timestamp.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
ART = ROOT / "article"
LEDGER = ART / "data" / "csv" / "evidence-ledger.csv"
RAW = ART / "scripts" / "Charter" / "raw"
DATE = "2026-11-18"
ESTIMAND = ("S = T_V8/T_ZE; ratio of round-level medians over 15 paired rounds; "
            "paired bootstrap B=10000, seed=20261117, percentile 95% CI")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_ledger() -> list[dict]:
    with open(LEDGER, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)]


def write_slug(slug: str, header: list[str], rows: list[dict],
               description: str, extra_prov: dict) -> None:
    d = RAW / slug
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "data.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)
    ledger_sha = sha256(LEDGER)
    prov = {
        "schema_version": "1.0.0",
        "kind": "charter_raw_provenance",
        "date": DATE,
        "slug": slug,
        "description": description,
        "source_ledger": str(LEDGER.relative_to(ROOT)),
        "source_ledger_sha256": ledger_sha,
        "estimand": ESTIMAND,
        "estimand_spec": "article/drafts/paired-bootstrap-estimand-spec.md",
        "run_ids": sorted({r["run_id"] for r in rows}),
        **extra_prov,
    }
    with open(d / "provenance.json", "w", encoding="utf-8") as f:
        json.dump(prov, f, indent=2, ensure_ascii=False)
    with open(d / "README.md", "w", encoding="utf-8") as f:
        f.write(f"# Charter raw data — {slug}\n\n"
                f"{description}\n\n"
                f"- Source: `{prov['source_ledger']}` "
                f"(sha256 `{prov['source_ledger_sha256'][:16]}…`)\n"
                f"- Estimand: {ESTIMAND}\n"
                f"- Runs: {', '.join(prov['run_ids'])}\n"
                f"- Regenerate: `python article/scripts/Ledger/export_charter_raw.py`\n"
                f"- Chart: `python article/scripts/Charter/main.py` (Stage 6)\n")
    print(f"{slug}: {len(rows)} rows")


def main() -> None:
    rows = read_ledger()
    primary = [r for r in rows if r["evidence_class"] == "primary"]

    # Chart 1 — diagnostic phases A/B/C per payload, both sites
    c1 = [r for r in primary if r["phase"] in ("A", "B", "C")]
    c1_rows = [{
        "phase": r["phase"], "site": r["site"], "document": r["boundary_detail"],
        "speedup": r["point_estimate"], "ci95_lower": r["ci95_lower"],
        "ci95_upper": r["ci95_upper"], "run_id": r["run_id"],
    } for r in c1]
    write_slug(
        "diagnostic-phase-speedup",
        ["phase", "site", "document", "speedup", "ci95_lower", "ci95_upper", "run_id"],
        c1_rows,
        "Access-pattern boundaries A (full materialization), B (partial "
        "projection), C (selective traversal): per-document speedup with 95% CI, "
        "both sites, primary runs only.",
        {"interpretation": "S < 1 favors the V8 baseline; S > 1 favors the on-demand parser (ZE)."},
    )

    # Chart 2 — repository boundary D
    c2 = [r for r in primary if r["phase"] == "D"]
    c2_rows = [{
        "site": r["site"], "store": r["boundary_detail"],
        "speedup": r["point_estimate"], "ci95_lower": r["ci95_lower"],
        "ci95_upper": r["ci95_upper"], "run_id": r["run_id"],
    } for r in c2]
    write_slug(
        "repository-phase-d-results",
        ["site", "store", "speedup", "ci95_lower", "ci95_upper", "run_id"],
        c2_rows,
        "Repository-boundary speedups (Phase D): warmed Mongo-cache canonical-"
        "bytes path vs file-store path, both sites. CI includes 1 for the "
        "file-store rows (negative result retained).",
        {"interpretation": "Mongo-cache rows: CI entirely above 1 on both sites; "
                           "file-store rows: CI includes 1 (no advantage)."},
    )

    # Chart 3 — HTTP endpoint E
    c3 = [r for r in primary if r["phase"] == "E"]
    c3_rows = [{
        "site": r["site"], "run_id": r["run_id"],
        "speedup": r["point_estimate"], "ci95_lower": r["ci95_lower"],
        "ci95_upper": r["ci95_upper"],
    } for r in c3]
    write_slug(
        "http-endpoint-phase-e-results",
        ["site", "run_id", "speedup", "ci95_lower", "ci95_upper"],
        c3_rows,
        "HTTP endpoint speedups (Phase E, GET /rekap): two dev-device runs and "
        "one server run, reported separately (no pooling).",
        {"interpretation": "Dev runs: CI includes 1; server run: CI entirely above 1."},
    )


if __name__ == "__main__":
    main()
