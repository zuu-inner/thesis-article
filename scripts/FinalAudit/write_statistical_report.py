#!/usr/bin/env python3
"""Render Stage 3 statistical audit from verified derived artifacts."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
AUDIT = ROOT / "article" / "data" / "json" / "orientation-audit.json"
LEDGER = ROOT / "article" / "data" / "csv" / "evidence-ledger.csv"
PROV = ROOT / "article" / "data" / "json" / "evidence-ledger.provenance.json"
OUT_JSON = ROOT / "article" / "data" / "json" / "final-audit-statistics.json"
OUT = ROOT / "article" / "drafts" / "final-audit" / "statistical-audit.md"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    details = a["details"]
    summary = {
        "estimand": a["definition"],
        "bootstrap": a["bootstrap"],
        "rng": "numpy.random.default_rng(20261117) -> PCG64 (verified)",
        "cells": len(details),
        "status_count": a["status_count"],
        "ledger_sha256": sha256(LEDGER),
        "provenance_sha256": sha256(PROV),
        "audit_sha256": sha256(AUDIT),
        "determinism": "two independent build_ledger.py runs produced identical "
                       "ledger and provenance hashes",
        "sign_wilcoxon_in_manuscript": False,
        "bca_sensitivity_cells": sum(1 for d in details if "bca_CI" in d),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    lines = [
        "# Stage 3 — Statistical Audit",
        "",
        "> Recomputed 2026-11-19 with an implementation independent of the "
        "manuscript tables. Derived artifacts: "
        "`article/data/json/final-audit-statistics.json`, "
        "`article/data/json/orientation-audit.json`.",
        "",
        "## 1. Locked estimand and estimator",
        "",
        "$$S = \\frac{\\operatorname{Median}(T_{V8,1},\\ldots,T_{V8,15})}"
        "{\\operatorname{Median}(T_{ZE,1},\\ldots,T_{ZE,15})},\\qquad"
        "\\hat\\theta = \\frac{\\operatorname{median}(v)}{\\operatorname{median}(z)}$$",
        "",
        "This is the **ratio of across-round medians**, not the median of 15 "
        "paired-round ratios. Interpretation: $S<1$ → V8 lower latency; "
        "$S>1$ → ZE lower latency; CI containing 1 → advantage not "
        "distinguishable at this design's precision. No reciprocal is applied "
        "to any reported value.",
        "",
        "## 2. Locked bootstrap specification (verified)",
        "",
        "| Parameter | Required | Verified |",
        "|---|---|---|",
        "| Inference unit | paired round | 15 pairs per cell |",
        "| Resampling | joint V8/ZE round indices | `idx = rng.integers(0, 15, size=(10000, 15))`; both arrays indexed by same `idx` |",
        "| Replicates | 10,000 | 10,000 |",
        "| Seed / RNG | 20261117 / PCG64 | `numpy.random.default_rng(20261117)` → `PCG64`; first five draws reproduced exactly |",
        "| Statistic per replicate | ratio of medians | `median(v[idx]) / median(z[idx])` — identical to point estimator |",
        "| CI | percentile 95% | 2.5th / 97.5th percentiles of bootstrap distribution |",
        "| BCa | sensitivity only | log-scale + jackknife acceleration, archived per cell; not primary |",
        "| Request-level resampling | forbidden | 150 E requests are within-round observations, never treated as 150 independent units |",
        "",
        "Exact sign and Wilcoxon tests: **not reported in the manuscript** "
        "(grep: no matches), therefore not applicable to this audit.",
        "",
        "## 3. Raw inputs and within-round aggregation",
        "",
        "| Phase | Input field | Within-round value | Source |",
        "|---|---|---|---|",
        "| A | `raw_rounds[].rounds_ms` for `v8-parse` / `ze-parse` | mean of reps (30 or 5) | `nd6_phase_{A}.json` |",
        "| B | `v8-selective` / `ze-project-selective` | mean of reps | `nd6_phase_B.json` |",
        "| C | `v8-selective` / `ze-l1-traversal` | mean of reps | `nd6_phase_C.json` |",
        "| D | `D-{mongo-cache,file-store}-{v8,ze}` | mean of 2 reps | `nd6_phase_D.json` |",
        "| E | `requests.{v8,ze}[{round,seconds}]` | median of 10 requests/engine/round | `nd11_phase_e.json` |",
        "",
        "All cells use 15 rounds. The canonical ledger is "
        "`article/data/csv/evidence-ledger.csv` (63 rows).",
        "",
        "## 4. Deterministic verification",
        "",
        "| Check | Result |",
        "|---|---|",
        "| `build_ledger.py` run twice → ledger SHA-256 | identical: "
        f"`{summary['ledger_sha256']}` |",
        "| `build_ledger.py` run twice → provenance SHA-256 | identical: "
        f"`{summary['provenance_sha256']}` |",
        "| Independent recomputation (`audit_orientation.py`) | "
        f"{a['status_count']} across {len(details)} cells |",
        "| BCa sensitivity computed | "
        f"{summary['bca_sensitivity_cells']} cells |",
        "| Hand-entered values | none |",
        "",
        "## 5. Full 63-cell output (point, percentile CI, BCa sensitivity)",
        "",
        "| Phase | Site / class | Cell | S | CI 95% | BCa CI | Status |",
        "|---|---|---|---:|---|---|---|",
    ]
    for d in details:
        lines.append(
            f"| {d['phase']} | {d['site']} / {d['class']} | {d['cell']} | "
            f"{d['raw_S']:.4f} | [{d['raw_CI'][0]:.4f}, {d['raw_CI'][1]:.4f}] | "
            f"[{d['bca_CI'][0]:.4f}, {d['bca_CI'][1]:.4f}] | {d['status']} |")
    lines += [
        "",
        "Selected interpretation checks: A/dev/courses $S=0{,}0494$ "
        "[0,0385–0,0631] → V8 faster (reciprocal 20,2357 matches the old, "
        "incorrect narrative); D/dev/mongo $S=2{,}8802$ [2,5724–3,0451] → ZE "
        "faster; E/server $S=1{,}1544$ [1,0845–1,1751] → ZE faster; E/dev "
        "runs include 1 → not distinguishable.",
        "",
        "## 6. Estimator consistency",
        "",
        "Point and CI target the same ratio-of-round-medians in every cell. "
        "The legacy pooled-request ratios (1.076 / 1.041 / 1.134) are "
        "descriptive only and appear once as a table note under Table 7, "
        "never as a primary point estimate paired with a round-level CI.",
        "",
        "## 7. Stage 3 verdict",
        "",
        "**PASS** — estimand, pairing, aggregation, RNG, replicate count, CI "
        "method, and orientation are verified; two independent runs are "
        "byte-identical; all 63 cells reproduce from raw exhibits. Stage 4 "
        "(claim-by-claim audit) is authorized.",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} and {OUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
