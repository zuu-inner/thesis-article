#!/usr/bin/env python3
"""Stage 9 content validation of the rendered PDF (read-only)."""
from __future__ import annotations

import csv
import json
import re
import os
from pathlib import Path

import pymupdf

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
PDF = ROOT / "article" / "drafts" / "article-draft.pdf"
LEDGER = ROOT / "article" / "data" / "csv" / "evidence-ledger.csv"
OUT = ROOT / "article" / "data" / "json" / "final-audit-pdf.json"

STALE = (
    "Second Author", "Third Author", "[used / did not use]",
    "RESEARCH METHODS/REVIEW METHODOLOGY", "Lasmadi",
    "fixed seed control order", "every directional conclusion",
    "crossing-heavy", "de-facto floor", "the application also pays allocation",
    "steady state a production server",
)
REQUIRED = (
    "MATERIALS AND METHODS", "RESULTS AND DISCUSSION", "CONCLUSION", "REFERENCE",
    "Declaration of Generative AI", "Conflict of Interest",
    "Figure 1.", "Figure 2.", "Figure 3.", "Figure 4.", "Figure 5.", "Figure 6.",
    "Table 1.", "Table 2.", "Table 3.", "Table 4.", "Table 5.", "Table 6.",
    "Table 7.", "Table 8.",
)
TRIPLE = re.compile(r"(\d+\.\d{4})\s*\[(\d+\.\d{4}),\s*(\d+\.\d{4})\]")


def main() -> None:
    doc = pymupdf.open(PDF)
    pages = [p.get_text() for p in doc]
    full = "\n".join(pages)
    with open(LEDGER, encoding="utf-8") as f:
        triples = {(r["point_estimate"], r["ci95_lower"], r["ci95_upper"])
                   for r in csv.DictReader(f)}
    shown = TRIPLE.findall(full)
    refs_present = all(f"[{n}]" in full for n in range(1, 29))
    checks = {
        "page_count": (len(doc), 14, len(doc) == 14),
        "no_stale_text": ([s for s in STALE if s in full], [],
                          not any(s in full for s in STALE)),
        "required_sections_and_captions": ([s for s in REQUIRED if s not in full],
                                           [], all(s in full for s in REQUIRED)),
        "references_1_to_28": (refs_present, True, refs_present),
        "numeric_triples": (len(shown), "all in ledger",
                            all(t in triples for t in shown)),
        "no_empty_pages": (min(len(p.strip()) for p in pages) > 200, True,
                           min(len(p.strip()) for p in pages) > 200),
    }
    summary = {
        "pdf_pages": len(doc),
        "pdf_metadata": {k: doc.metadata[k] for k in
                         ("title", "author", "subject", "keywords")},
        "checks": {k: {"observed": v[0], "expected": v[1],
                       "status": "PASS" if v[2] else "FAIL"}
                   for k, v in checks.items()},
        "displayed_triples": len(shown),
        "all_checks_pass": all(v[2] for v in checks.values()),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    for k, v in summary["checks"].items():
        print(f"{v['status']}  {k}: {v['observed']}")
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
