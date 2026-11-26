# Final Quality Review — Evidence-Based Audit of the AVITEC Manuscript

Date: 2026-11-19 · HEAD `a1fad918a7fccb6464722ac35723c29800ba7849` (unchanged) · branch `research/nd11-phase-d-e-synthesis` · working tree: 31 pre-existing dirty entries preserved · template `article/article.docx` pristine (894,262 B).

## Overall verdict

**NOT READY — LITERATURE BLOCKER.**

All scientific, statistical, evidence, reproducibility, and editorial checks pass. One AVITEC requirement fails and cannot be resolved by wording changes: only **20/28 (71.4%)** references are recent international peer-reviewed journal articles, against the guideline's **≥80%** threshold. At least **12 additional genuine qualifying journal articles** are needed; they were **not** added because AVITEC forbids irrelevant or metric-driven citations and none could be justified from the existing evidence without further literature work. The final label therefore follows the evidence, not the completion of the checklist.

## 1. Gate summary

| Stage | Result | Output |
|---|---|---|
| 0 Repository/artifact inventory | **PASS** (two submodules excluded by owner instruction) | `repository-inventory.md` |
| 1 Source-code audit | **PASS** | `source-code-audit.md` |
| 2 Experimental evidence audit | **PASS** (43/43 primary cells, E structure, 6/6 corpus hashes) | `experimental-evidence-audit.md` |
| 3 Statistical audit | **PASS** (63/63 cells, deterministic twice, PCG64 verified) | `statistical-audit.md` |
| 4 Claim-by-claim audit | **WARN → resolved in Stage 7** (2 FAIL + 7 WARN wording issues) | `claim-evidence-matrix.md` |
| 5 RQ framing | **WARN → resolved in Stage 7** (RQ3 wording) | `research-question-audit.md` |
| 6 Literature audit | **FAIL — LITERATURE BLOCKER** | `literature-audit.md` |
| 7 Manuscript revision | **PASS** (10 corrections; no numerical changes) | `manuscript-change-log.md` |
| 8 Figures/tables/metadata | **PASS** (45 displayed values, 43 chart rows, metadata identical) | `final-audit-artifacts.json` |
| 9 Final validation | **PASS** (DOCX 14/14 checks; PDF 14 pages, 6/6 content checks) | `final-audit-pdf.json`, this report |

## 2. Scientific correctness

- Measured implementation is `scanner8` (table-driven with intra-string SWAR), not scanner128 SIMD (`ze_json/src/ondemand/parallel.cpp` L287–311). Manuscript makes no SIMD claim.
- A–B: V8 is faster (S = 0.04–0.07 and 0.08–0.16); C: heterogeneous/payload-dependent; D: ZE advantage only on warmed Mongo canonical bytes (2.88/2.67), file-store negative (0.95/0.99); E: dev not distinguishable, server 1.1544. All match recomputed raw exhibits.
- No claim of parser-only benefit for D or E; no H₀ verdict; no CPU/memory/energy claim; mechanism explanations explicitly labeled as interpretations after Stage 7.
- Negative and near-parity results retained throughout.

## 3. Statistical validity

- Estimand `S = median(T_V8,i)/median(T_ZE,i)` over 15 paired rounds, **ratio of across-round medians** (not median of ratios), used identically in abstract, methods, results, tables, figures, and conclusion.
- Paired round-level bootstrap: B=10,000, seed `20261117`, `numpy.default_rng` → **PCG64** verified, joint index resampling, percentile 95% CI; BCa computed as sensitivity only (archived per cell).
- Phase E: 15 rounds × 20 requests total (10+10), 150/engine, 300/run, one body hash; 150 requests never treated as independent inferential units.
- No pooled-point/round-CI mismatch; legacy pooled 1.076/1.041/1.134 appears only as a Table 7 note.
- Two independent pipeline runs produced identical ledger SHA-256 `800218AF…` and provenance SHA-256 `1E5F1EE1…`; 63/63 cells recomputed from raw exhibits `MATCH`.

## 4. Evidence traceability

