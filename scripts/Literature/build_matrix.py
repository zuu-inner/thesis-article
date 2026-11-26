#!/usr/bin/env python3
"""Build article/drafts/literature-matrix.csv + article/drafts/crossref_verify.json.

Rebuilds the literature matrix from assets/bib/cites.bib (51 entries) and
verifies every DOI against Crossref (fallback DataCite for arXiv-style DOIs).
Include/exclude decisions are curated here, documented per row, and never
derived from bibliometric scores alone.

Read-only with respect to the bibliography: this script never edits
assets/bib/cites.bib.

CSV columns (13):
  bib_key, doi, title, year, venue, venue_type, include_status,
  decision_reason, article_role, crossref_registry, crossref_status,
  crossref_title_match, crossref_year_match
"""
from __future__ import annotations

import csv
import json
import re
import time
import urllib.error
import urllib.request
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
BIB = ROOT / "assets" / "bib" / "cites.bib"
OUT_CSV = ROOT / "article" / "drafts" / "literature-matrix.csv"
OUT_JSON = ROOT / "article" / "drafts" / "crossref_verify.json"
MAILTO = "rafizuhayr001@gmail.com"
UA = f"thesis-literature-audit/1.0 (mailto:{MAILTO})"

# --- curated include/exclude decisions (key -> (status, reason, role)) -------
INCLUDE = {
    # core: on-demand JSON + parser-technique lineage
    "10.1002_spe.3313": ("INCLUDE", "core basis: on-demand JSON parsing design (lazy materialization)", "intro+methods"),
    "10.48550_arXiv.1902.08318": ("INCLUDE", "simdjson: SIMD JSON parsing lineage; cite published VLDB Journal version 10.1007/s00778-019-00578-5 in manuscript", "intro+methods"),
    "10.14778_3115404.3115416": ("INCLUDE", "Mison: structural index + projection pushdown", "intro+methods"),
    "10.14778_3236187.3236207": ("INCLUDE", "Sparser: raw filtering before parse", "intro"),
    "10.14778_3436905.3436926": ("INCLUDE", "Pison: scalable structural index construction", "intro"),
    "10.14778_3137765.3137782": ("INCLUDE", "FAD.js: JIT speculative selective access in JS/Node", "intro+methods"),
    "10.1145_3503222.3507719": ("INCLUDE", "JSONSki: streaming fast-forwarding (top-venue ASPLOS, CPU)", "intro"),
    "10.1145_3297858.3304008": ("INCLUDE", "JPStream: query-parse joint compilation (top-venue ASPLOS, CPU)", "intro"),
    "10.1145_3623278.3624754": ("INCLUDE", "SIMD JSONPath with descendants (top-venue ASPLOS, CPU)", "related-work"),
    "10.1145_3448016.3452809": ("INCLUDE", "JSON Tiles: JSON analytics in relational engines", "intro"),
    "10.14778_3778092.3778109": ("INCLUDE", "streaming JSON schema validation (memory angle)", "related-work"),
    "10.14778_3746405.3746439": ("INCLUDE", "GpJSON: JSON processing across hardware (PVLDB)", "related-work"),
    # scalar/text pipeline components cited by ze_json lookups (@cite)
    "10.1002_spe.2984": ("INCLUDE", "number parsing at GB/s; source of lookups tables @cite", "methods"),
    "10.1002_spe.2920": ("INCLUDE", "UTF-8 validation lookup tables @cite", "methods"),
    "10.1002_spe.3296": ("INCLUDE", "URL parsing: vectorized scalar family adopted by Node.js", "intro"),
    "10.1002_spe.3396": ("INCLUDE", "DNS records parsing: SIMD text-parsing lineage", "intro"),
    "10.1002_spe.3261": ("INCLUDE", "UTF-8/16 transcoding AVX-512, adopted by Node.js", "intro"),
    "10.1002_spe.3036": ("INCLUDE", "transcoding billions of chars/s: SIMD text pipeline", "intro"),
    "10.1002_spe.2777": ("INCLUDE", "Base64 at memcpy speed: SIMD scalar pipeline", "intro"),
    "10.1002_spe.70105": ("INCLUDE", "ill-formed UTF-16 fixing, integrated in V8", "intro"),
    "10.1145_3859286": ("INCLUDE", "forgiving Base64 decoding, Node.js 25 integration", "intro"),
    # WebAssembly performance context (server/Node relevance)
    "10.1145_3487552.3487827": ("INCLUDE", "wasm vs JS performance study (IMC): environment variance", "intro+discussion"),
    "10.1145_3744916.3764533": ("INCLUDE", "wasm usage in Node.js empirical study (ICSE)", "intro+discussion"),
    "10.1145_3714465": ("INCLUDE", "wasm runtime research survey (TOSEM)", "intro"),
    "10.1145_3736169": ("INCLUDE", "wasm benchmarking on embedded (TACO): overhead context", "related-work"),
    "10.1145_3760387": ("INCLUDE", "Wasm-IO: server-side wasm beyond web (ACM TECS)", "related-work"),
    # methodology
    "10.1145_2807591.2807644": ("INCLUDE", "scientific benchmarking discipline (report medians/CI/variability); sole pre-2016 exception per year policy", "methods+stats"),
    # standard
    "10.17487_RFC8259": ("INCLUDE", "JSON format standard: compliance requirement", "methods"),
}

