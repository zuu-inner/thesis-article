# Laporan Akhir Finalisasi Naskah AVITEC — 25 November 2026

Naskah: **“On-Demand JSON Parsing in Node.js Servers via WebAssembly: A Multi-Boundary Evaluation”**
Target jurnal: AVITEC (ejournals.itda.ac.id/index.php/avitec) · Tip: Original Research Article
Tanggal audit: 2026-11-25 · Akses web: 2026-11-25 (kecuali bila disebut lain)

## 0. Ringkasan Eksekutif

| Item | Nilai |
|---|---|
| Referensi dalam daftar | **42** (41 DOI + 1 tanpa DOI) |
| Klasifikasi bukti | **34 Qualified · 1 Uncertain · 7 Not Qualified** |
| Rasio jurnal terkonfirmasi | **34/42 = 80,95 %** (batas atas 35/42 = 83,33 %) → ambang ≥80 % **terpenuhi** |
| Artikel jurnal peer-reviewed di Introduction | **35** (34 terkonfirmasi) → ambang ≥15 **terpenuhi** |
| Naskah build | `article/drafts/article-draft.docx` (3.592.419 B) + PDF 16 halaman (3.877.162 B) |
| Template AVITEC | `article/article.docx` 894.262 B, SHA-256 `9d540bd02c2eea55` — **utuh, tidak ditimpa** |
| Resolusi figur | DOCX & PDF **1.131–1.514 dpi** (semua 6 figur ≥1.000 dpi) + master SVG vektor |
| Eksperimen/angka | Tidak ada yang diubah; estimand, tabel, dan graf tetap |
| Git | Tidak ada commit, push, branch switch, reset, atau clean |
| Status Overall | **PASS dengan 2 Not Verified** ([27] peer review individual; tanggal editorial) |

Riwayat audit sebelumnya (`reference-eligibility-audit.md`, `article/analysis/content-consistency-audit.md`) **dipertahankan** sebagai catatan historis; laporan ini adalah status terkini yang menggantikan gate “LITERATURE BLOCKER” pada audit 28 referensi.

---

## A. Status Repository dan Working Tree

| Butir | Nilai |
|---|---|
| Branch | `research/nd11-phase-d-e-synthesis` |
| HEAD | `a1fad918a7fccb6464722ac35723c29800ba7849` |
| Entri dirty (total) | **34** — tidak berubah dari sebelum finalisasi karena seluruh artefak baru berada di dalam `article/` (untracked) |
| `article/` | seluruh pohon artikel **untracked** (belum di-track Git) |
| `assets/bib/cites.bib` | **dirty bawaan** (mtime 11:19, sebelum finalisasi ini); tidak disentuh pada pass ini; kerusakan key/DOI yang sudah ditandai audit sebelumnya masih ada dan sengaja tidak diperbaiki karena di luar cakupan tugas |
| Dirty lain (bawaan) | `.gitmodules`, `scripts/analyze_measurement/nd_d_e_synthesis.py`, `scripts/grapher/make-graph.ts`, submodule `saq-report`/`submission-thesis-supervisor`, penghapusan `thesis-proposal/` dan `utils/typ/*`, `reports/charts/*.csv` (untracked), `scripts/analyze_measurement/tests/` (untracked) |

Tidak ada perubahan yang dilakukan pada file di luar `article/`.

---

## B. Audit Bibliografi — 42 Referensi

### B.1 Sumber dan verifikasi metadata

- Sumber kebenaran bibliografi: **`article/data/bib/cites.bib`** — **tepat 42 entri**, 41 DOI unik + 1 entri tanpa DOI (`SchulzKumpel2025Constructing`, DMLR).
- Crossref: **41/41 DOI resolve** sebagai `journal-article` (34), `proceedings-article` (6), atau `report` (1 = RFC 8259). Tidak ada DOI duplikat. Metadata volume/issue/pages/year dikonfirmasi per DOI.
- Entri tanpa DOI: Schulz-Kümpel et al. (DMLR vol. 2, paper 6:1–73, 2025) — dikonfirmasi pada situs resmi `data.mlr.press` (JMLR family, rigorous review, 3 reviewer/submission) dan OpenReview; Crossref tidak memiliki record jurnal DMLR, sehingga DOI memang belum ditetapkan (ISSN juga masih *pending*).
- Kesimpulan: daftar referensi pada naskah (=42) dan `article/data/bib/cites.bib` (=42) **1:1 pada DOI/URL**, tanpa DOI yatim. Satu-satunya perbedaan adalah kapitalisasi satu DOI (`10.1109/ACCESS.2026.3732375` di naskah vs `10.1109/access.2026.3732375` di bib) — DOI bersifat case-insensitive (DOI Handbook 1.4) dan keduanya resolve ke objek yang sama.

