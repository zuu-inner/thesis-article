#!/usr/bin/env python3
"""Dump bibliography metadata for the curated INCLUDE set (read-only).

Prints author/title/year/venue/pages/doi for every INCLUDE key of
article/scripts/Literature/build_matrix.py, for use when composing the
IEEE-based reference list of the AVITEC manuscript.

Additionally verifies the simdjson published-version DOI
(10.1007/s00778-019-00578-5, The VLDB Journal) via Crossref, because the
manuscript cites the published journal version while assets/bib/cites.bib
carries the arXiv artifact (10.48550/arXiv.1902.08318).
"""
from __future__ import annotations

import json
import re
import urllib.request
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
BIB = ROOT / "assets" / "bib" / "cites.bib"
MAILTO = "rafizuhayr001@gmail.com"

INCLUDE_KEYS = [
    "10.1002_spe.3313", "10.48550_arXiv.1902.08318",
    "10.14778_3115404.3115416", "10.14778_3236187.3236207",
    "10.14778_3436905.3436926", "10.14778_3137765.3137782",
    "10.1145_3503222.3507719", "10.1145_3297858.3304008",
    "10.1145_3623278.3624754", "10.1145_3448016.3452809",
    "10.14778_3778092.3778109", "10.14778_3746405.3746439",
    "10.1002_spe.2984", "10.1002_spe.2920", "10.1002_spe.3296",
    "10.1002_spe.3396", "10.1002_spe.3261", "10.1002_spe.3036",
    "10.1002_spe.2777", "10.1002_spe.70105", "10.1145_3859286",
    "10.1145_3487552.3487827", "10.1145_3744916.3764533",
    "10.1145_3714465", "10.1145_3736169", "10.1145_3760387",
    "10.1145_2807591.2807644", "10.17487_RFC8259",
]


def parse_bib(path: Path) -> dict[str, dict]:
    text = path.read_text(encoding="utf-8")
    entries: dict[str, dict] = {}
    cur: dict | None = None
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r"@(\w+)\{([^,]+),", line)
        if m:
            if cur:
                entries[cur["key"]] = cur
            cur = {"kind": m.group(1).lower(), "key": m.group(2).strip(),
                   "fields": {}}
            continue
        if cur is None:
            continue
        if line == "}":
            entries[cur["key"]] = cur
            cur = None
            continue
        fm = re.match(r"(\w+)\s*=\s*(.*)", line)
        if fm:
            val = fm.group(2).rstrip().rstrip(",")
            val = val.strip("{}").strip()
            cur["fields"][fm.group(1).lower()] = val
    if cur:
        entries[cur["key"]] = cur
    return entries


def crossref(doi: str) -> dict | None:
    url = f"https://api.crossref.org/works/{doi}?mailto={MAILTO}"
    req = urllib.request.Request(url, headers={"User-Agent": f"refs-dump/1.0 (mailto:{MAILTO})"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("message", {})
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


def main() -> None:
    entries = parse_bib(BIB)
    for key in INCLUDE_KEYS:
        e = entries.get(key)
        if e is None:
            print(f"!! MISSING key in bib: {key}")
            continue
        f = e["fields"]
        venue = f.get("journal") or f.get("booktitle") or f.get("howpublished") or ""
        print(f"KEY: {key} [{e['kind']}]")
        print(f"  author  : {f.get('author', '')}")
        print(f"  title   : {f.get('title', '')}")
        print(f"  year    : {f.get('year', '')}")
        print(f"  venue   : {venue}")
        for fld in ("volume", "number", "pages", "doi", "publisher"):
            if f.get(fld):
                print(f"  {fld:7s}: {f[fld]}")
        print()

    print("== Crossref verify: simdjson published version ==")
    msg = crossref("10.1007/s00778-019-00578-5")
    if "error" in msg:
        print("ERROR:", msg["error"])
    else:
        print("title    :", (msg.get("title") or [""])[0])
        print("author   :", "; ".join(
            f"{a.get('given','')} {a.get('family','')}" for a in msg.get("author", [])))
        print("container:", (msg.get("container-title") or [""]))
        issued = msg.get("issued", {}).get("date-parts")
        print("year     :", issued[0][0] if issued else None)
        vol = msg.get("volume")
        issue = msg.get("issue")
        page = msg.get("page")
        print(f"vol/issue/page: {vol} / {issue} / {page}")


if __name__ == "__main__":
    main()
