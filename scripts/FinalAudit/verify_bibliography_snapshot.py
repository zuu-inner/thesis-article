#!/usr/bin/env python3
"""Verify the article bibliography snapshot against its canonical provenance."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Literature"))

from bibliography import (
    ARTICLE_ROOT,
    load_manifest,
    parse_bib,
    parse_bib_text,
    render_snapshot,
    selection_path,
    sha256_bytes,
    validate_selection,
    workspace_root,
)

SNAPSHOT = ARTICLE_ROOT / "data" / "bib" / "cites.bib"
PROVENANCE = ARTICLE_ROOT / "data" / "bib" / "cites.bib.provenance.json"
REGISTRY = ARTICLE_ROOT / "data" / "json" / "crossref_verify.json"
METADATA = ARTICLE_ROOT / "metadata.json"
DRAFT = ARTICLE_ROOT / "drafts" / "article-draft.md"
DEFAULT_REPORT = ARTICLE_ROOT / "data" / "json" / "bibliography-verification.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", default=None)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def git_output(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def manuscript_dois() -> tuple[set[str], list[int]]:
    text = DRAFT.read_text(encoding="utf-8-sig")
    reference_section = text.split("# REFERENCE", 1)[1] if "# REFERENCE" in text else ""
    references = re.findall(r"(?m)^\[(\d+)\]\s+(.*)$", reference_section)
    numbers = [int(number) for number, _ in references]
    dois = {
        match.group(1).rstrip(".").lower()
        for _, body in references
        if (match := re.search(r"doi:\s*(10\.\S+?)\.?\s*$", body, re.IGNORECASE))
    }
    return dois, numbers


def main() -> int:
    args = parse_args()
    root = workspace_root()
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    manifest_file = selection_path()
    manifest = load_manifest(manifest_file)

    source = provenance["source"]
    commit = source["commit"]
    if args.source_commit:
        requested = git_output(
            root, "rev-parse", "--verify", f"{args.source_commit}^{{commit}}"
        ).decode("ascii").strip()
        if requested != commit:
            raise SystemExit(f"provenance commit {commit} does not match requested {requested}")

    relative_path = source["path"]
    canonical_blob = git_output(root, "show", f"{commit}:{relative_path}")
    canonical_text = canonical_blob.decode("utf-8")
    canonical_entries = parse_bib_text(canonical_text)
    selected, excluded = validate_selection(canonical_entries, manifest)

    snapshot_bytes = SNAPSHOT.read_bytes()
    expected_snapshot = render_snapshot(selected)
    snapshot_entries = parse_bib(SNAPSHOT)
    snapshot_dois = {entry.doi.lower() for entry in snapshot_entries if entry.doi}

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry_results = registry.get("results", [])
    registry_dois = {
        result["doi"].lower(): result
        for result in registry_results
        if result.get("doi")
    }
    selected_dois = {entry.doi.lower() for entry in selected if entry.doi}
    selected_missing = sorted(doi for doi in selected_dois if registry_dois.get(doi, {}).get("status") != "found")

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    metadata_dois = {doi.lower() for doi in metadata["document"]["cites"]}
    draft_dois, reference_numbers = manuscript_dois()

    provenance_selection = provenance["selection"]
    provenance_snapshot = provenance["snapshot"]
    expected_selected_keys = [entry.key for entry in selected]
    expected_excluded_keys = [entry.key for entry in excluded]
    provenance_excluded_keys = [
        item["key"] for item in provenance_selection.get("excluded_entries", [])
    ]

    checks = {
        "canonical_commit_blob_matches_provenance": sha256_bytes(canonical_blob) == source["sha256"],
        "canonical_entry_count_matches_provenance": len(canonical_entries) == source["entry_count"],
        "selection_manifest_hash_matches": sha256_bytes(manifest_file.read_bytes()) == provenance_selection["sha256"],
        "selection_covers_canonical_registry": len(selected) + len(excluded) == len(canonical_entries),
        "selection_has_42_entries": len(selected) == 42,
        "selection_has_41_dois": len(selected_dois) == 41,
        "snapshot_hash_matches_provenance": sha256_bytes(snapshot_bytes) == provenance_snapshot["sha256"],
        "snapshot_is_exact_canonical_filter": snapshot_bytes == expected_snapshot,
        "snapshot_entry_count_matches_provenance": len(snapshot_entries) == provenance_snapshot["entry_count"],
        "provenance_selected_keys_match": provenance_selection.get("selected_keys") == expected_selected_keys,
        "provenance_excluded_keys_match": provenance_excluded_keys == expected_excluded_keys,
        "doi_registry_hash_matches": REGISTRY.exists()
        and sha256_bytes(REGISTRY.read_bytes()) == provenance.get("doi_registry", {}).get("sha256"),
        "doi_registry_covers_selected_dois": not selected_missing,
        "manuscript_doi_set_matches_snapshot": draft_dois == snapshot_dois,
        "metadata_doi_set_matches_snapshot": metadata_dois == snapshot_dois,
        "manuscript_has_42_contiguous_references": reference_numbers == list(range(1, 43)),
    }

    report = {
        "schema_version": "1.0.0",
        "kind": "bibliography_snapshot_verification",
        "source_commit": commit,
        "counts": {
            "canonical_entries": len(canonical_entries),
            "selected_entries": len(selected),
            "excluded_entries": len(excluded),
            "selected_dois": len(selected_dois),
            "registry_results": len(registry_results),
            "manuscript_references": len(reference_numbers),
        },
        "missing_registry_dois": selected_missing,
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}  {name}")
    print(f"report -> {args.report}")
    return 1 if report["failed_checks"] else 0


if __name__ == "__main__":
    sys.exit(main())
