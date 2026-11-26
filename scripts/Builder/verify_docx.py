#!/usr/bin/env python3
"""Read-only verification of the assembled AVITEC DOCX (editorial + layout)."""
from __future__ import annotations

import re
import sys
import zipfile
import os
from pathlib import Path

from docx import Document

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
DOCX = ROOT / "article" / "drafts" / "article-draft.docx"
PLACEHOLDERS = (
    "Second Author", "Third Author", "First Author",
    "RESEARCH METHODS", "REVIEW METHODOLOGY",
    "[used / did not use]", "November 2, 2026",
    "December 10, 2026", "December 15, 2026", "Lasmadi",
)
NOTE_PREFIX = "Note. The legacy pooled-request median ratios"


def main() -> int:
    doc = Document(DOCX)
    cp = doc.core_properties
    with zipfile.ZipFile(DOCX) as z:
        body = z.read("word/document.xml").decode("utf-8", "ignore")
        footnotes = z.read("word/footnotes.xml").decode("utf-8", "ignore")

    checks: list[tuple[str, bool, str]] = []
    checks.append(("title from metadata", bool(cp.title) and
                   "On-Demand JSON Parsing" in cp.title, cp.title[:70]))
    checks.append(("author from metadata", cp.author ==
                   "Rafi Indra Pramudhito Zuhayr", cp.author))
    checks.append(("subject not template 'Title'", cp.subject != "Title", cp.subject))
    checks.append(("keywords set", bool(cp.keywords), cp.keywords[:60]))
    checks.append(("no placeholder text",
                   not any(p in body for p in PLACEHOLDERS),
                   str([p for p in PLACEHOLDERS if p in body])))
    checks.append(("no footnote references",
                   "footnoteReference" not in body,
                   str(body.count("footnoteReference"))))
    checks.append(("no numbered footnotes",
                   not re.search(r'w:id="[1-9]\d*"', footnotes), "footnotes.xml"))
    checks.append(("no highlight markup", "w:highlight" not in body,
                   str(body.count("w:highlight"))))
    paras = [p.text for p in doc.paragraphs]
    note_hits = [i for i, t in enumerate(paras) if t.startswith(NOTE_PREFIX)]
    checks.append(("Table 7 note present", len(note_hits) == 1, str(len(note_hits))))
    if note_hits:
        nxt = paras[note_hits[0] + 1: note_hits[0] + 3]
        checks.append(("note before Discussion",
                       any(t.strip().upper() == "DISCUSSION" for t in nxt),
                       " | ".join(t[:40] for t in nxt)))
    all_text = "\n".join(
        [p.text for p in doc.paragraphs] +
        [c.text for t in doc.tables for r in t.rows for c in r.cells])
    stale = (
        "baseline spends 15", "on-demand path reaches S = 0.04",
        "Footnote (legacy", "Second Author", "Third Author",
    )
    checks.append(("no stale interpretation/placeholder in body",
                   not any(s in all_text for s in stale),
                   str([s for s in stale if s in all_text])))
    checks.append(("corrected A–C interpretation present",
                   "16–23" in all_text, "16–23 found"))
    checks.append(("9 docx tables (info + 8)", len(doc.tables) == 9,
                   str(len(doc.tables))))
    checks.append(("template pristine", (ROOT / "article" / "article.docx"
                                         ).stat().st_size == 894262, "894262 B"))

    failed = 0
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
        failed += int(not ok)
    print(f"RESULT: {len(checks) - failed}/{len(checks)} PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
