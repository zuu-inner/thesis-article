# Audit Provenance Bibliografi Artikel — 2026-11-26

## Keputusan

Snapshot bibliografi artikel bukan lagi salinan bebas. File
`article/data/bib/cites.bib` adalah filter byte-identik dari registri kanonik
root `assets/bib/cites.bib`, sedangkan `article/data/bib/article-selection.json`
mencatat 42 entri terpilih serta alasan 26 entri tidak terpilih.

## Sumber kanonik

- Repository: `https://github.com/zuudevs/thesis.git`
- Commit: `5f2043a426e52ee5af193920bccaafcbb2dc1aab`
- Path: `assets/bib/cites.bib`
- Git blob: `6fece41ebebcd0d3a20ee74cebc3ae67e6271f92`
- SHA-256 byte commit: `620a6150c5d336a7ab87f7bc6bf0f6b0d2c5219ba2faadb50b700d587a5beb4b`
- Isi: 68 entri, 66 DOI unik

Metadata volume/number untuk SPE UTF-16 diperbarui ke volume 56, issue 12,
halaman 1498–1509. Tahun ASPLOS '23 untuk `10.1145/3623278.3624754`
dikoreksi ke 2023 sesuai seriproceedings.

## Filter artikel

- Selected: 42 entri (41 DOI + 1 paper URL-only tanpa DOI)
- Excluded: 26 entri
- SHA-256 manifest selection:
  `b7e928d5509f188bbc43a50231a37761ff90dd8fad41941121524355b8d5710b`
- SHA-256 snapshot:
  `e648f8d5e7e9e364af420489364824f116cb414e08d17c89f1d6ef9d0a453ca9`

Tiga entri ditandai superseded hanya untuk artikel, tetapi tetap dipertahankan
di registri root karena histori/kode riset membutuhkan lineage tersebut:

- arXiv simdjson → versi jurnal `10.1007/s00778-019-00578-5`;
- IMC 2021 → `10.1145/3712197`;
- Wasm-IO → `10.1007/s10723-023-09669-8`.

Paper DMLR `SchulzKumpel2025Constructing` tetap tanpa DOI karena registry resmi
DMLR belum menetapkan DOI. Volume 2, article 6, halaman 1–73, dan URL
OpenReview diverifikasi dari indeks volume resmi DMLR.

## DOI registry

`article/data/json/crossref_verify.json` memuat 66 hasil registry untuk seluruh
DOI kanonik. Semua 41 DOI yang dipilih artikel berstatus `found`; title dan
year match tidak memiliki mismatch. Registry SHA-256 saat snapshot dibuat:
`6c1ec0a136d1d0732a0b041339959df8957011c1423c2f69f6f13c73e1743e7c`.

## Verifikasi

- `python scripts/FinalAudit/verify_bibliography_snapshot.py`: 16/16 PASS.
- `python scripts/FinalAudit/verify_final_manuscript.py`: 19/19 PASS.
- DOI-set manuscript = DOI-set snapshot (case-insensitive).
- Reference manuscript tetap 42 dan berurutan [1]–[42].
