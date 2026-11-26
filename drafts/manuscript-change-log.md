# Manuscript Change Log — Orientasi Speedup & Finalisasi

Tanggal: 2026-11-18 · HEAD: `a1fad918a7fccb6464722ac35723c29800ba7849` · branch `research/nd11-phase-d-e-synthesis`.
Semua perubahan hanya pada artefak artikel turunan. Raw exhibit, record, korpus, manifest, template `article/article.docx`, dan working tree dirty yang telah ada sebelumnya **tidak disentuh**. Tidak ada branch switch / reset / commit / push / merge.

## 1. Perubahan naskah (`article/drafts/article-draft.md`)

| # | Lokasi | Sebelum | Sesudah | Alasan | Bukti | Artefak diregenerasi |
|---|---|---|---|---|---|---|
| 1 | Abstract | `S = 0.04–0.07 (baseline spends 15–23× longer)`; `on-demand path runs at 0.04–0.07 of baseline's time` | V8 16–23× faster at full materialization; 6–13× under projection; crossover under traversal | `S = T_V8/T_ZE`; narasi lama membaca S sebagai `T_ZE/T_V8` | `speedup-orientation-audit.md` §4; raw `v8-parse` 0.012787 ms vs `ze-parse` 0.258747 ms | docx, pdf |
| 2 | Methods §Statistical Inference | `values below 1 favor the on-demand path`; `entirely below 1 indicates an on-demand advantage` | below 1 → V8 advantage; above 1 → on-demand advantage; explicitly "ratio of across-round medians" | definisi S dan estimand terkunci | audit §1; spec §4–§6 | docx, pdf |
| 3 | Methods (BCa) | klaim BCa tanpa artefak turunan | BCa log-scale + jackknife dari resample sama, archived | klaim harus dapat diverifikasi | `orientation-audit.json → bca_CI` (63 sel) | json |
| 4 | Results A | "on-demand path's round-median time is 0.04–0.07 of baseline's" | "V8's full parse took 16–23× less time (1/S 16.3–23.3)" | arah interpretasi | T3 + audit baris A | docx, pdf |
| 5 | Figure 4 caption | "Bars below 1.0 favor the on-demand parser" | "below 1.0 favor the V8 baseline; above favor on-demand" | caption bertentangan dengan sumbu S | `Charter/main.py` L81 (axis `S = T_V8/T_ZE`) | chart, docx, pdf |
| 6 | Results B | "on-demand projection runs at 0.08–0.16 of baseline's time" | "on-demand projection is 6–13× slower than V8" | arah interpretasi | T4 + audit 12 sel B | docx, pdf |
| 7 | Results C | reports/globalConfig = on-demand faster; schedules = baseline faster | dibalik: V8 faster on reports/globalConfig; on-demand faster on schedules/server assistants | arah interpretasi | T5 + audit 12 sel C | docx, pdf |
| 8 | Cost-model reading | globalConfig/reports "favor skipping the parse" | globalConfig (cheap parse) and reports (amortized parse) leave on-demand behind | konsisten dengan S | T5 | docx, pdf |
| 9 | Table 3–5 captions | tanpa penjelasan arah | `(S < 1 favors V8; S > 1 favors the on-demand path)` | transparansi pembacaan | definisi S | docx, pdf |
| 10 | Table 7 note | "Footnote (legacy convention...): ... in order." + referensi "footnote of Table 7" | "Note. The legacy pooled-request median ratios, which are not the estimand used in this article, were 1.076, 1.041, and 1.134 for the three runs, respectively." + "Table 7 note" | catatan harus langsung di bawah tabel, bukan footnote halaman | `reports/nd11-phase-d-e-synthesis.md` L19–21, L139–141; `verify_docx.py` | docx, pdf |
| 11 | Discussion RQ1 / Comparison / Conclusion | "advantage largest at full parse", "full-materialization advantage (15–23×)" | "disadvantage largest at full parse", "result runs opposite to native on-demand advantages", V8 16–23× faster | kesimpulan mengikuti estimand | audit + recomputation report | docx, pdf |
| 12 | Contributions / RQ | "where on-demand parsing gains hold", "affect the parser's advantage" | "where the wasm path wins, ties, or loses", "relative performance" | netral terhadap arah | definisi S | docx, pdf |
| 13 | Abstract panjang | 253 kata (>250 AVITEC) | 244 kata | batas format AVITEC | `avitec-requirements.md` | docx, pdf |

## 2. Perubahan generator / artefak turunan

| File | Perubahan | Alasan |
|---|---|---|
| `article/scripts/Ledger/build_ledger.py` | output ke `article/data/csv/evidence-ledger.csv` + `article/data/json/evidence-ledger.provenance.json` (sebelumnya `drafts/`, tidak sesuai lokasi kanonik) | satu source of truth; determinisme terverifikasi dua kali (hash identik) |
| `article/scripts/Ledger/export_charter_raw.py` | path ledger kanonik; `interpretation` chart 1 dibalik ke `S < 1 favors the V8 baseline` | konsistensi data chart |
| `article/scripts/Ledger/audit_orientation.py` | **baru** — audit independen 63 sel + BCa + 2 laporan + JSON | bukti audit & rekalkulasi |
| `article/scripts/Builder/build_docx.py` | keep-together + cantSplit untuk tabel ≤7 baris; core properties dari metadata; hapus comments/category template | Table 3–8 tidak terpecah; metadata bersih |
| `article/scripts/Builder/verify_docx.py` | **baru** — 12 pemeriksaan editorial | verifikasi dapat diulang |
| `article/scripts/Builder/finalize_pdf.py` | **baru** — salin core properties ke PDF + render QA PNG | metadata PDF kosong setelah ekspor Word |
| `article/drafts/charts/chart*.png/.svg` | regenerate dari data ledger (angka identik) | sinkronisasi pipeline |
| `article/scripts/Charter/raw/*/{data.csv,provenance.json,README.md}` | regenerate | sinkronisasi interpretasi |
| `article/scripts/Grapher/diagram/fig{1,2,3}.png` | regenerate dari SVG `article/assets/images/*.mmd.svg` (3×, Edge headless) | file PNG yang direferensikan naskah tidak ada |
| `article/drafts/stage9-handoff.md` | ditandai SUPERSEDED + path ledger diperbaiki | handoff lama tidak lagi menjadi rujukan akhir |

## 3. File yang sengaja TIDAK diubah

- `article/article.docx` — template pristine, 894.262 B (diverifikasi).
- `out/raw/**`, `out/measurements/**`, `reports/**`, `corpus/**`, `schemas/**` — raw evidence & provenance.
- `scripts/analyze_measurement/nd_d_e_synthesis.py` — analisis lama; perbaikan opsional hanya dengan instruksi eksplisit.
- `article/data/mmd/fig3-decision-flow.mmd` —Diagram inference sudah benar (above 1 → on-demand faster).
- Semua submodule, `.gitmodules`, dan 31 entri working-tree dirty yang sudah ada.
- Template masthead (Vol. 9 No. 1 February 2027, pp. 1-20, DOI contoh) — keputusan editorial jurnal.

## 4. Ringkasan angka

Nol nilai numerik diubah. 63/63 sel dari ledger terbukti identik dengan rekalkulasi independen dari raw exhibit. Perubahan bersifat interpretasi/teks, caption, note, dan perbaikan pipeline generasi artefak.
