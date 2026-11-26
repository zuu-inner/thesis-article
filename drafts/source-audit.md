# Source Audit — Artikel Original Research AVITEC

> **Tujuan**: inventaris sumber kebenaran naskah artikel, verbatim RQ/hipotesis,
> status bukti, konflik sumber, dan disiplin klaim. Semua angka naskah ditelusuri
> ke daftar ini (→ `evidence-ledger.csv`, Stage 2).
>
> **Tanggal audit**: 2026-11-18 · **Bahasa catatan**: Indonesia · simbol/path asli.
> **Dibaca pada**: working tree `v5`, HEAD `a1fad918a7fccb6464722ac35723c29800ba7849`
> (branch `research/nd11-phase-d-e-synthesis`, PR #79 OPEN — tidak di-merge,
> tidak di-commit; bukti A–E berada pada record/raw **ter-commit** di HEAD ini).

---

## 1. Identitas workspace & state checkout

- Repo root `v5`; submodules (gitlink index @ HEAD):
  - `ze_json` @ `01a143f` (ada di disk, tree bersih)
  - `saq-report` @ `534d9a8` (ada di disk)
  - `thesis-proposal` @ `4059b23` — **direktori TERHAPUS dari disk**; dokumen
    diambil verbatim via GitHub raw @4059b23 (§2.2)
  - `submission-thesis-supervisor` @ `015188c` — mapping dihapus di working
    `.gitmodules`; di luar domain riset (arahan pemilik), diabaikan.
- **Working tree dirty (didokumentasikan, TIDAK disentuh, tidak di-commit)**:
  `M .gitmodules`, `M scripts/grapher/make-graph.ts`, `D thesis-proposal`,
  `D utils/typ/{metadata.example.json,metadata.typ,strfmt.typ}`,
  23 CSV untracked `reports/charts/*`, `?? article/` (workspace artikel, ekstraksi
  ZIP segar; `article/article.docx` pristine 894.262 B, template asli tidak
  di-overwrite — draft = salinan).
- **Konsekuensi disiplin**: hasil pengukuran di bawah dinyatakan dari
  record/raw @ commit bersih masing-masing (`record.git_commit.dirty=false`),
  bukan dari state working tree saat ini.

## 2. Pertanyaan riset & hipotesis (verbatim)

### 2.1 RQ proposal — `docs/project/plans.md` L15–28 (verbatim)

> - **RQ1** — Seberapa jauh performa `ze_json` (native + wasm64) berbeda dari baseline
>   `JSON.parse`/`JSON.stringify` V8 yang dipakai server SAQ, pada korpus kerja SAQ
>   yang riil?
> - **RQ2** — Bagaimana pengaruh **arsitektur sistem** (site: server SAQ vs device dev;
>   ISA: native x86-64 vs wasm64) terhadap hasil ukur yang setara?
>   (Update 2026-11-13: server SAQ tereksekusi — matriks ND-6 di `saq_server`
>   = 1.30× vs dev 2.85×/3.00× (Node 24 era); lihat `reports/nd6-server-phase-matrix.md`
>   dan P5 di bawah. Kontrol runtime/hardware = ND-10.)
> - **RQ3** — Optimasi apa yang berdampak terukur (berbasis paper) tanpa melanggar
>   kebenaran (validitas, kepatuhan JSON)?
>
> **Hipotesis kerja**: parser on-demand C++23/SIMD > V8 pada korpus besar dan
> read-only; pada payload kecil SAQ keunggulan bisa tertelan overhead boundary
> (wasm/ABI), bukan hilang di algoritme — ini diukur, bukan diasumsikan.

### 2.2 H₀/H₁ — `thesis-proposal@4059b23/pages/bab_1/007-hipotesis.typ` (verbatim, via GitHub raw)

> *H#sub[0]* : Tidak terdapat perbedaan yang signifikan antara baseline JSON.parse bawaan runtime dan Parser JSON On-Demand ze_json terhadap latensi pemanggilan parser, throughput, dan konsumsi memori pada aplikasi pelaporan SAQ.
>
> *H#sub[1]* : Penerapan Parser JSON On-Demand ze_json pada aplikasi pelaporan SAQ menurunkan latensi pemanggilan parser (nanosecond dan ns/op) serta konsumsi memori secara signifikan dibandingkan baseline, dengan kenaikan beban prosesor yang terkendali, pada lingkungan pengujian tertutup dengan perangkat keras yang identik.

> Kedua hipotesis diuji melalui eksperimen terkendali yang dirancang pada Bab III,
> dengan tingkat signifikansi 5%.

