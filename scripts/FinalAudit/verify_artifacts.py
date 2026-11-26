#!/usr/bin/env python3
"""Stage 8 cross-format artifact verification (read-only)."""
from __future__ import annotations

import csv
import json
import re
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
ART = ROOT / "article"
DRAFT = ART / "drafts" / "article-draft.md"
META = ART / "metadata.json"
LEDGER = ART / "data" / "csv" / "evidence-ledger.csv"
RAW = ART / "scripts" / "Charter" / "raw"
OUT = ART / "data" / "json" / "final-audit-artifacts.json"

TRIPLE = re.compile(r"(\d+\.\d{4})\s*\[(\d+\.\d{4}),\s*(\d+\.\d{4})\]")
DOI = re.compile(r"doi:\s*(10\.\S+?)\.?\s*$")


def main() -> None:
    with open(LEDGER, encoding="utf-8") as f:
        ledger = list(csv.DictReader(f))
    ledger_triples = {(r["point_estimate"], r["ci95_lower"], r["ci95_upper"])
                      for r in ledger}
    text = DRAFT.read_text(encoding="utf-8")
    triples = TRIPLE.findall(text)
    bad_triples = [t for t in triples if t not in ledger_triples]

    # chart raw data vs ledger
    chart_checks = []
    for slug, keys in (
        ("diagnostic-phase-speedup", ("phase", "site", "document")),
        ("repository-phase-d-results", ("site", "store")),
        ("http-endpoint-phase-e-results", ("site", "run_id")),
    ):
        with open(RAW / slug / "data.csv", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        mismatches = 0
        for r in rows:
            site = r["site"]
            if slug == "diagnostic-phase-speedup":
                eid = f"{r['phase']}-primary-{site}-{r['document']}"
            elif slug == "repository-phase-d-results":
                store = r["store"].split("/")[-1]
                eid = f"D-primary-{site}-{store}"
            else:
                eid = f"E-primary-{site}-rekap-{r['run_id']}"
            match = [l for l in ledger if l["evidence_id"] == eid]
            if len(match) != 1 or any(
                abs(float(r[k]) - float(match[0][lk])) > 5e-5
                for k, lk in (("speedup", "point_estimate"),
                              ("ci95_lower", "ci95_lower"),
                              ("ci95_upper", "ci95_upper"))):
                mismatches += 1
        chart_checks.append({"slug": slug, "rows": len(rows),
                             "mismatches": mismatches})

    meta = json.loads(META.read_text(encoding="utf-8"))
    title = re.search(r"^%%TITLE:\s*(.+)$", text, re.M).group(1)
    keywords = [k.strip() for k in re.search(
        r"^%%KEYWORDS:\s*(.+)$", text, re.M).group(1).split(";") if k.strip()]
    ref_dois = [m.group(1) for line in text.splitlines()
                if (m := DOI.search(line))]
    summary = {
        "ledger_cells": len(ledger),
        "displayed_triples": len(triples),
        "unmatched_triples": bad_triples,
        "chart_checks": chart_checks,
        "figure_markers": text.count("%%FIGURE|"),
        "table_markers": text.count("%%TCAP|"),
        "reference_entries": len(ref_dois),
        "metadata_title_match": meta["document"]["title"]["primary"] == title,
        "metadata_keywords_match": meta["document"]["keywords"] == keywords,
        "metadata_cites_match": meta["document"]["cites"] == ref_dois,
    }
    OUT.write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "unmatched_triples"},
                     indent=1))
    print("unmatched triples:", bad_triples[:5])
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
