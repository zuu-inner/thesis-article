# Statistical Recomputation Report — AVITEC Manuscript

> Generated 2026-11-18 by `article/scripts/Ledger/audit_orientation.py` at HEAD `a1fad918a7fccb6464722ac35723c29800ba7849`. Read-only on all raw evidence; no experiment, record, exhibit, or corpus was modified.

## 1. Locked estimand and protocol

- $S = T_{V8}/T_{ZE}$; $T_{V8}$ = `JSON.parse` time, $T_{ZE}$ = on-demand wasm64 parser time.
- Primary estimand: $\hat\theta = \operatorname{median}(T_{V8,i}) / \operatorname{median}(T_{ZE,i})$ over 15 paired rounds (**ratio of across-round medians**, not the median of paired ratios).
- Within-round aggregation: A–D = harness `rounds_ms` (mean of reps); E = median of 10 requests per engine per round (20 requests TOTAL/round).
- CI: paired round-level percentile bootstrap, $B=10{,}000$, seed `20261117`, resampling the 15 pairs jointly; BCa (log scale, jackknife acceleration) computed as sensitivity only.

## 2. Deterministic validation

| Check | Result |
|---|---|
| `build_ledger.py` run twice, ledger SHA-256 identical | PASS |
| `build_ledger.py` run twice, provenance SHA-256 identical | PASS |
| Canonical ledger SHA-256 | `800218af02b4fdc3d18147dfcebd404b93c53e371908dc505fa56bbcee4311eb` |
| Canonical provenance SHA-256 | `1e5f1ee1207eb5179723131a851f6126d8a50c6d33b383910231fc9be6974db7` |
| Cells recomputed from raw exhibits | 63 |
| Cell-level verification | {'MATCH': 63} |
| Pairing (V8/ZE same round index) | preserved in every bootstrap replicate |
| Bootstrap replicates / seed / CI | 10,000 / 20261117 / percentile 95% |
| Hand-entered numbers | none |

## 3. Old versus new values (all 63 cells)

`Old S/CI` = value in the reviewed PDF (canonical ledger / Tables 3–7). `New S/CI` = independent recomputation from the archived raw exhibit. The numbers are **unchanged**; the manuscript's interpretation of A–C is what was corrected.

