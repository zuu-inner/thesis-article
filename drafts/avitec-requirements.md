# AVITEC Requirements — Verifikasi Halaman Resmi (2026-11-18)

> Sumber resmi: **AVITEC pindah domain** — domain lama `jurnal.itera.ac.id`
> (NXDOMAIN global, dicek via Cloudflare DoH). Portal aktif:
> `https://ejournals.itda.ac.id/index.php/avitec` — publisher
> **Institut Teknologi Dirgantara Adisutjipto (ITDA)** bekerja sama dengan FORTEI.
> (Jangan pakai catatan lama "ITERA" — sudah tidak akurat.)

## Identitas jurnal

| Butir | Nilai |
|---|---|
| Nama penuh | Aviation Electronics, Information Technology, Telecommunications, Electricals, and Controls (AVITEC) |
| P-ISSN / E-ISSN | 2685-2381 / 2715-2626 |
| Publisher | Dept. Electrical Engineering, ITDA, Yogyakarta |
| Akreditasi | SINTA 3 (id 8193); terindeks DOAJ; EBSCO via DOAJ |
| Review | single-anonymized (double atas permintaan); 2 terbit/tahun (Feb & Aug) |
| Lisensi | CC BY 4.0 |
| APC | IDR 600.000 / USD 40 (waiver tersedia) |
| URL submissions | `/index.php/avitec/about/submissions` |
| URL AI policy | `/index.php/avitec/pages/view/AI_Policy` |

## Author Guidelines (Original Research Article) — verbatim-facts

- **Length**: "Recommended length: 5,000-8,000 words, excluding references."
- **Title**: "must contain no more than 20 words … avoid unexplained abbreviations."
- **Abstract**: "a single paragraph of no more than 250 words, covering the
  research context or problem, objective, methods where relevant, principal
  findings, and scientific contribution." **Keywords**: "3-7 keywords, arranged
  from general concepts toward more specific terms."
- **Introduction**: "must cite at least 15 peer-reviewed journal articles";
  kritik literatur, gap, objective/novelty; prioritas 10 tahun terakhir.
- **References**: ≥15 total; "At least 80% of references must be from recent
  international peer-reviewed journals"; non-English refs ≤25% (+terjemahan
  judul dalam kurung siku); **numbered AVITEC in-text citation system**
  (IEEE-based): `[1]`, `[1,3,5]`, `[2-4]`, `[1,3-5,8]`, `[1,2]`; sitasi
  **sebelum** tanda baca; `Smith et al. [4]`; repeat original number;
  "Use the IEEE-based reference-list format specified in the current AVITEC
  template"; DOI wajib bila ada.
- **Figures/tables**: penomoran berurutan sesuai sitasi pertama; keterangan
  informatif; teks figur min. 8–10 pt; "Prefer vector formats"; raster >500 dpi
  (foto) / >1,000 dpi (line art); tabel editable; caption tabel jangan di
  text box.
- **Equations**: editable, bernomor, simbol/unit didefinisikan di pemakaian pertama.
- **Integrity**: laporan funding/COI; ketersediaan data/kode "where feasible".

## AI Policy (poin yang mengikat naskah ini)

- Penggunaan AI **diizinkan** untuk drafting/analysis/figures/programming,
  dengan **deklarasi**: "identify the tool or service and describe the purpose
  and extent of its use."
- "Where AI is part of the research methodology, authors must also report the
  relevant method, tool or model, inputs, verification, and limitations in the
  Methods section" → deklarasi terpisah dari (bukan pengganti) deskripsi metode.
- "Any AI-generated or AI-assisted figure or illustration must be appropriately
  identified." → caption figur/charter menyebut generasi bantuan AI.
- AI **tidak boleh** jadi author; konsekuensi konten tetap pada penulis.
- Tidak perlu deklarasi negatif bila tidak pakai AI; kasus kita: **perlu
  deklarasi** (agent coding digunakan menyusun naskah & chart; analisis
  statistik direkalkulasi dengan skrip deterministik).

## Template

`article/article.docx` (894.262 B, pristine) = template resmi saat ini yang
dipakai sebagai basis `article-draft.docx` (salinan, template asli tidak
di-overwrite). Isi template mengikuti format IEEE-based di atas.

## Konsekuensi checklist untuk naskah

- [ ] Word count body 5.000–8.000 (tanpa referensi) — target ~6.000.
- [ ] Title ≤20 kata.
- [ ] Abstract 1 paragraf ≤250 kata (target 180–220); 5 keywords (di rentang 3–7,
      muncul di abstract).
- [ ] Introduction ≥15 artikel jurnal peer-reviewed; ≥80% referensi jurnal
      internasional recent; sitasi numbered `[n]` IEEE-based, sebelum tanda baca.
- [ ] Figur: chart matplotlib (raster ≥1.000 dpi line-art class) + diagram
      (SVG/vector); caption informatif; identifikasi bantuan AI pada figur.
- [ ] Declaration of AI Use: tool (agent coding harness + model), tujuan,
      cakupan (drafting, chart generation, analisis rekalkulasi skripted),
      verifikasi manusia.
- [ ] Funding/COI: tanpa funding eksternal — dinyatakan apa adanya (tidak
      mengarang).
- [ ] Data/code availability: repo publik `zuudevs/ze_json`, `zuudevs/thesis`
      (record + exhibits), korpus manifest sha256.
