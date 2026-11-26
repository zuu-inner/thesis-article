#!/usr/bin/env python3
"""Finalize the exported article PDF metadata and render QA page images.

The Word COM export writes the page content but leaves the PDF Info dictionary
empty. This script copies the DOCX core properties (title, author, subject,
keywords) into the PDF metadata and renders every page to PNG for visual QA.

Word also rewrites every embedded raster figure at its "default resolution"
(~200 ppi) when it exports to PDF, regardless of the resolution stored in the
DOCX. Because AVITEC asks for >1,000 dpi on line art, this script re-inserts
the original figure binaries from the DOCX into the exported PDF, matching them
by their on-page display size. The replacement is a pure image swap: the
placement, size, and page layout are untouched.

Run after exporting article-draft.docx to article-draft.pdf with Word COM.
"""
from __future__ import annotations

import io
import os
import struct
from pathlib import Path

import pymupdf
from docx import Document

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
DOCX = ROOT / "article" / "drafts" / "article-draft.docx"
PDF = ROOT / "article" / "drafts" / "article-draft.pdf"
OUT = ROOT / "article" / "drafts" / "qa-render"

W_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def docx_images() -> list[dict]:
    """Inline images of the DOCX with their display size and binary payload."""
    doc = Document(DOCX)
    images = []
    for inline in doc.element.body.iter(f"{{{WP_NS}}}inline"):
        extent = inline.find(f"{{{WP_NS}}}extent")
        cx, cy = int(extent.get("cx")), int(extent.get("cy"))
        blip = inline.find(f".//{{{W_NS}}}blip")
        rid = blip.get(f"{{{R_NS}}}embed")
        blob = doc.part.related_parts[rid].blob
        pixels = None
        if blob[:8] == b"\x89PNG\r\n\x1a\n":
            pixels = struct.unpack(">II", blob[16:24])
        images.append({
            "blob": blob,
            "pixels": pixels,
            "width_in": cx / 914400,
            "height_in": cy / 914400,
        })
    return images


def restore_figure_resolution(pdf: pymupdf.Document, images: list[dict]) -> int:
    """Swap Word's downscaled figure XObjects for the DOCX originals.

    Figures are matched on their on-page size *and* aspect ratio: the three
    matplotlib charts share the same width, so width alone would map the last
    chart to the first one.
    """
    replaced = 0
    for page in pdf:
        for img in page.get_images(full=True):
            xref = img[0]
            for rect in page.get_image_rects(xref):
                w_in, h_in = rect.width / 72, rect.height / 72
                if h_in <= 0:
                    continue
                page_aspect = w_in / h_in
                best = None
                for candidate in images:
                    if candidate["pixels"] is None:
                        continue
                    dw = abs(candidate["width_in"] - w_in)
                    dh = abs(candidate["height_in"] - h_in)
                    if dw > 0.02 or dh > 0.02:
                        continue
                    cand_aspect = candidate["width_in"] / candidate["height_in"]
                    if abs(cand_aspect - page_aspect) / page_aspect > 0.005:
                        continue
                    distance = dw + dh
                    if best is None or distance < best[0]:
                        best = (distance, candidate)
                if best is None:
                    continue
                candidate = best[1]
                current = pdf.extract_image(xref)
                if current["width"] >= candidate["pixels"][0]:
                    continue  # already at (or above) the source resolution
                page.replace_image(xref, stream=io.BytesIO(candidate["blob"]))
                replaced += 1
    return replaced


def main() -> None:
    cp = Document(DOCX).core_properties
    images = docx_images()
    pdf = pymupdf.open(PDF)
    meta = dict(pdf.metadata or {})
    meta.update({
        "title": cp.title or "",
        "author": cp.author or "",
        "subject": cp.subject or "",
        "keywords": cp.keywords or "",
        "creator": "Microsoft Word (AVITEC template)",
    })
    pdf.set_metadata(meta)
    replaced = restore_figure_resolution(pdf, images)
    # A full rewrite is required here: MuPDF stores a replaced image as raw
    # samples, and an incremental save would leave those streams uncompressed
    # (>1 GB). garbage=4 drops the superseded objects, deflate=True compresses
    # the image streams, and clean=True rewrites the content streams. The
    # staging file lives next to the target so the final move stays on one
    # filesystem.
    staged = PDF.with_name(PDF.stem + ".staged.pdf")
    pdf.save(staged, garbage=4, deflate=True, clean=True)
    pdf.close()
    os.replace(staged, PDF)
    print(f"figure images restored to source resolution: {replaced}")

    OUT.mkdir(parents=True, exist_ok=True)
    pdf = pymupdf.open(PDF)
    for i, page in enumerate(pdf):
        page.get_pixmap(dpi=110).save(str(OUT / f"page-{i + 1:02d}.png"))
    print(f"PDF metadata set: {cp.title[:60]} | {cp.author} | {cp.subject}")
    print(f"rendered {len(pdf)} QA pages -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
