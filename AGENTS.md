# AGENTS.md — Repository Artikel Thesis

> Aturan kerja untuk agent dan kontributor repo artikel.

## Identitas repo

- Repo ini menyimpan sumber, builder, audit, dan output naskah artikel
  original research.
- Workspace riset utama berada di repo `v5`; saat repo artikel dipakai sebagai
  submodule, path workspace adalah parent superproject.
- Untuk checkout mandiri, set `THESIS_WORKSPACE_ROOT` ke path absolut root
  workspace `v5`.
- Naskah sumber kebenaran adalah `drafts/article-draft.md`.
- Template pristine adalah `article.docx`; jangan menimpanya saat build.

## Bahasa

- Naskah dan caption artikel: English.
- Dokumentasi operasional repo ini: Bahasa Indonesia.
- Kode, identifier, nama file, dan pesan commit: English.

## Workflow

- Baca `README.md` dan audit final terbaru sebelum mengubah pipeline.
- Jangan mengubah raw exhibit, measurement record, atau corpus di root `v5`.
- Turunan evidence harus menyimpan provenance path, hash, dan commit bila
  tersedia.
- Jangan commit `node_modules/`, cache, credential, atau `.env` lokal.
- Gunakan branch dan Pull Request; jangan push langsung ke `main`.
- Gunakan Conventional Commits: `type(scope): subject`.

## Verifikasi

- Perubahan naskah: jalankan builder dan
  `scripts/FinalAudit/verify_final_manuscript.py`.
- Perubahan chart/figure: regenerate dari data, bukan mengedit PNG hasil.
- Perubahan literature: audit DOI, eligibility, dan keterkaitan sitasi.
- Perubahan path/provenance: jalankan verifier dari checkout submodule dan
  checkout mandiri dengan `THESIS_WORKSPACE_ROOT`.
