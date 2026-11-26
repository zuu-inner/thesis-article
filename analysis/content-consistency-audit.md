# Audit Konsistensi Isi dan Revisi Substansi — Artikel AVITEC

Tanggal: 2026-11-20 · Repository `zuudevs/thesis`, branch `research/nd11-phase-d-e-synthesis`, HEAD `a1fad918a7fccb6464722ac35723c29800ba7849`.

## 1. Target output dan sumber kerja

Target output mengikuti keputusan pemilik proyek: draft isi di `article/drafts/`, analisis tertulis di `article/analysis/`, output lain di `article/data/<ekstensi>`, diagram Mermaid di `article/data/mmd/`, gambar di `article/assets/images/`, tools di `article/scripts/`, informasi penulis di `article/metadata.json`, dan templat DOCX disalin dari `data/template_article_avitec.docx` ke `article/drafts/`.

Inventarisasi artefak menunjukkan pasangan manuskrip paling mutakhir bukan PDF pukul 04:59 UTC yang disebut pemilik, melainkan:

| Artefak | Path | Ukuran | Hash SHA-256 (16) | Alasan pemilihan |
|---|---|---:|---|---|
| Markdown | `out/article-audit/working/article/drafts/article-draft-supervision-final.md` | 54.300 B | `34d460c2…` | Disebut eksplisit oleh audit literatur terbaru (`supervision-final-audit-note.md`, 12:51 waktu lokal ≈ 05:51 UTC); berisi seluruh keputusan sitasi terkunci |
| DOCX | `out/article-audit/working/article/drafts/article-draft-supervision-final.docx` | 2.226.046 B | `e3104ee9…` | Pasangan Markdown di atas; dipakai sebagai sumber gambar terverifikasi |

Catatan: pemilik menyebut `supervision-final-audit-note(1).md`; file yang sebenarnya ada di repository adalah `article/drafts/final-audit/supervision-final-audit-note.md` (tanpa `(1)`). Tidak ada file `(1)` lain ditemukan; audit yang dibaca adalah file aktual tersebut, yang isinya sesuai ringkasan 20/1/7.

Templat `data/template_article_avitec.docx` dan `article/article.docx` **identik** (hash `9D540BD02C2EEA55D04B…`), sehingga tidak ada konflik sumber templat.

## 2. Audit estimand dan interpretasi hasil — temuan utama

### 2.1 Definisi dan implementasi

Definisi terkunci: $S = T_{V8}/T_{ZE}$, dengan estimand primer $\hat\theta = \operatorname{median}_i(T_{V8,i})/\operatorname{median}_i(T_{ZE,i})$ atas 15 ronde berpasangan (ratio of across-round medians, bukan median dari rasio per-ronde). Konsekuensi matematis: $S<1$ → V8 lebih cepat; $S>1$ → ZE lebih cepat; CI memuat 1 → tidak dapat dibedakan.

Verifikasi terhadap kode dan evidence:

- `scripts/analyze_measurement/nd_d_e_synthesis.py` L225–240 (`bootstrap_median_ratio_ci`) menghitung `np.median(a[idx])/np.median(z[idx])` dengan `a = v8`, `z = ze`; L34–37 mendefinisikan headline speedup sebagai ratio of medians dan memisahkan `speedup_pooled_requests` yang bersifat deskriptif.
- `article/drafts/speedup-orientation-audit.md` (18 Nov) memverifikasi **63 sel** terhadap exhibit mentah: 63 MATCH. Field mapping A–E, satuan ms, pasangan indeks ronde, dan bootstrap joint-resample (seed `20261117`, B = 10.000) sesuai definisi.
- Figure 3 Mermaid (`article/data/mmd/fig3-decision-flow.mmd`) sudah benar (above 1 → on-demand faster).

### 2.2 Status naskah terbaru

Pemeriksaan menyeluruh terhadap 11 lokasi yang disebut pemilik (Methods, rumus skrip, tabel, caption, narasi tiap phase, CI, perbandingan site, abstrak, Discussion, Conclusion, serta pernyataan kontribusi/implikasi) menunjukkan **naskah `article-draft-supervision-final.md` sudah memakai interpretasi yang benar**, misalnya:

