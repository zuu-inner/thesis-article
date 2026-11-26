# Reference Eligibility Audit — AVITEC Manuscript

## 1. Executive Summary

Audit of all **28** references in the working revised manuscript. Result: **11 Qualified**, **9 Uncertain**, **8 Not Qualified**. Confirmed recent international peer-reviewed journal share = **39.29%** (11/28); potential upper bound if all Uncertain are evidenced = **71.43%** (20/28). Both are below the AVITEC 80% requirement. The Introduction cites all 28 references; confirmed peer-reviewed journal articles there = **11** (<15), potential upper bound = **20**. Overall literature gate: **FAIL**.

## 2. Audit Scope and Source Versions

- Target manuscript: `out/article-audit/working/article/drafts/article-draft-revised.md` (SHA-256 prefix `ec159297…`).
- Comparison manuscript: `article/drafts/article-draft.md` (`ee829c0d…`) — used only for citation-context comparison. All 28 DOI numbers and the Introduction citation set are identical; every reference's citation location/context is identical in both versions.
- Denominator source: the 28-entry reference list of the target manuscript. `assets/bib/cites.bib` and the 52-row literature matrix (29 INCLUDE / 23 EXCLUDE) are supporting registries.
- Snapshot `out/article-audit/article-audit.zip` contains the eight specified audit files; all eight are byte-identical to current disk copies.
- Repository: branch `research/nd11-phase-d-e-synthesis`, HEAD `a1fad918a7fccb6464722ac35723c29800ba7849`; 33 pre-existing dirty entries preserved.

## 3. Official AVITEC Requirements

URL: https://ejournals.itda.ac.id/index.php/avitec/about/submissions; accessed 2026-11-19. Relevant verbatim text:

- "Include at least 15 references in the manuscript. Under AVITEC's current requirements, the Introduction must cite at least 15 peer-reviewed journal articles. At least 80% of references must be from recent international peer-reviewed journals, with appropriate international coverage also maintained in the Introduction."
- "Prioritize literature from the past ten years ... Non-English references must not exceed 25% of the bibliography; provide an English translation of each such title in square brackets."
- Numbered AVITEC citations before punctuation; IEEE-based reference list; DOI where available; AI-use disclosure.

**3.1 Introduction international coverage (additional compliance check).** The Introduction draws on ACM, Springer, Wiley, VLDB Endowment and IETF sources across parsing, analytics, WebAssembly and benchmarking contexts. This is a qualitative auditor observation; AVITEC gives no numeric threshold for this clause beyond "appropriate international coverage", so none was invented.

**3.2 Non-English references (additional compliance check).** The ≤25% rule is explicitly present in the current official guideline. All 28 manuscript titles are English; non-English = 0/28 = 0.00% → PASS.

## 4. Operational Definitions

