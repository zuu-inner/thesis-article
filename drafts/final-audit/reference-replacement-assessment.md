# Reference Replacement Assessment

Date: 2026-11-19 · Follow-up to `reference-eligibility-audit.md`. No manuscript, bibliography, literature matrix, raw evidence or chart was modified.

## 1. Executive Summary

**Updated 2026-11-20 (supersedes earlier wording; see §14, §16):** Requirement A is **PASS** — 19 confirmed peer-reviewed journal articles in the Introduction (11 Qualified + eight Wiley articles with publisher review history), against AVITEC's minimum of 15; [20] remains Uncertain for peer review. Requirement B is **FAIL** — 11/28 = 39.29% Qualified, upper bound 20/28 = 71.43%. Wiley reclassification did not change eligibility: the nine SPE references remain Uncertain because official Wiley international-scope evidence could not be retrieved (403 direct; CAPTCHA via text proxy; web search unavailable). Only [23]→C1 is an approved replacement; no valid replacement exists for [10] or [24]. The conditional 23/28 = 82.14% scenario is **not** achieved in the bibliography.

## 2. Wiley Reclassification Results

All nine DOIs are Crossref `journal-article` in SPE. First-online vs issue dates are documented in the eligibility matrix; the manuscript's issue-year convention is retained. Official Wiley pages were inaccessible. [20] article category remains unverified. Eligibility unchanged: Uncertain.

## 3. Updated Eligibility Counts

| Status | Count |
|---|---:|
| Qualified | 11 |
| Uncertain | 9 |
| Not Qualified | 8 |
| Total | 28 |

Requirement A: **19 confirmed peer-reviewed journal articles in Introduction ≥ 15 → PASS** (the earlier '11 → FAIL' statement is SUPERSEDED by §14 and audit §24). Requirement B: **11/28 = 39.29%** confirmed / upper bound 20/28 = 71.43% → **FAIL** (<80%). Qualified, not total journal articles, is the Requirement B numerator.

## 4. Eight Not Qualified Reference Assessments

| Ref | Claim/function | Recommendation | Rationale |
|---:|---|---|---|
| [1] | RFC 8259 JSON standard | RETAIN | Foundational technical standard; removing it would harm compliance discussion, not improve scientific quality. |
| [6] | JSONSki bit-parallel fast-forwarding | RETAIN_AND_SUPPLEMENT | Specific technique with no verified journal equivalent found; supplement via [9] FAD.js (journal) and C3 Blaze. |
| [7] | JPStream joint query/parse compilation | RETAIN_AND_SUPPLEMENT | Specific compilation-based approach; journal support available via [4] Mison. |
| [10] | JSON Tiles frequently accessed keys | REPLACE | Analytics-on-JSON claim can be supported by C3 (PVLDB journal) with acceptable topical overlap. |
| [12] | Descendant-aware SIMD JSONPath | RETAIN_AND_SUPPLEMENT | Specific ASPLOS contribution; no verified journal replacement; supplement with selective-access journal sources. |
| [23] | Wasm performance depends on runtime | REPLACE | C1/C2 provide journal-level support for runtime/deployment performance. |
| [24] | Wasm usage in Node.js | REPLACE | C1 specifically studies server/container Wasm; C2 covers Node.js high-performance integration. |
| [28] | Hoefler & Belli benchmarking discipline | RETAIN | Foundational methodology reference; 2015 predates recency cutoff but remains scientifically necessary. |

> **SUPERSEDED (2026-11-20, see §13/§16):** the [10]→C3 'REPLACE' recommendation is rejected — C3 compiles JSON Schema for validation and does not detect frequently accessed keys. The [23]/[24]→C1/C2 shorthand is also superseded: only [23]→C1 is approved, and C2 is supplement-only, not a replacement for [24].

## 5. Foundational References to Retain

[1] RFC 8259, [28] benchmarking methodology, and the three specific technique papers [6], [7], [12] should not be removed merely to raise a ratio. Their claims can be supplemented by journal sources where appropriate.

## 6. Weak or Mismatched Citation Findings

[27] *Wasm-IO* is about low-level device interaction in industrial automation; its use for "server-side deployments beyond the browser" is Weak. Either narrow the claim to embedded/industrial Wasm or replace with C1. [20] article category (Short Communication) is unverified; its peer-review applicability remains Uncertain.

## 7. Targeted Literature Search Strategy

Search targeted claims rather than generic WebAssembly keywords: (a) server-side/container Wasm measurement; (b) JavaScript–Wasm/Node.js high-performance integration; (c) journal-level JSON processing acceleration; (d) JSON standards/background. Crossref was queried with `type:journal-article`, `from-pub-date:2016-01-01`, and relevant publisher prefixes; candidate metadata was cross-checked against official journal/policy pages where accessible.

