# Stage 5 — Research Question and Scientific Framing Audit

The original thesis proposal and supervisor submission are **excluded by owner instruction**; this audit evaluates the manuscript's RQs against the actual experiments only. No historical hypothesis is treated as tested unless the measured variables support it.

## 1. RQ1 — access-pattern boundary (phases A–C)

Manuscript wording: "How does the JSON access pattern — full materialization, partial projection, or selective traversal — affect the relative performance of the two parsers (phases A–C)?"

| Check | Evidence | Verdict |
|---|---|---|
| Are A, B, C actually three different access patterns on the same corpus? | A `v8-parse`/`ze-parse`; B `v8-selective`/`ze-project-selective`; C `v8-selective`/`ze-l1-traversal` (`nd6_bench.mjs` L244–313; Stage 1/2) | PASS |
| Does the design support a *relative* (ratio) answer rather than universal ranking? | 15 paired rounds per cell, `S = median(V8)/median(ZE)`, CI per boundary (Stage 3) | PASS |
| Do the measured directions match the framing? | A all 12 cells <1; B all 12 <1; C heterogeneous with CI crossing/inside/below 1 (Tables 3–5) | PASS |
| Is any unmeasured variable implied? | No memory/CPU/energy claims; mechanism explicitly labeled interpretation (Stage 4 #20) | PASS |

**Verdict: PASS.** RQ1 is answered within the measured access boundaries; the article must not generalize beyond them.

## 2. RQ2 — repository boundary (phase D)

Manuscript wording: "Does an on-demand advantage appear at the repository boundary of a real state-store workload (phase D)?"

| Check | Evidence | Verdict |
|---|---|---|
| Is the repository boundary actually measured? | Two stores, four paths `D-{mongo-cache,file-store}-{v8,ze}`; 15 paired rounds (Stage 2) | PASS |
| Does the wording isolate the parser? | No — it asks about an *advantage at the repository boundary*; manuscript explicitly states store design + parser, not parser-only (Methods/Results/Table 8) | PASS |
| Are negative results retained? | File-store S = 0.9526 / 0.9871 with CI including 1, reported in full | PASS |
| Cold-cache qualifier present? | Yes; `_ensureCacheBytes()` built lazily, cold transition not timed (`MongoJsonRepository.js` L114–131; Results D) | PASS |

**Verdict: PASS.** RQ2 must remain a repository-design question; no parser-only claim is permitted.

## 3. RQ3 — HTTP endpoint boundary (phase E)

Manuscript wording: "Does it transfer to a complete HTTP endpoint (phase E)?"

| Check | Evidence | Verdict |
|---|---|---|
| Is the endpoint actually measured end-to-end? | `GET /rekap`: middleware → 4 repo reads/counts → EJS render → response; 15 rounds × 20 requests (10+10), 300 requests/run, parity gate (Stage 2 §4; `rekapRoutes.js` L25–47) | PASS |
| Does the result support unqualified "transfer"? | No: dev runs 1.0501 [0.9347–1.1473] and 1.0278 [0.9740–1.1143] include 1; server 1.1544 [1.0845–1.1751] >1. Distinguishability differs by site | WARN (wording) |
| Is parsing isolated? | No; RQ asks about endpoint latency, and manuscript states non-parser work included | PASS |

**Verdict: WARN (resolved in Stage 7).** The question was scoped correctly, but the binary phrase "Does it transfer" invited an all-or-nothing reading the data do not support. Stage 7 revised it to: "To what extent does the repository-level difference persist in the end-to-end latency of `GET /rekap` (phase E)?"; the site-specific verdicts remain explicit in the Results.

## 4. Prohibition checks

| Prohibition | Status |
|---|---|
| Claim RQ2 isolates parser | Not present; explicitly denied |
| Claim RQ3 isolates parsing latency | Not present; explicitly denied |
| Claim proposal hypotheses were tested | Not present (and proposal excluded) |
| Claim universal on-demand superiority | Not present; A/B favor V8 and D file-store is a negative result |

## 5. Stage 5 gate

**WARN** — RQ1/RQ2 fully supported; RQ3 requires the wording refinement above. No scientific blocker. Stage 6 (literature audit) authorized.
