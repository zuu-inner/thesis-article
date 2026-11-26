#!/usr/bin/env python3
"""Render Stage 6 literature audit from the computed registry."""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
DATA = ROOT / "article" / "data" / "json" / "final-audit-literature.json"
OUT = ROOT / "article" / "drafts" / "final-audit" / "literature-audit.md"


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    lines = [
        "# Stage 6 — Literature and Reference Audit",
        "",
        "Official guidelines checked 2026-11-19 at "
        "`https://ejournals.itda.ac.id/index.php/avitec/about/submissions` "
        "(current AVITEC Author Guidelines). Registry verification: "
        "`article/data/json/crossref_verify.json` (updated 2026-11-19 to add "
        "the published VLDB Journal version of simdjson, ref [3], DOI "
        "`10.1007/s00778-019-00578-5`, verified via Crossref API).",
        "",
        "## 1. Requirement checks",
        "",
        "| Requirement | Value | Status |",
        "|---|---:|---|",
        f"| Title ≤ 20 words | {d['title_words']} | PASS |",
        f"| Abstract ≤ 250 words, single paragraph | {d['abstract_words']} | PASS |",
        f"| Keywords 3–7 | {d['keyword_count']} | PASS |",
        "| Manuscript length 5,000–8,000 words (excl. refs) | 5,254 prose (other definitions 5,487–7,648) | PASS |",
        f"| References ≥ 15 total | {d['reference_count']} | PASS |",
        f"| Introduction ≥ 15 peer-reviewed journal articles | {d['intro_journal_refs']} | PASS |",
        f"| ≥ 80% recent international peer-reviewed journals | {d['recent_journal_pct']}% "
        f"({d['recent_journal_refs']}/{d['reference_count']}) | **FAIL** |",
        f"| Non-English refs ≤ 25% | {d['non_english_refs']}% | PASS |",
        f"| DOI/registry verified | {d['crossref_found']}/{d['reference_count']} | PASS |",
        "| Numbered citations before punctuation | builder QA: 0 violations; [1]–[28] in first-appearance order | PASS |",
        "",
        "**Critical gap:** at least "
        f"**{d['min_additional_journal_refs_for_80pct']} additional genuine "
        "recent international journal articles** are needed to reach 80% "
        "((20+N)/(28+N) ≥ 0.8 ⇒ N ≥ 12). The Introduction requirement is "
        "already met; additions must support real claims, not padding.",
        "",
        "## 2. Classification rules",
        "",
        "- Journal = Crossref `type: journal-article`. `Proc. VLDB Endow.` is "
        "counted as a journal: Crossref reports `type: journal-article`, "
        "ISSN 2150-8097 (verified for DOI `10.14778/3115404.3115416`).",
        "- Excluded from the journal count: conference proceedings, RFC / "
        "standards, arXiv preprints, books, and non-indexed venues — even "
        "when they are legitimate and necessary citations.",
        "- \"Recent\" = published 2016 or later; ref [28] (2015) is a "
        "foundational benchmarking paper and is a proceedings article, so it "
        "is not counted either way.",
        "",
        "## 3. All 28 references",
        "",
        "| # | DOI | Year | Venue | Type | Journal? | Recent? | In Intro |",
        "|---:|---|---:|---|---|---|---|---|",
    ]
    for r in d["rows"]:
        lines.append(
            f"| {r['n']} | `{r['doi']}` | {r['year']} | {r['venue'][:48]} | "
            f"{r['venue_type']} | {'yes' if r['is_journal'] else 'no'} | "
            f"{'yes' if r['recent'] else 'no'} | "
            f"{'yes' if r['in_intro'] else 'no'} |")
    lines += [
        "",
        "## 4. Relevance checks on potentially weak citations",
        "",
        "- [1] RFC 8259 — necessary standards citation, not a journal; correct as used.",
        "- [2] Keiser & Lemire 2024 — Crossref abstract explicitly states that "
        "Apache Doris, the Node.js JavaScript runtime, Milvus, and Velox use "
        "On Demand; the Introduction's \"adopted by production systems, "
        "including the Node.js runtime itself\" is **supported** (Stage 4 #6 resolved PASS).",
        "- [6], [7], [10], [12], [23], [24], [28] — conference proceedings; "
        "relevant to their sentences but do not count toward the 80% journal requirement.",
        "- [3] was previously absent from the derived registry although cited in "
        "the manuscript; now corrected from Crossref (The VLDB Journal 28(6):941–960, 2019).",
        "",
        "## 5. Decision and required action",
        "",
        "No reference is fabricated and no irrelevant reference should be added "
        "purely to reach a quota (AVITEC explicitly discourages irrelevant "
        "citations and metric manipulation). The correct action is to source "
        "**12 additional, genuinely relevant, recent international journal "
        "articles** (e.g., peer-reviewed journal studies of JSON parsing, "
        "selective access, WebAssembly runtime performance, and rigorous "
        "performance methodology), verify each via Crossref, insert citations "
        "where they materially support the text, and regenerate the reference "
        "list, metadata, and literature registry. If such sources cannot be "
        "found, the manuscript is **not ready for submission** on literature "
        "grounds and the editor should be consulted.",
        "",
        "## 6. Stage 6 verdict",
        "",
        "**FAIL — LITERATURE BLOCKER.** All references exist and are verified, "
        "the Introduction has 20 journal citations (≥15), and all formatting "
        "criteria pass, but the recent-international-journal share is 71.4% "
        "against the 80% requirement. This blocker cannot be resolved by "
        "wording changes; Stage 7 will apply only the non-literature "
        "corrections from Stage 4/5, and the final verdict must reflect the "
        "unresolved literature gap.",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