## 8. Verified Replacement Candidates

Four candidates are listed in `reference-candidates.csv`. C1 (ACM TOSEM 2025, DOI `10.1145/3712197`) and C3 (PVLDB 2025, DOI `10.14778/3773749.3773764`) have High confidence with official journal/policy evidence. C2 (Electronics 2022, DOI `10.3390/electronics11193217`) and C4 (ACM Computing Surveys 2026, DOI `10.1145/3859866`) have Medium confidence because official publisher pages were partly inaccessible or relevance is contextual. No candidate is labeled Qualified here unless all eligibility evidence is available.

## 9. Replacement vs Supplement Scenarios

| Scenario | Total | Qualified | Percentage | Result | Notes |
|---|---:|---:|---:|---|---|
| Current (no Wiley evidence) | 28 | 11 | 39.29% | FAIL | 9 Uncertain not counted |
| Wiley all confirmed | 28 | 20 | 71.43% | FAIL | Needs 3 more |
| S1: Wiley confirmed + replace [10],[23],[24] | 28 | 23 | 82.14% | PASS | **SUPERSEDED — C3 rejected for [10]; see §13** |
| S2a: confirmed state + additions only | 85 | 68 | 80.00% | PASS | 57 additions needed from 11/28 — implausible |
| S2b: Wiley confirmed + additions only | 40 | 32 | 80.00% | PASS | 12 additions needed from 20/28 |
| S3: Wiley confirmed + replace 2 + add 2 | 30 | 24 | 80.00% | PASS | Hybrid; more disruptive than S1 |

Formulas: additions from confirmed 11: (11+x)/(28+x) ≥ 0.8 ⇒ x ≥ 57; from 20: (20+x)/(28+x) ≥ 0.8 ⇒ x ≥ 12.

## 10. Recommended Strategy — **SUPERSEDED (see §13)**

Prioritize **Scenario 1** only after the nine Wiley references are evidenced from official publisher pages: replace [23] with C1 (or C2 once verified), [24] with C1/C2, and [10] with C3. Retain [1], [28], [6], [7], [12]; supplement their claims with already-qualified journal sources [4], [9]. Do not add large numbers of weakly relevant references. If Wiley cannot be evidenced, the literature gate remains FAIL regardless of replacements because 11+3=14/28 = 50%.

## 11. Remaining Publication Blockers

1. Wiley primary-policy evidence gap (9 Uncertain).
2. 80% gate unmet unless three replacements are made after Wiley confirmation.
3. Introduction ≥15 journal articles gate unmet on confirmed evidence (11).
4. [27] weak relevance and unresolved year/DOI inconsistencies remain.
5. Plagiarism check and editorial metadata remain outside this task.


---

## 12. Final Evidence Correction and Replacement Decision (2026-11-19)

### 12.1 Wiley final evidence

Crossref journal and article endpoints were re-checked for all nine SPE references. They confirm serial identity, publisher, ISSN, DOI, title, authors and first-online/issue dates. Official Wiley aims/scope, peer-review policy, editorial board and article landing pages remained inaccessible after multiple URL attempts; the previously quoted promotional wording could not be re-verified. Therefore the nine references remain Uncertain. [21] first-online 2026-08-25 is the Version of Record; the Dec 2026 issue was still scheduled on 2026-11-19. [20] "Short Communication" remains unverified.

### 12.2 Claim-to-source matching

- **[23] → C1**: manuscript claim: "The performance of WebAssembly applications … depends strongly on the runtime environment and can deviate from native execution." C1 is a measurement study of Wasm container runtimes reporting startup/computation/system-interface/resource overheads versus Docker and standalone Wasm, attributing degradation to containerization, Wasm VM and WASI. **Direct** match → APPROVED REPLACEMENT.
- **[24] → C2**: manuscript claim: "Node.js is a major host of WebAssembly usage in practice." C2 is a Node.js/JS/Rust/Wasm performance architecture with stress tests; it demonstrates use of Wasm in Node.js but does not empirically establish "major host in practice". **Partial** match → APPROVED SUPPLEMENT ONLY; not an exact replacement.
- **[10] → C3**: manuscript claim: "JSON Tiles detects frequently accessed keys for analytics engines." C3 compiles JSON Schema for faster validation; it does not detect frequently accessed keys, perform JSON analytics, query execution or structural indexing. **Weak/Unsupported** → REJECTED — RELEVANCE MISMATCH.

### 12.3 Reassessment of [6], [7], [27]

