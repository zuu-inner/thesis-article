#!/usr/bin/env python3
"""Build the canonical literature matrix and DOI registry for the article.

The canonical registry remains in the research workspace.  This script applies
the article's explicit selection manifest, verifies every DOI against Crossref
(or DataCite for DOI-registered preprints), and writes derived article data.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from bibliography import (
    ARTICLE_ROOT,
    canonical_path,
    load_manifest,
    parse_bib_text,
    selection_path,
    validate_selection,
    workspace_root,
)

CANONICAL_REPOSITORY = "https://github.com/zuudevs/thesis.git"
MAILTO = "rafizuhayr001@gmail.com"
USER_AGENT = f"thesis-literature-audit/1.0 (mailto:{MAILTO})"
DEFAULT_MATRIX = ARTICLE_ROOT / "data" / "csv" / "literature-matrix.csv"
DEFAULT_REGISTRY = ARTICLE_ROOT / "data" / "json" / "crossref_verify.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--canonical", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--refresh", action="store_true", help="Re-query every DOI")
    parser.add_argument(
        "--refresh-doi",
        action="append",
        default=[],
        help="Re-query only this DOI (repeatable)",
    )
    return parser.parse_args()


def git_output(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def fetch_json(url: str, timeout: int = 30) -> dict | None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code in (404, 410):
                return None
            if error.code == 429 or error.code in (500, 502, 503, 504):
                time.sleep(2 * (attempt + 1))
                continue
            return None
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(1.5 * (attempt + 1))
    return None


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\\[a-zA-Z]+\s*", " ", value)
    value = value.replace("{", " ").replace("}", " ")
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def verify_doi(doi: str) -> dict:
    encoded = urllib.parse.quote(doi, safe="")
    crossref = fetch_json(
        f"https://api.crossref.org/works/{encoded}?mailto={urllib.parse.quote(MAILTO)}"
    )
    if crossref is not None:
        message = crossref.get("message", {})
        year = None
        for date_field in ("published-print", "published", "issued"):
            date_parts = (message.get(date_field) or {}).get("date-parts") or []
            if date_parts and date_parts[0]:
                year = date_parts[0][0]
                break
        containers = message.get("container-title") or []
        return {
            "doi": doi,
            "registry": "crossref",
            "status": "found",
            "title": (message.get("title") or [""])[0],
            "year": year,
            "container": containers[0] if containers else None,
            "volume": message.get("volume"),
            "issue": message.get("issue"),
            "page": message.get("page"),
            "url": message.get("URL"),
        }

    datacite = fetch_json(f"https://api.datacite.org/dois/{encoded}")
    if datacite is not None:
        attributes = datacite.get("data", {}).get("attributes", {})
        titles = attributes.get("titles") or [{}]
        return {
            "doi": doi,
            "registry": "datacite",
            "status": "found",
            "title": titles[0].get("title"),
            "year": attributes.get("publicationYear"),
            "container": attributes.get("publisher"),
            "volume": None,
            "issue": None,
            "page": None,
            "url": attributes.get("url"),
        }

    return {
        "doi": doi,
        "registry": None,
        "status": "not-found",
        "title": None,
        "year": None,
        "container": None,
        "volume": None,
        "issue": None,
        "page": None,
        "url": None,
    }


def title_matches(bib_title: str, registry_title: str | None) -> str:
    if not registry_title:
        return "n/a"
    left = normalize(bib_title)
    right = normalize(registry_title)
    if not left or not right:
        return "mismatch"
    if left[:40] in right or right[:40] in left:
        return "ok"
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    overlap = len(left_tokens & right_tokens) / max(1, len(left_tokens | right_tokens))
    return "ok" if overlap >= 0.75 else "mismatch"


def year_matches(bib_year: int | None, registry_year: int | None) -> str:
    if bib_year is None or registry_year is None:
        return "n/a"
    return "ok" if abs(bib_year - registry_year) <= 1 else "mismatch"


def entry_year(entry) -> int | None:
    value = entry.fields.get("year")
    match = re.search(r"\d{4}", value or "")
    return int(match.group(0)) if match else None


def main() -> int:
    args = parse_args()
    root = workspace_root()
    canonical = (args.canonical or canonical_path(root)).resolve()
    manifest_file = (args.manifest or selection_path()).resolve()
    matrix_path = args.matrix.resolve()
    registry_path = args.registry.resolve()

    canonical.relative_to(root)
    relative_path = canonical.relative_to(root).as_posix()
    commit = git_output(
        root, "rev-parse", "--verify", f"{args.source_commit}^{{commit}}"
    ).decode("ascii").strip()
    canonical_text = git_output(root, "show", f"{commit}:{relative_path}").decode("utf-8")
    entries = parse_bib_text(canonical_text)
    manifest = load_manifest(manifest_file)
    selected, excluded = validate_selection(entries, manifest)

    selected_by_key = {entry.key: entry for entry in selected}
    excluded_by_key = {entry.key: entry for entry in excluded}
    selected_items = {item["key"]: item for item in manifest["selected"]}
    excluded_items = {item["key"]: item for item in manifest["excluded"]}

    cached: dict[str, dict] = {}
    if registry_path.exists() and not args.refresh:
        existing = json.loads(registry_path.read_text(encoding="utf-8"))
        cached = {
            result["doi"].lower(): result
            for result in existing.get("results", [])
            if result.get("doi")
        }

    refresh_dois = {doi.lower() for doi in args.refresh_doi}
    verify_cache: dict[str, dict] = {}
    for entry in entries:
        doi = entry.doi
        if not doi:
            continue
        key = doi.lower()
        if key in cached and key not in refresh_dois and cached[key].get("status") == "found":
            verify_cache[key] = cached[key]
        else:
            verify_cache[key] = verify_doi(doi)
            time.sleep(0.25)

    rows: list[dict[str, object]] = []
    for entry in entries:
        fields = entry.fields
        doi = entry.doi or ""
        title = fields.get("title", "")
        year = entry_year(entry)
        venue = (
            fields.get("journal")
            or fields.get("booktitle")
            or fields.get("howpublished")
            or fields.get("publisher")
            or ""
        )
        venue_type = {
            "article": "journal",
            "inproceedings": "proceedings",
            "misc": "standard-or-misc",
        }.get(entry.kind, "misc")

        if entry.key in selected_by_key:
            decision = selected_items[entry.key]
            include_status = "INCLUDE"
            reason = decision["reason"]
            role = decision.get("role", "")
        else:
            decision = excluded_items[entry.key]
            include_status = "EXCLUDE"
            reason = decision["reason"]
            role = ""

        verification = verify_cache.get(doi.lower()) if doi else None
        if verification:
            registry = verification.get("registry") or ""
            status = verification.get("status") or "not-found"
            title_match = title_matches(title, verification.get("title"))
            year_match = year_matches(year, verification.get("year"))
        else:
            registry = ""
            status = "doi-missing"
            title_match = "n/a"
            year_match = "n/a"

        rows.append(
            {
                "bib_key": entry.key,
                "doi": doi,
                "title": title,
                "year": year if year is not None else "",
                "venue": venue,
                "venue_type": venue_type,
                "include_status": include_status,
                "decision_reason": reason,
                "article_role": role,
                "crossref_registry": registry,
                "crossref_status": status,
                "crossref_title_match": title_match,
                "crossref_year_match": year_match,
                "canonical_commit": commit,
            }
        )

    columns = [
        "bib_key",
        "doi",
        "title",
        "year",
        "venue",
        "venue_type",
        "include_status",
        "decision_reason",
        "article_role",
        "crossref_registry",
        "crossref_status",
        "crossref_title_match",
        "crossref_year_match",
        "canonical_commit",
    ]
    matrix_path.parent.mkdir(parents=True, exist_ok=True)
    with matrix_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    results = [verify_cache[key] for key in sorted(verify_cache)]
    registry_payload = {
        "schema_version": "1.1.0",
        "kind": "crossref_verification",
        "date": date.today().isoformat(),
        "source": {
            "repository": CANONICAL_REPOSITORY,
            "commit": commit,
            "path": relative_path,
            "entry_count": len(entries),
        },
        "results": results,
    }
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps(registry_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    included = sum(row["include_status"] == "INCLUDE" for row in rows)
    excluded_count = sum(row["include_status"] == "EXCLUDE" for row in rows)
    found = sum(row["crossref_status"] == "found" for row in rows)
    mismatches = [
        row
        for row in rows
        if row["crossref_status"] == "found"
        and (
            row["crossref_title_match"] == "mismatch"
            or row["crossref_year_match"] == "mismatch"
        )
    ]
    selected_missing = [
        row
        for row in rows
        if row["include_status"] == "INCLUDE"
        and row["doi"]
        and row["crossref_status"] != "found"
    ]

    print(
        f"rows: {len(rows)} | INCLUDE {included} | EXCLUDE {excluded_count} | "
        f"DOI found {found}/{len(verify_cache)} | mismatches {len(mismatches)}"
    )
    for row in mismatches:
        print(
            f"  CHECK: {row['bib_key']} title={row['crossref_title_match']} "
            f"year={row['crossref_year_match']}"
        )
    if selected_missing:
        for row in selected_missing:
            print(f"  MISSING: {row['bib_key']} doi={row['doi']} status={row['crossref_status']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
