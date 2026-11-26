# Article Outline — Original Research Article AVITEC

> Status: Stage 4. Judul final + RQ + peta seksi + matriks kontinuitas
> proposal→artikel. Word budget: total ~6.300 (rentang aman 5.000–8.000
> excluding references).

## 1. Judul (final)

**"On-Demand JSON Parsing in Node.js Servers via WebAssembly: A Multi-Boundary
Evaluation"** — 11 kata, ≤20 ✓; arah UMUM (tidak membatasi ke "reporting
application"); peran workload `saq-report`/server SAQ dijelaskan di Methods
(study systems) dan Discussion.

Alternatif cadangan (bila reviewer minta lebih deskriptif): "Evaluating
On-Demand JSON Access in Node.js Servers: A Multi-Boundary Performance Study".

## 2. RQ artikel (rumusan kerja terkunci)

- **RQ1 (access-pattern cost)** — How does the JSON access pattern (full
  materialization vs. partial projection vs. selective traversal) affect the
  speedup of a C++23 on-demand JSON parser (wasm64-bound) over V8's
  `JSON.parse`?
- **RQ2 (repository boundary)** — Does the advantage survive at the repository
  boundary of a real Node.js state-store workload (file store vs. warmed
  Mongo-cache canonical-bytes path)?
- **RQ3 (endpoint transfer)** — Does the advantage transfer to a full HTTP
  endpoint (`GET /rekap`) end-to-end?