[4] Mison (structural index + projection pushdown) and [9] FAD.js (JIT-based selective access) genuinely support the general selective-access claims near [6]/[7], but they do **not** reproduce the specific bit-parallel fast-forwarding or joint query/parse compilation contributions. Thus [6]/[7] remain RETAIN_AND_SUPPLEMENT; the supplement strengthens context but does not add Qualified references because [4]/[9] are already counted. For [27], C1's container-runtime measurements do concern server-like deployment, but Wasm-IO's industrial/embedded device focus remains a weak match to the manuscript's "server-side deployments beyond the browser" phrase. Recommendation: narrow the claim to embedded/industrial Wasm if [27] is retained, or replace with C1 only if the claim is rewritten to server/container Wasm. No manuscript edit was made here.

### 12.4 Final counts and scenarios

Current confirmed: 11 Qualified / 9 Uncertain / 8 Not Qualified. Requirement A FAIL (11<15; upper bound 20). Requirement B FAIL (39.29%; upper bound 71.43%).

If all Wiley references are later evidenced: Qualified 20. Applying only the approved C1 replacement for [23] gives **21/28 = 75.00% — FAIL**. If C2 is later qualified and the [24] claim is narrowed, the total would be 22/28 = 78.57% — still FAIL. C3 cannot be used for [10] without a relevance mismatch. Therefore at least **two additional valid qualified replacements** (or an equivalent supplement strategy with recalculated denominator) are still required after Wiley confirmation.

### 12.5 Final recommended strategy

Do not force three replacements. Approve only `[23] → C1`. Treat C2 as a supplement pending claim narrowing and further Wiley/MDPI evidence. Reject C3 for [10]. Retain foundational [1], [28], [6], [7], [12]. Identify two further journal candidates matching the manuscript's remaining non-journal-supported claims (selective access/JSON analytics and server-side Wasm adoption) before claiming the literature gate PASS. No bibliography or manuscript change was made in this task.


---

## 13. Final Artifact Correction — Latest Decisions and Arithmetic (2026-11-19)

Earlier §9 S1 and §10 are **SUPERSEDED**: S1 assumed C3 replaced [10], and §10 assumed C2/C3 were replacements. Both assumptions are rejected below.

| Existing reference | Candidate | Latest decision |
|---|---|---|
| [23] | C1 | **APPROVED REPLACEMENT** |
| [24] | C2 | **APPROVED SUPPLEMENT ONLY** (not a replacement; claim must be narrowed) |
| [10] | C3 | **REJECTED — RELEVANCE MISMATCH** |
| — | C4 | **BACKUP ONLY** — not counted in any scenario |

Claim-to-source matching: [23] claim "performance of WebAssembly applications … depends strongly on the runtime environment" is directly supported by C1's Wasm container measurement study (startup/computation/system-interface/resource; overhead attributed to containerization, Wasm VM, WASI). [24] claim "Node.js is a major host of WebAssembly usage in practice" is only partially supported by C2's performance architecture study; it demonstrates use but does not establish "major host in practice". [10] claim "JSON Tiles detects frequently accessed keys for analytics engines" is not supported by C3, which compiles JSON Schema for validation — a distinct concept.

Corrected arithmetic (all scenarios assume the nine Wiley references are first evidenced as Qualified):

| Scenario | Replacement(s) | Supplement(s) | Total | Qualified | Percentage | Result |
|---|---|---|---:|---:|---:|---|
| A | C1 for [23] | none | 28 | 21 | 75.00% | FAIL |
| B | C1 for [23] | C2 (if later Qualified) | 29 | 22 | 75.86% | FAIL |
| C | C1 for [23] + two further qualified replacements | none | 28 | 23 | 82.14% | PASS |
| D | C1 for [23] + two further qualified replacements | C2 | 29 | 24 | 82.76% | PASS |
| E | none | C2 only | 29 | 21 | 72.41% | FAIL |

Minimum qualified for a denominator of 29 is `ceil(0.8×29)=24`; for 28 it is 23. The earlier 22/28 figure for C2 was wrong because a supplement increases the denominator.

C4 confidence reconciled: `publication_confidence = Medium` (ACM journal-level evidence strong; article landing inaccessible) and `relevance_confidence = Medium` (contextual only). This replaces the earlier inconsistent High/Medium labels.

Final recommendation: approve only `[23] → C1`; keep C2 as supplement pending claim narrowing and MDPI evidence; reject C3 for [10]; retain foundational [1], [28], [6], [7], [12]; continue to treat the literature gate as **FAIL — LITERATURE BLOCKER** until at least two further valid qualified replacements are identified.


---