EXCLUDE = {
    "10.51219_JAIMLD_chakradhar-avinash-devarapalli_63": ("EXCLUDE", "venue quality: non-indexed venue, editorial standard below article bar", ""),
    "10.47852_bonviewAAES52024965": ("EXCLUDE", "venue quality: publisher with questionable editorial standards", ""),
    "10.31649_vitce_2.2026.121": ("EXCLUDE", "venue quality/indexing below article bar", ""),
    "10.1109_ICHCI67614.2025.11292539": ("EXCLUDE", "scope: browser micro-benchmark (matrix ops), peripheral to server JSON", ""),
    "10.48550_arXiv.2205.05464": ("EXCLUDE", "hardware: FPGA filtering, outside CPU/wasm scope", ""),
    "10.1145_3533737.3535094": ("EXCLUDE", "hardware: FPGA pipeline, outside CPU/wasm scope", ""),
    "10.1109_ASP-DAC66049.2026.11420760": ("EXCLUDE", "hardware: custom accelerator, outside software scope", ""),
    "10.1109_RTAS68450.2026.00024": ("EXCLUDE", "scope: worst-case execution time, embedded RT", ""),
    "10.1145_3733812.3765536": ("EXCLUDE", "scope: memory-safety tagging, security", ""),
    "10.1145_3426422.3426978": ("EXCLUDE", "scope: delimited continuations, language runtime", ""),
    "10.1109_SSE62657.2024.00054": ("EXCLUDE", "scope: WASI internals analysis", ""),
    "10.1109_CLOUD49709.2020.00056": ("EXCLUDE", "scope: edge wasm OS", ""),
    "10.1145_3572848.3577436": ("EXCLUDE", "scope: HPC MPI distribution", ""),
    "10.1109_ASE56229.2023.00088": ("EXCLUDE", "scope: differential testing of wasm runtimes", ""),
    "10.1109_ICT4S55073.2022.00014": ("EXCLUDE", "scope: energy measurement (energy not studied here)", ""),
    "10.1145_3593434.3593454": ("EXCLUDE", "scope: IoT energy/perf (device class)", ""),
    "10.48550_arXiv.2512.00035": ("EXCLUDE", "scope: IoT microcontrollers", ""),
    "10.1109_CLEI53233.2021.9640153": ("EXCLUDE", "scope: generic non-web evaluation", ""),
    "10.5753_sbesc_estendido.2020.13102": ("EXCLUDE", "scope: IoT JS performance", ""),
    "10.1109_IcETRAN62308.2024.10645198": ("EXCLUDE", "scope: generic web wasm applications", ""),
    "10.1109_PMBS56514.2022.00011": ("EXCLUDE", "scope: hardware counter metrics (not used: no counters measured)", ""),
    "10.1145_3611643.3616311": ("EXCLUDE", "scope: compiler inlining effects, orthogonal", ""),
    "simdjson-data": ("EXCLUDE", "data artifact (GitHub corpus), not cited literature; not used as corpus here", ""),
}

VENUE_TYPE = {"article": "journal", "inproceedings": "proceedings",
              "misc": "standard-or-misc"}


def parse_bib(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    entries: list[dict] = []
    kind = None
    cur: dict | None = None
    buf_key = None
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r"@(\w+)\{([^,]+),", line)
        if m:
            if cur:
                entries.append(cur)
            kind = m.group(1).lower()
            buf_key = m.group(2).strip()
            cur = {"key": buf_key, "kind": kind, "fields": {}}
            continue
        if cur is None:
            continue
        if line == "}":
            entries.append(cur)
            cur = None
            continue
        fm = re.match(r"(\w+)\s*=\s*(.*)", line)
        if fm and cur is not None:
            field = fm.group(1).lower()
            val = fm.group(2).rstrip().rstrip(",")
            val = val.strip("{}").strip()
            cur["fields"][field] = val
    if cur:
        entries.append(cur)
    return entries


def norm(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)  # strip crossref markup (e.g. <scp>)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def fetch(url: str, timeout: int = 30) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return None
            if e.code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            return None
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(1.5 * (attempt + 1))
    return None


