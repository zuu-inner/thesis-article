#!/usr/bin/env python3
"""Generate the article bibliography snapshot from the canonical root registry.

The canonical file is read from a specific Git commit, not from an arbitrary
working tree.  The generated snapshot is therefore reproducible and its
provenance sidecar can prove which canonical bytes were selected.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from bibliography import (
    ARTICLE_ROOT,
    canonical_path,
    load_manifest,
    parse_bib_text,
    render_snapshot,
    selection_path,
    sha256_bytes,
    sha256_text_bytes,
    sha256_text_file,
    validate_selection,
    workspace_root,
)

CANONICAL_REPOSITORY = "https://github.com/zuudevs/thesis.git"
ARTICLE_REPOSITORY = "https://github.com/zuu-inner/thesis-article.git"
DEFAULT_OUTPUT = ARTICLE_ROOT / "data" / "bib" / "cites.bib"
DEFAULT_PROVENANCE = ARTICLE_ROOT / "data" / "bib" / "cites.bib.provenance.json"
DEFAULT_REGISTRY = ARTICLE_ROOT / "data" / "json" / "crossref_verify.json"


def git_output(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def resolve_commit(root: Path, revision: str) -> str:
    return git_output(root, "rev-parse", "--verify", f"{revision}^{{commit}}").decode("ascii").strip()


def load_committed_canonical(root: Path, commit: str, relative_path: str) -> tuple[str, bytes]:
    blob = git_output(root, "show", f"{commit}:{relative_path}")
    return blob.decode("utf-8"), blob


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-commit",
        required=True,
        help="Canonical root commit containing assets/bib/cites.bib",
    )
    parser.add_argument("--canonical", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = workspace_root()
    canonical = (args.canonical or canonical_path(root)).resolve()
    manifest_file = (args.manifest or selection_path()).resolve()
    output = args.output.resolve()
    provenance_path = args.provenance.resolve()
    registry = args.registry.resolve()

    try:
        canonical.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"canonical bibliography must be inside workspace root: {canonical}") from exc
    relative_path = canonical.relative_to(root).as_posix()

    commit = resolve_commit(root, args.source_commit)
    canonical_text, canonical_blob = load_committed_canonical(root, commit, relative_path)

    working_text = canonical.read_text(encoding="utf-8-sig")
    if working_text.replace("\r\n", "\n") != canonical_text.replace("\r\n", "\n"):
        raise SystemExit(
            "working-tree canonical bibliography differs from the requested source commit; "
            "commit or restore the canonical file before generating the snapshot"
        )

    entries = parse_bib_text(canonical_text)
    manifest = load_manifest(manifest_file)
    selected, excluded = validate_selection(entries, manifest)

    snapshot = render_snapshot(selected)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(snapshot)

    manifest_by_key = {item["key"]: item for item in manifest["selected"]}
    excluded_by_key = {item["key"]: item for item in manifest["excluded"]}
    citation_order = sorted(
        (
            {
                "reference": item["reference"],
                "key": item["key"],
                "doi": item["doi"],
            }
            for item in manifest["selected"]
        ),
        key=lambda item: item["reference"],
    )

    provenance: dict[str, object] = {
        "schema_version": "1.0.0",
        "kind": "bibliography_snapshot_provenance",
        "source": {
            "repository": CANONICAL_REPOSITORY,
            "commit": commit,
            "path": relative_path,
            "git_blob_oid": git_output(root, "rev-parse", f"{commit}:{relative_path}")
            .decode("ascii")
            .strip(),
            "sha256": sha256_bytes(canonical_blob),
            "entry_count": len(entries),
            "doi_count": sum(entry.doi is not None for entry in entries),
        },
        "selection": {
            "path": "article/data/bib/article-selection.json",
            "sha256": sha256_text_file(manifest_file),
            "selected_key_count": len(selected),
            "excluded_key_count": len(excluded),
            "selected_keys": [entry.key for entry in selected],
            "excluded_entries": [
                {
                    "key": entry.key,
                    "doi": entry.doi,
                    "reason": excluded_by_key[entry.key]["reason"],
                }
                for entry in excluded
            ],
            "citation_order": citation_order,
        },
        "snapshot": {
            "repository": ARTICLE_REPOSITORY,
            "path": "article/data/bib/cites.bib",
            "sha256": sha256_text_bytes(snapshot),
            "entry_count": len(selected),
            "doi_count": sum(entry.doi is not None for entry in selected),
            "url_only_keys": [entry.key for entry in selected if entry.doi is None],
        },
    }

    if registry.exists():
        registry_data = json.loads(registry.read_text(encoding="utf-8"))
        provenance["doi_registry"] = {
            "path": "article/data/json/crossref_verify.json",
            "sha256": sha256_text_file(registry),
            "result_count": len(registry_data.get("results", [])),
        }

    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    provenance_path.write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"canonical: {commit} ({len(entries)} entries)")
    print(f"snapshot:  {output} ({len(selected)} entries, sha256={provenance['snapshot']['sha256']})")
    print(f"provenance: {provenance_path}")
    print("selected reasons:", ", ".join(item["key"] for item in manifest["selected"][:3]), "...")
    print("manifest reasons verified for", len(manifest_by_key), "selected entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
