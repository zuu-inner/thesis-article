# Stage 3 — Statistical Audit

> Recomputed 2026-11-19 with an implementation independent of the manuscript tables. Derived artifacts: `article/data/json/final-audit-statistics.json`, `article/data/json/orientation-audit.json`.

## 1. Locked estimand and estimator

$$S = \frac{\operatorname{Median}(T_{V8,1},\ldots,T_{V8,15})}{\operatorname{Median}(T_{ZE,1},\ldots,T_{ZE,15})},\qquad\hat\theta = \frac{\operatorname{median}(v)}{\operatorname{median}(z)}$$

This is the **ratio of across-round medians**, not the median of 15 paired-round ratios. Interpretation: $S<1$ → V8 lower latency; $S>1$ → ZE lower latency; CI containing 1 → advantage not distinguishable at this design's precision. No reciprocal is applied to any reported value.

## 2. Locked bootstrap specification (verified)

| Parameter | Required | Verified |
|---|---|---|
| Inference unit | paired round | 15 pairs per cell |
| Resampling | joint V8/ZE round indices | `idx = rng.integers(0, 15, size=(10000, 15))`; both arrays indexed by same `idx` |
| Replicates | 10,000 | 10,000 |
| Seed / RNG | 20261117 / PCG64 | `numpy.random.default_rng(20261117)` → `PCG64`; first five draws reproduced exactly |
| Statistic per replicate | ratio of medians | `median(v[idx]) / median(z[idx])` — identical to point estimator |
| CI | percentile 95% | 2.5th / 97.5th percentiles of bootstrap distribution |
| BCa | sensitivity only | log-scale + jackknife acceleration, archived per cell; not primary |
| Request-level resampling | forbidden | 150 E requests are within-round observations, never treated as 150 independent units |

Exact sign and Wilcoxon tests: **not reported in the manuscript** (grep: no matches), therefore not applicable to this audit.

## 3. Raw inputs and within-round aggregation

| Phase | Input field | Within-round value | Source |
|---|---|---|---|
| A | `raw_rounds[].rounds_ms` for `v8-parse` / `ze-parse` | mean of reps (30 or 5) | `nd6_phase_{A}.json` |
| B | `v8-selective` / `ze-project-selective` | mean of reps | `nd6_phase_B.json` |
| C | `v8-selective` / `ze-l1-traversal` | mean of reps | `nd6_phase_C.json` |
| D | `D-{mongo-cache,file-store}-{v8,ze}` | mean of 2 reps | `nd6_phase_D.json` |
| E | `requests.{v8,ze}[{round,seconds}]` | median of 10 requests/engine/round | `nd11_phase_e.json` |

All cells use 15 rounds. The canonical ledger is `article/data/csv/evidence-ledger.csv` (63 rows).

## 4. Deterministic verification

| Check | Result |
|---|---|
| `build_ledger.py` run twice → ledger SHA-256 | identical: `800218af02b4fdc3d18147dfcebd404b93c53e371908dc505fa56bbcee4311eb` |
| `build_ledger.py` run twice → provenance SHA-256 | identical: `1e5f1ee1207eb5179723131a851f6126d8a50c6d33b383910231fc9be6974db7` |
| Independent recomputation (`audit_orientation.py`) | {'MATCH': 63} across 63 cells |
| BCa sensitivity computed | 63 cells |
| Hand-entered values | none |

## 5. Full 63-cell output (point, percentile CI, BCa sensitivity)