### B.2 Koreksi metadata yang diterapkan

| Ref | Nilai lama | Nilai terverifikasi | Sumber verifikasi |
|---|---|---|---|
| [16] | `F. Frăsincar` | `F. Frasincar` | SpringerLink article page (author: *Flavius Frasincar*) |
| [28] | early view, pp. 1–12 | vol. 56, no. 12, pp. 1498–1509, 2026 | Crossref `10.1002/spe.70105` + PDF penerbit |
| [29] | early view | vol. 24, no. 1, pp. 1–23, 2026 | Crossref `10.1145/3859286` |
| [18],[20],[30],[33],[34],[35] | nomor artikel karangan (mis. `art. no. 46`) | rentang halaman Crossref (`pp. 1–46`, `1–25`, `1–22`, `1–47`, `1–21`, `1–30`) | Crossref (tidak ada nomor artikel pada record ACM) |
| [2] | “On demand JSON…” | “On-demand JSON…” | judul resmi Wiley/Crossref |
| [12] | `year = {2024}` pada bib | `year = {2023}` pada bib | Crossref + `series = {ASPLOS '23}` (naskah sudah 2023) |

Nomor artikel *art. no.* Elsevier/JGC/WWW/MDPI (`101478`, `102537`, `101686`, `34`, `28`, `341`) **dipertahankan** karena memang supplied publisher. Nomor artikel karangan ACM **dihapus** karena tidak dapat diverifikasi.

### B.3 Klasifikasi (Qualified / Uncertain / Not Qualified)

Matriks lengkap 42 baris (dengan bukti per baris): **`article/drafts/final-audit/reference-eligibility-42.csv`**

| Status | Jumlah | Rincian |
|---|---:|---|
| Qualified | **34** | 34 artikel jurnal: SPE (8), PVLDB (7), ACM TOS/TACO/TOSEM/PACMPL/PACMMOD (7), Information Systems (3), Springer (VLDB J., WWW, JGC, EMSE, FCS = 5), IEEE (Access, CAL = 2), MDPI Future Internet (1), DMLR (1) |
| Uncertain | **1** | **[27]** Mula & Lemire, “Base64 encoding and decoding…”, SPE 50(2):89–97 (2020) — artikel *Short Communication*; PDF penerbit tidak memuat baris Received/Revised/Accepted sehingga review individual tidak terbukti. **Tidak dihitung di numerator** |
| Not Qualified | **7** | [1] RFC 8259 (standar, bukan jurnal) + 6 paper conference proceedings: [6],[7],[10],[12],[32],[38] |

### B.4 Bukti tingkat jurnal/penerbit yang dipakai (akses 2026-11-25)

| Publisher/serial | Bukti yang diperoleh | Status |
|---|---|---|
| Wiley SPE (9 artikel) | Snapshot resmi `web.archive.org/web/20250530060619/onlinelibrary.wiley.com/journal/1097024x`: aims/scope, editors dari 5 negara, CiteScore 8 / IF 2,6, acceptance 12 % + **PDF penerbit** berisi riwayat review untuk 8 dari 9 artikel | 8 Qualified, 1 Uncertain |
| PVLDB (7) | `vldb.org/pvldb`: “*PVLDB is a scholarly journal … with a journal-style reviewing and quality-assurance process*” | Qualified |
| ACM (7) | `acm.org/publications/journals`: journals peer-reviewed, COPE; prinsip PACM (≥3 reviewer dengan review tertulis, ≥2 siklus revisi) | Qualified |
| Springer Nature (5) | `link.springer.com/brands/springer/journal-policies` (bagian *Peer review*), penerbit global 2.700+ jurnal | Qualified |
| Elsevier Information Systems (3) | Snapshot *Guide for Authors* `web.archive.org/web/20240422095307/…`: “*single anonymized review process … minimum of two independent expert reviewers*” | Qualified |
| MDPI Future Internet (1) | Record DOAJ ISSN 1999-5903: “*Single anonymous peer review*”, publisher MDPI AG (CH), URL editorial board + aims/scope | Qualified |
| IEEE Access (1) | `ieeeaccess.ieee.org`: jurnal peer-reviewed multimidisiplin, “*rapid peer review*”, “*Stages of Peer Review*”, “*Recognized globally*” | Qualified |
| IEEE Computer Architecture Letters (1) | `computer.org/csdl-pub-home-cal` (live): statement EIC “*Manuscripts submitted to CAL undergo a rigorous peer-review, driven by an editorial board of world-class experts*”; “*Since 2002 … has published peer-reviewed papers*”; “530+ Peer Reviewed Papers Published”; menu Peer Review | Qualified |
| DMLR (1) | `data.mlr.press`: DMLR = anggota keluarga JMLR, “*rigorous review process*”, 3 reviewer per submission, rebuttal/revisi, EIC lintas negara | Qualified (tanpa DOI, ISSN pending) |

