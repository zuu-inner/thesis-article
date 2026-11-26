# Repository Artikel Thesis

Repository ini memuat sumber naskah, pipeline pembangkitan DOCX/PDF, data
evidence, dan audit naskah artikel original research. Repo ini dipisah dari
workspace riset `v5` karena memiliki siklus release dan reviewer yang berbeda,
tetapi tetap dapat dipasang sebagai submodule pada path `article/` di workspace
`v5`.

## Peta repository

| Path | Peran |
|---|---|
| `drafts/article-draft.md` | Sumber kebenaran isi naskah |
| `drafts/final-audit/` | Audit editorial, statistik, literatur, dan artefak |
| `scripts/Builder/` | Build DOCX, ekspor PDF, finalisasi, dan verifikasi |
| `scripts/Ledger/` | Evidence ledger dan rekalkulasi statistik |
| `scripts/Charter/` | Data serta generator chart |
| `scripts/Grapher/` | Diagram Mermaid, SVG master, dan rasterisasi |
| `scripts/Literature/` | Filter bibliografi kanonik, matriks, dan verifikasi DOI |
| `scripts/FinalAudit/` | Gerbang audit independen |
| `data/` | Data turunan dan provenance evidence |
| `assets/` | Gambar, SVG master, dan evidence visual |
| `article.docx` | Template AVITEC pristine; tidak boleh ditimpa |
| `metadata.json` | Metadata naskah dan identitas penulis |

## Kebutuhan workspace riset

Default toolchain artikel membaca research workspace dari posisi submodule
`v5/article/`. Untuk checkout mandiri, set workspace root secara eksplisit:

```powershell
$env:THESIS_WORKSPACE_ROOT = 'D:\path\to\v5'
```

Build reproducible membutuhkan Python dan, untuk build DOCX/PDF, Word COM pada
Windows. `node_modules/` hanya diperlukan untuk renderer diagram.

## Pipeline build

```powershell
# 1) rasterisasi master SVG figur pada resolusi submission
python scripts/Grapher/rasterize_diagrams.py --scale 9

# 2) build DOCX dari template resmi
python scripts/Builder/build_docx.py

# 3) ekspor PDF melalui Word COM
pwsh -File scripts/Builder/export_pdf.ps1

# 4) finalisasi metadata, pulihkan resolusi figur, dan render QA
python scripts/Builder/finalize_pdf.py

# 5) validasi independen naskah final
python scripts/FinalAudit/verify_final_manuscript.py
```

Audit naskah terkini berada di
`drafts/final-audit/final-report-2026-11-25.md`; provenance bibliografi
terkini berada di `drafts/final-audit/bibliography-provenance-2026-11-26.md`.

## Provenance snapshot

Snapshot awal repo ini berasal dari working tree artikel pada 2026-11-25 dan
mengacu pada workspace riset commit `a1fad918a7fccb6464722ac35723c29800ba7849`.
Snapshot bibliografi aktif sekarang dibuat ulang sebagai filter terverifikasi
dari registri kanonik root commit
`5f2043a426e52ee5af193920bccaafcbb2dc1aab`.

Template AVITEC `article.docx` harus mempertahankan SHA-256 awalnya; file
tersebut adalah artefak pristine, bukan output build.

## Bibliografi kanonik

`data/bib/article-selection.json` adalah manifest eksplisit untuk 42 referensi
artikel dan alasan terpilih/tidaknya terhadap 68 entri registri kanonik. File
`data/bib/cites.bib` adalah hasil filter, bukan sumber kebenaran; provenance
lengkap ada di `data/bib/cites.bib.provenance.json`. Hash SHA-256 untuk artefak
teks turunan dihitung setelah normalisasi EOL ke LF sehingga checkout Windows
dan Unix menghasilkan provenance yang sama. Generator dan audit juga menulis
artefak teks tracked dengan newline LF eksplisit agar status Git tetap bersih.

Untuk checkout sebagai submodule, jalankan dari root workspace:

```powershell
python article/scripts/Literature/build_matrix.py `
  --source-commit 5f2043a426e52ee5af193920bccaafcbb2dc1aab
python article/scripts/Literature/build_bibliography_snapshot.py `
  --source-commit 5f2043a426e52ee5af193920bccaafcbb2dc1aab
python article/scripts/FinalAudit/verify_bibliography_snapshot.py `
  --source-commit 5f2043a426e52ee5af193920bccaafcbb2dc1aab
```

Untuk checkout mandiri, set `THESIS_WORKSPACE_ROOT` lebih dahulu. Gunakan
`--refresh` atau `--refresh-doi <doi>` hanya ketika registry DOI perlu
diperbarui; hasil registry yang sudah terverifikasi digunakan sebagai cache.

## Git

- Branch perubahan tidak pernah langsung diarahkan ke `main`.
- Gunakan Conventional Commits (`type(scope): subject`).
- Raw evidence workspace riset tetap berada di repo `v5`; repo ini menyimpan
  salinan turunan, ledger, dan provenance yang diperlukan untuk audit naskah.
