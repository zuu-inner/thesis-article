#!/usr/bin/env python3
"""Add the published VLDB Journal version of simdjson (ref [3]) to the
derived literature registry; it was cited in the manuscript but absent from
the matrix and Crossref verification artifacts. Verified at
https://api.crossref.org/works/10.1007/s00778-019-00578-5 on 2026-11-19.
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
MATRIX = ROOT / "article" / "data" / "csv" / "literature-matrix.csv"
CROSSREF = ROOT / "article" / "data" / "json" / "crossref_verify.json"
DOI = "10.1007/s00778-019-00578-5"


def main() -> None:
    with open(MATRIX, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = rows[0].keys()
    if not any(r["doi"] == DOI for r in rows):
        rows.append({
            "bib_key": "10.1007_s00778-019-00578-5",
            "doi": DOI,
            "title": "Parsing gigabytes of JSON per second",
            "year": "2019",
            "venue": "The VLDB Journal",
            "venue_type": "journal",
            "include_status": "INCLUDE",
            "decision_reason": "published journal version of simdjson; replaces arXiv in manuscript [3]",
            "article_role": "intro+methods",
            "crossref_registry": "crossref",
            "crossref_status": "found",
            "crossref_title_match": "ok",
            "crossref_year_match": "ok",
        })
        with open(MATRIX, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(fields))
            w.writeheader()
            w.writerows(rows)
    cr = json.loads(CROSSREF.read_text(encoding="utf-8"))
    if not any(r["doi"] == DOI for r in cr["results"]):
        cr["results"].append({
            "doi": DOI, "registry": "crossref", "status": "found",
            "title": "Parsing gigabytes of JSON per second", "year": 2019,
            "container": "The VLDB Journal",
        })
        CROSSREF.write_text(json.dumps(cr, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    print(f"registry fixed: {DOI}")


if __name__ == "__main__":
    main()