Tidak ada klaim yang dinaikkan tanpa bukti yang bisa diakses; halaman yang terblokir (Wiley live, MDPI live, IEEE Xplore, SCImago) dicatat sebagai **fail akses**, bukan sebagai bukti.

### B.5 Catatan penting untuk editor

- Margin ambang 80 % hanya **0,95 poin persentase** pada hitungan konservatif (34/42). Jika editorial office menghitung [27] (Short Communication SPE) sebagai peer-reviewed, rasionya 83,33 %. Bila editor skeptis terhadap [42] (DMLR tanpa DOI/ISSN), rasionya turun ke 78,57 % — **satu referensi jurnal yang ditolak akan menggagalkan ambang**.
- Rekomendasi aman: ganti [1] RFC 8259 (standar) atau [38] SC 2015 (conference, 2015) dengan satu artikel jurnal 2019+ yang relevan bila margin tipis dianggap berisiko.

### B.6 Penyelesaian blocker [41] (IEEE Computer Architecture Letters)

Blocker terakhir pada audit sebelumnya (evidence peer review CAL tidak dapat diakses) **ditutup** pada 2026-11-25 lewat halaman resmi IEEE Computer Society yang dirender JS (`https://www.computer.org/csdl-pub-home-cal`; path lama `csdl/magazine/cal` kini 404):

| Bukti | Isi kutipan |
|---|---|
| Statement Editor-in-Chief (Sudhanva Gurumurthi) | “*Manuscripts submitted to CAL undergo a rigorous peer-review, driven by an editorial board of world-class experts, and with a fast turnaround time.*” |
| Deskripsi resmi publikasi | “*Since 2002, IEEE Computer Architecture Letters has published peer-reviewed papers with high impact on all areas of uni- and multiprocessor computer systems, computer architecture, microarchitecture, and workload characterization.*” |
| Metrik pada halaman | “530+ Peer Reviewed Papers Published”, Impact Factor 2.0, Established 2002 |
| Menu Peer Review | Reviewer Resources · Editor Resources · Guest Editor Resources · Editor-in-Chief Resources + pengumuman “CAL Thanks 2025 Reviewers” |
| Indeks resmi | CSDL RSS `periodicals/letters/ca` menautkan artikel ke `csdl/journal/ca/...` dengan prefix DOI `doi.ieeecomputersociety.org/10.1109/LCA.2026.*` |

Efeknya: **[41] naik dari “belum terverifikasi” → Qualified**. Klasifikasi agregat tetap **34 Qualified · 1 Uncertain · 7 Not Qualified** (posisi [41] memang sudah Qualified secara implisit karena Crossref menandainya `journal-article`; kini buktinya eksplisit).

---

## C. Perubahan pada Naskah dan pada Pipeline Build

Semua perubahan dibatasi pada naskah, bibliografi, dan perkakas build artikel; **tidak ada angka hasil, estimand, tabel data, atau graf yang diubah**.

