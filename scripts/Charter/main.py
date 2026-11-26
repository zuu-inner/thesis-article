#!/usr/bin/env python3
"""Deterministic Matplotlib chart generator for the AVITEC article.

Reads raw chart data from article/scripts/Charter/raw/<slug>/data.csv (written
by export_charter_raw.py from the validated evidence ledger) and renders three
figures. No numbers are hardcoded here; every plotted value comes from the
CSV files. Estimand (see article/drafts/paired-bootstrap-estimand-spec.md):

    S = T_V8 / T_ZE  (S > 1: on-demand parser faster)
    point = ratio of round-level medians over 15 paired rounds
    CI    = 95% paired-bootstrap percentile interval (B=10000, seed 20261117)

Usage:
    python main.py [--raw DIR] [--out DIR] [--dpi N] [--format png,svg]

Outputs (default): article/drafts/charts/chart1-diagnostic-phase-speedup.png/.svg
                   article/drafts/charts/chart2-repository-phase-d.png/.svg
                   article/drafts/charts/chart3-http-endpoint-phase-e.png/.svg
"""
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()

# Okabe-Ito accessible palette
COLOR = {"A": "#0072B2", "B": "#E69F00", "C": "#009E73",
         "dev_device": "#0072B2", "saq_server": "#D55E00"}
PHASE_LABEL = {"A": "A: full materialization",
               "B": "B: partial projection",
               "C": "C: selective traversal"}
DOC_ORDER = ["courses", "assistants", "lecturers", "schedules", "reports",
             "globalConfig"]
SITE_LABEL = {"dev_device": "dev device", "saq_server": "SAQ server"}


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def style_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)


def chart1(raw: Path, out: Path, dpi: int, formats: list[str]) -> None:
    rows = read_csv(raw / "diagnostic-phase-speedup" / "data.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.6), sharey=True)
    width = 0.26
    for ax, site in zip(axes, ("dev_device", "saq_server")):
        xs = range(len(DOC_ORDER))
        for k, phase in enumerate(("A", "B", "C")):
            vals = []
            for doc in DOC_ORDER:
                m = [r for r in rows
                     if r["phase"] == phase and r["site"] == site
                     and r["document"] == doc]
                if len(m) != 1:
                    raise ValueError(f"missing/ambiguous row {phase}/{site}/{doc}")
                vals.append(float(m[0]["speedup"]))
            ax.bar([x + (k - 1) * width for x in xs], vals, width,
                   color=COLOR[phase], label=PHASE_LABEL[phase],
                   edgecolor="black", linewidth=0.4)
        ax.axhline(1.0, color="black", linewidth=1.0, linestyle="--")
        ax.set_yscale("log")
        ax.set_xticks(list(xs))
        ax.set_xticklabels(DOC_ORDER, rotation=30, ha="right", fontsize=8)
        ax.set_title(SITE_LABEL[site], fontsize=10)
        ax.set_xlabel("document")
        style_axes(ax)
    axes[0].set_ylabel("speedup  S = T_V8 / T_ZE  (log scale)")
    axes[0].set_ylim(0.02, 3.5)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8,
               frameon=False, bbox_to_anchor=(0.5, -0.04))
    fig.suptitle("Access-pattern boundaries (A-C): per-document speedup",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    save(fig, out, "chart1-diagnostic-phase-speedup", dpi, formats)


def forest(rows: list[dict], labels: list[str], colors: list[str],
           title: str, xlabel: str, out: Path, name: str, dpi: int,
           formats: list[str]) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 0.62 * len(rows) + 1.9))
    ys = list(range(len(rows) - 1, -1, -1))
    for y, r, c, lab in zip(ys, rows, colors, labels):
        lo, hi, pt = float(r["ci95_lower"]), float(r["ci95_upper"]), float(r["speedup"])
        ax.errorbar(pt, y, xerr=[[pt - lo], [hi - pt]], fmt="o",
                    color=c, ecolor=c, elinewidth=1.6, capsize=4,
                    markersize=5.5, capthick=1.4)
        ax.annotate(f"{pt:.2f} [{lo:.2f}, {hi:.2f}]",
                    (hi, y), textcoords="offset points", xytext=(8, -3),
                    fontsize=8)
    ax.axvline(1.0, color="black", linewidth=1.0, linestyle="--")
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontsize=11)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    style_axes(ax)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    save(fig, out, name, dpi, formats)


def chart2(raw: Path, out: Path, dpi: int, formats: list[str]) -> None:
    rows = read_csv(raw / "repository-phase-d-results" / "data.csv")
    order = [("dev_device", "repository/mongo-cache"),
             ("dev_device", "repository/file-store"),
             ("saq_server", "repository/mongo-cache"),
             ("saq_server", "repository/file-store")]
    labels, sel, colors = [], [], []
    for site, store in order:
        m = [r for r in rows if r["site"] == site and r["store"] == store]
        if len(m) != 1:
            raise ValueError(f"missing/ambiguous D row {site}/{store}")
        sel.append(m[0])
        labels.append(f"{SITE_LABEL[site]} — {'Mongo cache' if 'mongo' in store else 'File store'}")
        colors.append(COLOR[site])
    forest(sel, labels, colors,
           "Repository boundary (Phase D): speedup with 95% CI",
           "speedup  S = T_V8 / T_ZE", out, "chart2-repository-phase-d",
           dpi, formats)


def chart3(raw: Path, out: Path, dpi: int, formats: list[str]) -> None:
    rows = read_csv(raw / "http-endpoint-phase-e-results" / "data.csv")
    # stable order: dev runs first (by run_id), then server
    dev = sorted([r for r in rows if r["site"] == "dev_device"],
                 key=lambda r: r["run_id"])
    srv = sorted([r for r in rows if r["site"] == "saq_server"],
                 key=lambda r: r["run_id"])
    sel = dev + srv
    labels, colors = [], []
    for r in sel:
        rid = r["run_id"]
        commit = rid.split("-")[-1][:7]
        labels.append(f"{SITE_LABEL[r['site']]} ({commit})")
        colors.append(COLOR[r["site"]])
    forest(sel, labels, colors,
           "HTTP endpoint GET /rekap (Phase E): speedup with 95% CI",
           "speedup  S = T_V8 / T_ZE", out, "chart3-http-endpoint-phase-e",
           dpi, formats)


def save(fig, out: Path, name: str, dpi: int, formats: list[str]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        path = out / f"{name}.{fmt}"
        fig.savefig(path, dpi=dpi, bbox_inches="tight",
                    facecolor="white", format=fmt)
        print(f"wrote {path.relative_to(ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raw", default=str(ROOT / "article" / "scripts" / "Charter" / "raw"))
    ap.add_argument("--out", default=str(ROOT / "article" / "drafts" / "charts"))
    ap.add_argument("--dpi", type=int, default=1000)
    ap.add_argument("--format", default="png,svg")
    args = ap.parse_args()
    raw, out = Path(args.raw), Path(args.out)
    formats = [f.strip() for f in args.format.split(",") if f.strip()]
    chart1(raw, out, args.dpi, formats)
    chart2(raw, out, args.dpi, formats)
    chart3(raw, out, args.dpi, formats)


if __name__ == "__main__":
    main()
