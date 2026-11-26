#!/usr/bin/env python3
"""Inspect an AVITEC docx structure (read-only). Usage: inspect_template.py [path]"""
import sys
import os
from pathlib import Path

from docx import Document

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "article" / "article.docx"
doc = Document(target)
print(f"== file: {target}")

print("== core properties ==")
cp = doc.core_properties
for k in ("title", "author", "subject", "keywords", "last_modified_by",
          "created", "modified", "template"):
    print(f"{k}: {getattr(cp, k, None)}")

print("== sections ==")
for i, s in enumerate(doc.sections):
    print(i, s.page_width, s.page_height, s.left_margin, s.right_margin,
          s.top_margin, s.bottom_margin)

print("== styles in use ==")
styles: dict[str, int] = {}
for p in doc.paragraphs:
    styles[p.style.name] = styles.get(p.style.name, 0) + 1
print(styles)

print("== paragraphs ==")
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t or p.style.name != "Normal":
        print(f"{i:3d} [{p.style.name}] {t[:110]!r}")

print("== tables ==")
print("count:", len(doc.tables))
for i, t in enumerate(doc.tables):
    st = t.style.name if t.style is not None else None
    print(f"-- table {i}: rows={len(t.rows)} cols={len(t.columns)} style={st}")
    for r in t.rows[:2]:
        print("   ", [c.text.strip()[:34] for c in r.cells])

print("== inline shapes ==", len(doc.inline_shapes))