- 11 primary records re-validated: 11/11 PASS; 43 primary point estimates recomputed from `out/raw/<run_id>/` exhibits with `MATCH`.
- 63-row ledger with 126 SHA-256 file provenance entries; 45 numeric triples displayed in the manuscript all match ledger values.
- Six corpus per-file SHA-256 values in all three Phase E records and on disk match `corpus/benchmarks/saq_payload_v1/MANIFEST.json`; the "LIVE store" label is documented, but **no "live operational data" claim** is made.
- Excluded: Node 24 run `0dcb418`, core-0.3.1 run `3376d07` (corroboration only), `thesis-proposal` and `submission-thesis-supervisor` (owner instruction).

## 5. Reproducibility

Generators and derived outputs are retained: `article/scripts/Ledger/`, `Charter/`, `Builder/`, `Grapher/`, `FinalAudit/`; derived JSON under `article/data/json/`; charts under `article/drafts/charts/`; diagrams regenerated from `article/data/mmd/` + Pele SVG. Rebuild order: ledger → audit → charter export → charts → DOCX → DOCX verify → Word COM PDF → PDF finalizer → final-audit verifiers.

## 6. Literature compliance

| Criterion | Result |
|---|---|
| References total | 28 (≥15 ✓) |
| Crossref/registry verified | 28/28 ✓ |
| Introduction journal citations | 20 (≥15 ✓) |
| Recent international journal share | **20/28 = 71.4% (FAIL; need ≥80%, i.e. ≥23/28, or 12 more journal refs if added)** |
| Title words | 11 (≤20 ✓) |
| Abstract words | 244 (≤250 ✓) |
| Keywords | 5 (3–7 ✓) |
| Word count | 5,326 prose / 6,035 body (5,000–8,000 ✓) |
| Non-English refs | 0% (≤25% ✓) |
| Citation format | [1]–[28] first-appearance order, 0 post-punctuation ✓ |

Ref [3] was missing from the derived registry although cited in the manuscript; it was re-verified via Crossref (`The VLDB Journal` 28(6):941–960, 2019, `journal-article`) and added to `literature-matrix.csv` / `crossref_verify.json`. PVLDB is counted as a journal on Crossref evidence (`type: journal-article`, ISSN 2150-8097); proceedings, RFC, and arXiv are not counted.

## 7. Editorial completeness

- Final DOCX/PDF regenerated from the revised Markdown; template untouched.
- No placeholders, no future editorial dates in the draft, correct method heading, complete factual AI declaration, no highlight markup, no automatic footnote (Table 7 uses an inline note directly under the table).
- PDF: 14 pages, metadata title/author/subject/keywords correct, no empty pages, all figures/tables/captions and references [1]–[28] present; visual spot-check of changed pages confirmed rendered correctness.
- `verify_docx.py`: **14/14 PASS**; `verify_final_pdf.py`: **6/6 PASS**.

## 8. Remaining blockers and risks

1. **Literature (critical):** 12 genuine recent international journal articles must be added (or the editor consulted). This alone determines the NOT READY verdict.
2. Plagiarism similarity check not performed (no tool/account in this environment) — required before submission.
3. Article history dates are editorial placeholders; masthead (Vol. 9 No. 1 February 2027, pp. 1-20, DOI example) remains a template artifact.
4. Single run per cell (except E dev ×2); intervals are within-run; no cross-site pooling; no CPU/memory/energy/cold-cache measurements.
5. PR #79 remains open; 31 pre-existing dirty entries and submodule dirt preserved; no commit/push/merge/branch switch.

## 9. Submission readiness decision

**NOT READY — LITERATURE BLOCKER.** After 12 verified, relevant journal references are added and the bibliography/citation numbering/metadata/registries are regenerated, Stages 6–9 must be re-run. There is no scientific or statistical blocker: every displayed number is traceable to raw evidence and the estimand is applied consistently.

## 10. Handoff

- Final manuscript source: `article/drafts/article-draft.md`; generated DOCX: `article/drafts/article-draft.docx`; **final PDF: `article/drafts/article-draft.pdf`** (14 pages).
- Nine audit deliverables: `article/drafts/final-audit/*.md`.
- Derived verification JSON: `article/data/json/final-audit-{evidence,statistics,literature,artifacts,pdf}.json` and `orientation-audit.json`.
- Untouched: `article/article.docx`, `out/raw/**`, `reports/**`, `corpus/**`, submodule pointers, pre-existing dirty entries.