| # | Perubahan | Lokasi | Alasan |
|---|---|---|---|
| C1 | Paragraf baru: formal/query/storage (JSON algebra, SJSON, CORES, instance-aware rewriting, dsJSON) | Introduction ¶4 | Mengintegrasikan 9 referensi baru secara substantif (bukan padding) |
| C2 | Paragraf baru: biaya transisi/data-exchange/streaming pada boundary JS↔Wasm | Introduction ¶5 | Dasar untuk Discussion ¶ “delivery mechanism” ([35],[36],[37]) |
| C3 | Paragraf benchmarking/statistik: order effect, resampling, BCa, coverage | Introduction ¶6 + Methods (Protocol, Inference) | Menopang klaim metodologis yang sudah ada ([38]–[42]) |
| C4 | Penyebutan “Table 7” pada Methods diganti “the phase-E results table” | Methods ¶ Statistical Inference | AVITEC: penomoran tabel mengikuti sitasi pertama; sebelumnya urutan pertama = 1,2,7,3,… → kini 1…8 |
| C5 | “1.15x” → “1.15×” | Discussion ¶ endpoint | Konsistensi simbol perkalian |
| C6 | Penomoran ulang seluruh sitasi + rebuild daftar referensi (42) | Seluruh naskah | Urutan berdasarkan kemunculan pertama 1…42 |
| C7 | `year` ASPLOS '23 dan metadata SPE 70105 dikoreksi | `article/data/bib/cites.bib` | Sinkronisasi bib dengan metadata resmi |
| C8 | Figur 1–3 di-raster ulang pada 9× dari master SVG yang sama | `article/scripts/Grapher/diagram/fig*.png` | Menutup AVITEC D11 (line art >1.000 dpi): 505/451/390 dpi → **1.514/1.353/1.169 dpi**. Master SVG (vektor) tidak berubah; gambar byte-identik dengan artefak terverifikasi pada skala 3× (sha `1363e54b…`, `12f570f1…`, `81c6a8ef…`), sehingga konten visual tidak bergeser |
| C9 | Perkakas build/QA baru & perbaikan | `article/scripts/Grapher/rasterize_diagrams.py`, `article/scripts/FinalAudit/verify_final_manuscript.py`, `article/scripts/Builder/build_docx.py`, `article/scripts/Builder/finalize_pdf.py` | Rasterisasi figur dapat direproduksi; validasi independen 19 check; Word berhenti mengompres gambar saat build; PDF mengembalikan figur ke resolusi sumber |

Kalimat yang sudah ada dan dipertahankan (terverifikasi ulang): klaim “Node.js mengadopsi on-demand” [2] — didukung abstract/pendahuluan Keiser & Lemire (“*Several systems use On Demand: … the Node.js JavaScript runtime …*”); klaim “primitives terintegrasi di V8/Node.js” [21]–[29] — didukung PDF penerbit (mis. spe.3296 “*The Node.js environment adopted our C++ library*”, spe.70105 “*Our software is part of the Google JavaScript engine (V8)*”, spe.3261 “*part of the popular Node.js JavaScript runtime*”).

Tidak ada referensi lama yang dibuang; 26 dari 28 referensi sebelumnya dipertahankan, Yan et al. (DOI `10.1145/3487552.3487827`) dan Seidler et al. digantikan oleh Liu et al. (`10.1145/3712197`, TOSEM 2025) dan Kjorveziroski & Filiposka (`10.1007/s10723-023-09669-8`, J. Grid Computing 2023) sesuai keputusan audit sebelumnya.

---

## D. Checklist Kepatuhan AVITEC

Ambang diambil dari `article/drafts/avitec-requirements.md` (halaman Author Guidelines resmi, diverifikasi 2026-11-18).

