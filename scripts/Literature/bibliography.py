"""Shared helpers for the canonical-to-article bibliography pipeline."""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
ENTRY_START = re.compile(r"(?mi)^@(\w+)\s*\{\s*([^,\s]+)\s*,")
FIELD_START = re.compile(r"^\s*([A-Za-z][\w-]*)\s*=\s*(.*)$")


@dataclass(frozen=True)
class BibEntry:
    key: str
    kind: str
    fields: dict[str, str]
    block: str

    @property
    def doi(self) -> str | None:
        return self.fields.get("doi")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _strip_outer_braces(value: str) -> str:
    value = value.strip()
    if not (value.startswith("{") and value.endswith("}")):
        return value
    depth = 0
    for index, char in enumerate(value):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0 and index != len(value) - 1:
                return value
    return value[1:-1].strip()


def parse_bib(path: Path) -> list[BibEntry]:
    """Parse the simple, one-field-per-line BibTeX used by this workspace."""
    return parse_bib_text(path.read_text(encoding="utf-8-sig"))


def parse_bib_text(text: str) -> list[BibEntry]:
    matches = list(ENTRY_START.finditer(text))
    entries: list[BibEntry] = []
    seen: set[str] = set()

    for index, match in enumerate(matches):
        depth = 1
        cursor = match.end()
        while cursor < len(text) and depth:
            char = text[cursor]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            cursor += 1
        if depth:
            raise ValueError(f"unterminated BibTeX entry starting at line {match.start()}")

        block = text[match.start():cursor].rstrip()
        key = match.group(2).strip()
        if key in seen:
            raise ValueError(f"duplicate BibTeX key: {key}")
        seen.add(key)

        fields: dict[str, str] = {}
        for raw_line in block.splitlines()[1:]:
            field_match = FIELD_START.match(raw_line)
            if not field_match:
                continue
            name = field_match.group(1).lower()
            raw_value = field_match.group(2).strip()
            if raw_value.endswith(","):
                raw_value = raw_value[:-1].rstrip()
            fields[name] = _strip_outer_braces(raw_value)

        entries.append(
            BibEntry(
                key=key,
                kind=match.group(1).lower(),
                fields=fields,
                block=block,
            )
        )

    return entries


def workspace_root() -> Path:
    configured = os.environ.get("THESIS_WORKSPACE_ROOT")
    if configured:
        return Path(configured).resolve()
    return ARTICLE_ROOT.parent.resolve()


def canonical_path(root: Path | None = None) -> Path:
    root = root or workspace_root()
    return root / "assets" / "bib" / "cites.bib"


def selection_path() -> Path:
    return ARTICLE_ROOT / "data" / "bib" / "article-selection.json"


def load_manifest(path: Path | None = None) -> dict:
    path = path or selection_path()
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("kind") != "bibliography_selection":
        raise ValueError(f"unexpected selection manifest kind: {data.get('kind')}")
    return data


def validate_selection(
    canonical: list[BibEntry],
    manifest: dict,
) -> tuple[list[BibEntry], list[BibEntry]]:
    """Validate a selection against the canonical registry.

    Returns ``(selected_entries, excluded_entries)`` in canonical order.
    """
    canonical_by_key = {entry.key: entry for entry in canonical}
    selected_items = manifest.get("selected")
    excluded_items = manifest.get("excluded")
    if not isinstance(selected_items, list) or not isinstance(excluded_items, list):
        raise ValueError("selection manifest must contain selected and excluded lists")

    selected_keys = [item.get("key") for item in selected_items]
    excluded_keys = [item.get("key") for item in excluded_items]
    if any(not key for key in selected_keys + excluded_keys):
        raise ValueError("every selection entry must have a key")
    if len(selected_keys) != len(set(selected_keys)):
        raise ValueError("duplicate key in selected selection")
    if len(excluded_keys) != len(set(excluded_keys)):
        raise ValueError("duplicate key in excluded selection")
    overlap = set(selected_keys) & set(excluded_keys)
    if overlap:
        raise ValueError(f"keys cannot be both selected and excluded: {sorted(overlap)}")

    missing_selected = set(selected_keys) - set(canonical_by_key)
    missing_excluded = set(excluded_keys) - set(canonical_by_key)
    if missing_selected or missing_excluded:
        raise ValueError(
            "selection references keys absent from canonical registry: "
            f"{sorted(missing_selected | missing_excluded)}"
        )

    unclassified = set(canonical_by_key) - set(selected_keys) - set(excluded_keys)
    if unclassified:
        raise ValueError(f"canonical entries are unclassified: {sorted(unclassified)}")

    selected_dois: list[str] = []
    for item in selected_items:
        entry = canonical_by_key[item["key"]]
        expected_doi = entry.doi
        actual_doi = item.get("doi")
        if actual_doi != expected_doi:
            raise ValueError(
                f"DOI mismatch for {entry.key}: manifest={actual_doi!r}, canonical={expected_doi!r}"
            )
        if expected_doi:
            selected_dois.append(expected_doi.lower())
    if len(selected_dois) != len(set(selected_dois)):
        raise ValueError("duplicate DOI in selected entries")

    selected = [canonical_by_key[key] for key in selected_keys]
    excluded = [canonical_by_key[key] for key in excluded_keys]
    selected.sort(key=lambda entry: canonical.index(entry))
    excluded.sort(key=lambda entry: canonical.index(entry))
    return selected, excluded


def render_snapshot(entries: list[BibEntry]) -> bytes:
    return ("\n".join(entry.block for entry in entries) + "\n").encode("utf-8")
