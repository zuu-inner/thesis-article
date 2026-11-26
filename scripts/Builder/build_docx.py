#!/usr/bin/env python3
"""Build article/drafts/article-draft.docx from article/drafts/article-draft.md.

Uses the pristine AVITEC template article/article.docx as a copy (the template
file itself is never modified). Fills the article-info table (history,
abstract, keywords), rebuilds the body with template styles, inserts figures
and tables, then runs QA checks and updates article/metadata.json
(document.title.primary, keywords, cites in citation order).
"""
from __future__ import annotations

import json
import re
import shutil
import struct
import os
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
ART = ROOT / "article"
TEMPLATE = ART / "article.docx"
DRAFT_MD = ART / "drafts" / "article-draft.md"
OUT_DOCX = ART / "drafts" / "article-draft.docx"
OUT_META = ART / "metadata.json"

TOKEN_RE = re.compile(r"(`[^`]+`|\*[^*]+\*)")
DOI_RE = re.compile(r"doi:\s*(10\.\S+?)\.?\s*$")


def ref_doi(par: str) -> str | None:
    m = DOI_RE.search(par)
    return m.group(1) if m else None


def parse_draft(md_text: str) -> tuple[dict, list]:
    meta: dict = {}
    blocks: list = []
    lines = md_text.replace("\r\n", "\n").split("\n")
    i, para_buf = 0, []

    def flush():
        if para_buf:
            blocks.append(("para", " ".join(para_buf).strip()))
            para_buf.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush()
            i += 1
            continue
        if line.startswith("%%"):
            flush()
            body = line[2:]
            handled = False
            for key in ("TYPE", "TITLE", "AUTHOR", "AFFIL", "AUTHORINFO",
                        "HISTORY", "KEYWORDS"):
                if body.startswith(key + ":"):
                    meta[key] = body[len(key) + 1:].strip()
                    handled = True
                    break
            if handled:
                i += 1
                continue
            if body.startswith("ABSTRACT"):
                buf = []
                i += 1
                while (i < len(lines) and lines[i].strip()
                       and not lines[i].startswith(("%%", "#"))):
                    buf.append(lines[i].strip())
                    i += 1
                meta["ABSTRACT"] = " ".join(buf)
                continue
            if body.startswith("TCAP|"):
                blocks.append(("tcap", body[5:].strip()))
            elif body.startswith("TNOTE|"):
                blocks.append(("tnote", body[6:].strip()))
            elif body.startswith("FIGURE|"):
                _, path, caption = body.split("|", 2)
                blocks.append(("figure", (path.strip(), caption.strip())))
            elif body.startswith("SUPP|"):
                _, label, text = body.split("|", 2)
                blocks.append(("supp", (label.strip(), text.strip())))
            else:
                raise ValueError(f"unknown marker: {line[:60]}")
            i += 1
            continue
        if line.startswith("### "):
            flush()
            blocks.append(("h3", line[4:].strip()))
        elif line.startswith("## "):
            flush()
            blocks.append(("h2", line[3:].strip()))
        elif line.startswith("# "):
            flush()
            blocks.append(("h1", line[2:].strip()))
        elif line.lstrip().startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        elif re.match(r"^\[\d+\]\s", line):
            flush()
            blocks.append(("para", line.strip()))
            i += 1
            continue
        else:
            para_buf.append(line.strip())
        i += 1
    flush()
    return meta, blocks


def add_runs(p, text: str, size: int | None = None) -> None:
    for tok in TOKEN_RE.split(text):
        if not tok:
            continue
        if tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            r = p.add_run(tok[1:-1])
            r.font.name = "Consolas"
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r = p.add_run(tok[1:-1])
            r.italic = True
        else:
            r = p.add_run(tok)
        if size is not None:
            r.font.size = Pt(size)


def png_size(path: Path) -> tuple[int, int]:
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def add_figure(doc, path: str, caption: str) -> None:
    abs_path = ROOT / path
    w, h = png_size(abs_path)
    width_in = 6.1
    if width_in * h / w > 6.8:
        width_in = 6.8 * w / h
    p = doc.add_paragraph(style="Figure")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(abs_path), width=Inches(width_in))
    cap = doc.add_paragraph(style="Caption")
    add_runs(cap, caption, size=9)


def add_table(doc, caption: str, rows: list) -> None:
    cap = doc.add_paragraph(style="Caption for table")
    add_runs(cap, caption, size=9)
    ncols = max(len(r) for r in rows)
    t = doc.add_table(rows=len(rows), cols=ncols)
    t.style = doc.styles["Table Grid"]
    # repeat the header row when a table splits across pages
    tr_pr = t.rows[0]._tr.get_or_add_trPr()
    tr_pr.append(tr_pr.makeelement(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tblHeader",
        {}))
    keep_together = len(rows) <= 7  # data tables (T3–T8) stay on one page
    if keep_together:
        cap.paragraph_format.keep_with_next = True
    for ri, trow in enumerate(t.rows):
        if keep_together:
            tr_pr = trow._tr.get_or_add_trPr()
            tr_pr.append(tr_pr.makeelement(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cantSplit",
                {}))
        for ci in range(ncols):
            cell = t.cell(ri, ci)
            cell.text = rows[ri][ci] if ci < len(rows[ri]) else ""
            for p in cell.paragraphs:
                if keep_together and ri < len(t.rows) - 1:
                    p.paragraph_format.keep_with_next = True
                for r in p.runs:
                    r.font.size = Pt(9)
                    if ri == 0:
                        r.bold = True