| # | Persyaratan AVITEC | Ambang | Terukur | Status | Bukti |
|---|---|---|---|---|---|
| D1 | Panjang naskah tanpa referensi | 5.000–8.000 kata | 6.950 kata (hitungan inklusif: prosa + tabel + caption + suplemen); 6.513 kata (semantik QA build); 5.796 kata prosa | **Pass** | `verify_final_manuscript.py` + QA `build_docx.py` |
| D2 | Judul | ≤20 kata | 11 kata | **Pass** | `%%TITLE:` |
| D3 | Abstrak satu paragraf | ≤250 kata | 244 kata, 1 paragraf | **Pass** | QA build + PDF p.1 |
| D4 | Kata kunci | 3–7 | 5 (4 muncul verbatim di abstrak) | **Pass** | QA build |
| D5 | Introduction mengutip ≥15 artikel jurnal peer-reviewed | ≥15 | 35 artikel jurnal (34 terkonfirmasi; 1 Uncertain) | **Pass** | hitungan sitasi independen |
| D6 | ≥80 % referensi dari jurnal internasional peer-reviewed terkini | ≥80 % | 34/42 = **80,95 %** konservatif; 35/42 = 83,33 % bila [27] dihitung | **Pass** (margin tipis) | `reference-eligibility-42.csv` |
| D7 | Referensi non-Inggris | ≤25 % | 0/42 = 0 % | **Pass** | semua judul berbahasa Inggris |
| D8 | Sitasi numbered gaya IEEE, sebelum tanda baca, nomor asli diulang | 0 pelanggaran | 66 sebutan, 42 unik, 0 sitasi setelah tanda baca, urutan kemunculan pertama = 1…42 | **Pass** | QA build + validasi independen |
| D9 | DOI bila tersedia | semua yang punya DOI | 41/42; [42] memang tanpa DOI (diverifikasi) | **Pass** | Crossref + data.mlr.press |
| D10 | Penomoran figur/tabel sesuai sitasi pertama | berurutan | Figur 1–6 berurutan; Tabel 1–8 berurutan (setelah C4) | **Pass** | skrip urutan + PDF p.4–12 |
| D11 | Resolusi raster line-art >1.000 dpi (vektor lebih disukai) | ≥1.000 dpi | DOCX: 1.514 / 1.353 / 1.169 / 1.195 / 1.131 / 1.131 dpi (Figur 1–6); PDF: identik setelah pemulihan resolusi; master SVG tersedia (vektor) | **Pass** | pengukuran piksel vs ukuran tampil di DOCX dan PDF |
| D12 | Deklarasi penggunaan AI (tool, tujuan, cakupan, verifikasi) | ada | “Declaration of Generative AI and AI-assisted Technologies” + penanda AI pada caption tiap figur | **Pass** | PDF p.14 |
| D13 | Funding / COI / ketersediaan data & kode | ada | ketiganya ada (tanpa funding eksternal, tanpa konflik kepentingan, repo + manifest sha256) | **Pass** | PDF p.14 |
| D14 | Urutan penomoran rujukan | IEEE-based | 42 entri, format konsisten | **Pass** | PDF p.15–16 |
| D15 | Peer review artikel [27] (SPE Short Communication) | bukti individual | tidak ada baris review di PDF penerbit | **Not Verified** | tidak masuk numerator; ambang tetap terpenuhi |
| D16 | Tanggal editorial (Submitted/Revised/Accepted) | diisi redaksi | masih placeholder “to be assigned by the editorial office” | **Not Verified** | keputusan editorial; dibiarkan sesuai audit sebelumnya |

Catatan D11: Word secara default menulis ulang gambar saat ekspor PDF pada “default resolution” (~200 ppi). Karena itu `build_docx.py` kini menyetel `w:doNotAutoCompressPictures` dan `finalize_pdf.py` mengembalikan binari figur sumber ke dalam PDF (pencocokan berdasarkan ukuran tampil **dan** rasio aspek, lalu penyimpanan ulang dengan `garbage=4, deflate=True`). Hasil akhir: PDF 3.877.162 B dengan keenam figur pada resolusi sumber.

---

## E. Build dan Validasi

### E.1 Pipeline build (sistem build aktual proyek)

```
# 1) rasterisasi master SVG figur 1-3 pada 9x (dapat direproduksi)
python article/scripts/Grapher/rasterize_diagrams.py --scale 9
→ fig1-boundaries.png 9234x4041 (sha 90a5e5d5…), fig2-measurement-protocol.png 5184x9198 (a5208a9b…),
  fig3-decision-flow.png 7128x7740 (2e1f7ee6…)

# 2) build DOCX dari template resmi
python article/scripts/Builder/build_docx.py
→ saved: article/drafts/article-draft.docx (3.592.419 B, template intact: 894.262 B)

# 3) ekspor PDF (Word COM)
pwsh -File article/scripts/Builder/export_pdf.ps1  →  article/drafts/article-draft.pdf

# 4) finalisasi PDF: metadata + pemulihan resolusi figur + render QA
python article/scripts/Builder/finalize_pdf.py
→ 16 halaman dirender ke article/drafts/qa-render/page-01…16.png
```