## 14. Synchronization with Final Wiley Reclassification (2026-11-19) — SUPERSEDES Earlier Requirement A Statements

Earlier statements that Requirement A failed with only 11 confirmed journal articles are **SUPERSEDED**. Section 24 of `reference-eligibility-audit.md` reclassified eight Wiley references to `peer_review_status = Confirmed` using publisher article PDFs with Received/Revised/Accepted histories. Requirement A counts peer-reviewed journal articles, not the stricter Qualified set used for the 80% gate.

**Current bibliography status (no replacements applied):**

| Metric | Value | Verdict |
|---|---:|---|
| Unique Introduction references | 28 | — |
| Confirmed peer-reviewed journal articles in Introduction | 19 | **PASS** (≥15) |
| Qualified for 80% gate | 11/28 = 39.29% | **FAIL** |
| Potential upper bound for 80% gate | 20/28 = 71.43% | **FAIL** |
| Uncertain | 9 | — |
| Not Qualified | 8 | — |

The 19 count consists of the 11 already Qualified plus Wiley [2], [14], [15], [16], [17], [18], [19], [21]. [20] remains Uncertain for peer review.

**Active candidate decisions (unchanged):** [23]→C1 APPROVED REPLACEMENT; [24]→C2 APPROVED SUPPLEMENT ONLY; [10]→C3 REJECTED — RELEVANCE MISMATCH; C4 BACKUP ONLY.

**Conditional arithmetic:**

| Scenario | Replacements | Supplements | Total | Qualified | Percentage | Verdict |
|---|---|---|---:|---:|---:|---|
| Current bibliography | none | none | 28 | 11 | 39.29% | FAIL |
| Hypothetical: all Wiley international-evidenced | none | none | 28 | 20 | 71.43% | FAIL |
| + C1 replaces [23] | C1 | none | 28 | 21 | 75.00% | FAIL |
| + C2 supplement (if later Qualified) | C1 | C2 | 29 | 22 | 75.86% | FAIL |
| + two further qualified replacements | C1 + 2 others | none | 28 | 23 | 82.14% | PASS |
| + two further replacements + C2 supplement | C1 + 2 others | C2 | 29 | 24 | 82.76% | PASS |

These are hypothetical scenarios; approved replacement decisions have **not** been applied to the manuscript or bibliography. The current bibliography remains 11 Qualified and fails the 80% gate. C2 is supplement-only and must increase the denominator to 29 if added. C3 remains rejected for [10].

**Remaining gap:** international-status evidence for nine Wiley articles; two further qualified replacements (or equivalent denominator-correct supplement strategy) are still needed before the 80% gate can pass.


---

## 15. Targeted Journal Replacement Validation (2026-11-19)

### 15.1 Updated Eligibility Baseline

Current bibliography remains **11 Qualified / 9 Uncertain / 8 Not Qualified (28 total)**. Eight Wiley articles have `peer_review_status = Confirmed` from publisher article PDFs; [20] remains Uncertain for peer review; all nine remain Uncertain for international status. Requirement A (Introduction-only) = **19 confirmed peer-reviewed journal articles ≥ 15 → PASS**. Requirement B = **11/28 = 39.29% → FAIL** (upper bound 20/28 = 71.43%). No bibliography change has been made.

### 15.2 Candidate D1 — JSON Search Key Distribution

D1 is a verified journal article: IJ-AI Vol 14 No 3 (June 2025), DOI `10.11591/ijai.v14.i3.pp2537-2546`, publisher IAES, ISSN 2089-4872/2252-8938, Crossref `journal-article`. The official editorial-policy page confirms single-blind review by at least two anonymous independent reviewers and states that all published articles underwent rigorous peer review; it also describes IAES as an international scientific association and its journals as international peer-reviewed open-access. Publication eligibility: **Qualified (Medium confidence)** — independent Scopus verification was not possible (source page redirect loop), although the journal page lists Scopus source 21100901206.

Full text was read: D1 compares AVL tree, BST, linear search and binary search over large-scale JSON files under normal, left-skewed and right-skewed search-key distributions, with dense/sparse indexing. Target claim [10] is: "JSON Tiles detects frequently accessed keys for analytics engines". Relevance: **Partial** (JSON indexing/search context) but **not Direct** — D1 does not detect frequently accessed keys, does not implement JSON Tiles, and does not study structural indexing for analytics engines. Decision: **REJECTED — RELEVANCE MISMATCH** for [10]; usable only as a conditional supplement if the manuscript claim is revised to JSON search/indexing performance.

### 15.3 Candidate D2a — Serverless WebAssembly Orchestration