- Baris 86: "Values above 1 … favor the on-demand path; values below 1 … favor the V8 baseline."
- Baris 92: CI entirely above 1 → on-demand advantage; entirely below 1 → V8 advantage.
- Baris 106: Phase A $S=0{,}04$–$0{,}07$ dinyatakan sebagai **V8 15–23× lebih cepat**.
- Baris 108 (caption Figure 4): "Bars below the dashed 1.0 line favor the V8 baseline."
- Baris 112–114: Phase C sebagai crossover region dengan arah per payload yang benar.
- Baris 174, 186, 202, 204: Discussion dan Conclusion konsisten.

**Kesimpulan:** ketidaksesuaian yang disebut pemilik ada pada PDF lama pukul 04:59 UTC (`article/drafts/article-draft.pdf`, 19 Nov 09:19 lokal), bukan pada pasangan sumber terbaru. Koreksi orientasi sudah diterapkan pada 19 Nov dan tercatat di `speedup-orientation-audit.md` serta `manuscript-change-log.md`. Tidak ada angka yang diubah atau ditransformasi resiprokal dalam task ini.

### 2.3 Dua isi yang masih perlu diperbaiki

| ID | Lokasi | Masalah | Bukti | Tindakan |
|---|---|---|---|---|
| CR-01 | Results > Phase D | Pengulangan frasa biaya first-build dalam satu paragraf ("the cost of building the canonical cache the first time lies outside the measurement window" dan "the cost of the first build lies outside the measurement window") | Teks naskah baris 149 | Hapus duplikasi; pertahankan satu pernyataan warm-cache + cold-path sebagai future work |
| CR-02 | Discussion > endpoint | "a 15% endpoint gain" tidak mengikuti estimand; $S=1{,}1544$ → penurunan latensi $\approx 1-1/1{,}1544=13{,}4\%$ | Methods baris 86; Table 7 `1.1544 [1.0845, 1.1751]` | Ubah menjadi "a 1.15x endpoint speedup (about 13% lower latency)" |

Kedua perubahan tercatat di `article/data/csv/content-revision-ledger.csv` dan diterapkan di `article/drafts/article-draft-content-review.md`.

## 3. Audit metodologi dan batas pengukuran

| Aspek | Status | Bukti di naskah/evidence |
|---|---|---|
| 15 paired rounds, 3 warmup, rotasi urutan | PASS | Methods baris 76 |
| Estimand ratio of medians + paired bootstrap B=10.000 seed 20261117 + BCa | PASS | Baris 86–90; skrip L225–268 |
| Phase A full parse / B projection / C traversal | PASS | Baris 104–142; Tabel 3–5 |
| Phase D repository design, warmed Mongo vs file store | PASS | Baris 143–154; Tabel 6; negatif file-store dipertahankan |
| Phase D bukan klaim cold-start | PASS | Baris 149 setelah CR-01 |
| Phase E endpoint terpisah dari in-process; parity gate 300 body; pooled ratio hanya catatan | PASS | Baris 156–170; Tabel 7 + TNOTE |
| Primary vs supporting runs (core 0.3.1) | PASS | Baris 57, 72, 114, 149; tidak digabung |
| Dua site, runtime label Node 26.13.1/V8 14.6; history Node 24 tidak digabung | PASS | Baris 96, 182 |
| Threats to Validity (latency-only, wasm64-only, warm-cache, satu run/sel) | PASS | Baris 188–190 |

Tidak ada perubahan pada RQ1–RQ3, estimand, 15 ronde, Phase D warm-cache, raw exhibit, tabel hasil, angka, chart, atau Threats to Validity.

## 4. Audit literatur (baseline audit 20 Nov ≈ 05:55 UTC)

Status aktual `reference-eligibility-matrix.csv` (28 baris): **Qualified 20 · Uncertain 1 · Not Qualified 7**.

- Requirement A: 20 artikel jurnal peer-reviewed terkonfirmasi di Introduction ≥ 15 → **PASS**. [20] tidak dihitung.
- Requirement B: $20/28 = 71{,}43\% < 80\%$; ambang `ceil(0.8×28)=23`; **kekurangan 3 Qualified** → **FAIL**.
- Skenario 21/28 = 75% hanya jika [20] memperoleh bukti review individual; tetap FAIL dan bersifat hipotetis.