QA build: abstract 244 kata · keywords 5 · body 6.513 · prose 5.796 · supp 232 · `citation_first_order_ok: true` · `citations_unique: [1…42]` · `citations_after_punctuation: 0` · `doi_count/unique: 41/41` · figures 6 · tables 8.
`article/metadata.json` diperbarui otomatis (judul, 5 keyword, 41 DOI pada `document.cites`; entri tanpa DOI tidak dapat dimasukkan).

### E.2 Validasi independen (19/19 PASS)

`python article/scripts/FinalAudit/verify_final_manuscript.py` → `article/drafts/final-audit/validation-2026-11-25.json`

Judul ≤20 kata · abstrak 1 paragraf ≤250 kata · 3–7 keyword · panjang body 5.000–8.000 · 42 referensi bernomor kontigu · seluruh 42 direferensikan · urutan kemunculan pertama 1…42 · 0 sitasi setelah tanda baca · tanpa DOI duplikat · set DOI naskah = set DOI bib (case-insensitive) · urutan figur 1–6 · urutan tabel 1–8 · 42 paragraf referensi di DOCX · 9 tabel di DOCX · 6 gambar di DOCX · **semua gambar ≥1.000 dpi** · PDF memuat [1]–[42] · PDF memuat Figure 1–6 dan Table 1–8 · deklarasi AI ada di PDF.

### E.3 Ekspor PDF dan pemeriksaan visual

PDF: **16 halaman**, metadata (title/author/subject/keywords) terisi, seluruh bagian dan caption ada (MATERIALS AND METHODS, RESULTS AND DISCUSSION, CONCLUSION, REFERENCE, Declaration of Generative AI, Conflict of Interest, Figure 1–6, Table 1–8).
Halaman 1, 4, 5, 7, 12 diperiksa ulang setelah re-rasterisasi dan pemulihan resolusi: judul+abstrak+info artikel, Figur 1–3, dan Figur 6 + Tabel 7 tampil utuh, tanpa teks terpotong, tabel meluber, atau artefak gambar.

### E.4 Perkakas QA yang usang (tidak dipakai sebagai gate)

| Perkakas | Status | Catatan |
|---|---|---|
| `article/scripts/Builder/verify_docx.py` | 13/14 PASS | Satu check gagal karena **ekspektasi usang**: skrip mencari literal “16–23”, sedangkan naskah (benar) berbunyi “15–23×” yang diturunkan dari S = 0,0428–0,0669 (1/S = 23,4…15,0). Tidak ada perubahan naskah yang dibuat untuk memenuhi check usang tersebut; nilai 15–23 sudah konsisten di abstrak, Results, Discussion, dan Conclusion. |
| `article/scripts/FinalAudit/verify_final_pdf.py` | Tidak dipakai | Ekspektasi lama: 28 referensi dan 14 halaman; naskah final 42 referensi / 16 halaman. |

---

## F. Git State, Risiko, dan Langkah Berikutnya

### F.1 Git

Branch `research/nd11-phase-d-e-synthesis`, HEAD `a1fad918a7fccb6464722ac35723c29800ba7849`, **34 entri dirty**. **Tidak ada commit, push, stash, checkout, reset, atau clean**; tidak ada branch baru. Semua perubahan berada di dalam `article/` (untracked) sehingga belum pernah masuk riwayat Git.

### F.2 Artefak yang berubah pada pass ini

| Artefak | SHA-256 (16) | Ukuran |
|---|---|---|
| `article/drafts/article-draft.md` | `17676793cd5ee1e6` | 59.967 B |
| `article/drafts/article-draft.docx` | `e9073ec5970bce6a` | 3.592.419 B |
| `article/drafts/article-draft.pdf` | `63c61449d1674104` | 3.877.162 B |
| `article/data/bib/cites.bib` | `79c842684b8e5419` | 68.881 B |
| `article/drafts/final-audit/reference-eligibility-42.csv` | `dc6ff93e4d6788a7` | 10.442 B |
| `article/drafts/final-audit/validation-2026-11-25.json` | `c08c191066d6e6c1` | 4.720 B |
| `article/scripts/Grapher/diagram/fig1-boundaries.png` | `90a5e5d5dab875df` | 609.433 B |
| `article/scripts/Grapher/diagram/fig2-measurement-protocol.png` | `a5208a9bacd19b13` | 853.883 B |
| `article/scripts/Grapher/diagram/fig3-decision-flow.png` | `2e1f7ee697bd9bcb` | 825.729 B |
| `article/article.docx` (template) | `9d540bd02c2eea55` | 894.262 B (utuh) |