| Phase | Site / Run | Cell | Old S | New S | Old CI | New CI | Verification |
|---|---|---|---:|---:|---|---|---|
| A | dev_device (6d87bf3) | courses | 0.0494 | 0.0494 | [0.0385, 0.0631] | [0.0385, 0.0631] | MATCH |
| A | dev_device (6d87bf3) | assistants | 0.0544 | 0.0544 | [0.0356, 0.0620] | [0.0356, 0.0620] | MATCH |
| A | dev_device (6d87bf3) | lecturers | 0.0428 | 0.0428 | [0.0361, 0.0509] | [0.0361, 0.0509] | MATCH |
| A | dev_device (6d87bf3) | schedules | 0.0446 | 0.0446 | [0.0390, 0.0500] | [0.0390, 0.0500] | MATCH |
| A | dev_device (6d87bf3) | reports | 0.0613 | 0.0613 | [0.0501, 0.0688] | [0.0501, 0.0688] | MATCH |
| A | dev_device (6d87bf3) | globalConfig | 0.0445 | 0.0445 | [0.0424, 0.0532] | [0.0424, 0.0532] | MATCH |
| B | dev_device (6d87bf3) | courses | 0.1229 | 0.1229 | [0.0763, 0.1361] | [0.0763, 0.1361] | MATCH |
| B | dev_device (6d87bf3) | assistants | 0.1059 | 0.1059 | [0.0779, 0.1172] | [0.0779, 0.1172] | MATCH |
| B | dev_device (6d87bf3) | lecturers | 0.0755 | 0.0755 | [0.0678, 0.1233] | [0.0678, 0.1233] | MATCH |
| B | dev_device (6d87bf3) | schedules | 0.1287 | 0.1287 | [0.1158, 0.1386] | [0.1158, 0.1386] | MATCH |
| B | dev_device (6d87bf3) | reports | 0.1594 | 0.1594 | [0.0808, 0.1651] | [0.0808, 0.1651] | MATCH |
| B | dev_device (6d87bf3) | globalConfig | 0.0987 | 0.0987 | [0.0639, 0.1716] | [0.0639, 0.1716] | MATCH |
| C | dev_device (6d87bf3) | courses | 0.9223 | 0.9223 | [0.7527, 1.1191] | [0.7527, 1.1191] | MATCH |
| C | dev_device (6d87bf3) | assistants | 1.1680 | 1.1680 | [0.9287, 1.2401] | [0.9287, 1.2401] | MATCH |
| C | dev_device (6d87bf3) | lecturers | 1.0455 | 1.0455 | [0.8701, 1.1343] | [0.8701, 1.1343] | MATCH |
| C | dev_device (6d87bf3) | schedules | 1.6454 | 1.6454 | [1.5058, 1.9726] | [1.5058, 1.9726] | MATCH |
| C | dev_device (6d87bf3) | reports | 0.2861 | 0.2861 | [0.2382, 0.3228] | [0.2382, 0.3228] | MATCH |
| C | dev_device (6d87bf3) | globalConfig | 0.0452 | 0.0452 | [0.0353, 0.0595] | [0.0353, 0.0595] | MATCH |
| D | dev_device (6d87bf3) | repository/mongo-cache | 2.8802 | 2.8802 | [2.5724, 3.0451] | [2.5724, 3.0451] | MATCH |
| D | dev_device (6d87bf3) | repository/file-store | 0.9526 | 0.9526 | [0.7673, 1.1093] | [0.7673, 1.1093] | MATCH |
| A | saq_server (8a1324b) | courses | 0.0493 | 0.0493 | [0.0426, 0.0549] | [0.0426, 0.0549] | MATCH |
| A | saq_server (8a1324b) | assistants | 0.0669 | 0.0669 | [0.0472, 0.0689] | [0.0472, 0.0689] | MATCH |
| A | saq_server (8a1324b) | lecturers | 0.0520 | 0.0520 | [0.0479, 0.0550] | [0.0479, 0.0550] | MATCH |
| A | saq_server (8a1324b) | schedules | 0.0569 | 0.0569 | [0.0495, 0.0580] | [0.0495, 0.0580] | MATCH |
| A | saq_server (8a1324b) | reports | 0.0576 | 0.0576 | [0.0494, 0.0596] | [0.0494, 0.0596] | MATCH |
| A | saq_server (8a1324b) | globalConfig | 0.0501 | 0.0501 | [0.0482, 0.0532] | [0.0482, 0.0532] | MATCH |
| B | saq_server (8a1324b) | courses | 0.1228 | 0.1228 | [0.1034, 0.1326] | [0.1034, 0.1326] | MATCH |
| B | saq_server (8a1324b) | assistants | 0.1130 | 0.1130 | [0.0692, 0.1170] | [0.0692, 0.1170] | MATCH |
| B | saq_server (8a1324b) | lecturers | 0.0828 | 0.0828 | [0.0729, 0.1260] | [0.0729, 0.1260] | MATCH |
| B | saq_server (8a1324b) | schedules | 0.1282 | 0.1282 | [0.1209, 0.1383] | [0.1209, 0.1383] | MATCH |
| B | saq_server (8a1324b) | reports | 0.1436 | 0.1436 | [0.0860, 0.1583] | [0.0860, 0.1583] | MATCH |
| B | saq_server (8a1324b) | globalConfig | 0.1043 | 0.1043 | [0.0735, 0.1594] | [0.0735, 0.1594] | MATCH |
| C | saq_server (8a1324b) | courses | 0.8561 | 0.8561 | [0.7492, 1.0427] | [0.7492, 1.0427] | MATCH |
| C | saq_server (8a1324b) | assistants | 1.4194 | 1.4194 | [1.2267, 1.4548] | [1.2267, 1.4548] | MATCH |
| C | saq_server (8a1324b) | lecturers | 0.9562 | 0.9562 | [0.9052, 0.9767] | [0.9052, 0.9767] | MATCH |
| C | saq_server (8a1324b) | schedules | 1.4983 | 1.4983 | [1.0874, 1.5556] | [1.0874, 1.5556] | MATCH |
| C | saq_server (8a1324b) | reports | 0.3087 | 0.3087 | [0.2581, 0.3280] | [0.2581, 0.3280] | MATCH |
| C | saq_server (8a1324b) | globalConfig | 0.0469 | 0.0469 | [0.0392, 0.0531] | [0.0392, 0.0531] | MATCH |
| D | saq_server (8a1324b) | repository/mongo-cache | 2.6654 | 2.6654 | [2.5083, 2.8573] | [2.5083, 2.8573] | MATCH |
| D | saq_server (8a1324b) | repository/file-store | 0.9871 | 0.9871 | [0.9705, 1.0387] | [0.9705, 1.0387] | MATCH |
| E | dev_device (8556513) | http GET /rekap end-to-end | 1.0501 | 1.0501 | [0.9347, 1.1473] | [0.9347, 1.1473] | MATCH |
| E | dev_device (6979e3f) | http GET /rekap end-to-end | 1.0278 | 1.0278 | [0.9740, 1.1143] | [0.9740, 1.1143] | MATCH |
| E | saq_server (530f751) | http GET /rekap end-to-end | 1.1544 | 1.1544 | [1.0845, 1.1751] | [1.0845, 1.1751] | MATCH |
| A | dev_device (3376d07) | courses | 0.0522 | 0.0522 | [0.0412, 0.0549] | [0.0412, 0.0549] | MATCH |
| A | dev_device (3376d07) | assistants | 0.0477 | 0.0477 | [0.0367, 0.0558] | [0.0367, 0.0558] | MATCH |
| A | dev_device (3376d07) | lecturers | 0.0480 | 0.0480 | [0.0413, 0.0525] | [0.0413, 0.0525] | MATCH |
| A | dev_device (3376d07) | schedules | 0.0503 | 0.0503 | [0.0449, 0.0567] | [0.0449, 0.0567] | MATCH |
| A | dev_device (3376d07) | reports | 0.0474 | 0.0474 | [0.0434, 0.0559] | [0.0434, 0.0559] | MATCH |
| A | dev_device (3376d07) | globalConfig | 0.0426 | 0.0426 | [0.0380, 0.0447] | [0.0380, 0.0447] | MATCH |
| B | dev_device (3376d07) | courses | 0.1121 | 0.1121 | [0.0861, 0.1367] | [0.0861, 0.1367] | MATCH |
| B | dev_device (3376d07) | assistants | 0.0984 | 0.0984 | [0.0748, 0.1220] | [0.0748, 0.1220] | MATCH |
| B | dev_device (3376d07) | lecturers | 0.0777 | 0.0777 | [0.0712, 0.1182] | [0.0712, 0.1182] | MATCH |
| B | dev_device (3376d07) | schedules | 0.1262 | 0.1262 | [0.1029, 0.1581] | [0.1029, 0.1581] | MATCH |
| B | dev_device (3376d07) | reports | 0.1070 | 0.1070 | [0.0802, 0.1584] | [0.0802, 0.1584] | MATCH |
| B | dev_device (3376d07) | globalConfig | 0.0898 | 0.0898 | [0.0672, 0.1901] | [0.0672, 0.1901] | MATCH |
| C | dev_device (3376d07) | courses | 0.7891 | 0.7891 | [0.6675, 1.0005] | [0.6675, 1.0005] | MATCH |
| C | dev_device (3376d07) | assistants | 1.0254 | 1.0254 | [0.9742, 1.1919] | [0.9742, 1.1919] | MATCH |
| C | dev_device (3376d07) | lecturers | 0.8529 | 0.8529 | [0.8060, 0.9586] | [0.8060, 0.9586] | MATCH |
| C | dev_device (3376d07) | schedules | 1.4970 | 1.4970 | [1.4532, 1.5596] | [1.4532, 1.5596] | MATCH |
| C | dev_device (3376d07) | reports | 0.2652 | 0.2652 | [0.2273, 0.3140] | [0.2273, 0.3140] | MATCH |
| C | dev_device (3376d07) | globalConfig | 0.0498 | 0.0498 | [0.0352, 0.0738] | [0.0352, 0.0738] | MATCH |
| D | dev_device (3376d07) | repository/mongo-cache | 2.3989 | 2.3989 | [1.9596, 2.9061] | [1.9596, 2.9061] | MATCH |
| D | dev_device (3376d07) | repository/file-store | 0.9495 | 0.9495 | [0.8698, 1.0922] | [0.8698, 1.0922] | MATCH |