D2a (`10.1007/s10922-023-09753-0`, Journal of Network and Systems Management, Springer, 2023) is a verified peer-reviewed international journal article (journal aims explicitly state peer-reviewed original research; Springer policies; SCOPUS/SCIE indexing listed). Article-level evidence: Received 11 Mar 2023, Accepted 16 Jun 2023, Published 10 Jul 2023; Kubernetes shim/operator extension, 9 serverless functions, 2× faster deployment and smaller artifacts with comparable execution. Publication eligibility: **Qualified (High)**. Relevance to [24] ("Node.js is a major host of WebAssembly usage in practice"): **Weak** — no Node.js experiment or adoption measurement. Decision: **REJECTED — RELEVANCE MISMATCH**; also excluded as overlapping follow-on to D2b.

### 15.4 Candidate D2b — WebAssembly Serverless Benchmarking

D2b (`10.1007/s10723-023-09669-8`, Journal of Grid Computing, Springer, 2023) is a verified peer-reviewed international journal article (aims/scope, Springer policies, SCOPUS/SCIE indexing). Article-level evidence: 13-function benchmark suite, WasmEdge/Wasmer/Wasmtime vs containerd, Wasm runtimes better in 10/13 tests; public artifact repository linked by the article; Version of Record 26 Jun 2023. Publication eligibility: **Qualified (High)**. Relevance to [24]: **Weak** — it measures server-side Wasm runtime performance and cold starts, not Node.js usage. Decision: **PENDING — CLAIM REQUIRES REVISION**; it is the selected representative of the B group and may serve as a conditional supplement for a server-side Wasm deployment claim, but **cannot replace [24] as written**.

### 15.5 D2a vs D2b Overlap Assessment

Same authors (Kjorveziroski & Filiposka), same year (2023), adjacent Springer venues, overlapping serverless-Wasm research program. D2b introduces the 13-function benchmark suite and runtime comparison; D2a cites D2b (reference 39) and extends it to Kubernetes orchestration with a different workload (9 functions). They are not duplicate publications, but they are closely related. Only **D2b** is retained as a candidate; D2a is not counted. Counting both to raise the ratio would be inappropriate.

### 15.6 Claim-to-Source Mapping for [10]

Manuscript claim: "Beyond in-process servers, JSON Tiles detects frequently accessed keys for analytics engines [10]." D1 studies search-key *distribution effects* on search performance in JSON streams; it does not detect frequently accessed keys. C3 (already rejected) compiles JSON Schema for validation. Neither is a functional equivalent of JSON Tiles. **[10] remains unreplaced.**

### 15.7 Claim-to-Source Mapping for [24]

Manuscript claim: "Node.js is a major host of WebAssembly usage in practice [24]." Neither D2a nor D2b studies Node.js; they study serverless runtimes/orchestration. The claim would need revision to "server-side WebAssembly deployment/runtime performance" before D2b could support it. No replacement is approved for [24] as written.

### 15.8 Candidate Eligibility Summary

| Candidate | Publication eligibility | Relevance to target | Decision |
|---|---|---|---|
| D1 | Qualified (Medium) | Partial for [10] | Rejected — relevance mismatch |
| D2a | Qualified (High) | Weak for [24] | Rejected — relevance mismatch + overlap |
| D2b | Qualified (High) | Weak for [24] | Pending — claim requires revision |
| C1 | Qualified (High) | Direct for [23] | Approved replacement (unchanged) |
| C2 | Uncertain | Partial for [24] | Supplement only (unchanged) |
| C3 | Qualified (High) | Weak for [10] | Rejected (unchanged) |
| C4 | Qualified (Medium) | Contextual | Backup only (unchanged) |

### 15.9 Replacement Decision

Active replacements remain **only [23] → C1**. No approved replacement exists for [10] or [24]. D1 is rejected; D2b is pending revision; D2a is excluded for overlap.

### 15.10 Replacement Arithmetic

| Scenario | Replacements | Supplements | Total | Qualified | Percentage | Result |
|---|---|---|---:|---:|---:|---|
| Current bibliography | none | none | 28 | 11 | 39.29% | FAIL |
| Hypothetical: all Wiley evidenced | none | none | 28 | 20 | 71.43% | FAIL |
| + C1 replaces [23] | C1 | none | 28 | 21 | 75.00% | FAIL |
| + D1 also counted (rejected) | C1+D1 | none | 28 | 22 | 78.57% | FAIL |
| + D2b also counted (pending) | C1+D1+D2b | none | 28 | 23 | 82.14% | PASS only hypothetically |
| C1 + D1 + D2b as supplements | C1 | D1+D2b | 30 | 24 | 80.00% | Hypothetical only |