Perkakas baru: `article/scripts/Grapher/rasterize_diagrams.py` (rasterisasi figur, deterministik), `article/scripts/FinalAudit/verify_final_manuscript.py` (validasi independen 19 check), `article/scripts/Builder/export_pdf.ps1` (ekspor PDF Word COM), plus QA render 16 halaman di `article/drafts/qa-render/`.

### F.3 Risiko tersisa

1. **Margin ambang 80 % hanya 0,95 pp** pada hitungan konservatif — satu referensi jurnal yang ditolak oleh editor akan menggagalkan D6 (lihat rekomendasi B.5).
2. **[27] Uncertain** — tidak ada bukti review individual; bila editor menghitungnya, D6 menguat; bila tidak, D6 tetap lolos.
3. **[42] DMLR tanpa DOI dan ISSN pending** — D9 tetap Pass (DOI memang belum ada), namun D6 bergantung pada pengakuan DMLR sebagai jurnal peer-reviewed internasional.
4. **Ukuran naskah** bertambah dari 2,2 MB menjadi 3,6 MB (DOCX) dan 3,9 MB (PDF) karena resolusi figur yang tinggi; masih wajar, tetapi bila portal impose batas upload, PDF 3,9 MB aman sementara SVG master bisa disertakan sebagai lampiran vektor.
5. **Tanggal editorial** (D16) masih placeholder — menunggu keputusan redaksi.
6. `assets/bib/cites.bib` tetap dirty dengan kerusakan key/DOI yang sudah dilaporkan; file ini bukan bibliografi naskah dan tidak diubah pada pass ini.

### F.4 Langkah berikutnya yang disarankan

1. Kirim master SVG (`article/assets/images/fig1-3*.mmd.svg`) bersama DOCX bila editor meminta format vektor.
2. Putuskan [27]: konfirmasi peer review Short Communication dari Wiley, atau ganti dengan artikel jurnal lain yang terbukti.
3. Bila editor memang menuntut margin lebih lebar, ganti [1]/[38] dengan satu jurnal 2019+ yang relevan.
4. Isi tanggal editorial setelah acceptance/assignment redaksi.
5. Commit + PR (branch baru, Conventional Commits) bila pemilik repo mengizinkan; `article/` masih untracked dan perlu ditambahkan secara eksplisit.

---

### Lampiran — Sumber web yang diakses (2026-11-25)

- AVITEC Author Guidelines: `https://ejournals.itda.ac.id/index.php/avitec/about/submissions` (diakses 2026-11-18, dipakai sebagai sumber ambang; tidak diubah).
- Crossref API per DOI (41 DOI).
- Wiley SPE snapshot: `http://web.archive.org/web/20250530060619/https://onlinelibrary.wiley.com/journal/1097024x`
- Elsevier *Guide for Authors* snapshot: `http://web.archive.org/web/20240422095307/https://www.sciencedirect.com/journal/information-systems/publish/guide-for-authors`
- PVLDB: `https://vldb.org/pvldb/`
- ACM Journals: `https://www.acm.org/publications/journals`
- Springer Nature journal policies: `https://link.springer.com/brands/springer/journal-policies`
- SpringerLink article pages: `10.1007/s11280-025-01336-0`, `10.1007/s10723-023-09669-8`
- MDPI Future Internet via DOAJ: `https://doaj.org/api/search/journals/issn:1999-5903`
- IEEE Access: `https://ieeeaccess.ieee.org/`
- IEEE Computer Architecture Letters (live, peer-review statement): `https://www.computer.org/csdl-pub-home-cal`
- IEEE Computer Architecture Letters (arsip): `http://web.archive.org/web/20220929200205/https://www.computer.org/csdl-pub-home-cal`
- IEEE CSDL RSS CAL (DOI prefix `doi.ieeecomputersociety.org/10.1109/LCA.2026.*`): `https://www.computer.org/csdl/api/rss/periodicals/letters/ca/rss.xml`
- DMLR: `https://data.mlr.press/` dan `https://openreview.net/forum?id=x7kCj9OU2c`
- Akses gagal (dicatat, bukan bukti): Wiley live (403/CAPTCHA), MDPI live (403), IEEE Xplore (403), SCImago (403), OpenReview UI (browser check).
