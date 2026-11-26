# Stage 7 — Manuscript Change Log (Final Evidence-Based Audit)

Date: 2026-11-19 · Source manuscript: `article/drafts/article-draft.md` (edited in place; template `article/article.docx` untouched) · HEAD unchanged `a1fad918a7…`.

No numerical result, estimand, CI, run classification, or reference count was changed. All revisions are wording/attribution corrections required by Stages 4–5. The literature blocker from Stage 6 is **not** resolved here (no references were added for quota reasons).

| # | Section | Previous wording | Revised wording | Reason | Evidence | Artifacts regenerated |
|---:|---|---|---|---|---|---|
| 1 | Introduction ¶1 | "the application **pays** allocation, property-creation, and garbage-collection costs for content it never reads" | "the application **can incur** … — a general property of eager parsing that this latency-only protocol does not measure" | Claim #5 WARN: mechanism not measured | Stage 4 matrix #5; protocol records (latency only) | docx |
| 2 | Introduction ¶3 | "which makes them the de-facto floor against which any replacement … must be measured" | "so they form a demanding baseline against which any replacement … must be measured" | Claim #7 WARN: unmeasured "floor" | Stage 4 #7 | docx |
| 3 | Methods ¶1 | "allowing the corpus documents and their derived structures to **coexist with the JavaScript heap**" | "a 64-bit linear address space for its arena; this is a design property of the binding, **not a measured memory result**" | Claim #10 WARN: architectural claim framed as result | `cabi.cpp` L90–120; Stage 1 | docx |
| 4 | Results A | "here the **crossing-heavy** on-demand path loses to the engine's highly optimized built-in parser" | "the on-demand path — which makes more, smaller calls across the binding — loses …; crossing cost is a **plausible explanation but was not isolated**" | Claim #17 WARN: causal attribution not measured | Stage 4 #17; A records have no isolated crossing factor | docx |
| 5 | Results D | "the warmed path is the steady state **a production server reaches** after its first read of each domain" | "cached bytes are built lazily and reused until a write; cost of first build outside window; characterizing the cold transition remains future work" | Claim #22 WARN: unmeasured production behavior | `MongoJsonRepository.js` L114–131 | docx |
| 6 | Discussion | "**Every crossing … costs** … the delivery overhead **disappears into** a 2.7–2.9× win" | "delivery mechanism is a **plausible contributor** … not isolated … crossing counts and marshalling time were not measured … **interpretation rather than established mechanism**" | Claim #25 WARN | Stage 4 #25 | docx |
| 7 | Comparison with Prior Results | "crossing cost, per-call binding overhead, and V8's optimized parser **overwhelm** the lazy strategy" | "observed disadvantage is **consistent with** the combined effect …; the protocol **does not isolate** those contributions" | Claim #27 WARN | Stage 4 #27 | docx |
| 8 | Threats to Validity | "paired design, rotation, warmup, and **fixed seed control order and start-up effects**" | "paired design, rotation, and warmup **address** order and start-up effects; fixed bootstrap seed **makes resampling reproducible and does not control measurement effects**" | Claim #26 FAIL: seed cannot control measurement order/startup | Stage 3 RNG verification | docx |
| 9 | Reproducibility | "Supporting runs … corroborate **every directional conclusion** reported here" | "Supporting runs reproduce the **A–D per-document ordering and repository shape** on the dev device; **they do not cover the endpoint**" | Claim #16 FAIL: no supporting E runs | ledger supporting rows; Stage 2 | docx |
| 10 | Introduction / RQs | "RQ3: **Does it transfer** to a complete HTTP endpoint?" | "RQ3: **To what extent does the repository-level difference persist** in the end-to-end latency of `GET /rekap`?" | Stage 5 WARN: binary framing unsupported by dev/server split | Stage 5; E CIs | docx |

Resolved without change: Stage 4 #6 — ref [2] Crossref abstract explicitly names the Node.js runtime among On Demand adopters, so the Introduction claim stands.

## Files changed in this revision

- `article/drafts/article-draft.md` (10 edits above)
- `article/drafts/article-draft.docx` (regenerated; builder QA: abstract 244, prose 5,326, citations [1]–[28] ordered, 0 post-punctuation, 28 DOI, 6 figures, 8 tables)
- `article/drafts/final-audit/research-question-audit.md` (RQ3 resolution note)

## Files deliberately not changed

- Numerical tables, chart data, raw records/exhibits, corpus, manifest, template DOCX, git state.
- Reference list and citation numbering (literature blocker remains open by design).
