# Final Quality Review — AVITEC Original Research Article

Tanggal: 2026-11-18 · HEAD `a1fad918a7fccb6464722ac35723c29800ba7849` · branch `research/nd11-phase-d-e-synthesis` (31 entri dirty pra-eksisting) · template `article/article.docx` pristine (894.262 B).

## A. Statistical correctness

| Kriteria | Status | Bukti |
|---|---|---|
| Mapping field V8/ZE diverifikasi dari raw data & source code | ✅ | `speedup-orientation-audit.md` §2: `v8-parse`↔`ze-parse`, `v8-selective`↔`ze-project-selective`/`ze-l1-traversal`, D per-store, E request `v8`/`ze`; `scripts/bench/nd6_bench.mjs` L246/L253/L262/L289/L302; `build_ledger.py` L122–236 |
| A–C diaudit terhadap kemungkinan rasio terbalik | ✅ | 36 sel A–C: PDF S = raw S (contoh A/dev/courses 0.0494 = 0.012787/0.258747 ms). **Angka tidak dibalik; interpretasi yang diperbaiki** |
| D–E diverifikasi ulang | ✅ | D mongo 2.8802/2.6654 (CI > 1), file 0.9526/0.9871 (CI memuat 1); E 1.0501/1.0278/1.1544; legacy pooled 1.076/1.041/1.134 diverifikasi di `reports/nd11-phase-d-e-synthesis.md` L19–21, L139–141 |
| Semua angka memakai satu orientasi S = T_V8/T_ZE | ✅ | 63/63 sel `MATCH` dari rekalkulasi independen (`orientation-audit.json`) |
| Estimand tetap ratio of across-round medians | ✅ | `θ = median(T_V8,i)/median(T_ZE,i)`, dinyatakan eksplisit di Methods ("not the median of fifteen paired-round ratios") |
| Agregasi per-round A–D / E sesuai protokol | ✅ | A–D `rounds_ms` mean-of-reps; E median 10 request/engine/ronde; 20 request TOTAL/ronde |
| Bootstrap 15 paired rounds, B=10.000, seed 20261117 | ✅ | `boot_ci()` L91–96; audit memakai `idx` joint; dua run ledger identik (SHA-256 `800218AF…`, `1E5F1EE1…`) |
| CI primer percentile; BCa sensitivitas | ✅ | percentile 2,5/97,5; BCa log-scale + jackknife tersimpan di `orientation-audit.json` (`bca_CI`) |
| Semua angka punya provenance | ✅ | ledger 63 baris, 126 file SHA-256; provenance per sel di audit JSON |

## B. Manuscript consistency

| Kriteria | Status | Bukti / catatan |
|---|---|---|
| Abstract diperbarui | ✅ | 244 kata (≤250), 5/5 keyword, interpretasi A–C benar |
| Methods benar | ✅ | nilai >1 → ZE lebih cepat; <1 → V8; estimand, agregasi, bootstrap, BCa dinyatakan |
| Figure 3 benar | ✅ | sudah benar sejak awal (`above 1 → on-demand faster`); tidak diubah |
| Table 3–7 konsisten | ✅ | angka identik, caption T3–T5 diberi penjelasan arah; T7 note langsung di bawah tabel |
| Figure 4–6 konsisten | ✅ | chart diregenerate dari ledger (angka identik); caption Fig 4 arah diperbaiki; Fig 5/6 sudah benar |
| Results & Discussion konsisten | ✅ | RQ1, cost-model, comparison with prior results, runtime narrative diperbaiki |
| Conclusion konsisten | ✅ | V8 16–23× (A), 6–13× (B), crossover (C); D/E sesuai data |
| Tidak ada interpretasi arah terbalik | ✅ | grep lintas `article/` hanya menemukan kutipan historis di laporan audit/rekalkulasi |
| Hasil negatif tidak dihapus | ✅ | file-store D (CI memuat 1), dev E (CI memuat 1), C crossover dipertahankan |

## C. Layout & editorial

