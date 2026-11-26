#!/usr/bin/env python3
"""Rasterize the SVG diagram masters to PNG at publication resolution.

The three workflow diagrams (Figures 1-3) are authored as SVG masters in
``article/assets/images/*.mmd.svg`` (rendered by the ``pele`` renderer, see
``src/renderer.ts``). Word cannot embed SVG through the current build path, so
the masters are rasterized with headless Chrome.

Usage (from the repository root)::

    python article/scripts/Grapher/rasterize_diagrams.py --scale 9

``--scale`` is the device scale factor applied to the SVG intrinsic size.
The AVITEC author guidelines ask for >1,000 dpi on line art; at the display
widths used in ``build_docx.py`` (Figure 1: 6.10 in, Figure 2: 3.83 in,
Figure 3: 6.10 in) a scale of 9 yields roughly 1,150-1,520 dpi.

The output is deterministic: rendering the same master with the same scale
reproduces the PNG byte-for-byte, so the figures can be regenerated and
re-verified instead of being treated as opaque binaries.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
IMAGES = ROOT / "article" / "assets" / "images"
OUT_DIR = ROOT / "article" / "scripts" / "Grapher" / "diagram"

# name -> (intrinsic width, intrinsic height) taken from the SVG root element
DIAGRAMS = {
    "fig1-boundaries": (1026, 449),
    "fig2-measurement-protocol": (576, 1022),
    "fig3-decision-flow": (792, 860),
}

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_browser(explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    found = shutil.which("chrome") or shutil.which("msedge")
    if not found:
        raise SystemExit("No Chromium browser found; pass --browser <path>.")
    return found


def rasterize(browser: str, svg: Path, width: int, height: int, scale: int, out: Path) -> None:
    url = svg.resolve().as_uri()
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--default-background-color=FFFFFFFF",
        f"--force-device-scale-factor={scale}",
        f"--window-size={width},{height}",
        f"--screenshot={out}",
        url,
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scale", type=int, default=9, help="device scale factor (default: 9)")
    parser.add_argument("--browser", default=None, help="path to Chrome/Edge executable")
    parser.add_argument("--out-dir", default=None, help="override the output directory")
    parser.add_argument("--dry-run", action="store_true", help="only report the planned output")
    args = parser.parse_args()

    browser = None if args.dry_run else find_browser(args.browser)
    out_dir = Path(args.out_dir) if args.out_dir else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        for name, (width, height) in DIAGRAMS.items():
            svg = IMAGES / f"{name}.mmd.svg"
            if not svg.exists():
                raise SystemExit(f"missing SVG master: {svg}")
            target = out_dir / f"{name}.png"
            if args.dry_run:
                print(f"plan: {svg} -> {target} ({width * args.scale}x{height * args.scale} px)")
                continue
            staged = Path(tmp) / target.name
            rasterize(browser, svg, width, height, args.scale, staged)
            digest = hashlib.sha256(staged.read_bytes()).hexdigest()
            shutil.copyfile(staged, target)
            try:
                shown = target.relative_to(ROOT)
            except ValueError:
                shown = target
            print(f"wrote {shown} ({width * args.scale}x{height * args.scale} px, sha256 {digest[:16]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
