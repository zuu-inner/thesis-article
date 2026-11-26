# Stage 4 — Claim-to-Evidence Matrix

Scope: current working manuscript `article/drafts/article-draft.md` (read in full, 2026-11-19) and its generated DOCX. Evidence hierarchy: raw records/exhibits → protocol → implementation → deterministic ledger → reports → manuscript. Stage 2/3 reports supply the recomputed values.

Verdict key: **PASS** = claim directly supported; **WARN** = plausible but not measured or over-broad; **FAIL** = contradicted/misleading, requires correction.

| # | Section / para | Claim (concise quotation) | Evidence file & location | Run/ID, field/function | Verification | Verdict | Required correction |
|---:|---|---|---|---|---|---|---|
| 1 | Abstract | "on-demand path is 16–23× slower than V8 (S = 0.04–0.07)" | `data/csv/evidence-ledger.csv` A rows; `out/raw/zuu-20261115071747-6d87bf3/nd6_phase_A.json` | `v8-parse`/`ze-parse`, 15 rounds | 1/S of 12 cells = 16.3–23.3; audit §4 | PASS | none |
| 2 | Abstract | "6–13× slower (S = 0.08–0.16)" | ledger B rows | `v8-selective`/`ze-project-selective` | 1/S = 6.27–13.24 | PASS | none |
| 3 | Abstract | "D 2.88× (2.67× server); file-store no advantage" | ledger D rows; Stage 2 §3 | `D-mongo-cache-*`, `D-file-store-*` | CI >1 / includes 1 | PASS | none |
| 4 | Abstract | "E not distinguishable dev (1.05/1.03), modest server (1.15)" | ledger E rows; `nd11_phase_e.json` | requests 10+10/round | dev CIs include 1; server CI >1 | PASS | none |
| 5 | Intro ¶1 | "the application also pays allocation, property-creation, and garbage-collection costs for content it never reads" | no measurement of allocation/GC in this study | — | Mechanism claim; protocol is latency-only | WARN | soften to "can incur" and label as general V8 behavior, not measured here |
| 6 | Intro ¶2 | "adopted by production systems, including the Node.js runtime itself [2]" | ref [2] (Keiser & Lemire, SPE 2024) | — | to be checked in Stage 6; not directly evidenced by experiments | WARN | keep only if ref [2] supports; else remove "Node.js runtime itself" |
| 7 | Intro ¶3 | "Several of these primitives are integrated in V8 and Node.js, which makes them the de-facto floor" | no direct measurement of primitive integration | — | background claim | WARN | soften to "motivate the baseline" |
| 8 | Methods ¶1 | "alternative vectorized scanners measured slower in this configuration during development" | `ze_json/src/ondemand/parallel.cpp` L294–305 | P4-2 run `zuu-20261109053632-85afad7` | source comment + measured medians | PASS | none |
| 9 | Methods ¶1 | "default byte-level scanner (scanner8)" | `parallel.cpp` L287–311; `ze_json.mjs` L58–62, L192 | `structural_scan()` returns `&scanner8` | verified Stage 1 | PASS | none; do not call it SIMD-accelerated |
| 10 | Methods ¶1 | "wasm64 ... allowing corpus documents and derived structures to coexist with the JavaScript heap" | `cabi.cpp` L90–120 (bump heap), `Arena`/slots | — | architectural fact, not measured | WARN | phrase as design property, not measured result |
| 11 | Methods ¶3 | "regeneration with the same seed is byte-identical" | `corpus/.../MANIFEST.json` generation.seed=20261108; Stage 2 §5 | 6 file hashes | manifest + on-disk hashes match; determinism stated | PASS | none |
| 12 | Protocol | "three untimed warmup iterations per path, then 15 measured rounds" | records `config.warmup_runs=3`, `config.repeats=15`; harness | A–E | verified Stage 2 metadata | PASS | none |
| 13 | Protocol | "all 11 primary records pass [validator]" | `scripts/measurement-schema/validate.py` | 11 record paths | re-run: 11 PASS / 0 FAIL | PASS | none |
| 14 | Inference | "ratio of across-round medians, not median of paired ratios" | `build_ledger.py` L138; Stage 3 | `median(v)/median(z)` | verified | PASS | none |
| 15 | Inference | "fixed seed 20261117" + BCa sensitivity archived | `orientation-audit.json`, Stage 3 | PCG64, B=10000 | verified twice | PASS | none |
| 16 | Reproducibility | "Supporting runs ... corroborate every directional conclusion reported here" | ledger supporting rows; E has no supporting runs | `3376d07` A–D only | A–D ordering and D shape reproduce; E does not have supporting runs | **FAIL** | restrict to "A–D per-document ordering and repository shape" |
| 17 | Results A | "crossing-heavy on-demand path loses to the engine's highly optimized built-in parser" | no crossing-count comparison in A | A exhibit records `binding_calls` but no causal isolation | plausible explanation, not measured | WARN | label as plausible explanation, not established mechanism |
| 18 | Results B | "on-demand projection 6–13× slower; intervals <1" | ledger B rows | 12 cells | verified Stage 2 | PASS | none |
| 19 | Results C | per-payload direction and CI readings | ledger C rows | 12 cells | verified | PASS | none |
| 20 | Results C | cost-model reading "consistent interpretation rather than a proven mechanism" | no per-field access counts | — | explicitly labeled | PASS | none; keep disclaimer |
| 21 | Results D | "2.88/2.67 ... largest advantage anywhere" | ledger D + A–C/E | all 43 cells | max S = 2.88 | PASS | none |
| 22 | Results D | "warm-cache steady state a production server reaches after its first read" | `MongoJsonRepository.js` L114–131 | `_ensureCacheBytes` invalidated on write | cache lifecycle in code; steady state not timed | WARN | phrase as design consequence, not measured production behavior |
| 23 | Results E | "four repository reads + EJS render + HTTP stack" | `saq-report/routes/rekapRoutes.js` L25–47 | 4 `readCount()`/`read().length`, `res.render` | verified Stage 1 | PASS | none; no other routes claimed |
| 24 | Results E | legacy pooled ratios only in Table 7 note | Table 7 note; ledger | 1.076/1.041/1.134 | verified in report L19–21/L139–141 | PASS | none |
| 25 | Discussion | "Every crossing ... costs parameter marshalling and a runtime switch ... delivery overhead disappears into a 2.7–2.9× win" | no crossing count or marshalling timing measured | — | architectural explanation | WARN | label as explanatory hypothesis, not measured result |
| 26 | Discussion | "fixed seed control order and start-up effects" | bootstrap seed only affects resampling | `default_rng(20261117)` | **wrong attribution**: order/startup handled by rotation+warmup, not seed | **FAIL** | rewrite: rotation/warmup address order/startup; fixed seed only makes bootstrap reproducible |
| 27 | Comparison | "crossing cost, per-call binding overhead, optimized V8 parser overwhelm the lazy strategy" | no isolation of crossing cost | — | plausible causal story | WARN | label as interpretation consistent with data, not experimentally isolated |
| 28 | Threats | "does not measure memory, CPU time, energy; cold-cache unmeasured" | protocol config, records | — | verified | PASS | none |
| 29 | Threats | "cells whose CI contains 1 ... never equality" | ledger/Stage 3 | — | verified | PASS | none |
| 30 | Conclusion | all numeric summary + boundary limits | Stage 2/3 | — | verified | PASS | none |

## Required corrections summary

1. **FAIL #26** — remove the claim that a fixed bootstrap seed controls order/start-up effects.
2. **FAIL #16** — narrow the supporting-run claim to A–D ordering and repository shape.
3. **WARN #5, #7, #10, #17, #22, #25, #27** — soften unmeasured mechanism/causal phrasing; explicitly label as plausible explanations or design properties.
4. **WARN #6** — conditional on Stage 6 verifying what ref [2] actually supports.

## Stage 4 gate

**WARN** — no numerical or statistical failure; 2 FAIL + 7 WARN are wording/attribution issues resolved in Stage 7. Stages 5–6 authorized.
