#!/usr/bin/env python3
"""Stage 6 literature compliance computation (read-only on evidence)."""
from __future__ import annotations

import csv
import json
import re
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
MATRIX = ROOT / "article" / "data" / "csv" / "literature-matrix.csv"
SELECTION = ROOT / "article" / "data" / "bib" / "article-selection.json"
DRAFT = ROOT / "article" / "drafts" / "article-draft.md"
OUT = ROOT / "article" / "data" / "json" / "final-audit-literature.json"


def main() -> None:
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    selected = sorted(selection["selected"], key=lambda item: item["reference"])
    with open(MATRIX, encoding="utf-8") as f:
        matrix = {r["bib_key"]: r for r in csv.DictReader(f)}
    intro = DRAFT.read_text(encoding="utf-8").split("# INTRODUCTION", 1)[1]
    intro = intro.split("# MATERIALS AND METHODS", 1)[0]
    intro_nums = sorted({int(n) for n in re.findall(r"\[(\d+)\]", intro)})

    rows = []
    for i, item in enumerate(selected, 1):
        m = matrix.get(item["key"], {})
        vtype = m.get("venue_type", "UNKNOWN")
        is_journal = vtype == "journal"
        year = int(m.get("year", 0) or 0)
        doi = item.get("doi")
        rows.append({
            "n": i, "key": item["key"], "doi": doi, "year": year,
            "venue": m.get("venue", ""), "venue_type": vtype,
            "is_journal": is_journal, "recent": year >= 2016,
            "qualifying": is_journal and year >= 2016,
            "in_intro": i in intro_nums,
            "crossref_status": m.get("crossref_status", "") if doi else "url-only",
            "include_status": m.get("include_status", ""),
        })
    j = sum(r["is_journal"] for r in rows)
    q = sum(r["qualifying"] for r in rows)
    intro_j = sum(r["is_journal"] and r["in_intro"] for r in rows)
    needed_total = None
    # (q + N) / (total + N) >= 0.8  ->  N >= (0.8*total - q)/0.2
    import math
    needed_total = max(0, math.ceil((0.8 * len(rows) - q) / 0.2 - 1e-9))
    needed_intro = max(0, 15 - intro_j)
    text = DRAFT.read_text(encoding="utf-8")
    title = re.search(r"^%%TITLE:\s*(.+)$", text, re.M).group(1)
    abstract = text.split("%%ABSTRACT:", 1)[1].split("\n\n", 1)[0].strip()
    keywords = re.search(r"^%%KEYWORDS:\s*(.+)$", text, re.M).group(1)
    summary = {
        "reference_count": len(rows),
        "crossref_found": sum(r["crossref_status"] == "found" for r in rows),
        "journal_refs": j,
        "recent_journal_refs": q,
        "journal_pct": round(100 * j / len(rows), 1),
        "recent_journal_pct": round(100 * q / len(rows), 1),
        "intro_distinct_citations": len(intro_nums),
        "intro_journal_refs": intro_j,
        "min_additional_journal_refs_for_80pct": needed_total,
        "min_additional_intro_journal_refs": needed_intro,
        "title_words": len(title.split()),
        "abstract_words": len(abstract.split()),
        "keyword_count": len([k for k in keywords.split(";") if k.strip()]),
        "non_english_refs": 0,
        "rows": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, indent=1))
    print("intro journal refs:", [r["n"] for r in rows if r["is_journal"] and r["in_intro"]])
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