## 4. Reciprocal cross-check (diagnostic only)

The reviewed manuscript described $S=0{,}0494$ for A/dev/courses as “the baseline spends 15–23× longer”. Numerically $1/S = 20{,}2357$, which is exactly the reciprocal of the reported ratio. This confirms that the old *text* read $S$ as $T_{ZE}/T_{V8}$; the value itself is correct for $S=T_{V8}/T_{ZE}$ (`v8-parse` median 0.012787 ms vs `ze-parse` median 0.258747 ms). No reciprocal was applied to any reported number.

## 5. Phase D and E verification

- D: mongo-cache $S=2{,}8802$ [2,5724–3,0451] (dev) and $2{,}6654$ [2,5083–2,8573] (server); both CIs entirely above 1 → ZE faster. File-store $S=0{,}9526$ [0,7673–1,1093] and $0{,}9871$ [0,9705–1,0387]; CIs include 1 → not distinguishable. **Unchanged.**
- E: dev `8556513` $S=1{,}0501$ [0,9347–1,1473], dev `6979e3f` $S=1{,}0278$ [0,9740–1,1143], server `530f751` $S=1{,}1544$ [1,0845–1,1751]. Legacy pooled ratios 1.076/1.041/1.134 verified at `reports/nd11-phase-d-e-synthesis.md` L19–21, L139–141; they are descriptive, not the estimand. **Unchanged.**

## 6. BCa sensitivity

BCa intervals (log scale, jackknife acceleration, same seed and resamples) are recorded per cell in `article/data/json/orientation-audit.json` under `bca_CI`. They are sensitivity only and do not replace the percentile CI; the manuscript's claim that a BCa variant was computed is thereby backed by a deterministic derived artifact.

## 7. Conclusion

All 63 cells reproduce exactly from raw exhibits under the locked estimand. No numeric value required correction; the blocker was an inverted *interpretation* of phases A–C, corrected in the manuscript source. Negative results and intervals containing 1 are retained. No hypothesis verdict, CPU/memory/energy claim, or cross-run pooling is introduced.