The 82.14% line requires three replacements that are **not approved**: D1 is rejected and D2b is pending claim revision. Therefore it is not a valid path under the current evidence. If supplements are added without removing references, the denominator rises to 29 or 30, as shown.

### 15.11 Remaining Literature Gap

Two additional **approved and relevant** qualified replacements are still needed beyond C1 before 23/28 can be claimed, assuming all nine Wiley articles are first evidenced for international status. At present the international-status gap for Wiley and the absence of valid [10]/[24] replacements both remain open.

### 15.12 Final Recommendation

Do not add D1 or D2a/b to the bibliography for the purpose of reaching 80%. Keep C1 as the sole approved replacement. If the manuscript claim at [24] is narrowed to server-side Wasm deployment, D2b may be reconsidered as a supplement in a separate, explicitly approved revision task. Literature gate remains **FAIL — LITERATURE BLOCKER**; no submission-readiness claim is made.


---

## 16. Targeted Literature Search & Final Replacement Selection (2026-11-20)

### 16.1 Executive Summary (final)

Requirement A remains **PASS**: 19 confirmed peer-reviewed journal articles in the Introduction, versus the AVITEC minimum of 15. Requirement B remains **FAIL**: 11/28 = 39.29% Qualified, with an upper bound of 20/28 = 71.43%. Wiley international evidence was re-attempted and remains unavailable; [20]'s peer review remains Uncertain. C1 is the only approved replacement ([23]); no journal candidate directly supports the claims at [10] or [24]. Four new candidates (E1–E4) were searched and verified; none is approved as a replacement. The conditional 23/28 scenario is hypothetical only, and the manuscript is **not** submission-ready.

### 16.2 Final Wiley Evidence Status

Seven official Wiley URLs were re-attempted on 2026-11-20: `onlinelibrary.wiley.com/page/journal/1097024x/homepage/aims.htm`, `.../homepage/guide.htm`, `.../homepage/editorialboard.html`, `onlinelibrary.wiley.com/journal/1097024x` — each returned HTTP 403; the same URLs through a text-extraction proxy returned "Performing security verification"/CAPTCHA; the Wiley Author Services peer-review page resolved only to a dashboard shell. Web search was unavailable (HTTP 402 on repeated attempts). No primary Wiley text was read, so the previously quoted phrase ("internationally respected and rigorously refereed") remains an unverified lead and is **not** used as evidence.

Article-level evidence is unchanged: publisher PDFs in `assets/papers/10.1002_spe.*.pdf` confirm Research Article status with Received/Revised/Accepted histories for [2], [14], [15], [16], [17], [18], [19], [21] → peer review **Confirmed**. [20] (`10.1002/spe.2777`) is a Short Communication in the publisher PDF with no review dates → peer review **Uncertain**. All nine remain `international_status = Uncertain` and `eligibility = Uncertain`. [21] first-online 2026-08-25 is the Version of Record; Vol 56 Issue 12 (Dec 2026) was still scheduled, not published, on 2026-11-20. No status was changed to reach the 80% target.

| Ref | DOI | Peer review | International | Eligibility |
|---|---|---|---|---|
| [2] | 10.1002/spe.3313 | Confirmed | Uncertain | Uncertain |
| [14] | 10.1002/spe.2984 | Confirmed | Uncertain | Uncertain |
| [15] | 10.1002/spe.2920 | Confirmed | Uncertain | Uncertain |
| [16] | 10.1002/spe.3296 | Confirmed | Uncertain | Uncertain |
| [17] | 10.1002/spe.3396 | Confirmed | Uncertain | Uncertain |
| [18] | 10.1002/spe.3261 | Confirmed | Uncertain | Uncertain |
| [19] | 10.1002/spe.3036 | Confirmed | Uncertain | Uncertain |
| [20] | 10.1002/spe.2777 | Uncertain | Uncertain | Uncertain |
| [21] | 10.1002/spe.70105 | Confirmed | Uncertain | Uncertain |

### 16.3 ACM TOSEM International Verification (C1)

Journal-specific pages were attempted on 2026-11-20: `https://dl.acm.org/journal/tosem/AimsScope`, `https://dl.acm.org/journal/tosem/EditorialBoard`, `https://dl.acm.org/journal/tosem` — HTTP 403 direct; CAPTCHA via text proxy. The ACM organizational page *was* read via proxy: ACM describes itself as "the world's largest educational and scientific computing society", with a "larger global network of professional peers", regional councils and chapters worldwide. That is **publisher-level** evidence and does not by itself prove that TOSEM specifically has international scope.