Keputusan sitasi terkunci terverifikasi di naskah: [10] JSON Tiles dipertahankan dengan klaim "automatically detects the most important keys … columnar-like scan"; [23] = C1 `10.1145/3712197` (ACM TOSEM 2025); [24] tetap proceedings ICSE dengan pembatasan "510 NPM packages"; [27] = D2b `10.1007/s10723-023-09669-8` (J. Grid Computing 2023). DOI lama `10.1145/3487552.3487827` dan `10.1145/3760387` tidak muncul di naskah final. Sitasi sekunder `[23,25]` (baris 180) dan `[23,26]` (baris 186) konsisten dengan konteks klaim.

Wiley [2], [14]–[19], [21]: international status Confirmed berdasarkan bukti tingkat jurnal (screenshot SCImago di `article/assets/evidence/scimago-software-practice-experience-2025.png`; frasa "internationally respected and rigorously refereed"; ISSN cocok dengan serial Crossref) ditambah review artikel dari PDF penerbit → 8 Qualified. [20] international Confirmed tetapi peer review artikel **Uncertain** → tetap di luar numerator. Bukti jurnal tidak dipakai untuk mengklaim review individual [20].

### Upaya tambahan 3 referensi Qualified

Pencarian time-boxed via OpenAlex (`title_and_abstract.search`) untuk topik yang benar-benar dibahas naskah — JSONPath/SIMD structural indexing, selective JSON query, compiled JSON parsing — menghasilkan nol kandidat jurnal yang relevan dan tervalidasi (satu-satunya hasil adalah preprint Zenodo non-relevan). Kandidat sebelumnya (C2/C3/C4/D1/D2a/E1–E4) tetap pada keputusan semula. Menambah referensi sebagai supplement juga tidak menyelesaikan ambang: $(20+x)/(28+x)\ge0{,}8 \Rightarrow x\ge12$. Oleh karena itu **tidak ada citation padding** dan Requirement B dinyatakan **FAIL dengan kekurangan 3**.

## 5. Kesinambungan argumen

Rantai `Research Gap → RQ → Method → Boundary → Result → Discussion → Conclusion` dapat ditelusuri:

- Gap: evaluasi existing mengukur satu boundary (baris 23) → RQ1–RQ3 (baris 27) → lima phase (baris 25, 51) → hasil per-boundary (baris 104–170) → Discussion per RQ (baris 174–178) → Conclusion per boundary (baris 202).
- Kontribusi (i) boundary-resolved evidence, (ii) locked estimand, (iii) checksum-proven pipeline (baris 25) dapat ditelusuri ke Tabel 8, Methods, dan Data Availability.
- Implikasi praktis (baris 176, 178, 204) dibatasi pada store yang dapat menyajikan canonical bytes dan selective traversal dengan fraksi kecil; tidak mengklaim kemenangan parser murni.
- Future work (baris 206) berasal dari keterbatasan nyata: cold path, memori/CPU/energi, comparator native-in-process, endpoint tambahan, pengulangan run.

## 6. Pernyataan dan placeholder

Satu-satunya placeholder editorial ditemukan di baris 6: `Submitted: [to be assigned by the editorial office] Revised: [pending] Accepted: [pending]`. Sesuai instruksi, **tidak diisi** — ini memerlukan keputusan pemilik/editorial office. Identitas penulis, afiliasi, ORCID, funding, conflict of interest, author contributions, data availability, dan deklarasi AI diambil apa adanya dari `article/metadata.json` dan naskah sumber; tidak ada yang direkayasa. Tidak ada placeholder "Second Author"/"Third Author" atau "[used / did not use]".

## 7. Status verifikasi akhir

| Item | Status |
|---|---|
| Sumber manuskrip terbaru diidentifikasi (hash + timestamp) | PASS |
| Definisi estimand vs implementasi skrip | PASS |
| Interpretasi A–E vs $S=T_{V8}/T_ZE$ di naskah terbaru | PASS |
| Verifikasi 63 sel terhadap raw exhibit (audit 18 Nov) | PASS |
| Dua perbaikan substansi (CR-01, CR-02) | PASS |
| Requirement A (20 ≥ 15) | PASS |
| Requirement B (20/28 = 71,43%) | FAIL — kurang 3 |
| 3 referensi Qualified tambahan tanpa mengorbankan relevansi | UNVERIFIED — tidak ditemukan |
| Placeholder tanggal editorial | UNVERIFIED — keputusan pemilik |
| Kesiapan submit | FAIL — gate literatur belum terpenuhi |
