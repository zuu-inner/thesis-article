# Figure & Table Plan — AVITEC Article

> Stage 4. Setiap figur/tabel: sumber data (ledger/raw), generator, caption
> draft (English), dan aturan pelabelan. Semua angka traceable ke
> `evidence-ledger.csv` / raw exhibit (bukan laporan PR #79).

## A. Diagram (Mermaid → SVG, Pele) — `article/scripts/Grapher/diagram/`

CLI: `npm run Grapher -- <input.mmd> <output.svg> <theme.css>` (di
`article/scripts/`, tema `Grapher/themes/academic.css`). Singular folder
`diagram/` (folder `diagrams/` plural kosong didokumentasikan; tidak dipakai).

| File | Konten | Dipakai |
|---|---|---|
| `fig1-boundaries.mmd` | flowchart LR: pipeline saq-report → 5 boundary A–E (access layer → repository → HTTP endpoint), V8 path vs ZE path | Fig. 1 (Methods §2.2) |
| `fig2-measurement-protocol.mmd` | flowchart: run structure (warmup → 15 rounds → per-path reps / per-request alternation → parity gate → record+exhibit → validator → ledger → estimand+bootstrap) | Fig. 2 (Methods §2.3–2.4) |
| `fig3-decision-flow.mmd` | flowchart TD: inferensi (round medians → paired resample → CI → interpretasi CI vs 1 → per-boundary claim discipline) | Fig. 3 (Methods §2.4) |

Catatan: diagram digenerate dengan bantuan agent (AI-assisted) — dicantumkan
pada caption/declaration sesuai AI Policy.

## B. Chart (Matplotlib, bukan Seaborn) — `article/scripts/Charter/main.py`

Deterministik: CLI `python main.py --raw article/scripts/Charter/raw --out
article/drafts/charts --dpi 1000`; membaca CSV `raw/`, tanpa angka hardcode;
tema garis 1.0× selalu tampil; hasil negatif & ketidakpastian (CI) tampil.
Output PNG (raster, ≥1.000 dpi sesuai guideline AVITEC line-art) + SVG.

| Slug (raw dir) | Chart | Isi |
|---|---|---|
| `diagnostic-phase-speedup` | **Chart 1** — grouped bar (log y) per payload: 6 dokumen × (A,B,C) × 2 site; garis 1.0×; nilai <1 (ZE menang) & >1 (V8 menang) tampil | data.csv: phase,site,doc,point,lo,hi |
| `repository-phase-d-results` | **Chart 2** — forest plot D: 4 sel (dev/server × mongo-cache/file-store), point + CI 95%, garis 1.0× | data.csv: site,store,point,lo,hi |
| `http-endpoint-phase-e-results` | **Chart 3** — forest plot E: 3 run (dev ×2, server), point + CI, garis 1.0× | data.csv: site,run,point,lo,hi |

Caption draft (AI-assistance dicantumkan):
- Fig. 4 (Chart 1): "Per-payload speedup S = T_V8/T_ZE at the access-pattern
  boundaries (A: full materialization, B: partial projection, C: selective
  traversal) on both sites. Bars show the ratio of round-level medians
  (15 paired rounds); whiskers show bootstrap 95% CIs. Values below 1 favor
  the on-demand parser. Note the logarithmic scale."
- Fig. 5 (Chart 2): "Repository-boundary speedups (Phase D). Mongo-cache =
  warmed canonical-bytes path; file store = I/O-bound path. Error bars:
  95% paired-bootstrap CIs."
- Fig. 6 (Chart 3): "HTTP endpoint speedups (Phase E, GET /rekap) for the two
  dev-device runs and the server run. Error bars: 95% paired-bootstrap CIs;
  intervals including 1.0 indicate the advantage is not distinguishable at
  this design's precision."

## C. Tabel (naskah)

| No | Judul | Isi | Sumber |
|---|---|---|---|
| T1 | Corpus `saq_payload_v1` | 6 dokumen, bytes, sha256 (disingkat), peran store | MANIFEST.json |
| T2 | Run provenance | run_id, site, commit, core/js/ABI, Node/V8, wasm sha (disingkat), class primary/supporting | ledger kolom 5–11 |
| T3 | Phase A results | per doc × site: point [CI] | ledger A rows |
| T4 | Phase B results | per doc × site: point [CI] | ledger B rows |
| T5 | Phase C results | per doc × site: point [CI] | ledger C rows |
| T6 | Phase D results | store × site: point [CI] + interpretasi | ledger D rows |
| T7 | Phase E results | 3 run: point [CI] (+ pooled convention footnote) | ledger E rows |
| T8 | Claim-boundary matrix | fase × apa yang diukur × klaim sah | outline §6 |

Format angka tabel: `2.88 [2.57, 3.05]` (2 desimal; S tanpa "×" di kolom, "×"
disebut di header: "Speedup S = T_V8/T_ZE").

## D. Aturan konsistensi

1. Semua "speedup" = S = T_V8/T_ZE (>1 = on-demand faster) — tidak pernah
   dibalik.
2. CI selalu dilampirkan untuk hasil inferensial (D, E); A–C deskriptif
   per-doc dengan CI tetap ditampilkan (hasil bootstrap sama prosedurnya).
3. Nilai <1 dilaporkan apa adanya (file-store, C reports/globalConfig).
4. Angka era Node 24 (2.85×/3.00×; server 1.30×) hanya muncul di Discussion
   sebagai narasi berlabel runtime lama — bukan bagian hasil.
5. Pooled-request convention (1.076/1.041/1.134) hanya sebagai catatan kaki T7.