def verify(doi: str) -> dict:
    out = {"doi": doi, "registry": None, "status": None, "title": None,
           "year": None, "container": None}
    cr = fetch(f"https://api.crossref.org/works/{doi}?mailto={MAILTO}")
    if cr is not None:
        msg = cr.get("message", {})
        out["registry"] = "crossref"
        title = (msg.get("title") or [""])[0]
        year = None
        if msg.get("issued", {}).get("date-parts"):
            year = msg["issued"]["date-parts"][0][0]
        container = (msg.get("container-title") or [""])
        out.update(status="found", title=title, year=year,
                   container=container[0] if container else None)
        return out
    dc = fetch(f"https://api.datacite.org/dois/{doi}")
    if dc is not None:
        attrs = dc.get("data", {}).get("attributes", {})
        titles = attrs.get("titles") or [{}]
        out.update(registry="datacite", status="found",
                   title=titles[0].get("title"),
                   year=attrs.get("publicationYear"),
                   container=attrs.get("publisher"))
        return out
    out["status"] = "not-found"
    return out


def main() -> None:
    entries = parse_bib(BIB)
    print(f"bib entries parsed: {len(entries)}")

    rows: list[dict] = []
    verify_cache: dict[str, dict] = {}

    for e in entries:
        key = e["key"]
        f = e["fields"]
        doi = f.get("doi", "")
        title = f.get("title", "")
        year_raw = f.get("year", "")
        m = re.search(r"\d{4}", year_raw)
        year = int(m.group(0)) if m else None
        venue = f.get("journal") or f.get("booktitle") or f.get("howpublished") \
            or f.get("publisher") or ""
        vtype = VENUE_TYPE.get(e["kind"], "misc")

        dec = INCLUDE.get(key) or EXCLUDE.get(key) or \
            ("UNRESOLVED", "no curated decision — review manually", "")
        status, reason, role = dec

        row = {
            "bib_key": key,
            "doi": doi,
            "title": title,
            "year": year if year is not None else "",
            "venue": venue,
            "venue_type": vtype,
            "include_status": status,
            "decision_reason": reason,
            "article_role": role,
            "crossref_registry": "",
            "crossref_status": "",
            "crossref_title_match": "",
            "crossref_year_match": "",
        }

        if doi:
            if doi not in verify_cache:
                verify_cache[doi] = verify(doi)
                time.sleep(0.4)  # polite rate
            v = verify_cache[doi]
            row["crossref_registry"] = v["registry"] or ""
            row["crossref_status"] = v["status"]
            if v["status"] == "found":
                t_ok = bool(v["title"]) and (
                    norm(v["title"])[:40] in norm(title) or
                    norm(title)[:40] in norm(v["title"]))
                y_ok = (v["year"] is not None and year is not None
                        and abs(int(v["year"]) - year) <= 1)
                row["crossref_title_match"] = "ok" if t_ok else "mismatch"
                row["crossref_year_match"] = "ok" if y_ok else "mismatch"
            else:
                row["crossref_title_match"] = "n/a"
                row["crossref_year_match"] = "n/a"
        else:
            row["crossref_status"] = "doi-missing"
            row["crossref_title_match"] = "n/a"
            row["crossref_year_match"] = "n/a"
        rows.append(row)

    cols = ["bib_key", "doi", "title", "year", "venue", "venue_type",
            "include_status", "decision_reason", "article_role",
            "crossref_registry", "crossref_status", "crossref_title_match",
            "crossref_year_match"]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump({"schema_version": "1.0.0",
                   "kind": "crossref_verification",
                   "date": "2026-11-18",
                   "results": list(verify_cache.values())},
                  fh, indent=2, ensure_ascii=False)

    inc = sum(1 for r in rows if r["include_status"] == "INCLUDE")
    exc = sum(1 for r in rows if r["include_status"] == "EXCLUDE")
    ok = sum(1 for r in rows if r["crossref_status"] == "found")
    mismatch = sum(1 for r in rows if "mismatch" in (r["crossref_title_match"],
                                                     r["crossref_year_match"]))
    print(f"rows: {len(rows)} | INCLUDE {inc} | EXCLUDE {exc} | "
          f"crossref found {ok} | mismatches {mismatch}")
    for r in rows:
        if r["crossref_status"] != "found" or "mismatch" in (
                r["crossref_title_match"], r["crossref_year_match"]):
            print(f"  CHECK: {r['bib_key']} doi={r['doi'] or '-'} "
                  f"status={r['crossref_status']} "
                  f"title={r['crossref_title_match']} "
                  f"year={r['crossref_year_match']}")


if __name__ == "__main__":
    main()