| Phase | Site / class | Cell | S | CI 95% | BCa CI | Status |
|---|---|---|---:|---|---|---|
| A | dev_device / primary | courses | 0.0494 | [0.0385, 0.0631] | [0.0377, 0.0601] | MATCH |
| A | dev_device / primary | assistants | 0.0544 | [0.0356, 0.0620] | [0.0426, 0.0649] | MATCH |
| A | dev_device / primary | lecturers | 0.0428 | [0.0361, 0.0509] | [0.0361, 0.0509] | MATCH |
| A | dev_device / primary | schedules | 0.0446 | [0.0390, 0.0500] | [0.0368, 0.0472] | MATCH |
| A | dev_device / primary | reports | 0.0613 | [0.0501, 0.0688] | [0.0521, 0.0744] | MATCH |
| A | dev_device / primary | globalConfig | 0.0445 | [0.0424, 0.0532] | [0.0428, 0.0536] | MATCH |
| B | dev_device / primary | courses | 0.1229 | [0.0763, 0.1361] | [0.0853, 0.1361] | MATCH |
| B | dev_device / primary | assistants | 0.1059 | [0.0779, 0.1172] | [0.0680, 0.1157] | MATCH |
| B | dev_device / primary | lecturers | 0.0755 | [0.0678, 0.1233] | [0.0668, 0.1223] | MATCH |
| B | dev_device / primary | schedules | 0.1287 | [0.1158, 0.1386] | [0.1159, 0.1392] | MATCH |
| B | dev_device / primary | reports | 0.1594 | [0.0808, 0.1651] | [0.0818, 0.1665] | MATCH |
| B | dev_device / primary | globalConfig | 0.0987 | [0.0639, 0.1716] | [0.0601, 0.1657] | MATCH |
| C | dev_device / primary | courses | 0.9223 | [0.7527, 1.1191] | [0.7442, 1.0700] | MATCH |
| C | dev_device / primary | assistants | 1.1680 | [0.9287, 1.2401] | [0.9649, 1.2665] | MATCH |
| C | dev_device / primary | lecturers | 1.0455 | [0.8701, 1.1343] | [0.8701, 1.1343] | MATCH |
| C | dev_device / primary | schedules | 1.6454 | [1.5058, 1.9726] | [1.4794, 1.9224] | MATCH |
| C | dev_device / primary | reports | 0.2861 | [0.2382, 0.3228] | [0.2555, 0.3374] | MATCH |
| C | dev_device / primary | globalConfig | 0.0452 | [0.0353, 0.0595] | [0.0356, 0.0611] | MATCH |
| D | dev_device / primary | repository/mongo-cache | 2.8802 | [2.5724, 3.0451] | [2.6483, 3.2489] | MATCH |
| D | dev_device / primary | repository/file-store | 0.9526 | [0.7673, 1.1093] | [0.7673, 1.1110] | MATCH |
| A | saq_server / primary | courses | 0.0493 | [0.0426, 0.0549] | [0.0423, 0.0548] | MATCH |
| A | saq_server / primary | assistants | 0.0669 | [0.0472, 0.0689] | [0.0472, 0.0690] | MATCH |
| A | saq_server / primary | lecturers | 0.0520 | [0.0479, 0.0550] | [0.0499, 0.0552] | MATCH |
| A | saq_server / primary | schedules | 0.0569 | [0.0495, 0.0580] | [0.0555, 0.0585] | MATCH |
| A | saq_server / primary | reports | 0.0576 | [0.0494, 0.0596] | [0.0491, 0.0596] | MATCH |
| A | saq_server / primary | globalConfig | 0.0501 | [0.0482, 0.0532] | [0.0408, 0.0508] | MATCH |
| B | saq_server / primary | courses | 0.1228 | [0.1034, 0.1326] | [0.0991, 0.1326] | MATCH |
| B | saq_server / primary | assistants | 0.1130 | [0.0692, 0.1170] | [0.0691, 0.1170] | MATCH |
| B | saq_server / primary | lecturers | 0.0828 | [0.0729, 0.1260] | [0.0729, 0.1260] | MATCH |
| B | saq_server / primary | schedules | 0.1282 | [0.1209, 0.1383] | [0.1187, 0.1376] | MATCH |
| B | saq_server / primary | reports | 0.1436 | [0.0860, 0.1583] | [0.0860, 0.1598] | MATCH |
| B | saq_server / primary | globalConfig | 0.1043 | [0.0735, 0.1594] | [0.0735, 0.1594] | MATCH |
| C | saq_server / primary | courses | 0.8561 | [0.7492, 1.0427] | [0.7465, 1.0249] | MATCH |
| C | saq_server / primary | assistants | 1.4194 | [1.2267, 1.4548] | [1.2949, 1.4609] | MATCH |
| C | saq_server / primary | lecturers | 0.9562 | [0.9052, 0.9767] | [0.9007, 0.9767] | MATCH |
| C | saq_server / primary | schedules | 1.4983 | [1.0874, 1.5556] | [1.0958, 1.5556] | MATCH |
| C | saq_server / primary | reports | 0.3087 | [0.2581, 0.3280] | [0.2408, 0.3238] | MATCH |
| C | saq_server / primary | globalConfig | 0.0469 | [0.0392, 0.0531] | [0.0414, 0.0581] | MATCH |
| D | saq_server / primary | repository/mongo-cache | 2.6654 | [2.5083, 2.8573] | [2.5083, 2.8573] | MATCH |
| D | saq_server / primary | repository/file-store | 0.9871 | [0.9705, 1.0387] | [0.9574, 1.0110] | MATCH |
| E | dev_device / primary | http GET /rekap end-to-end | 1.0501 | [0.9347, 1.1473] | [0.9560, 1.1557] | MATCH |
| E | dev_device / primary | http GET /rekap end-to-end | 1.0278 | [0.9740, 1.1143] | [0.9729, 1.1143] | MATCH |
| E | saq_server / primary | http GET /rekap end-to-end | 1.1544 | [1.0845, 1.1751] | [1.1048, 1.1836] | MATCH |
| A | dev_device / supporting | courses | 0.0522 | [0.0412, 0.0549] | [0.0440, 0.0565] | MATCH |
| A | dev_device / supporting | assistants | 0.0477 | [0.0367, 0.0558] | [0.0367, 0.0558] | MATCH |
| A | dev_device / supporting | lecturers | 0.0480 | [0.0413, 0.0525] | [0.0415, 0.0528] | MATCH |
| A | dev_device / supporting | schedules | 0.0503 | [0.0449, 0.0567] | [0.0438, 0.0553] | MATCH |
| A | dev_device / supporting | reports | 0.0474 | [0.0434, 0.0559] | [0.0409, 0.0527] | MATCH |
| A | dev_device / supporting | globalConfig | 0.0426 | [0.0380, 0.0447] | [0.0381, 0.0447] | MATCH |
| B | dev_device / supporting | courses | 0.1121 | [0.0861, 0.1367] | [0.0783, 0.1336] | MATCH |
| B | dev_device / supporting | assistants | 0.0984 | [0.0748, 0.1220] | [0.0654, 0.1158] | MATCH |
| B | dev_device / supporting | lecturers | 0.0777 | [0.0712, 0.1182] | [0.0684, 0.1124] | MATCH |
| B | dev_device / supporting | schedules | 0.1262 | [0.1029, 0.1581] | [0.1054, 0.1603] | MATCH |
| B | dev_device / supporting | reports | 0.1070 | [0.0802, 0.1584] | [0.0793, 0.1584] | MATCH |
| B | dev_device / supporting | globalConfig | 0.0898 | [0.0672, 0.1901] | [0.0562, 0.1274] | MATCH |
| C | dev_device / supporting | courses | 0.7891 | [0.6675, 1.0005] | [0.6071, 0.9826] | MATCH |
| C | dev_device / supporting | assistants | 1.0254 | [0.9742, 1.1919] | [0.9526, 1.1298] | MATCH |
| C | dev_device / supporting | lecturers | 0.8529 | [0.8060, 0.9586] | [0.7906, 0.9235] | MATCH |
| C | dev_device / supporting | schedules | 1.4970 | [1.4532, 1.5596] | [1.4376, 1.5513] | MATCH |
| C | dev_device / supporting | reports | 0.2652 | [0.2273, 0.3140] | [0.2250, 0.2981] | MATCH |
| C | dev_device / supporting | globalConfig | 0.0498 | [0.0352, 0.0738] | [0.0368, 0.0760] | MATCH |
| D | dev_device / supporting | repository/mongo-cache | 2.3989 | [1.9596, 2.9061] | [1.9622, 2.9638] | MATCH |
| D | dev_device / supporting | repository/file-store | 0.9495 | [0.8698, 1.0922] | [0.8357, 1.0437] | MATCH |

Selected interpretation checks: A/dev/courses $S=0{,}0494$ [0,0385–0,0631] → V8 faster (reciprocal 20,2357 matches the old, incorrect narrative); D/dev/mongo $S=2{,}8802$ [2,5724–3,0451] → ZE faster; E/server $S=1{,}1544$ [1,0845–1,1751] → ZE faster; E/dev runs include 1 → not distinguishable.

## 6. Estimator consistency

Point and CI target the same ratio-of-round-medians in every cell. The legacy pooled-request ratios (1.076 / 1.041 / 1.134) are descriptive only and appear once as a table note under Table 7, never as a primary point estimate paired with a round-level CI.

## 7. Stage 3 verdict

**PASS** — estimand, pairing, aggregation, RNG, replicate count, CI method, and orientation are verified; two independent runs are byte-identical; all 63 cells reproduce from raw exhibits. Stage 4 (claim-by-claim audit) is authorized.