| Kriteria | Status | Bukti |
|---|---|---|
| Table 7 = table note, bukan automatic footnote | ✅ | `%%TNOTE|Note. The legacy pooled-request median ratios...`; `verify_docx.py`: 0 `footnoteReference`, note sebelum Discussion |
| Tidak ada placeholder penulis | ✅ | 0 hit Second/Third/First Author di docx |
| Tidak ada tanggal editorial masa depan di draft | ✅ | history = `[to be assigned...]/[pending]`; template asli (berisi 2 Nov/10 Des/15 Des 2026) tidak disentuh |
| Heading metode = MATERIALS AND METHODS | ✅ | terlihat di halaman 2 PDF |
| AI declaration lengkap & faktual | ✅ | tool, tujuan, cakupan, verifikasi, tanggung jawab penulis; tanpa highlight |
| Highlight template dihapus | ✅ | `w:highlight` = 0 |
| Table 8 tidak terpecah | ✅ | utuh di halaman 12 (keep-together + cantSplit); T3–T7 juga utuh |
| Pagination & referensi diperiksa | ✅ | 14 halaman; tidak ada halaman kosong; referensi [1]–[28] terbaca, tidak terpisah tidak wajar |
| Seluruh PDF diperiksa visual | ✅ | 14/14 PNG di `article/drafts/qa-render/page-01..14.png`; figur, tabel, caption, header, penomoran, running head benar |

## D. Verification

- `verify_docx.py`: **14/14 PASS** (properties, placeholder, footnote, highlight, note, interpretasi, tabel, template).
- Builder QA: abstract 244; prose 5.254 kata (≥5.000 AVITEC); 5/5 keyword; sitasi [1]–[28] urut; 0 sitasi pasca-tanda-baca; 28 DOI unik; 6 figur; 8 tabel.
- Word count alternatif: prose+supp 5.487; body incl. caption/tabel 5.963; Word ≈7.648 — semua dalam rentang 5.000–8.000 "excluding references".
- Determinism: ledger & provenance identik pada dua eksekusi; audit 63/63 MATCH; BCa 63 sel.
- Provenance: 126 file SHA-256; raw exhibit tidak diubah (hash diverifikasi per sel oleh audit).

## E. Remaining risks (harus diungkapkan)

1. **Pemeriksaan plagiarisme belum dijalankan** (tidak ada alat/akun di lingkungan ini) — wajib sebelum submit.
2. **Requirement AVITEC ≥80% referensi jurnal internasional recent**: 20/28 (71,4%) berlabel jurnal; opsi tambah 3–4 referensi atau argumentasi ke editor. Non-English 0% ✓; ≥15 jurnal di Introduction ✓.
3. **Masthead template** (Vol. 9 No. 1 February 2027, pp. 1-20, DOI contoh `10.28989/avitec.v9i1.3941`) sengaja dibiarkan — keputusan editorial, bukan data artikel.
4. **Article history** masih placeholder — editorial akan menetapkan Submitted/Revised/Accepted.
5. **H₀ agregat tidak diputuskan**; tidak ada klaim CPU/memori/energi; D = store design + parser, bukan parser murni; E = end-to-end. Semua sudah dinyatakan di naskah.
6. **Satu run per sel** (kecuali E dev ×2); CI mengukur variabilitas antar-ronde dalam-run; tidak ada pooling lintas site/run/commit.
7. **`scripts/analyze_measurement/nd_d_e_synthesis.py` belum di-patch** (opsional, sesuai spec §11) — laporan committed lama tetap immutable; tidak dipakai sebagai sumber angka artikel.
8. **PR #79 tetap OPEN**, tidak di-merge; working tree dirty 31 entri tidak disentuh.

## F. Verdict

**WARN** — blocker kritis (orientasi interpretasi A–C, Table 7 note, template placeholder, pagination) telah diperbaiki dan dibuktikan dari raw exhibit; seluruh kriteria statistik, konsistensi naskah, dan layout pada §10 lolos. Keterbatasan yang tersisa bersifat editorial/eksternal (plagiarisme, rasio referensi, masthead, tanggal editorial) dan tercantum di atas — bukan kegagalan statistik.

## G. Handoff

- **Source manuscript**: `article/drafts/article-draft.md`
- **Generated deliverables**: `article/drafts/article-draft.docx`, `article/drafts/article-draft.pdf` (**14 halaman**), `article/drafts/qa-render/page-01..14.png`
- **Template (jangan diubah)**: `article/article.docx` (894.262 B, pristine)
- **Bukti statistik**: `article/drafts/speedup-orientation-audit.md`, `article/drafts/statistical-recomputation-report.md`, `article/data/json/orientation-audit.json`
- **Riwayat perubahan**: `article/drafts/manuscript-change-log.md`
- **Regen**: `python article/scripts/Ledger/build_ledger.py` → `audit_orientation.py` → `export_charter_raw.py` → `python article/scripts/Charter/main.py` → `python article/scripts/Builder/build_docx.py` → `verify_docx.py` → Word COM export → `python article/scripts/Builder/finalize_pdf.py`.
- **Git**: tidak ada branch switch, reset, checkout, commit, push, atau merge.