Conclusion: C1 retains `international_status = Confirmed` and `publication_eligibility = Qualified` on the prior combination of ACM journals page, ACM Peer Review Policy, global-society evidence and Crossref `journal-article`, but the **journal-specific** aims/scope and editorial-board evidence gap is explicitly recorded. No ACM journal was assumed international merely because ACM publishes it; the gap is noted rather than filled by inference. C1 stays **APPROVED REPLACEMENT** for [23].

### 16.4 Target [10] Search Strategy and Results

Manuscript claim (working revised manuscript, line 17): "Beyond in-process servers, JSON Tiles detects frequently accessed keys for analytics engines [10]." Discovery used Crossref (`query.bibliographic`, `type:journal-article`, `from-pub-date:2016-01-01`) and OpenAlex (`title_and_abstract.search`, `fulltext.search`, `type:article`, `from_publication_date:2016-01-01`) with queries: *frequently accessed keys JSON analytics indexing*, *hot key detection JSON*, *JSON key access frequency indexing analytics*, *JSON structural index query analytics*, *JSON query acceleration index keys*, *frequently accessed keys JSON* (full text). Searches returned mostly adjacent topics (Pison/Mison already in the bibliography; JSON Schema validation; generic database indexing; unrelated journals).

Two verifiable new journal candidates were examined (limit respected): **E1** `10.3390/info10100291` "Blind Queries Applied to JSON Document Stores" and **E2** `10.1145/3654980` "Temporal JSON Keyword Search". Both are peer-reviewed international journal articles, but E1 rewrites blind queries over heterogeneous JSON in MongoDB and E2 searches temporal versions of JSON documents. Neither detects frequently accessed keys nor provides analytics-engine structural indexing equivalent to JSON Tiles. Earlier C3 (JSON Schema validation) and D1 (search-key distribution over AVL/BST/LS/BS) remain rejected. **Verdict: no valid journal replacement exists for [10] as written; report the gap rather than force a candidate.**

### 16.5 Target [24] Search Strategy and Results

Manuscript claim (line 21): "Node.js is a major host of WebAssembly usage in practice [24]." Discovery used OpenAlex `title_and_abstract.search:WebAssembly Node.js`, `...:WebAssembly Node.js usage empirical`, plus Crossref/Crossref title queries. Two new candidates were examined: **E3** `10.7256/2454-0714.2025.2.74049` "WebAssembly performance in the Node.js environment" and **E4** `10.1016/j.jss.2019.110395` (CBRJS Rust/Node.js/WebAssembly framework). Neither measures ecosystem adoption or establishes "major host in practice": E3 benchmarks JS vs Wasm in Node.js and proposes a test methodology; E4 presents a legacy-code repackaging framework. E3 also lacks international/peer-review evidence (Russian journal, russia-white-list-3 only). D2a/D2b remain Weak/rejected-or-pending, and C2 remains supplement-only. **Verdict: no journal article directly supports the [24] claim as written.**

### 16.6 Candidate-by-Candidate Eligibility

| Candidate | DOI | Journal / year | Peer review | International | Eligibility | Evidence note |
|---|---|---|---|---|---|---|
| E1 | 10.3390/info10100291 | Information (MDPI), 2019 | Confirmed (MDPI COPE, official aims) | Confirmed ("international, scientific open access journal") | Qualified (High) | Official aims read 2026-11-20 via proxy |
| E2 | 10.1145/3654980 | PACMMOD (ACM), 2024 | Confirmed (ACM policy) | Confirmed (ACM-level; journal page CAPTCHA) | Qualified (Medium) | Crossref abstract; journal-specific gap |
| E3 | 10.7256/2454-0714.2025.2.74049 | Software Systems and Computational Methods, 2025 | Uncertain | Uncertain | Uncertain (Low) | No official policy/scope retrieved |
| E4 | 10.1016/j.jss.2019.110395 | J. Systems and Software (Elsevier), 2019 | Confirmed | Confirmed (supporting indexing; official scope not retrieved) | Qualified (Medium) | Crossref metadata; shares authors with C2 |
| C2 | 10.3390/electronics11193217 | Electronics (MDPI), 2022 | Confirmed (official aims) | Confirmed ("international, peer-reviewed") | **Qualified** (new evidence) | Decision unchanged: supplement only |
| C1 | 10.1145/3712197 | ACM TOSEM, 2025 | Confirmed | Confirmed (journal-level gap) | Qualified | Approved replacement for [23] |

New evidence for C2: the official MDPI *Electronics* aims page (accessed 2026-11-20 via text proxy) states "Electronics (ISSN 2079-9292) is an international, peer-reviewed, open access journal" and MDPI is a COPE member enforcing rigorous peer review. This **resolves only publication eligibility**; it does not change the relevance-based decision (supplement only).