def set_cell(cell, text: str) -> None:
    cell.text = text


def fill_front(doc, meta: dict, corr_block: str) -> None:
    ps = doc.paragraphs
    ps[0].text = meta.get("TYPE", "")
    ps[1].text = meta.get("TITLE", "")
    ps[2].text = meta.get("AUTHOR", "")
    ps[3].text = meta.get("AFFIL", "")
    ps[4].text = meta.get("AUTHORINFO", "")
    t = doc.tables[0]
    keywords_set = False
    for row in t.rows:
        for cell in row.cells:
            txt = cell.text
            if "Corresponding Author" in txt:
                # also wipes the template's example-reference list in this cell
                set_cell(cell, corr_block)
            elif "Article history" in txt:
                set_cell(cell, "Article history:\n" + meta.get("HISTORY", ""))
            elif txt.strip().startswith("The abstract"):
                set_cell(cell, meta.get("ABSTRACT", ""))
            elif "Keywords" in txt:
                set_cell(cell, "Keywords: " + meta.get("KEYWORDS", ""))
                keywords_set = True
    if not keywords_set:
        for row in t.rows:
            for cell in row.cells:
                if cell.text.strip().startswith(meta.get("ABSTRACT", "")[:40]):
                    cell.text = meta.get("ABSTRACT", "") + "\n\nKeywords: " \
                        + meta.get("KEYWORDS", "")


W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def fill_running_head(doc, running_head: str) -> None:
    """Replace the template's 'First Author, et. al.: ...' placeholder text in
    the odd-page running head; the tab + PAGE field runs stay untouched."""
    for p in doc.sections[0].header.paragraphs:
        if "First Author" in p.text and p.runs:
            p.runs[0].text = running_head
            return


def clear_body(doc) -> None:
    body = doc.element.body
    keep = {p._p for p in doc.paragraphs[:6]}
    keep.add(doc.tables[0]._tbl)
    for child in list(body):
        if child.tag.endswith("}sdt"):
            # template example content (e.g. sample reference list) lives in
            # a content control invisible to python-docx paragraph iteration
            text = "".join(t.text or "" for t in child.iter(f"{W_NS}t"))
            if "Lasmadi" in text:
                body.remove(child)
            continue
        if child.tag.endswith("}p") or child.tag.endswith("}tbl"):
            if child not in keep:
                body.remove(child)


def build_body(doc, meta: dict, blocks: list) -> None:
    pending_tcap = None
    in_refs = False
    for kind, payload in blocks:
        if kind == "h1":
            in_refs = payload.strip().upper() == "REFERENCE"
            doc.add_paragraph(payload,
                              style="Reference Head" if in_refs else "Heading 1")
        elif kind == "h2":
            doc.add_paragraph(payload, style="Heading 2")
        elif kind == "h3":
            doc.add_paragraph(payload, style="Heading 3")
        elif kind == "para":
            p = doc.add_paragraph(style="Text")
            if in_refs:
                add_runs(p, payload, size=9)
                pf = p.paragraph_format
                pf.left_indent = Inches(0.3)
                pf.first_line_indent = Inches(-0.3)
            else:
                add_runs(p, payload)
        elif kind == "figure":
            add_figure(doc, payload[0], payload[1])
        elif kind == "tcap":
            pending_tcap = payload
        elif kind == "table":
            add_table(doc, pending_tcap or "", payload)
            pending_tcap = None
        elif kind == "tnote":
            p = doc.add_paragraph(style="Text")
            add_runs(p, payload, size=9)
            for r in p.runs:
                r.italic = True
        elif kind == "supp":
            label, text = payload
            p = doc.add_paragraph(style="Supplementary Material")
            r = p.add_run(label + ": ")
            r.bold = True
            add_runs(p, text)


