# Stage 9 — Handoff Report: Original Research Article AVITEC

> **SUPERSEDED (2026-11-18, sesi koreksi orientasi):** angka tidak berubah, tetapi
> interpretasi fase A–C telah dibetulkan mengikuti $S=T_{V8}/T_ZE$. Rujukan akhir:
> `speedup-orientation-audit.md`, `statistical-recomputation-report.md`,
> `manuscript-change-log.md`, dan `final-quality-review.md`. Path ledger kanonik =
> `article/data/csv/evidence-ledger.csv` (bukan `drafts/`).

Tanggal: 2026-11-18 · Naskah: **"On-Demand JSON Parsing in Node.js Servers via WebAssembly: A Multi-Boundary Evaluation"** · Git: HEAD `a1fad91` (PR #79 tetap OPEN, tidak di-merge), seluruh `article/` untracked/dirty terdokumentasi — tidak ada commit/push/merge/PR yang dilakukan.

## A. Deliverable final

| Artefak | Path | Status |
|---|---|---|
| Master naskah (English) | `article/drafts/article-draft.md` (51.518 B) | final, edit di sini |
| Docx siap submit | `article/drafts/article-draft.docx` (2.198.099 B) | final |
| PDF render Word | `article/drafts/article-draft.pdf` (977.175 B, **13 halaman**) | final |
| QA visual halaman | `article/drafts/qa-render/page-01..13.png` | 13/13 diinspeksi |
| Metadata (title/keywords/cites) | `article/metadata.json` | terisi otomatis oleh builder |
| Template resmi | `article/article.docx` (894.262 B) | **PRISTINE — tidak disentuh** |

## B. Definition of Done — 11 butir

| # | Butir | Status | Bukti |
|---|---|---|---|
| 1 | Naskah lengkap Abstract→References (English), 5 fase A–E dijelaskan utuh di Methods/Results | ✅ | prose 5.055 kata (≥5.000), abstrak 221 (≤250); QA builder |
| 2 | Estimand terkunci: θ = rasio median ronde atas 15 ronde berpasangan; paired bootstrap B=10.000, seed 20261117, percentile 95%; BCa = sensitivitas; E = median-of-10 per ronde; A–D = mean-of-reps | ✅ | `article/drafts/paired-bootstrap-estimand-spec.md` |
| 3 | Semua angka traceable ke record/raw exhibit | ✅ | `article/data/csv/evidence-ledger.csv` 63 baris + `article/data/json/evidence-ledger.provenance.json` (126 file SHA-256) |
| 4 | Statistik direkonstruksi independen (bukan salin laporan/PR #79) | ✅ | re-run dari exhibit; koreksi estimand E: dev 1,050 [0,9347–1,1473] & 1,028 [0,9740–1,1143]; server 1,154 [1,0845–1,1751]; pooled lama hanya footnote T7 |
| 5 | Chart & diagram dihasilkan dari data arsip, dicakup Declaration of AI Use | ✅ | 3 chart PNG 1000 dpi (`Charter/main.py`) + 3 diagram SVG/PNG (Edge headless 3×); caption tiap figur memuat keterangan bantuan AI |
| 6 | Template tidak di-overwrite; author hanya dari `metadata.json`; tanpa tanggal/funding karangan | ✅ | builder menyalin template → draft; history = placeholder `[to be assigned by the editorial office]`/`[pending]` |
| 7 | QA numerik builder PASS | ✅ | abstrak 221; 5/5 keywords di abstrak; sitasi [1]–[28] urut kemunculan pertama; 0 pelanggaran posisi-pasca-tanda baca; 28 DOI unik; 6 figur; 8 tabel |
| 8 | PDF + QA visual semua halaman | ✅ | 13/13 halaman PNG diinspeksi (front matter, 3 diagram, 3 chart, 9 tabel docx, 28 referensi, declarations) |
| 9 | Declaration of Generative AI sesuai AI Policy AVITEC | ✅ | bagian SUPP di naskah + ditempatkan di docx |
| 10 | Pemeriksaan plagiarisme | ❌ **belum dijalankan** | tidak tersedia alat/akun Turnitin di lingkungan kerja — **wajib sebelum submit** |
| 11 | Keputusan header masthead (Vol. 9 No. 1 February 2027 pp. 1-20 + DOI contoh `10.28989/avitec.v9i1.3941`) | ⏸ dibiarkan apa adanya | artefak template resmi (bagian editorial) — diserahkan ke pemilik |

Perbaikan terakhir pada build final: blok 7 contoh referensi template di **w:sdt** (content control tak terlihat python-docx) dibersihkan; running head halaman ganjil diisi `Zuhayr: On-Demand JSON Parsing in Node.js Servers via WebAssembly`; baris header tabel data di-set repeat saat tabel terpotong halaman (Tabel 8 hal. 11→12).

## C. Status gate Stage 0–9

| Stage | Isi | Status |
|---|---|---|
| 0 | Source audit (provenance verbatim RQ/H₀, 11 run primary + pilot excluded) | ✅ `drafts/source-audit.md` |
| 1 | Spec estimand | ✅ `drafts/paired-bootstrap-estimand-spec.md` |
| 2 | Evidence ledger + provenance | ✅ `article/data/csv/evidence-ledger.csv` + `article/data/json/evidence-ledger.provenance.json` |
| 3 | Literature matrix (28 INCLUDE, 23 EXCLUDE; Crossref 50/50 OK) | ✅ `drafts/literature-matrix.md` |
| 4 | Outline | ✅ |
| 5 | Figure & table plan | ✅ |
| 6 | Chart + diagram | ✅ `scripts/Charter/`, `scripts/Grapher/diagram/` |
| 7 | Draft markdown | ✅ `drafts/article-draft.md` |
| 8 | Docx + PDF + QA | ✅ `drafts/article-draft.docx/.pdf` |
| 9 | Handoff | ✅ file ini |

## D. Keputusan terbuka untuk pemilik

1. **Persentase referensi jurnal**: requirement AVITEC "≥80% referensi jurnal internasional recent" — terpenuhi 20/28 (71,4%) berlabel jurnal (PVLDB 6 refs dihitung jurnal di matrix). Opsi: (a) tambah 3–4 referensi jurnal, atau (b) serahkan argumentasi ke editor. Non-English refs 0% ✓; ≥15 jurnal di Introduction ✓ (17–19).
2. **Masthead/DOI contoh** di header halaman 1 — dibiarkan (bagian editorial) atau diminta editor mengganti.
3. **Tanggal history kosong** (Submitted/Revised/Accepted placeholder) — OK sampai editorial menugaskan.
4. **Opsional**: patch `scripts/analyze_measurement/nd_d_e_synthesis.py` (point E → round-level; kolom A–C → C′) — hanya dieksekusi dengan instruksi eksplisit.

## E. Larangan klaim (guardrails yang dijaga naskah)

- H₀ tidak diputuskan; interval memuat 1 = "not distinguishable", bukan "equality".
- Memori/CPU/energi **tidak diukur** — disebut eksplisit di Threats to Validity.
- Fase D = gabungan desain store + parser (bukan parser murni); Mongo cache = warm steady-state; cold path unmeasured (future work).
- Angka era Node 24 (2,85×/3,00× dev; 1,30× server) = histori berlabel runtime, tidak dipool ke bukti.
- Scanner = scanner8 default via wasm64; **tanpa** klaim "SIMD-accelerated".
- Tidak ada pooling lintas site/run/estimand; dev phase-E dua run dilaporkan terpisah.

## F. Angka kunci (untuk audit cepat; S = T_V8/T_ZE)

- **A** (full materialization): dev 0,0494/0,0544/0,0428/0,0446/0,0613/0,0445; server 0,0493/0,0669/0,0520/0,0569/0,0576/0,0501
- **B** (partial projection): dev 0,1229/0,1059/0,0755/0,1287/0,1594/0,0987; server 0,1228/0,1130/0,0828/0,1282/0,1436/0,1043
- **C** (selective traversal): dev 0,9223/1,1680/1,0455/1,6454/0,2861/0,0452; server 0,8561/1,4194/0,9562/1,4983/0,3087/0,0469
- **D** (repository): mongo 2,8802 [2,5724–3,0451] dev / 2,6654 [2,5083–2,8573] server; file 0,9526 [0,7673–1,1093] / 0,9871 [0,9705–1,0387]; supporting (core 0.3.1): mongo 2,3989 [1,9596–2,9061], file 0,9495 [0,8698–1,0922]
- **E** (HTTP GET /rekap): dev `8556513` 1,0501 [0,9347–1,1473]; dev re-run `6979e3f` 1,0278 [0,9740–1,1143]; server `530f751` 1,1544 [1,0845–1,1751]

## G. Cara regen (semua dari workspace ini)

```powershell
# 1. Chart (PNG 1000 dpi + SVG) — data dari ledger
$env:PYTHONIOENCODING='utf-8'
python article/scripts/Ledger/export_charter_raw.py   # export data chart
python article/scripts/Charter/main.py               # 3 chart

# 2. Diagram SVG → PNG (Edge headless, 3x scale)
#    ref: fig1-boundaries 1026,449 · fig2-measurement-protocol 576,1022 · fig3-decision-flow 792,860
& 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' --headless=new --disable-gpu `
  --user-data-dir=$env:TEMP\opencode\edge-profile2 --force-device-scale-factor=3 `
  --window-size=<w>,<h> --virtual-time-budget=8000 --screenshot=<out.png> "file:///<svg>"

# 3. Ledger + provenance
python article/scripts/Ledger/build_ledger.py

# 4. Docx (menyalin template -> drafts, fill front/body, QA, update metadata.json)
python article/scripts/Builder/build_docx.py

# 5. PDF via Word COM + QA PNG
$w = New-Object -ComObject Word.Application; $w.Visible=$false
$d = $w.Documents.Open("<abs>\article\drafts\article-draft.docx", $false, $true)
$d.ExportAsFixedFormat("<abs>\article\drafts\article-draft.pdf", 17)
$d.Close($false); $w.Quit()
python -c "import pymupdf,pathlib; out=pathlib.Path(r'article/drafts/qa-render'); doc=pymupdf.open(r'article/drafts/article-draft.pdf'); [doc[i].get_pixmap(dpi=110).save(str(out/f'page-{i+1:02d}.png')) for i in range(len(doc))]"
```

Urutan wajib: edit `article-draft.md` → (opsional ledger/chart) → `build_docx.py` → PDF → QA PNG.

## H. Catatan lingkungan (untuk reproduksi)

- `$env:PYTHONIOENCODING='utf-8'` wajib tiap panggilan python.
- Word COM untuk PDF; pymupdf (pip) untuk render QA PNG.
- Edge headless: pakai `--headless=new` + `Start-Process -Wait` + profile terpisah di temp opencode.
- Word count multi-definisi: prose-only 5.055; prose+supp 5.288; body QA metric 5.756; Word ~7.627 — semua dalam rentang 5.000–8.000 AVITEC "excluding references".
