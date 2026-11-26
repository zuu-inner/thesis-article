#!/usr/bin/env python3
"""Dump canonical metadata for the article's explicitly selected references."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from bibliography import (
    ARTICLE_ROOT,
    load_manifest,
    parse_bib_text,
    selection_path,
    validate_selection,
    workspace_root,
)

PROVENANCE = ARTICLE_ROOT / "data" / "bib" / "cites.bib.provenance.json"
REGISTRY = ARTICLE_ROOT / "data" / "json" / "crossref_verify.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", default=None)
    return parser.parse_args()


def git_output(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def main() -> int:
    args = parse_args()
    root = workspace_root()
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    revision = args.source_commit or provenance["source"]["commit"]
    commit = git_output(
        root, "rev-parse", "--verify", f"{revision}^{{commit}}"
    ).decode("ascii").strip()
    relative_path = provenance["source"]["path"]
    canonical_text = git_output(root, "show", f"{commit}:{relative_path}").decode("utf-8")
    entries = parse_bib_text(canonical_text)
    manifest = load_manifest(selection_path())
    selected, _ = validate_selection(entries, manifest)
    by_key = {entry.key: entry for entry in selected}

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry_by_doi = {
        result["doi"].lower(): result
        for result in registry.get("results", [])
        if result.get("doi")
    }

    for item in sorted(manifest["selected"], key=lambda value: value["reference"]):
        entry = by_key[item["key"]]
        fields = entry.fields
        venue = (
            fields.get("journal")
            or fields.get("booktitle")
            or fields.get("howpublished")
            or ""
        )
        print(f"REF {item['reference']:02d} | {entry.key} [{entry.kind}]")
        print(f"  author  : {fields.get('author', '')}")
        print(f"  title   : {fields.get('title', '')}")
        print(f"  year    : {fields.get('year', '')}")
        print(f"  venue   : {venue}")
        for field in ("volume", "number", "articleno", "pages", "doi", "publisher"):
            if fields.get(field):
                print(f"  {field:7s}: {fields[field]}")
        if entry.doi:
            verification = registry_by_doi.get(entry.doi.lower(), {})
            print(
                "  registry: "
                f"{verification.get('registry', '-')} / {verification.get('status', '-')}"
            )
        else:
            print("  registry: url-only (no DOI assigned)")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
