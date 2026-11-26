from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bibliography import parse_bib_text, validate_selection


class BibliographyTests(unittest.TestCase):
    def test_parser_preserves_nested_braces_and_extracts_doi(self) -> None:
        entries = parse_bib_text(
            "@article{key,\n"
            "title = {Title with {JSON}},\n"
            "doi = {10.1000/example},\n"
            "year = {2024}\n"
            "}\n"
        )
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].key, "key")
        self.assertEqual(entries[0].doi, "10.1000/example")
        self.assertEqual(entries[0].fields["title"], "Title with {JSON}")

    def test_duplicate_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate BibTeX key: key"):
            parse_bib_text("@article{key,\nyear = {2024}\n}\n@article{key,\nyear = {2025}\n}\n")

    def test_selection_must_cover_canonical_registry(self) -> None:
        canonical = parse_bib_text(
            "@article{one,\ndoi = {10.1000/one},\nyear = {2024}\n}\n"
            "@article{two,\ndoi = {10.1000/two},\nyear = {2025}\n}\n"
        )
        manifest = {
            "selected": [{"key": "one", "doi": "10.1000/one"}],
            "excluded": [],
        }
        with self.assertRaisesRegex(ValueError, "unclassified"):
            validate_selection(canonical, manifest)

    def test_selection_rejects_manifest_doi_mismatch(self) -> None:
        canonical = parse_bib_text(
            "@article{one,\ndoi = {10.1000/one},\nyear = {2024}\n}\n"
        )
        manifest = {
            "selected": [{"key": "one", "doi": "10.1000/wrong"}],
            "excluded": [],
        }
        with self.assertRaisesRegex(ValueError, "DOI mismatch"):
            validate_selection(canonical, manifest)


if __name__ == "__main__":
    unittest.main()