def qa(meta: dict, blocks: list) -> dict:
    body_paras = []
    prose_words = 0
    supp_words = 0
    in_refs = False
    for kind, payload in blocks:
        if kind == "h1":
            in_refs = payload.strip().upper() == "REFERENCE"
            continue
        if kind == "para":
            if not in_refs:
                body_paras.append(payload)
                prose_words += len(payload.split())
        elif kind == "supp":
            supp_words += len(payload[1].split())
        elif kind in ("table",):
            for row in payload:
                body_paras.append(" ".join(row))
        elif kind == "figure":
            body_paras.append(payload[1])
        elif kind == "tnote":
            body_paras.append(payload)
    body_text = " ".join(body_paras)
    abstract = meta.get("ABSTRACT", "")
    keywords = [k.strip() for k in meta.get("KEYWORDS", "").split(";") if k.strip()]

    seen, order_ok = set(), True
    expect = 1
    for m in re.finditer(r"\[(\d+)\]", body_text):
        n = int(m.group(1))
        if n not in seen:
            seen.add(n)
            if n != expect:
                order_ok = False
            expect += 1
    after_punct = len(re.findall(r"[.,;]\s*\[\d+\]", body_text))
    dois = [d for d in (ref_doi(p) for k, p in blocks if k == "para") if d]
    return {
        "abstract_words": len(abstract.split()),
        "keywords": keywords,
        "keywords_in_abstract": [k for k in keywords
                                 if k.lower() in abstract.lower()],
        "body_words": len(body_text.split()),
        "prose_words": prose_words,
        "supp_words": supp_words,
        "citation_first_order_ok": order_ok,
        "citations_unique": sorted(seen),
        "citations_after_punctuation": after_punct,
        "doi_count": len(dois),
        "doi_unique": len(set(dois)),
        "figures": sum(1 for k, _ in blocks if k == "figure"),
        "tables": sum(1 for k, _ in blocks if k == "table"),
    }


def keep_picture_resolution(doc) -> None:
    """Ask Word not to recompress the embedded raster figures.

    AVITEC asks for >1,000 dpi on line art. Without this document setting,
    Word rewrites every figure at its "default resolution" (220 ppi) when the
    DOCX is exported to PDF, which silently drops the figure resolution even
    though the DOCX itself keeps the high-resolution PNG. The OOXML switch
    ``w:doNotAutoCompressPictures`` is the Word equivalent of
    "Do not compress images in file".
    """
    settings = doc.settings.element
    tag = qn("w:doNotAutoCompressPictures")
    if settings.find(tag) is not None:
        return
    element = settings.makeelement(tag, {})
    later = ("w:forceUpgrade", "w:captions", "w:readModeInkLockDown",
             "w:smartTagType", "w:shapeDefaults", "w:doNotEmbedSmartTags",
             "w:decimalSymbol", "w:listSeparator")
    anchor = None
    for child in settings:
        if child.tag in {qn(name) for name in later}:
            anchor = child
            break
    if anchor is None:
        settings.append(element)
    else:
        anchor.addprevious(element)


def main() -> None:
    meta, blocks = parse_draft(DRAFT_MD.read_text(encoding="utf-8-sig"))
    shutil.copyfile(TEMPLATE, OUT_DOCX)
    doc = Document(OUT_DOCX)
    m = json.loads((ART / "metadata.json").read_text(encoding="utf-8"))
    a = m["authors"]["corresponding"]
    inst = a.get("institute", {})
    addr = inst.get("address", {})
    corr_name = " ".join(x for x in (a.get("first_name"), a.get("middle_name"),
                                     a.get("last_name")) if x)
    corr_block = (f"Corresponding Author:\n{corr_name}, "
                  f"{inst.get('department', '')}, {inst.get('name', '')}, "
                  f"{addr.get('city', '')}, {addr.get('country', '')}. "
                  f"Email: {a.get('email', '')}")
    fill_front(doc, meta, corr_block)
    title_short = meta.get("TITLE", "").split(":")[0].strip()
    fill_running_head(doc, f"{a.get('last_name', '')}: {title_short}")
    clear_body(doc)
    build_body(doc, meta, blocks)
    cp = doc.core_properties
    cp.title = meta.get("TITLE", "")
    cp.author = corr_name  # from article/metadata.json only
    cp.subject = meta.get("TYPE", "")
    cp.keywords = meta.get("KEYWORDS", "")
    cp.comments = ""
    cp.category = ""
    keep_picture_resolution(doc)
    doc.save(OUT_DOCX)
    print(f"saved: {OUT_DOCX.relative_to(ROOT)} "
          f"({OUT_DOCX.stat().st_size} B, template intact: "
          f"{TEMPLATE.stat().st_size} B)")

    report = qa(meta, blocks)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # metadata.json — document.title.primary, keywords, cites (citation order)
    m = json.loads(OUT_META.read_text(encoding="utf-8"))
    m["document"]["title"]["primary"] = meta.get("TITLE", "")
    m["document"]["keywords"] = [k.strip() for k in
                                 meta.get("KEYWORDS", "").split(";") if k.strip()]
    dois = [d for d in (ref_doi(p) for k, p in blocks if k == "para") if d]
    m["document"]["cites"] = dois
    OUT_META.write_text(
        json.dumps(m, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"metadata updated: title, {len(m['document']['keywords'])} keywords, "
          f"{len(dois)} cites -> {OUT_META.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