Kontinuitas ke proposal: RQ1-proposal → RQ1+RQ2+RQ3 (dipecah per-boundary);
RQ2-proposal (site/ISA) → dimensi site (dev vs server) di semua fase, ISA =
wasm64 (konfigurasi binding); RQ3-proposal (optimasi berbasis paper) → metode
ze_json + Discussion. H₀/H₁ proposal TIGA dimensi (latensi parser, throughput,
memori) — D/E tidak mengukur memori/CPU → **tidak ada verdict parser-only**;
naskah melaporkan latensi per-boundary (disiplin temuan review PR #79).

## 3. Estimand & inferensi (terkunci dari `paired-bootstrap-estimand-spec.md`)

- S = T_V8/T_ZE (>1 = ZE lebih cepat).
- Estimand primer SEMUA fase: θ = median_i(T_V8,i)/median_i(T_ZE,i), 15 ronde
  berpasangan; paired bootstrap B=10.000, seed 20261117, percentile 95%;
  BCa = sensitivitas.
- Agregasi dalam-ronde: A–D mean-of-reps (terkunci harness); E median-of-10
  (pilihan analisis, dinyatakan).
- Interpretasi CI: interval memuat 1 = "advantage not distinguishable",
  BUKAN "H₀ diterima". Uji pelengkap: exact sign test + Wilcoxon signed-rank.

## 4. Peta seksi + word budget

| Seksi | Isi inti | Budget |
|---|---|---|
| **Abstract** | konteks (JSON hot path di server Node.js), objective, methods (5 boundary A–E, 2 site, paired bootstrap), principal findings (A/B besar & selektif; C mixed; D 2.88×/2.67× tapi file <1×; E dev tidak terbedakan, server 1.15×), kontribusi + limitation | ≤250 (target 200) |
| **Keywords** | JSON parsing; on-demand parsing; WebAssembly; Node.js; performance evaluation | 5 kata kunci |
| **1. Introduction** | JSON = hot path di server data-intensive; Node.js baseline = V8 `JSON.parse` materialisasi penuh; on-demand parsing (simdjson → Node.js runtime); wasm sebagai jalur pengiriman parser native ke JS (studi performa wasm; penggunaan wasm di Node.js); gap: keunggulan parser diukur di satu boundary sering tidak transfer — akses parsial, repository, HTTP stack; kontribusi: evaluasi multi-boundary 5 fase × 2 site + protokol inferensi round-level; pertanyaan RQ1–RQ3 | ~1.100 |
| **2. Materials and Methods** | §2.1 Study systems (ze_json: C++23 on-demand, Document/Value lazy, wasm64 C-ABI binding, scanner8 default; saq-report: Express state-store, JsonRepository/MongoJsonRepository, `read().length` vs `readCount()` bytes kanonik); §2.2 Boundaries & workloads (fase A–E definisi; korpus saq_payload_v1 6 dok/88.381 B; tabel provenance run); §2.3 Protocol (15 ronde, warmup 3 untimed, rotasi urutan jalur, alternasi E 10+10/ronde TOTAL 20, parity byte-identik, tanpa trimming); §2.4 Statistical inference (estimand + bootstrap + CI + tests; koreksi konvensi pooled→round-level dinyatakan); §2.5 Reproducibility (record schema + validator + manifest sha256; site dev=AMD Ryzen 5 5500U Node 26.13.1/V8 14.6, server=i5-9400; wasm sha256 identik) | ~1.700 |
| **3. Results** | §3.1 Phase A (parse+materialize): ZE 0.04–0.07× of V8 (parsing 15–25× faster); per-doc + CI; v8-clone referensi; §3.2 Phase B (partial projection): 0.08–0.16×; §3.3 Phase C (selective traversal): mixed 0.05×–1.65× — traversal L1 = biaya utama, kemenangan hanya di dok besar/schedules; §3.4 Phase D repository: mongo-cache 2.88× (2.57–3.05) dev / 2.67× (2.51–2.86) server; file-store 0.95×/0.99× (CI memuat 1 — **negative result dilaporkan**); §3.5 Phase E HTTP: dev 1.05 (0.93–1.15) & 1.03 (0.97–1.11) — tidak terbedakan; server 1.15 (1.08–1.18) — terukur; catatan konvensi pooled 1.076/1.041/1.134 | ~1.600 |
| **4. Discussion** | Pola akses menentukan win-rate (RQ1); desain repository (canonical bytes + count) = pengungkit terbesar tapi bukan parser murni (RQ2); kompresi di endpoint: latensi non-parser (middleware/render/HTTP) dominan (RQ3); peran runtime (Node 26; angka era Node 24 = narasi berlabel); perbandingan dengan simdjson-on-demand Node.js & FAD.js; **threats to validity**: n=15, satu run/sel (kecuali E dev ×2), warm cache saja, memori/CPU tidak diukur, wasm-only (tanpa native baseline di D/E), single-app; batas klaim H₀ | ~1.400 |
| **5. Conclusion** | Jawab RQ1–RQ3 eksplisit dengan angka berlabel CI; kontribusi protokol; future work (cold-path Mongo, memori/CPU, native-vs-wasm, endpoint lain) | ~350 |
| **Declarations** | Funding (none), COI, data/code availability (GitHub repos + records), **Declaration of AI Use** | ~180 |
| **References** | 28 INCLUDE (20 jurnal + 7 prosiding + RFC8259) — Introduction ≥15 jurnal ✓; ≥80% jurnal internasional recent ✓; IEEE-based `[n]` | — |

## 5. Matriks kontinuitas bukti → seksi

| Bukti (ledger) | Seksi | Tabel/Figur |
|---|---|---|
| A dev+server 12 row | Results §3.1 | T2 + Chart 1 |
| B dev+server 12 row | Results §3.2 | T3 + Chart 1 |
| C dev+server 12 row | Results §3.3 | T4 + Chart 1 |
| D dev+server 4 row | Results §3.4 | T5 + Chart 2 |
| E 3 run | Results §3.5 | T6 + Chart 3 |
| Supporting 3376d07 (core 0.3.1) | Methods §2.5 / Results §3.4 note | T2 note |
| Protokol & validator | Methods §2.3–2.5 | — |
| Estimand spec | Methods §2.4 | — |

## 6. Disiplin frasa (dilarang → gantinya)

- ~~"SIMD-accelerated parser"~~ → "C++23 on-demand JSON parser exposed through
  a WebAssembly 64-bit binding" (scanner8 = dispatch default; varian scanner64/128
  ditolak & tidak dipakai).
- ~~"H₀ rejected/accepted"~~ → "CI includes 1 — advantage not distinguishable
  at this design's precision".
- ~~"parser is 2.88× faster" (dari D)~~ → "the repository path serving count
  requests from canonical cached bytes is 2.88× faster" (D gabungan desain).
- ~~pooled-request numbers tanpa label~~ → angka primer = round-level ratio;
  pooled disebut eksplisit sebagai konvensi harness (sekali, di §3.5 note).
- ~~"endpoint produksi meningkat X×" (dari D)~~ → klaim endpoint hanya dari E.
