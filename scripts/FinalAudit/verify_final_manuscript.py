#!/usr/bin/env python3
"""Independent end-to-end validation of the AVITEC manuscript.

This script deliberately re-implements the checks instead of importing
``article/scripts/Builder/build_docx.py`` so that a builder bug cannot hide a
defect. It validates the canonical Markdown source, the built DOCX, and the
exported PDF, and writes a machine-readable report.

Usage::

    python article/scripts/FinalAudit/verify_final_manuscript.py

Output: ``article/drafts/final-audit/validation-<date>.json`` plus a console
summary. Exit code is non-zero when a hard check fails.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from datetime import date
import os
from pathlib import Path

from docx import Document

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
MD = ROOT / "article" / "drafts" / "article-draft.md"
BIB = ROOT / "article" / "data" / "bib" / "cites.bib"
DOCX = ROOT / "article" / "drafts" / "article-draft.docx"
PDF = ROOT / "article" / "drafts" / "article-draft.pdf"
OUT_DIR = ROOT / "article" / "drafts" / "final-audit"

W_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


# --------------------------------------------------------------------- helpers
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(blob: bytes) -> tuple[int, int] | None:
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", blob[16:24])
    return None


def words(text: str) -> int:
    return len(text.split())


# ------------------------------------------------------------------ markdown
def parse_markdown() -> dict:
    text = MD.read_text(encoding="utf-8-sig")
    lines = text.replace("\r\n", "\n").split("\n")

    meta: dict[str, str] = {}
    abstract_lines: list[str] = []
    body_lines: list[str] = []
    ref_lines: list[str] = []
    section = "meta"

    for line in lines:
        if line.startswith("%%"):
            body = line[2:]
            if body.startswith("ABSTRACT"):
                section = "abstract"
                continue
            key, _, value = body.partition(":")
            if key in {"TYPE", "TITLE", "AUTHOR", "AFFIL", "AUTHORINFO", "HISTORY", "KEYWORDS"}:
                meta[key] = value.strip()
                section = "meta"
                continue
            section = "body"
            body_lines.append(line)
            continue
        if line.startswith("# "):
            if line[2:].strip().upper() == "REFERENCE":
                section = "refs"
                continue
            section = "body"
            body_lines.append(line)
            continue
        if section == "abstract":
            if line.strip():
                abstract_lines.append(line.strip())
            continue
        if section == "refs":
            ref_lines.append(line)
        elif section == "body":
            body_lines.append(line)

    abstract = " ".join(abstract_lines)
    body_text = "\n".join(body_lines)
    return {
        "meta": meta,
        "abstract": abstract,
        "body_text": body_text,
        "ref_text": "\n".join(ref_lines),
    }


def count_words_by_kind(body_text: str) -> dict:
    """Word counts for the AVITEC length rule.

    ``inclusive`` counts every visible body token (paragraphs, table cells,
    captions, figure captions, notes, supplementary material) and therefore is
    the conservative upper bound; ``prose`` counts paragraph text only.
    """
    inclusive = 0
    prose = 0
    in_table = False
    for raw in body_text.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            in_table = False
            continue
        if line.startswith("%%"):
            in_table = False
            payload = line[2:]
            if payload.startswith("FIGURE|"):
                inclusive += words(payload.split("|", 2)[2])
            elif payload.startswith(("TCAP|", "TNOTE|")):
                inclusive += words(payload.split("|", 1)[1])
            elif payload.startswith("SUPP|"):
                inclusive += words(payload.split("|", 2)[2])
            continue
        if line.startswith("#"):
            in_table = False
            continue
        if line.startswith("|"):
            in_table = True
            inclusive += words(line.replace("|", " "))
            continue
        prose += words(line)
        inclusive += words(line)
    return {"inclusive": inclusive, "prose": prose}


def parse_references(ref_text: str) -> list[dict]:
    refs: list[dict] = []
    for line in ref_text.split("\n"):
        m = re.match(r"^\[(\d+)\]\s+(.*)$", line.strip())
        if not m:
            continue
        body = m.group(2)
        doi = re.search(r"doi:\s*(10\.\S+?)\.?\s*$", body)
        url = re.search(r"URL:\s*(\S+?)\.?\s*$", body)
        refs.append({
            "number": int(m.group(1)),
            "text": body,
            "doi": doi.group(1).rstrip(".") if doi else None,
            "url": url.group(1).rstrip(".") if url else None,
        })
    return refs


def bib_dois() -> list[str]:
    text = BIB.read_text(encoding="utf-8-sig")
    return sorted(set(re.findall(r"doi\s*=\s*\{([^}]+)\}", text)))


# ---------------------------------------------------------------------- docx
def inspect_docx() -> dict:
    doc = Document(DOCX)
    paragraphs = [p.text for p in doc.paragraphs]
    ref_paras = [p for p in paragraphs if re.match(r"^\[\d+\]\s", p.strip())]

    images = []
    for idx, inline in enumerate(doc.element.body.iter(f"{{{WP_NS}}}inline"), 1):
        ext = inline.find(f"{{{WP_NS}}}extent")
        cx, cy = int(ext.get("cx")), int(ext.get("cy"))
        blip = inline.find(f".//{{{W_NS}}}blip")
        rid = blip.get(f"{{{R_NS}}}embed")
        blob = doc.part.related_parts[rid].blob
        px = png_size(blob)
        w_in, h_in = cx / 914400, cy / 914400
        dpi_x = px[0] / w_in if px and w_in else None
        dpi_y = px[1] / h_in if px and h_in else None
        images.append({
            "index": idx,
            "pixels": list(px) if px else None,
            "display_in": [round(w_in, 3), round(h_in, 3)],
            "dpi": [round(dpi_x), round(dpi_y)] if dpi_x else None,
            "sha256": hashlib.sha256(blob).hexdigest()[:16],
        })
    return {
        "paragraphs": len(paragraphs),
        "reference_paragraphs": len(ref_paras),
        "tables": len(doc.tables),
        "images": images,
        "core_properties": {
            "title": doc.core_properties.title,
            "author": doc.core_properties.author,
            "subject": doc.core_properties.subject,
            "keywords": doc.core_properties.keywords,
        },
    }


# ----------------------------------------------------------------------- pdf
def inspect_pdf() -> dict:
    import pymupdf

    pdf = pymupdf.open(PDF)
    meta = pdf.metadata or {}
    text = "\n".join(page.get_text() for page in pdf)
    pages = len(pdf)
    pdf.close()
    return {
        "pages": pages,
        "metadata": {k: meta.get(k) for k in ("title", "author", "subject", "keywords")},
        "has_all_references": all(f"[{n}]" in text for n in range(1, 43)),
        "has_figures": all(f"Figure {n}." in text for n in range(1, 7)),
        "has_tables": all(f"Table {n}." in text for n in range(1, 9)),
        "has_ai_declaration": "Declaration of Generative AI" in text,
        "has_conflict_of_interest": "Conflict of Interest" in text,
    }


# --------------------------------------------------------------------- checks
def main() -> int:
    md = parse_markdown()
    meta, body_text = md["meta"], md["body_text"]
    refs = parse_references(md["ref_text"])
    counts = count_words_by_kind(body_text)

    cited: list[int] = []
    for m in re.finditer(r"\[(\d+(?:,\s*\d+)*)\]", body_text):
        for part in m.group(1).split(","):
            cited.append(int(part))
    unique_cited = sorted(set(cited))
    first_appearance: list[int] = []
    for n in cited:
        if n not in first_appearance:
            first_appearance.append(n)
    after_punct = len(re.findall(r"[.,;]\s*\[\d+(?:,\s*\d+)*\]", body_text))

    fig_mentions = [int(n) for n in re.findall(r"Figure\s+(\d+)", body_text)]
    tab_mentions = [int(n) for n in re.findall(r"Table\s+(\d+)", body_text)]
    first_fig: list[int] = []
    first_tab: list[int] = []
    for n in fig_mentions:
        if n not in first_fig:
            first_fig.append(n)
    for n in tab_mentions:
        if n not in first_tab:
            first_tab.append(n)

    manuscript_dois = sorted({r["doi"] for r in refs if r["doi"]})
    bib = bib_dois()
    # DOI comparison is case-insensitive (DOI Handbook 1.4): the suffix may be
    # registered in upper or lower case, e.g. 10.1109/ACCESS... vs 10.1109/access...
    md_doi_ci = {d.lower() for d in manuscript_dois}
    bib_doi_ci = {d.lower() for d in bib}
    doi_case_differences = sorted(
        d for d in manuscript_dois if d.lower() in bib_doi_ci and d not in set(bib)
    )
    docx = inspect_docx()
    pdf = inspect_pdf()

    keywords = [k.strip() for k in meta.get("KEYWORDS", "").split(";") if k.strip()]
    abstract = md["abstract"]

    checks = {
        "title_le_20_words": words(meta.get("TITLE", "")) <= 20,
        "abstract_single_paragraph_250_words": words(abstract) <= 250 and "\n" not in abstract.strip(),
        "keywords_3_to_7": 3 <= len(keywords) <= 7,
        "body_5000_to_8000_words": 5000 <= counts["inclusive"] <= 8000,
        "references_contiguous_1_to_42": [r["number"] for r in refs] == list(range(1, 43)),
        "all_references_cited": unique_cited == list(range(1, 43)),
        "citation_first_appearance_order": first_appearance == list(range(1, 43)),
        "no_citation_after_punctuation": after_punct == 0,
        "no_duplicate_doi": len(manuscript_dois) == len(refs) - 1,  # one entry has no DOI
        "manuscript_doi_set_matches_bib": md_doi_ci == bib_doi_ci,
        "figures_1_to_6_in_order": first_fig == list(range(1, 7)),
        "tables_1_to_8_in_order": first_tab == list(range(1, 9)),
        "docx_reference_paragraphs_42": docx["reference_paragraphs"] == 42,
        "docx_tables_9": docx["tables"] == 9,
        "docx_images_6": len(docx["images"]) == 6,
        "figure_resolution_at_least_1000_dpi": all(
            img["dpi"] and min(img["dpi"]) >= 1000 for img in docx["images"]
        ),
        "pdf_has_all_references": pdf["has_all_references"],
        "pdf_has_figures_and_tables": pdf["has_figures"] and pdf["has_tables"],
        "pdf_has_ai_declaration": pdf["has_ai_declaration"],
    }
    hard_fail = [name for name, ok in checks.items() if not ok]

    report = {
        "generated": date.today().isoformat(),
        "source": {
            "markdown": {"path": str(MD.relative_to(ROOT)), "sha256": sha256(MD)},
            "docx": {"path": str(DOCX.relative_to(ROOT)), "sha256": sha256(DOCX), "bytes": DOCX.stat().st_size},
            "pdf": {"path": str(PDF.relative_to(ROOT)), "sha256": sha256(PDF), "bytes": PDF.stat().st_size},
            "bib": {"path": str(BIB.relative_to(ROOT)), "sha256": sha256(BIB)},
        },
        "counts": {
            "title_words": words(meta.get("TITLE", "")),
            "abstract_words": words(abstract),
            "keywords": keywords,
            "body_words_inclusive": counts["inclusive"],
            "body_words_prose": counts["prose"],
            "references": len(refs),
            "doi_manuscript": len(manuscript_dois),
            "doi_bib": len(bib),
            "doi_case_differences": doi_case_differences,
            "citation_mentions": len(cited),
            "citation_unique": len(unique_cited),
            "citations_after_punctuation": after_punct,
            "figures": len(fig_mentions),
            "tables": len(tab_mentions),
        },
        "docx": docx,
        "pdf": pdf,
        "checks": checks,
        "failed_checks": hard_fail,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"validation-{date.today().isoformat()}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    for name, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(f"\nreport -> {out.relative_to(ROOT)}")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