- "Recent" = publication year **2016 or later**, an audit convention for comparability with earlier audits; **not** claimed as an official AVITEC cutoff. Rolling ten-year sensitivity from 2026-11-19 changes nothing because the only pre-2016 item ([28], 2015) is already excluded.
- "International" = auditor criteria based on official international scope/global editorial evidence and reputable indexing; this is an audit interpretation, not an official AVITEC definition.
- "Peer-reviewed" requires official journal/publisher policy evidence. DOI, Crossref, ISSN, publisher reputation and citation counts alone are not sufficient.
- Publication type follows official serial identity: PVLDB is a journal (https://vldb.org/pvldb/); Crossref `type` is supporting metadata only.

## 5. Evidence and Verification Method

Official publisher/journal pages, policy pages, the AVITEC guideline, and Crossref API per DOI were consulted; access date 2026-11-19 for all web sources. Wiley journal/peer-review pages returned 403/no output; ACM DOI detail pages returned 403. Failures are recorded, not replaced by assumptions. Crossref found metadata for 28/28 but is not used as proof of peer review or international status.

## 6. Reference-by-Reference Findings

| # | Publication type | Peer review | Journal eligible | International | Year | Recency | Eligibility |
|---:|---|---|---|---|---:|---|---|
| 1 | Standard / RFC | Not Applicable | No | Not Applicable | 2017 | Recent | Not Qualified |
| 2 | Journal | Uncertain | Yes | Uncertain | 2024 | Recent | Uncertain |
| 3 | Journal | Confirmed | Yes | Confirmed | 2019 | Recent | Qualified |
| 4 | Journal | Confirmed | Yes | Confirmed | 2017 | Recent | Qualified |
| 5 | Journal | Confirmed | Yes | Confirmed | 2018 | Recent | Qualified |
| 6 | Conference proceedings | Confirmed | No | Confirmed | 2022 | Recent | Not Qualified |
| 7 | Conference proceedings | Confirmed | No | Confirmed | 2019 | Recent | Not Qualified |
| 8 | Journal | Confirmed | Yes | Confirmed | 2020 | Recent | Qualified |
| 9 | Journal | Confirmed | Yes | Confirmed | 2017 | Recent | Qualified |
| 10 | Conference proceedings | Confirmed | No | Confirmed | 2021 | Recent | Not Qualified |
| 11 | Journal | Confirmed | Yes | Confirmed | 2025 | Recent | Qualified |
| 12 | Conference proceedings | Confirmed | No | Confirmed | 2024 | Recent | Not Qualified |
| 13 | Journal | Confirmed | Yes | Confirmed | 2025 | Recent | Qualified |
| 14 | Journal | Uncertain | Yes | Uncertain | 2021 | Recent | Uncertain |
| 15 | Journal | Uncertain | Yes | Uncertain | 2021 | Recent | Uncertain |
| 16 | Journal | Uncertain | Yes | Uncertain | 2024 | Recent | Uncertain |
| 17 | Journal | Uncertain | Yes | Uncertain | 2025 | Recent | Uncertain |
| 18 | Journal | Uncertain | Yes | Uncertain | 2023 | Recent | Uncertain |
| 19 | Journal | Uncertain | Yes | Uncertain | 2022 | Recent | Uncertain |
| 20 | Journal | Uncertain | Yes | Uncertain | 2020 | Recent | Uncertain |
| 21 | Journal | Uncertain | Yes | Uncertain | 2026 | Recent | Uncertain |
| 22 | Journal | Confirmed | Yes | Confirmed | 2026 | Recent | Qualified |
| 23 | Conference proceedings | Confirmed | No | Confirmed | 2021 | Recent | Not Qualified |
| 24 | Conference proceedings | Confirmed | No | Confirmed | 2026 | Recent | Not Qualified |
| 25 | Journal | Confirmed | Yes | Confirmed | 2025 | Recent | Qualified |
| 26 | Journal | Confirmed | Yes | Confirmed | 2025 | Recent | Qualified |
| 27 | Journal | Confirmed | Yes | Confirmed | 2025 | Recent | Qualified |
| 28 | Conference proceedings | Confirmed | No | Confirmed | 2015 | Not Recent | Not Qualified |

Per-reference detail (authors, DOI, venue, claim, relevance, URLs, decision reason) is in `reference-eligibility-matrix.csv`.

## 7. Peer-review Assessment

Confirmed for [3] (Springer journal policies), PVLDB references (4, 5, 8, 9, 11, 13) via PVLDB's official "journal-style reviewing" statement, ACM journals (22, 25, 26, 27) and ACM proceedings via the ACM Peer Review Policy. Not Applicable for [1] (IETF standards process). Uncertain for the nine Wiley SPE references because official Wiley pages were inaccessible.

## 8. International Journal Assessment

Confirmed for [3] (official "International Journal on Very Large Data Bases", SCOPUS/SCIE indexed), PVLDB (VLDB Endowment/ACM global community) and ACM journals (global society). Uncertain for the nine Wiley SPE references. Proceedings are international but remain outside the journal numerator.

## 9. Publication Year and Recency Assessment

All years checked against manuscript and Crossref. Discrepancies: [12] manuscript/BibTeX/matrix 2024 vs Crossref/RV 2023 — 2024 used; [22] manuscript/BibTeX/matrix 2026 vs Crossref/RV 2027 — 2026 used. Both remain recent. [28] 2015 → Not Recent. No year was chosen to improve the percentage.

## 10. Citation Relevance Assessment

Most references directly or contextually support their claims. [27] *Wasm-IO* (low-level device interaction in industry automation) is cited for "server-side deployments beyond the browser"; support is **Weak** — venue eligibility does not repair topical mismatch. Negative/heterogeneous results remain supported by [23], [24], [28].

## 11. Introduction Requirement Recalculation

Unique references cited in Introduction: **28** (all 28). Confirmed peer-reviewed journal articles: **11** → **FAIL** against ≥15. Potential upper bound if the nine Uncertain SPE references are evidenced: **20** → would pass. Uncertain references are excluded from the main result.

## 12. 80% Requirement Recalculation

Denominator = all **28** references, including RFC and proceedings. Qualified **11**, Uncertain **9**, Not Qualified **8**.

- Confirmed proportion = 11/28 × 100 = **39.29%** — FAIL.
- Potential upper bound = (11+9)/28 × 100 = **71.43%** — still FAIL.
- With denominator 28, at least **23 Qualified** are needed. Current shortfall = **12**; if Uncertain SPE references are evidenced, shortfall = **3**.
- If adding without removing: **57** new qualifying journals needed from confirmed state, or **12** if Uncertain are confirmed. Replacing 3 non-qualified references with genuinely relevant journals would reach 23/28 with denominator unchanged. These are post-audit calculations, not the prior assumed 12.

These are proportion bounds, not statistical confidence intervals.

## 13. Uncertain References and Evidence Gaps

The nine Wiley SPE references are Uncertain only because official scope/board and peer-review pages were inaccessible. No assumption was substituted. ACM DOI detail pages were also inaccessible; Crossref metadata plus official ACM policy pages were used instead, with this limitation documented.

## 14. Recommended Reference Actions

1. Obtain official Wiley evidence for *Software: Practice and Experience* to resolve nine Uncertain references; this raises confirmed Qualified from 11 to 20 but still leaves 80% failing.
2. Replace or supplement at least 3 non-qualified references with genuinely relevant recent international journal articles (on-demand/selective JSON, structural indexes, Wasm boundary overhead, benchmarking methodology). Do not add irrelevant sources merely to satisfy the quota.
3. Review [27] relevance; add a directly relevant server-side Wasm journal source or narrow the claim if retained.
4. Keep [1] RFC 8259 and methodology proceedings that materially support the study; they remain in the denominator by rule.
5. Reconcile [12] and [22] years in a separate bibliographic cleanup; no changes made here.

## 15. Final Literature Gate Verdict

**FAIL — LITERATURE BLOCKER.** Neither AVITEC reference requirement is met on confirmed evidence: Introduction 11<15 journal articles; overall 39.29%<80%. This audit is complete; the manuscript is not submission-ready.

## 16. Source URLs and Access Dates

- AVITEC guidelines: https://ejournals.itda.ac.id/index.php/avitec/about/submissions (accessed 2026-11-19)
- Crossref API per DOI: `https://api.crossref.org/works/<DOI>` (accessed 2026-11-19)
- The VLDB Journal: https://www.springer.com/journal/778; policies: https://link.springer.com/brands/springer/journal-policies
- PVLDB official site: https://vldb.org/pvldb/
- ACM journals: https://www.acm.org/publications/journals; peer-review policy: https://www.acm.org/publications/policies/peer-review; proceedings: https://www.acm.org/publications/proceedings
- RFC 8259: https://www.rfc-editor.org/rfc/rfc8259
- Wiley SPE journal (403): https://onlinelibrary.wiley.com/journal/1097024x; Wiley peer-review page (no output): https://authorservices.wiley.com/author-resources/Journal-Authors/Peer-review/index.html
- ACM DOI detail pages (403), e.g. `https://dl.acm.org/doi/10.1145/3623278.3624754`


---

## 17. Wiley Reclassification (follow-up audit, 2026-11-19)

The nine previously Uncertain Wiley references were re-checked individually through the Crossref API for each DOI. All nine are `type: journal-article` in the `Software: Practice and Experience` serial (Wiley, ISSN 0038-0644 / 1097-024X). First-online and issue dates were reconciled and are now recorded per row in the eligibility matrix. The manuscript's issue-year convention is retained: e.g. [15] online 2020-10-29 / issue 2021-05 → 2021; [20] online 2019-11-26 / issue 2020-02 → 2020; [21] online 2026-08-25 / issue 2026-12 → 2026.

Official Wiley journal pages (aims and scope, editorial board, peer-review guidelines, article landing pages) returned 403 or no usable output from this environment, including `onlinelibrary.wiley.com`, `authorservices.wiley.com`, and ISSN/DOAJ mirrors. Therefore the claim that SPE is "internationally respected and rigorously refereed" could not be independently evidenced from primary publisher pages. Crossref metadata establishes publication type and dates, **not** peer-review or international status. Per the audit rule "no evidence, no claim", the nine references remain **Uncertain**; no automatic upgrade was applied. For [20], the previously reported "Short Communication" category could not be verified (Crossref has no `subtype` field).

## 18. Evidence Updates

- Added per-DOI Crossref URLs to `peer_review_evidence` and `international_evidence` for all nine Wiley rows as metadata support only.
- Added first-online vs issue-date reconciliation to `year_source` and `notes`.
- Preserved the earlier audit text above as historical record; this section documents the follow-up rather than silently replacing prior findings.

## 19. Recalculated AVITEC Requirements (unchanged by Wiley follow-up)

- Qualified: **11**; Uncertain: **9**; Not Qualified: **8**; total **28**.
- Introduction: 28 unique cited references; confirmed peer-reviewed journals **11** (<15) → FAIL; potential upper bound **20** (≥15).
- 80% gate: confirmed **11/28 = 39.29%**; potential upper bound **20/28 = 71.43%**; both below 80% → FAIL.
- With denominator fixed at 28, **23 Qualified** are required. If all Wiley references were later evidenced, Qualified would be 20 and three one-for-one replacements would suffice (23/28 = 82.14%).

## 20. Updated Eligibility Counts

| Status | Count | Change from first audit |
|---|---:|---|
| Qualified | 11 | none |
| Uncertain | 9 | none (Wiley evidence gap remains) |
| Not Qualified | 8 | none |

## 21. Remaining Publication Blockers

1. Wiley peer-review/international evidence inaccessible → nine Uncertain; confirmed ratios remain below both AVITEC gates.
2. Even the optimistic upper bound (71.43%) is below 80%, so at least three academically justified journal replacements are needed if Wiley is confirmed.
3. Reference [27] relevance remains Weak; [12]/[22] year discrepancies and the `cites.bib` arXiv/journal DOI mismatch remain open bibliographic cleanup items.
4. This audit does not edit the manuscript, bibliography, literature matrix, or historical evidence.


---

## 22. Final Evidence Correction (2026-11-19)

Journal-level Wiley evidence re-checked: Crossref journal endpoint `https://api.crossref.org/journals/1097-024X` confirms the serial title *Software Practice and Experience*, publisher Wiley, ISSN 0038-0644/1097-024X, with 5,552 deposited DOIs. Crossref article endpoints confirm all nine DOI records as `journal-article` with author, title, issue, pages, first-online and issue dates. Attempts to retrieve official Wiley aims/scope, peer-review policy, editorial board and article landing pages returned 403 or JS-only output (`onlinelibrary.wiley.com`, `authorservices.wiley.com`). The earlier promotional phrase "internationally respected and rigorously refereed" could not be re-verified from an accessible primary page. Accordingly the nine references remain **Uncertain**; Crossref metadata is not treated as evidence of peer review or international status.

Article-level reconciliation: every DOI/title/author matches the manuscript; publication years follow the issue-year convention. [21] first-online 2026-08-25 is the Version of Record; Vol 56 No 12 (Dec 2026) was still scheduled on the 2026-11-19 access date and is not described as published. [20] "Short Communication" category remains unverified.

Candidate publication eligibility: C1 (ACM TOSEM, DOI `10.1145/3712197`) is Qualified — ACM journals page states peer-reviewed scholarly journals; ACM Peer Review Policy applies; ACM About page documents global society/membership. C3 (PVLDB, DOI `10.14778/3773749.3773764`) is Qualified — PVLDB official page calls it a scholarly journal with strict quality assurance, rapid reviews, an editorial board and review board. C2 (Electronics, DOI `10.3390/electronics11193217`) is Uncertain for international status: the publisher-hosted PDF at `mdpi-res.com` verifies Article type, academic editors, received/accepted/published dates, and Crossref journal endpoint verifies MDPI/ISSN, but MDPI aims/scope and peer-review pages were inaccessible.

Recalculation: confirmed 11 Qualified / 9 Uncertain / 8 Not Qualified. Requirement A FAIL (11<15; upper bound 20). Requirement B FAIL (39.29%; upper bound 71.43%). If Wiley were later confirmed (20), only C1 is an approved replacement ([23]) → 21/28 = 75.00%, still FAIL. At least two further valid replacements are needed; C3 is rejected for [10] on relevance grounds and C2 is not an exact replacement for [24].

Final verdict: literature gate remains **FAIL — LITERATURE BLOCKER**; no PASS is claimed.


---

## 23. Final Audit Artifact Correction (2026-11-19) — SUPERSEDES §22 DOI/Evidence Fields

**23.1 DOI correction log.** The previous matrix used truncated/non-specific DOIs (notably `10.1002/spe`). All 28 DOIs were re-extracted from the working revised manuscript reference list and verified against Crossref article endpoints. 22 rows changed DOI.

| Reference | Previous DOI | Corrected DOI |
|---|---|---|
| [2] | `10.1002/spe` | `10.1002/spe.3313` |
| [4] | `10.14778/3115404` | `10.14778/3115404.3115416` |
| [5] | `10.14778/3236187` | `10.14778/3236187.3236207` |
| [6] | `10.1145/3503222` | `10.1145/3503222.3507719` |
| [7] | `10.1145/3297858` | `10.1145/3297858.3304008` |
| [8] | `10.14778/3436905` | `10.14778/3436905.3436926` |
| [9] | `10.14778/3137765` | `10.14778/3137765.3137782` |
| [10] | `10.1145/3448016` | `10.1145/3448016.3452809` |
| [11] | `10.14778/3746405` | `10.14778/3746405.3746439` |
| [12] | `10.1145/3623278` | `10.1145/3623278.3624754` |
| [13] | `10.14778/3778092` | `10.14778/3778092.3778109` |
| [14] | `10.1002/spe` | `10.1002/spe.2984` |
| [15] | `10.1002/spe` | `10.1002/spe.2920` |
| [16] | `10.1002/spe` | `10.1002/spe.3296` |
| [17] | `10.1002/spe` | `10.1002/spe.3396` |
| [18] | `10.1002/spe` | `10.1002/spe.3261` |
| [19] | `10.1002/spe` | `10.1002/spe.3036` |
| [20] | `10.1002/spe` | `10.1002/spe.2777` |
| [21] | `10.1002/spe` | `10.1002/spe.70105` |
| [23] | `10.1145/3487552` | `10.1145/3487552.3487827` |
| [24] | `10.1145/3744916` | `10.1145/3744916.3764533` |
| [28] | `10.1145/2807591` | `10.1145/2807591.2807644` |

No `10.1002/spe` remains as an article DOI in the matrix. Manuscript and `cites.bib` were not edited.

**23.2 Wiley journal-level evidence.** Official Wiley URLs were re-attempted on 2026-11-19: aims `https://onlinelibrary.wiley.com/page/journal/1097024x/homepage/aims.htm` → 403; author guide `.../homepage/guide.htm` → 403; journal overview `https://onlinelibrary.wiley.com/journal/1097024X` → 403; Author Services peer-review page returned only a JS shell. The earlier promotional wording ("internationally respected and rigorously refereed") could not be re-verified from an accessible primary page. Crossref journal endpoint `https://api.crossref.org/journals/1097-024X` confirms serial identity (Wiley; ISSN 0038-0644/1097-024X; 5,552 DOIs) but is **not** evidence of peer review or international status. Therefore the nine Wiley rows remain Uncertain.

**23.3 Wiley article-level evidence.** Each DOI was resolved through the Crossref article endpoint; title, authors, type, first-online and issue dates match the manuscript. Official Wiley landing pages returned 403.

| Ref | Article DOI | Title | Authors | Type | First online | Issue | Vol/issue/pages |
|---|---|---|---|---|---|---|---|
| [2] | `10.1002/spe.3313` | On-demand JSON: A better way to parse documents? | Keiser, Lemire | journal-article | 2024-01-18 | 2024-06 | 54(6):1074-1086 |
| [14] | `10.1002/spe.2984` | Number parsing at a gigabyte per second | Lemire | journal-article | 2021-05-11 | 2021-08 | 51(8):1700-1727 |
| [15] | `10.1002/spe.2920` | Validating UTF-8 in less than one instruction per byte | Keiser, Lemire | journal-article | 2020-10-29 | 2021-05 | 51(5):950-964 |
| [16] | `10.1002/spe.3296` | Parsing millions of URLs per second | Nizipli, Lemire | journal-article | 2023-12-09 | 2024-05 | 54(5):744-758 |
| [17] | `10.1002/spe.3396` | Parsing millions of DNS records per second | Koekkoek, Lemire | journal-article | 2024-12-10 | 2025-04 | 55(4):778-788 |
| [18] | `10.1002/spe.3261` | Transcoding unicode characters with AVX-512 instructions | Clausecker, Lemire | journal-article | 2023-09-12 | 2023-12 | 53(12):2430-2462 |
| [19] | `10.1002/spe.3036` | Transcoding billions of Unicode characters per second | Lemire, Muła | journal-article | 2021-10-13 | 2022-02 | 52(2):555-575 |
| [20] | `10.1002/spe.2777` | Base64 encoding and decoding at almost the speed of a memory copy | Muła, Lemire | journal-article | 2019-11-26 | 2020-02 | 50(2):89-97 |
| [21] | `10.1002/spe.70105` | Fixing ill-formed UTF-16 strings with SIMD instructions | Clausecker, Lemire | journal-article | 2026-08-25 | 2026-12 (scheduled) | 56(12):1498-1509 |

[20] remains labelled Short Communication in prior notes but the article category could not be verified; [21] first-online 2026-08-25 is the Version of Record; Dec 2026 issue was still scheduled on 2026-11-19.

**23.4 Evidence mapping correction.** The AVITEC guideline URL (`https://ejournals.itda.ac.id/index.php/avitec/about/submissions`) was found in `peer_review_evidence` and `international_evidence` columns and removed. AVITEC guidelines now serve only as authority for the two requirement thresholds. Each of the 28 rows received evidence URLs appropriate to its column: ACM journals/peer-review policy, Springer journal policies, PVLDB publication policy/review board, IETF RFC Editor, or documented Wiley/Crossref attempts. Crossref remains metadata support, not peer-review/international proof.

**23.5 Revised eligibility decisions.** Counts are unchanged: 11 Qualified / 9 Uncertain / 8 Not Qualified. Requirement A: 11 confirmed Introduction journal articles (<15) → FAIL (upper bound 20). Requirement B: 11/28 = 39.29% confirmed; upper bound 20/28 = 71.43% → FAIL. "Recent" remains the 2016+ operational definition, not an official AVITEC cutoff.

**23.6 Remaining evidence gaps.** Official Wiley aims/scope, IFA and editorial board remain inaccessible; MDPI journal policy pages also inaccessible; ACM/PVLDB article landing pages returned 403 from this environment, though official journal-level policies are available. No literature-gate PASS is claimed.


---

## 24. Final Wiley Reclassification (2026-11-19) — SUPERSEDES §23 Eligibility Dimensions

**24.1 Journal-level verification.** The official Wiley URLs were re-attempted through direct `webfetch`, Python urllib with browser user-agent, and a text proxy: `https://onlinelibrary.wiley.com/page/journal/1097024x/homepage/aims.htm`, `.../homepage/guide.htm`, and `https://onlinelibrary.wiley.com/journal/1097024X` returned 403; the proxy returned a CAPTCHA/security-verification page. No accessible primary text from those pages was obtained in this environment. The earlier quoted statements ("internationally respected and rigorously refereed", editorial-board geography) are therefore treated as unverified leads, not as confirmed evidence.

**24.2 Article-level verification.** All nine DOIs were matched to the working manuscript and to publisher article PDFs archived at `assets/papers/10.1002_spe.*.pdf`. The PDFs confirm journal article status, article category, authors, and publication-specific review history (Received/Revised/Accepted) for eight articles. [20] is explicitly labelled SHORT COMMUNICATION — a journal article category, not automatically non-peer-reviewed — but its archived PDF has no review dates, so its peer-review status remains Uncertain.

| Ref | DOI | Category | Review evidence (publisher PDF) | Peer review | International | Eligibility |
|---|---|---|---|---|---|---|
| [2] | `10.1002/spe.3313` | Research Article | Received 30 Dec 2022; Revised 30 Nov 2023; Accepted 23 Dec 2023 | Confirmed | Uncertain | Uncertain |
| [14] | `10.1002/spe.2984` | Research Article | Received 11 Jan 2021; Revised 22 Mar 2021; Accepted 23 Apr 2021 | Confirmed | Uncertain | Uncertain |
| [15] | `10.1002/spe.2920` | Research Article | Received 10 Aug 2020; Revised 6 Oct 2020; Accepted 9 Oct 2020 | Confirmed | Uncertain | Uncertain |
| [16] | `10.1002/spe.3296` | Research Article | Received 31 May 2023; Revised 30 Oct 2023; Accepted 16 Nov 2023 | Confirmed | Uncertain | Uncertain |
| [17] | `10.1002/spe.3396` | Research Article | Received 4 Sep 2024; Revised 9 Nov 2024; Accepted 15 Nov 2024 | Confirmed | Uncertain | Uncertain |
| [18] | `10.1002/spe.3261` | Research Article | Received 8 Dec 2022; Revised 10 Jul 2023; Accepted 4 Aug 2023 | Confirmed | Uncertain | Uncertain |
| [19] | `10.1002/spe.3036` | Research Article | Received 30 Jul 2021; Accepted 20 Sep 2021 | Confirmed | Uncertain | Uncertain |
| [20] | `10.1002/spe.2777` | Short Communication | No received/revised/accepted line found in archived publisher PDF | Uncertain | Uncertain | Uncertain |
| [21] | `10.1002/spe.70105` | Research Article | Received 9 Feb 2026; Revised 11 Aug 2026; Accepted 16 Aug 2026 | Confirmed | Uncertain | Uncertain |

**24.3 Reclassification decisions.** Eight Wiley references now have `peer_review_status = Confirmed` at article level; [20] remains Uncertain for peer review. All nine remain `international_status = Uncertain` because official aims/scope and editorial-board evidence was not retrievable. Consequently all nine remain `eligibility = Uncertain` for the 80% gate. This is not a forced retention: it follows the evidence actually available.

**24.4 Recalculated Requirement A.** Introduction citation locations were re-checked against the working manuscript. Unique Introduction references = 28. Confirmed peer-reviewed journal articles = **19** (the prior 11 Qualified plus eight Wiley articles with publisher review history; [20] still Uncertain). **19 ≥ 15 → PASS** for the Introduction-only requirement. This does **not** imply the 80% gate passes. If [20] is later evidenced, the count becomes 20.

**24.5 Recalculated Requirement B.** Qualified for the combined 80% criterion remains **11**; Uncertain **9**; Not Qualified **8**. Confirmed proportion = **11/28 = 39.29%**; potential upper bound = **20/28 = 71.43%**. **FAIL**. The 2016+ recency cutoff remains an operational audit definition, not an official AVITEC cutoff.

**24.6 Remaining literature blocker.** The remaining blocker is international-status evidence for the nine Wiley articles. No new candidates were searched and no bibliography change was made. Literature gate remains FAIL for Requirement B.
