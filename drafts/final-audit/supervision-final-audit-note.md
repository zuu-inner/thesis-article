# Final Supervision Audit Note — Literature Gate & Citation Mapping

Tanggal: 2026-11-20 · Menyertai `article-draft-supervision-final.md` / `.docx`.
Draft untuk bimbingan; **bukan** pernyataan publication gate lulus.

## 1. Final Reference Eligibility Audit

Sumber kebenaran: `reference-eligibility-matrix.csv` (28 baris, diperbarui untuk [23] dan [27]).

| Eligibility | Count | Perubahan dari baseline |
|---|---:|---|
| Qualified | 20 | +1 ([23] → C1) + 8 Wiley (international terbukti) |
| Uncertain | 1 | [20] Wiley — peer review artikel belum terkonfirmasi |
| Not Qualified | 7 | −1 ([23] keluar) |
| Total | 28 | 0 (one-for-one replacement) |

Keputusan final per referensi yang diubah:

| Ref | DOI final | Sumber | Eligibility | Bukti |
|---|---|---|---|---|
| [10] | 10.1145/3448016.3452809 | JSON Tiles, SIGMOD 2021 | Not Qualified (proceedings) | Abstrak: auto-detects most important keys, extracts transparently, columnar-like scan; claim dipersempit, referensi dipertahankan |
| [23] | 10.1145/3712197 | C1, ACM TOSEM 34(6) 1–22, 2025 | Qualified | Crossref `journal-article`; ACM peer-review policy; review history 2024-06-20/2024-12-10; portability/sandboxing in abstract |
| [24] | 10.1145/3744916.3764533 | ICSE 2026 | Not Qualified (proceedings) | Abstrak: 510 NPM packages, 217 unique Wasm modules; klaim dipersempit, referensi dipertahankan |
| [27] | 10.1007/s10723-023-09669-8 | D2b, J. Grid Computing 21(3) art.34, 2023 | Qualified | Crossref `journal-article`; Springer aims/policies; 13-function WasmEdge/Wasmer/Wasmtime vs containerd |

Wiley [2], [14]–[21] — pembaruan 2026-11-20 berdasarkan screenshot SCImago yang disimpan di `article/assets/evidence/scimago-software-practice-experience-2025.png` (nama jurnal *Software - Practice and Experience*, publisher John Wiley and Sons Ltd, country United Kingdom, ISSN 00380644/1097024X — cocok dengan serial Crossref 1097-024X, publication type Journals, SJR 2025 0.688/Q2, H-index 84, coverage 1971-2026). Deskripsi scope memuat frasa **"internationally respected and rigorously refereed"**: ini adalah **bukti tingkat jurnal** untuk `international_status`, sehingga kesembilan entri ditetapkan **Confirmed**. Negara, publisher, ISSN, kategori, dan SJR Q2 bersifat pendukung; Q2 **bukan** bukti tunggal peer review.

Bukti review tetap dibedakan per artikel. Delapan referensi ([2], [14]–[19], [21]) memiliki `peer_review_status = Confirmed` dari PDF penerbit (Received/Revised/Accepted) dan kini memenuhi seluruh kriteria → **Qualified**. [20] tetap **Uncertain** untuk peer review (Short Communication; PDF tidak memuat tanggal Received/Revised/Accepted), sehingga `eligibility`-nya tetap **Uncertain** walaupun international status-nya Confirmed — pernyataan jurnal "rigorously refereed" tidak dibaca sebagai bukti review artikel tertentu.

Keterbatasan: halaman SCImago live tidak dapat diakses dari lingkungan audit (403 langsung; CAPTCHA via proxy teks), sehingga **tidak ada URL halaman yang diverifikasi dan tidak ada URL direkayasa**; bukti yang dipakai adalah screenshot yang disimpan di repository. Sembilan PDF lokal tetap menjadi bukti review artikel, bukan bukti international scope. HTTP 403 tidak diartikan sebagai kegagalan jurnal.

ACM TOSEM (C1): halaman jurnal-spesifik (aims/scope, editorial board) tetap terhalang 403/CAPTCHA; status Qualified dipertahankan berdasarkan ACM journals page + ACM Peer Review Policy + cakupan global ACM, dengan gap ini tercatat.

## 2. Decision Ledger

| DOI | Existing decision | New evidence | Action | Reason |
|---|---|---|---|---|
| 10.1145/3448016.3452809 | Retain/narrow [10] | Abstrak OpenAlex dikonfirmasi ulang | Retain, narrowed | Kontribusi unik deteksi key penting; tidak ada jurnal setara (D1/E1/E2/C3 ditolak) |
| 10.1145/3712197 | Approved [23] | Crossref metadata lengkap | Applied | Replacement disetujui; one-for-one |
| 10.1145/3744916.3764533 | Retain/narrow [24] | Abstrak: 510/217 | Retain, narrowed | "major host" tidak diukur |
| 10.1007/s10723-023-09669-8 | Pending for [24], supplement for server-side claim | Crossref + Springer | Applied to [27] | Klaim [27] adalah server-side benchmark; D2b tepat, D2a overlap |
| 10.1145/3760387 | [27] Wasm-IO | Abstrak: peripheral I/O industrial | Removed | Tidak mendukung klaim server-side |
| 10.1145/3487552.3487827 | lama [23] | — | Removed | Diganti C1 |
| C2/C3/C4/D1/D2a/E1–E4 | rejected/supplement/backup | tidak ada bukti baru | unchanged | Tidak ada alasan baru untuk membuka ulang |
| 10.1002/spe.* (9) | international Uncertain | screenshot SCImago (scope 'internationally respected and rigorously refereed'; ISSN cocok) | international → Confirmed; eligibility 8 → Qualified, [20] tetap Uncertain | Bukti tingkat jurnal; review artikel tetap dari PDF penerbit |

