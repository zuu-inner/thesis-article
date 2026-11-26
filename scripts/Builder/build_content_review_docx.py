#!/usr/bin/env python3
"""Build the content-review DOCX from article/drafts/article-draft-content-review.md.

Thin wrapper around build_docx.py primitives. Uses the AVITEC template named by
the project owner (data/template_article_avitec.docx) and writes ONLY the new
review draft. It never modifies article/article.docx, article/metadata.json, or
any older manuscript/DOCX/PDF.

Figures are reused byte-for-byte from the previously verified
article-draft-supervision-final.docx; no new chart or diagram is generated.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import os
from pathlib import Path

from docx import Document

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
DRAFTS = ROOT / "article" / "drafts"
TEMPLATE = ROOT / "data" / "template_article_avitec.docx"
SOURCE_MD = DRAFTS / "article-draft-content-review.md"
OUT_DOCX = DRAFTS / "article-draft-content-review.docx"
META = ROOT / "article" / "metadata.json"
BUILDER = Path(__file__).with_name("build_docx.py")
VERIFIED_DOCX = (ROOT / "out" / "article-audit" / "working" / "article"
                 / "drafts" / "article-draft-supervision-final.docx")
FIGURE_STEMS = [
    "fig1-boundaries",
    "fig2-measurement-protocol",
    "fig3-decision-flow",
    "chart1-diagnostic-phase-speedup",
    "chart2-repository-phase-d",
    "chart3-http-endpoint-phase-e",
]


def reuse_figures() -> dict[str, Path]:
    """Extract the six already-verified figure PNGs into a temp directory.

    Image blobs are taken in document order from the inline drawing relationships
    of the previously verified DOCX, so the figures are byte-identical to the
    ones used by the latest manuscript.
    """
    ref = Document(VERIFIED_DOCX)
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    rids = [el.get(f"{{{ns['r']}}}embed")
            for el in ref.element.body.iter(f"{{{ns['a']}}}blip")]
    rids = [rid for rid in rids if rid and rid in ref.part.related_parts]
    assert len(rids) == len(FIGURE_STEMS), (
        f"unexpected figure count in verified source DOCX: {len(rids)}")
    tmp = Path(tempfile.mkdtemp(prefix="avitec_content_review_figs_"))
    out = {}
    for stem, rid in zip(FIGURE_STEMS, rids):
        p = tmp / f"{stem}.png"
        p.write_bytes(ref.part.related_parts[rid].blob)
        out[stem] = p
    return out


def main() -> None:
    spec = importlib.util.spec_from_file_location("builder", BUILDER)
    b = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b)

    figures = reuse_figures()
    meta, blocks = b.parse_draft(SOURCE_MD.read_text(encoding="utf-8-sig"))
    patched = []
    for kind, payload in blocks:
        if kind == "figure":
            path, caption = payload
            stem = Path(path).stem
            if stem not in figures:
                raise RuntimeError(f"no verified figure for {stem}")
            patched.append((kind, (str(figures[stem]), caption)))
        else:
            patched.append((kind, payload))
    blocks = patched

    shutil.copyfile(TEMPLATE, OUT_DOCX)
    doc = Document(OUT_DOCX)

    m = json.loads(META.read_text(encoding="utf-8"))
    a = m["authors"]["corresponding"]
    inst = a.get("institute", {})
    addr = inst.get("address", {})
    name = " ".join(x for x in (a.get("first_name"), a.get("middle_name"),
                                a.get("last_name")) if x)
    corr = (f"Corresponding Author:\n{name}, {inst.get('department', '')}, "
            f"{inst.get('name', '')}, {addr.get('city', '')}, "
            f"{addr.get('country', '')}. Email: {a.get('email', '')}")

    b.fill_front(doc, meta, corr)
    b.fill_running_head(doc, f"{a.get('last_name', '')}: "
                             f"{meta.get('TITLE', '').split(':')[0].strip()}")
    b.clear_body(doc)
    b.build_body(doc, meta, blocks)

    cp = doc.core_properties
    cp.title = meta.get("TITLE", "")
    cp.author = name
    cp.subject = meta.get("TYPE", "")
    cp.keywords = meta.get("KEYWORDS", "")
    cp.comments = ""
    cp.category = ""
    doc.save(OUT_DOCX)

    report = b.qa(meta, blocks)
    print(f"saved: {OUT_DOCX.relative_to(ROOT)} ({OUT_DOCX.stat().st_size} B)")
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
