# Stage 0 — Repository and Artifact Inventory

Audit date: 2026-11-19 · Workspace: `D:\kuliah_\7_semester\skripsi\v5`

## 1. Repository identity

| Item | Verified value | Method |
|---|---|---|
| Remote | `https://github.com/zuudevs/thesis.git` (fetch + push) | `git remote -v` |
| Branch | `research/nd11-phase-d-e-synthesis` | `git branch --show-current` |
| HEAD | `a1fad918a7fccb6464722ac35723c29800ba7849` | `git rev-parse HEAD` — matches expected |
| Working tree | 31 dirty entries before execution | `git status --porcelain` |

Pre-existing modifications (preserved, not touched by this audit): `M .gitmodules`, `M saq-report`, `M scripts/grapher/make-graph.ts`, `M submission-thesis-supervisor`, `D thesis-proposal`, `D utils/typ/metadata.example.json`, `D utils/typ/metadata.typ`, `D utils/typ/strfmt.typ`, `?? article/`, and 22 untracked `reports/charts/*.csv`.

## 2. Submodules (from Git tree)

| Submodule | Pinned gitlink | Working-tree HEAD | Status in this audit |
|---|---|---|---|
| `ze_json` | `01a143f118238370c6079f6bf3796d302c547341` | identical | **IN SCOPE** — source audited |
| `saq-report` | `534d9a819e01225157b7b1cb9cefd0839a22b69b` | identical (dirty) | **IN SCOPE** — source audited |
| `thesis-proposal` | `4059b23bcefd4df24b30d5abeb1a3c58722b4226` | directory absent; object unavailable locally | **EXCLUDED — owner instruction** (no fetch, no claim) |
| `submission-thesis-supervisor` | `015188cea747ec714cd460de6af3c3da40361b99` | identical (dirty); absent from `.gitmodules` (hence `git submodule status` errors) | **EXCLUDED — owner instruction**; mismatch documented only |

No other gitlink entries exist (`git ls-files --stage | 160000` returned exactly these four).

## 3. Manuscript versus template

| Role | Path | Size | Note |
|---|---|---:|---|
| **Pristine AVITEC template** | `article/article.docx` | 894,262 B | Never modified; verified at every rebuild |
| **Working manuscript (source of truth)** | `article/drafts/article-draft.md` | 52,958 B | Edited directly; all revisions flow through this |
| Generated DOCX | `article/drafts/article-draft.docx` | 2,225,653 B | Built from template + Markdown by `Builder/build_docx.py` |
| Generated PDF | `article/drafts/article-draft.pdf` | 989,275 B | 14 pages; metadata from DOCX core properties |
| QA renders | `article/drafts/qa-render/page-01..14.png` | 14 files | Visual QA artifacts |

Supporting artifacts: `article/metadata.json`; prior reports (`source-audit.md`, `paired-bootstrap-estimand-spec.md`, `figure-table-plan.md`, `avitec-requirements.md`, `speedup-orientation-audit.md`, `statistical-recomputation-report.md`, `manuscript-change-log.md`, `final-quality-review.md`, `stage9-handoff.md`) — **treated as claims to re-verify, not as evidence**.

## 4. Scripts, data, and evidence directories (in scope)

- Generators: `article/scripts/Ledger/{build_ledger,export_charter_raw,audit_orientation}.py`, `article/scripts/Charter/main.py`, `article/scripts/Builder/{build_docx,verify_docx,finalize_pdf,inspect_template}.py`, `article/scripts/Grapher/` (Mermaid/Pele pipeline), `article/scripts/Literature/`.
- Derived data: `article/data/csv/evidence-ledger.csv` (63 rows), `article/data/json/evidence-ledger.provenance.json` (126 files), `article/data/json/crossref_verify.json`, `article/data/json/orientation-audit.json`, `article/data/csv/literature-matrix.csv`.
- Chart data/outputs: `article/scripts/Charter/raw/*/{data.csv,provenance.json,README.md}`, `article/drafts/charts/chart{1,2,3}*.{png,svg}`, `article/assets/images/*.svg`.
- Raw evidence: `out/raw/<run_id>/` — all 11 primary exhibits present (`nd6_phase_{A,B,C,D}.json` ×2 sites, `nd11_phase_e.json` ×3); `reports/nd14/`, `reports/nd11/` records; `corpus/benchmarks/saq_payload_v1/MANIFEST.json`.
- Implementation evidence: `ze_json/{include,src,bindings}`, `saq-report/{repositories,routes,views}`.

## 5. Missing / inaccessible artifacts

- `thesis-proposal` working tree and pinned object `4059b23…` — **excluded by owner instruction**; no attempt to fetch or reconstruct.
- `submission-thesis-supervisor` `.gitmodules` mapping — absent; excluded by owner instruction; working tree itself readable but not audited.
- No primary-run exhibit is missing from `out/raw/`; no manuscript source is missing.

## 6. Stage 0 verdict

**PASS (with recorded exclusions).** Repository identity matches the expected checkout; both in-scope submodules are available at their pinned commits; the actual manuscript is identified as `article/drafts/article-draft.md` with generated DOCX/PDF; all primary evidence artifacts are present. Stage 1 is authorized.