Time-boxed search 2026-11-20 untuk [6]/[7]/[12] (bit-parallel fast-forwarding, compiled JSON parsing, selective JSON access) tidak menemukan artikel jurnal yang mendukung teknik spesifik tersebut; kandidat yang muncul adalah [9] FAD.js (sudah dikutip, Qualified) atau jurnal non-relevan. Tidak ada replacement dipaksakan.

## 3. Final Citation-to-Claim Mapping

| Ref | Klaim di manuskrip | Sumber mendukung? | Status |
|---|---|---|---|
| [10] | JSON Tiles auto-detects most important keys, extracts transparently, columnar-like scan | Ya (abstrak) | proceedings; Not Qualified |
| [23] | Wasm performance depends on runtime; portability/sandboxing | Ya (C1 abstract) | journal; Qualified |
| [24] | Empirical study of 510 NPM packages, Wasm in Node.js ecosystem | Ya (abstrak) | proceedings; Not Qualified |
| [27] | Server-side WebAssembly runtime deployments | Ya (D2b benchmark) | journal; Qualified |
| [25] | Runtime landscape surveyed; sandboxed environment | Ya (survey abstract) | journal; Qualified |
| [26] | Interpreter/JIT overheads on constrained targets; native comparison | Ya (benchmark abstract) | journal; Qualified |

Sitasi sekunder: baris 180 `[23, 25]` (portability/sandboxing), baris 186 `[23, 26]` (environment-dependent deviations). Tidak ada klaim sensor/aktuator/peripheral I/O yang tertinggal.

## 4. Final Requirement A / B Calculation

**Requirement A** — Introduction mengutip 28 referensi unik. Artikel jurnal peer-reviewed terkonfirmasi: **20** (11 Qualified baseline + 8 Wiley + C1; [27] → D2b tetap jurnal sehingga tidak mengurangi hitungan). [20] tidak dihitung karena peer review artikelnya tetap Uncertain. Minimum AVITEC 15 → **PASS**.

**Requirement B** — numerator Qualified = **20**, denominator = **28**.

| Skenario | Qualified | Total | Persentase | Status |
|---|---:|---:|---:|---|
| Final bibliography (aktual) | 20 | 28 | 71.43% | **FAIL** |
| Jika [20] kelak memperoleh bukti review individual | 21 | 28 | 75.00% | FAIL — hipotetis, bukan hasil |
| Target AVITEC | 23 | 28 | 82,14% | — |

Ambang `ceil(0,80 × 28) = 23`. Kekurangan aktual: **3 Qualified** (23 − 20). Skenario 21/28 = 75,00% hanya mungkin jika [20] kelak memperoleh bukti review individual; itu tetap FAIL dan **bukan hasil aktual**. Requirement B **tidak dinyatakan PASS**.

## 5. Supervisor Briefing

**What changed.** Empat keputusan terkunci diimplementasikan di naskah akhir: [10] dan [24] dipersempit redaksinya tanpa mengganti sumber; [23] → C1 (ACM TOSEM); [27] → D2b (J. Grid Computing). Dua sitasi sekunder diperbaiki (`[23,25]`, `[23,26]`). Entri bibliografi, eligibility matrix, literature matrix, dan dua entri BibTeX diselaraskan. Satu-for-one replacement sehingga denominator tetap 28.

**Why.** Klaim lama "major host" melampaui bukti 510 paket; "frequently accessed keys" tidak sesuai terminologi abstrak JSON Tiles; Wasm-IO adalah studi peripheral I/O industrial, bukan benchmark server-side; C1 adalah measurement study container-runtime yang sesuai dengan klaim [23].

**What remains uncertain.** International status Wiley telah terselesaikan melalui bukti tingkat jurnal (screenshot SCImago), tetapi review individual [20] tetap Uncertain; halaman SCImago live tidak terverifikasi (403/CAPTCHA); bukti jurnal-spesifik TOSEM masih terbuka; dan masih diperlukan **3 Qualified replacement** relevan tambahan. Karena itu Requirement B tetap FAIL.

**Current status.** Riset dan validasi eksperimen tidak berubah: RQ1–RQ3, estimand, 15 rounds, phase D warm-cache, tabel, chart, dan Threats to Validity utuh. Naskah ini **draft untuk bimbingan**, bukan final submission copy.

**Questions for supervisor.**
1. Apakah bukti peer-review individual [20] dapat diperoleh (mis. dari versi publikasi lain), atau apakah [20] harus diganti? Screenshot SCImago hanya membuktikan status jurnal, bukan review artikel [20].
2. Apakah dua pengganti tambahan boleh diarahkan ke topik selective JSON access/JSONPath dengan jurnal yang relevan, mengingat teknik spesifik [6]/[7]/[12] belum punya padanan jurnal terverifikasi?
3. Apakah status Qualified C1 perlu dibuktikan lebih lanjut dengan aims/scope TOSEM sebelum bibliografi final?