**Disiplin H₀**: H₀ proposal berdimensi tiga (latensi parser, throughput,
konsumsi memori). Fase D/E **tidak** mengukur memori/CPU → H₀ proposal
**belum diputuskan** oleh data D/E; naskah melaporkan hasil latensi
per-boundary, bukan verdict parser-only (temuan Codex P2 #2, PR #79).

## 3. Restatement RQ untuk artikel + matriks kontinuitas

Naskah artikel (arah judul UMUM — optimasi kinerja parsing JSON on-demand untuk
server Node.js via WebAssembly, tanpa membatasi ke "reporting application";
peran workload `saq-report`/server SAQ dijelaskan di Discussion):

- **RQ-A1 (access-pattern cost)** — Bagaimana biaya pola akses JSON (full
  materialization vs proyeksi parsial vs traversal selektif) memengaruhi
  keunggulan relative parser on-demand versus `JSON.parse` V8?
  → dijawab **fase A, B, C** (dev + server).
- **RQ-A2 (repository boundary)** — Apakah keunggulan tersebut bertahan setelah
  melewati batas repository pada workload state-store nyata (file vs warm
  Mongo-cache)?
  → dijawab **fase D**.
- **RQ-A3 (endpoint transfer)** — Apakah keunggulan tersebut transfer ke endpoint
  HTTP penuh `GET /rekap`?
  → dijawab **fase E**.

| Proposal RQ | Artikel RQ | Fase | Catatan |
|---|---|---|---|
| RQ1 (perbedaan performa vs baseline, korpus SAQ) | RQ-A1 + RQ-A2 + RQ-A3 | A–E | satu pertanyaan dibagi per-boundary |
| RQ2 (arsitektur sistem: site, ISA) | dimensi site (dev vs server) pada semua fase; ISA wasm64 = konfigurasi binding artikel | A–E | "native x86-64" diukur di jalur lain (nd14 termasuk?), artikel memakai jalur wasm64 |
| RQ3 (optimasi berbasis paper) | metode ze_json (§Methods: on-demand desain, lookups @cite) + Discussion | — | bukan estimand utama |
| H₀/H₁ | bukan verdict parser-only; per-boundary latensi | D, E | §2.2 |

## 4. Inventaris bukti (record tervalidasi)

Semua record **PASS** `scripts/measurement-schema/validate.py`
(dijalankan ulang 2026-11-17): **11/11 PASS**.

| # | Eksperimen | Run ID | Site | Kelas | Commit root | Record |
|---|---|---|---|---|---|---|
| 1 | A dev | `zuu-20261115071747-6d87bf3` | dev_device | primary | `6d87bf3` | `reports/nd14/…nd6-a-dev_device.record.json` |
| 2 | B dev | `zuu-20261115075332-6d87bf3` | dev_device | primary | `6d87bf3` | idem B |
| 3 | C dev | `zuu-20261115080838-6d87bf3` | dev_device | primary | `6d87bf3` | idem C |
| 4 | D dev | `zuu-20261115080840-6d87bf3` | dev_device | primary | `6d87bf3` | idem D |
| 5 | A–D dev supporting | `zuu-20261115{005811,010151,010153,010155}-3376d07` | dev_device | supporting (core 0.3.1) | `3376d07` | 4 record |
| 6 | A server | `server-lanjut-20261116060843-8a1324b` | saq_server | primary | `8a1324b` | `reports/nd14/…nd6-a-saq_server.record.json` |
| 7 | B server | `server-lanjut-20261116060900-8a1324b` | saq_server | primary | `8a1324b` | idem B |
| 8 | C server | `server-lanjut-20261116060915-8a1324b` | saq_server | primary | `8a1324b` | idem C |
| 9 | D server | `server-lanjut-20261116060933-8a1324b` | saq_server | primary | `8a1324b` | idem D |
| 10 | E dev run 1 | `zuu-20261116101458-8556513` | dev_device | primary | `8556513` | `reports/nd11/…nd11-phase-e-dev_device.record.json` |
| 11 | E dev re-run | `zuu-20261117000112-6979e3f` | dev_device | primary | `6979e3f` | idem |
| 12 | E pilot | `zuu-20261116235636-ab255f5` | dev_device | **pilot — EXCLUDED** | `ab255f5` | protokol beda: 2 ronde × 3 request TOTAL |
| 13 | E server | `server-lanjut-20261117003513-530f751` | saq_server | primary | `530f751` | `reports/nd11/…nd11-phase-e-saq_server.record.json` |

Raw exhibit: `reports/nd14/raw/<run_id>/nd6_phase_{A,B,C,D}.json` dan
`reports/nd11/raw/<run_id>/nd11_phase_e.json` (+ salinan byte-identik di
`out/raw/<run_id>/` — diverifikasi dipakai bergantian).

## 5. Verifikasi protokol (dari kode harness, bukan ringkasan)

- **Fase A–D** (`scripts/bench/nd6_bench.mjs`): 15 ronde independen; warmup 3
  untimed; **urutan jalur dirotasi per ronde** (`off = r % paths.length`);
  nilai ronde = **mean of reps** (`dt/reps`, `runPathRound` L387–392);
  reps = `targetReps(bytes)` = 30/5 per dokumen (D: 2); tanpa trimming;
  alternasi kontrol bias urutan; record menyimpan mean/median/P95/stddev antar-ronde.
- **Fase E** (`scripts/bench/nd11_phase_e.mjs`): 15 ronde × **20 request TOTAL
  per ronde** (10 V8 + 10 ZE; `(r+k)%2`, eksekusi sekuensial, start-engine
  bergantian); n = 150 request/engine, 300 total; warmup 3/jalur untimed;
  **parity gate** — seluruh 300 body byte-identik (1 hash unik; mismatch = run
  void); raw per-request tersimpan penuh (`{round, seconds, body_bytes,
  body_sha256}`); `speedup_in_run` harness = rasio median pooled 150 request
  (konvensi deskriptif — lihat §6).
- **Korpus**: `corpus/benchmarks/saq_payload_v1` — 6 dokumen, 88.381 B total,
  max 39.209 B, seed generator 20261108, manifest sha256 per dokumen
  (provenance terbukti; `MANIFEST.json`).
- **Boundary fase** (dari desain `docs/measurement/nd6-benchmark-plan.md`,
  `nd11-phase-e-http.md`): A = full materialization (parse/clone); B = proyeksi
  parsial L2 `project(shape)`; C = deep selective access L1; D = lapisan
  repository (`read().length` vs `readCount()` bytes kanonik; mongo-cache =
  warm steady-state, file-store = I/O); E = HTTP `GET /rekap` end-to-end
  (middleware → routing → handler 4 repo → render EJS → respons).

## 6. Konvensi statistik (TERKUNCI — lihat spec lengkap)

Dokumen spesifikasi: **`article/drafts/paired-bootstrap-estimand-spec.md`**
(verdict WARN; seluruh keputusan berbukti). Ringkas:

- **Estimand primer semua fase**: θ = `median_i(T_V8,i) / median_i(T_ZE,i)`
  atas **15 ronde berpasangan** (S = T_V8/T_ZE dipertahankan).
- **Paired bootstrap**: resample ronde joint, B = 10.000, seed `20261117`,
  percentile 95%; BCa (skala log) = sensitivitas, bukan primer.
- **Koreksi terhadap angka lama** (dari `nd_d_e_synthesis.py`, PR #79):
  - Phase E point → rasio median ronde: dev 1,076→**1,050** (CI 0,935–1,147),
    re-run 1,041→**1,028** (CI 0,974–1,114), server 1,134→**1,154**
    (CI 1,085–1,175). Verdict per run tidak berubah.
  - Phase A–C: `speedup_median` diseragamkan ke rasio median (nilai lama =
    median rasio per-ronde, divergensi hingga 22% per sel) → disimpan sebagai
    `paired_median_ratio` sekunder.
  - Phase D sudah konsisten (2,880×/0,953× dev; 2,665×/0,987× server) — CI
    ter-reproduksi persis.
- **Larangan klaim**: tidak ada verdict H₀ parser-only dari D/E; tidak ada
  klaim memori/CPU; tidak ada pooling lintas run/site/commit/boundary;
  angka era Node 24 (`0dcb418`, verdict 2,85×/3,00×, server 1,30×) = histori
  berlabel runtime, tidak dicampur.

## 7. Fakta teretablas (untuk Methods/Metadata naskah)

| Fakta | Nilai | Sumber |
|---|---|---|
| Runtime dev | Node 26.13.1 (V8 14.6.202.34-node.40), AMD Ryzen 5 5500U 12 thread, 7,4 GB, Windows 10.0.26200 | record `host` |
| Runtime server | Node 26.13.1 (idem), i5-9400 6 core, 7,9 GB, Windows 10.0.26300 | record `host` |
| Library | ze_json core 0.3.2, js 0.3.0, ABI 2026000302; wasm64 C-ABI | record `library` |
| Artifact wasm | sha256 `9795f2e8…5fe373` **identik dev & server** (E + D) | record `library.artifact_sha256` |
| Pairing saq-report | D: `8c7f2d4` (canonical-bytes cache `readCount()`); E: `534d9a8` | record `library.version` |
| Respons `/rekap` | 47.888 B, 1 hash unik per run: server `a6236b6c…`, dev mirror `a18c7b4a…` | exhibit E |
| Scanner | wasm64 binding; scanner8 = dispatch default; scanner64/128 ditolak (P4-2) | `ze_json` docs/audit |
| Parser on-demand | `Document`/`Value`/`ArrayIter`/`ObjectIter`, teruji (75 gtest) sejak P7 | `docs/research/audit-2026-11-12.md` §3 |
| Hot path SAQ | `express.json()`, `JsonRepository.js`, `MongoJsonRepository.js`, `exportService.js` | `saq-report` @ `534d9a8` |
| Tidak diukur | memori, CPU, cold-cache Mongo, jaringan antar-mesin, export XLSX/DOCX | protokol |

## 8. Konflik sumber & status PR #79

- **PR #79** (`research/nd11-phase-d-e-synthesis` → `main`, **OPEN**): laporan
  sintesis D↔E **tidak diadopsi sebagai fakta final**; dua temuan Codex P2
  unresolved: (1) estimand E point/CI tidak konsisten → **diselesaikan** oleh
  spec estimand (§6); (2) verdict H₀ melampaui boundary → **dibatasi** (§2.2).
  Laporan committed tidak diubah; naskah artikel memakai konvensi terkoreksi
  dan menjelaskan perbedaannya.
- **Era runtime lama**: `reports/charts/nd6-phase-{a,b,c}.csv` = run
  `zuu-20261112063944-0dcb418` (Node **v24.19.0**, ze_json `14592a0`,
  saq `7930009`) — **tidak comparable** dengan angka artikel; semua nilai
  A–C direkalkulasi dari nd14 (Node 26). Sanity §7.1 master prompt
  (A ≈ 0,04–0,06×; B ≈ 0,08–0,15×; C mixed) berasal dari era lama; nilai
  final menyesuaikan rekalkulasi nd14.
- **Angka sanity D/E lama** (dipakai sebagai cross-check, bukan sumber):
  D dev mongo 2,880× (CI 2,572–3,045) / server 2,665× (2,508–2,857) /
  file 0,953×/0,987×; E dev 1,076×/1,041× (CI memuat 1) / server 1,134×
  (1,084–1,175) — konsisten dengan spec (pooled = konvensi harness lama).

## 9. Peta file pipeline artikel

| Artefak | Path | Status |
|---|---|---|
| Spesifikasi estimand | `article/drafts/paired-bootstrap-estimand-spec.md` | ✅ Stage 1.5 |
| Audit sumber (file ini) | `article/drafts/source-audit.md` | ✅ Stage 0–1 |
| Evidence ledger (16 kolom) | `article/drafts/evidence-ledger.csv` | ⏳ Stage 2 |
| Matriks literatur | `article/drafts/literature-matrix.csv` | ⏳ Stage 3 |
| Verifikasi Crossref | `article/drafts/crossref_verify.json` | ⏳ Stage 3 |
| Outline | `article/drafts/article-outline.md` | ⏳ Stage 4 |
| Rencana figur/tabel | `article/drafts/figure-table-plan.md` | ⏳ Stage 4 |
| Diagram Mermaid | `article/scripts/Grapher/diagram/*.mmd` (+SVG) | ⏳ Stage 5 |
| Data chart | `article/scripts/Charter/raw/<slug>/{data.csv,provenance.json,README.md}` | ⏳ Stage 5 |
| Generator chart | `article/scripts/Charter/main.py` → `article/drafts/charts/*.png` | ⏳ Stage 6 |
| Naskah | `article/drafts/article-draft.md` → `article-draft.docx` | ⏳ Stage 7–8 |
| Metadata | `article/metadata.json` (title/keywords/cites) | ⏳ Stage 8 |

CLI Grapher terkonfirmasi: `npm run Grapher -- <input.mmd> <output.svg>
<theme.css>` (tsx + pele 1.13.0; tema `Grapher/themes/academic.css`).

## 10. Batas klaim naskah (checklist disiplin)

1. Fase A–C **wajib tampil** di Methods & Results (tidak boleh hilang).
2. "C++23 on-demand JSON parser exposed through a WebAssembly 64-bit
   binding"; scanner8 default; **dilarang** klaim "SIMD-accelerated".
3. S = T_V8/T_ZE konsisten di naskah/tabel/label chart (estimand §6).
4. D = repository-level; E = endpoint-level; tidak ada inferensi lintas-boundary
   sebagai bukti kausal; dev vs server = narasi kontekstual.
5. Negatif result dilaporkan (file-store <1×; E dev CI memuat 1; acceptance
   ≥1,5× tidak tercapai di fase E kedua site; server D-file 0,987×).
6. Tidak mengarang author/afiliasi/funding/tanggal; author hanya dari
   `article/metadata.json`; Declaration of AI Use sesuai policy AVITEC.
7. Artifacts tidak mengubah: hasil eksperimen, source code, submodule pointer,
   raw exhibit, validated record; eksperimen baru dilarang.
