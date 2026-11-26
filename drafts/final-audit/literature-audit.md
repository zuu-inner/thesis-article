# Stage 6 — Literature and Reference Audit

Official guidelines checked 2026-11-19 at `https://ejournals.itda.ac.id/index.php/avitec/about/submissions` (current AVITEC Author Guidelines). Registry verification: `article/data/json/crossref_verify.json` (updated 2026-11-19 to add the published VLDB Journal version of simdjson, ref [3], DOI `10.1007/s00778-019-00578-5`, verified via Crossref API).

## 1. Requirement checks

| Requirement | Value | Status |
|---|---:|---|
| Title ≤ 20 words | 11 | PASS |
| Abstract ≤ 250 words, single paragraph | 244 | PASS |
| Keywords 3–7 | 5 | PASS |
| Manuscript length 5,000–8,000 words (excl. refs) | 5,254 prose (other definitions 5,487–7,648) | PASS |
| References ≥ 15 total | 28 | PASS |
| Introduction ≥ 15 peer-reviewed journal articles | 20 | PASS |
| ≥ 80% recent international peer-reviewed journals | 71.4% (20/28) | **FAIL** |
| Non-English refs ≤ 25% | 0% | PASS |
| DOI/registry verified | 28/28 | PASS |
| Numbered citations before punctuation | builder QA: 0 violations; [1]–[28] in first-appearance order | PASS |

**Critical gap:** at least **12 additional genuine recent international journal articles** are needed to reach 80% ((20+N)/(28+N) ≥ 0.8 ⇒ N ≥ 12). The Introduction requirement is already met; additions must support real claims, not padding.

## 2. Classification rules

- Journal = Crossref `type: journal-article`. `Proc. VLDB Endow.` is counted as a journal: Crossref reports `type: journal-article`, ISSN 2150-8097 (verified for DOI `10.14778/3115404.3115416`).
- Excluded from the journal count: conference proceedings, RFC / standards, arXiv preprints, books, and non-indexed venues — even when they are legitimate and necessary citations.
- "Recent" = published 2016 or later; ref [28] (2015) is a foundational benchmarking paper and is a proceedings article, so it is not counted either way.

## 3. All 28 references

| # | DOI | Year | Venue | Type | Journal? | Recent? | In Intro |
|---:|---|---:|---|---|---|---|---|
| 1 | `10.17487/RFC8259` | 2017 | RFC 8259 | standard-or-misc | no | yes | yes |
| 2 | `10.1002/spe.3313` | 2024 | Software: Practice and Experience | journal | yes | yes | yes |
| 3 | `10.1007/s00778-019-00578-5` | 2019 | The VLDB Journal | journal | yes | yes | yes |
| 4 | `10.14778/3115404.3115416` | 2017 | Proc. VLDB Endow. | journal | yes | yes | yes |
| 5 | `10.14778/3236187.3236207` | 2018 | Proc. VLDB Endow. | journal | yes | yes | yes |
| 6 | `10.1145/3503222.3507719` | 2022 | Proceedings of the 27th {ACM} {International} {C | proceedings | no | yes | yes |
| 7 | `10.1145/3297858.3304008` | 2019 | Proceedings of the Twenty-Fourth International C | proceedings | no | yes | yes |
| 8 | `10.14778/3436905.3436926` | 2020 | Proc. VLDB Endow. | journal | yes | yes | yes |
| 9 | `10.14778/3137765.3137782` | 2017 | Proc. VLDB Endow. | journal | yes | yes | yes |
| 10 | `10.1145/3448016.3452809` | 2021 | Proceedings of the 2021 International Conference | proceedings | no | yes | yes |
| 11 | `10.14778/3746405.3746439` | 2025 | Proc. VLDB Endow. | journal | yes | yes | yes |
| 12 | `10.1145/3623278.3624754` | 2024 | Proceedings of the 28th ACM International Confer | proceedings | no | yes | yes |
| 13 | `10.14778/3778092.3778109` | 2025 | Proc. VLDB Endow. | journal | yes | yes | yes |
| 14 | `10.1002/spe.2984` | 2021 | Software: Practice and Experience | journal | yes | yes | yes |
| 15 | `10.1002/spe.2920` | 2021 | Software: Practice and Experience | journal | yes | yes | yes |
| 16 | `10.1002/spe.3296` | 2024 | Software: Practice and Experience | journal | yes | yes | yes |
| 17 | `10.1002/spe.3396` | 2025 | Software: Practice and Experience | journal | yes | yes | yes |
| 18 | `10.1002/spe.3261` | 2023 | Software: Practice and Experience | journal | yes | yes | yes |
| 19 | `10.1002/spe.3036` | 2022 | Software: Practice and Experience | journal | yes | yes | yes |
| 20 | `10.1002/spe.2777` | 2020 | Software: Practice and Experience | journal | yes | yes | yes |
| 21 | `10.1002/spe.70105` | 2026 | Software: Practice and Experience | journal | yes | yes | yes |
| 22 | `10.1145/3859286` | 2026 | ACM Trans. Archit. Code Optim. | journal | yes | yes | yes |
| 23 | `10.1145/3487552.3487827` | 2021 | Proceedings of the 21st ACM Internet Measurement | proceedings | no | yes | yes |
| 24 | `10.1145/3744916.3764533` | 2026 | Proceedings of the 2026 IEEE/ACM 48th Internatio | proceedings | no | yes | yes |
| 25 | `10.1145/3714465` | 2025 | ACM Trans. Softw. Eng. Methodol. | journal | yes | yes | yes |
| 26 | `10.1145/3736169` | 2025 | ACM Trans. Archit. Code Optim. | journal | yes | yes | yes |
| 27 | `10.1145/3760387` | 2025 | ACM Trans. Embed. Comput. Syst. | journal | yes | yes | yes |
| 28 | `10.1145/2807591.2807644` | 2015 | Proceedings of the International Conference for  | proceedings | no | no | yes |

## 4. Relevance checks on potentially weak citations

- [1] RFC 8259 — necessary standards citation, not a journal; correct as used.
- [2] Keiser & Lemire 2024 — Crossref abstract explicitly states that Apache Doris, the Node.js JavaScript runtime, Milvus, and Velox use On Demand; the Introduction's "adopted by production systems, including the Node.js runtime itself" is **supported** (Stage 4 #6 resolved PASS).
- [6], [7], [10], [12], [23], [24], [28] — conference proceedings; relevant to their sentences but do not count toward the 80% journal requirement.
- [3] was previously absent from the derived registry although cited in the manuscript; now corrected from Crossref (The VLDB Journal 28(6):941–960, 2019).

## 5. Decision and required action

No reference is fabricated and no irrelevant reference should be added purely to reach a quota (AVITEC explicitly discourages irrelevant citations and metric manipulation). The correct action is to source **12 additional, genuinely relevant, recent international journal articles** (e.g., peer-reviewed journal studies of JSON parsing, selective access, WebAssembly runtime performance, and rigorous performance methodology), verify each via Crossref, insert citations where they materially support the text, and regenerate the reference list, metadata, and literature registry. If such sources cannot be found, the manuscript is **not ready for submission** on literature grounds and the editor should be consulted.

## 6. Stage 6 verdict

**FAIL — LITERATURE BLOCKER.** All references exist and are verified, the Introduction has 20 journal citations (≥15), and all formatting criteria pass, but the recent-international-journal share is 71.4% against the 80% requirement. This blocker cannot be resolved by wording changes; Stage 7 will apply only the non-literature corrections from Stage 4/5, and the final verdict must reflect the unresolved literature gap.