### 16.7 Claim-to-Source Matching

- **[10]** "JSON Tiles detects frequently accessed keys for analytics engines." E1 = blind querying heterogeneous JSON (MongoDB); E2 = temporal JSON keyword search; C3 = JSON Schema validation; D1 = search-key distribution effects on AVL/BST/LS/BS. None detects frequently accessed keys or performs analytics-engine structural indexing. All → mismatch.
- **[24]** "Node.js is a major host of WebAssembly usage in practice." C2 = Node.js/JS/Rust/Wasm performance integration; E3 = Node.js Wasm benchmarking methodology; E4 = Rust/Node.js/Wasm repackaging framework; D2a/D2b = serverless Wasm runtimes with no Node.js measurement. These support "Wasm can be used with/in Node.js" but not "Node.js is a major host in practice". All → mismatch or Partial only.

### 16.8 Accepted and Rejected Candidates

- **Accepted replacement:** C1 for [23] (unchanged).
- **Supplement only:** C2 for [24] (decision preserved; eligibility now Qualified).
- **Rejected for [10]:** C3, D1, E1, E2.
- **Rejected for [24]:** D2a (also overlap), E3 (eligibility + relevance), E4 (relevance).
- **Pending claim revision:** D2b — may serve only as a supplement for a rewritten "server-side Wasm deployment" claim, never as a replacement for [24] as written.
- **Backup only:** C4.
- **Excluded for overlap:** D2a relative to D2b (same authors/year, D2a cites D2b); E4 relative to C2 (same authors, related program) — not counted twice.

### 16.9 Replacement Strategy

Keep exactly one approved one-for-one replacement ([23]→C1). Do not add D1, D2a/b, E1–E4, or C2 to the bibliography to raise the ratio. Any future use of D2b requires a separate, explicitly approved academic claim revision; any use of E1/E2/E3/E4 requires either a matching claim revision or an independently justified supplementation decision. Foundational [1] RFC 8259, [28] benchmarking methodology and [6]/[7]/[12] specific-technique papers are retained; their claims may be supplemented by already-Qualified journal sources [4]/[9], which does not change the numerator.

### 16.10 Updated Requirement B Calculation

| Scenario | Replacements | Supplements | Total | Qualified | Percentage | Verdict |
|---|---|---|---:|---:|---:|---|
| Current bibliography (actual) | none | none | 28 | 11 | 39.29% | FAIL |
| Hypothetical: all nine Wiley international-evidenced | none | none | 28 | 20 | 71.43% | FAIL |
| + C1 replaces [23] (approved) | C1 | none | 28 | 21 | 75.00% | FAIL |
| Hypothetical: + two further approved replacements | C1 + 2 | none | 28 | 23 | 82.14% | PASS — not achieved |
| If [20] stays Uncertain: + two approved replacements | C1 + 2 | none | 28 | 22 | 78.57% | FAIL |
| C1 + two replacements as supplements | C1 | 2 | 30 | 23 | 76.67% | FAIL |
| C1 + two replacements + one supplement | C1 | 3 | 31 | 24 | 77.42% | FAIL |

For denominator 28 the minimum is ceil(0.8×28) = 23; for 29 it is 24; for 30 it is 24. Supplementing without removing raises the denominator and must not be reported with denominator 28. The 23/28 = 82.14% line assumes two replacements that are **not approved**; it is a target scenario, never the current status. `2016+` remains the operational recency definition, not an official AVITEC cutoff.

### 16.11 Remaining Literature Blockers

1. International-status evidence for the nine Wiley SPE articles (official pages inaccessible).
2. Article-level peer-review dates for [20] (Short Communication).
3. Journal-specific aims/scope/board evidence for ACM TOSEM (C1), notwithstanding retained Qualified status.
4. No valid journal replacement for [10]'s "frequently accessed keys" claim.
5. No valid journal replacement for [24]'s "Node.js is a major host in practice" claim.
6. Even with all Wiley evidenced and C1 applied, 21/28 = 75.00% — still short of 23.

### 16.12 Final Recommendation

Do not treat the literature gate as passed. Retain C1 as the sole approved replacement; keep C2 supplement-only; reject C3, D1, D2a, E1, E2, E3, E4 for the stated reasons; keep D2b pending claim revision and C4 as backup. Resolve the Wiley international evidence gap and [20] peer-review evidence first; then, if the manuscript claims are revised to match available evidence, reconsider D2b/E-series as documented supplements in a separate task. **Verdict: `FAIL — LITERATURE BLOCKER`; the manuscript is not ready for submission.**

