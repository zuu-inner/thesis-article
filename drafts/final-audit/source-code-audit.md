# Stage 1 — Submodule and Source-Code Audit

Scope: `ze_json` @ `01a143f118238370c6079f6bf3796d302c547341` and `saq-report` @ `534d9a819e01225157b7b1cb9cefd0839a22b69b`. `thesis-proposal` and `submission-thesis-supervisor` are **excluded by owner instruction**; no claim in this report depends on them.

## 1. ze_json — measured implementation

| Item | Verified implementation | Evidence |
|---|---|---|
| Default scanner | `scanner8`, a table-driven byte scanner with an 8-byte SWAR block step **only inside string interiors** | `src/ondemand/scalar.cpp` L7–44; `core::kJsonCharClass` table load L57–60; SWAR `swar_eq` L66–70 |
| Structural scan dispatch | `structural_scan()` returns `&scanner8` unconditionally (both 64-bit and fallback branches) | `src/ondemand/parallel.cpp` L287–311; documented P4-2 measured decision L294–305 |
| `scanner64` | Standalone SWAR variant (`utils/swar.hpp`), **not** the default; measured slower on 5/6 corpora | `parallel.cpp` L13–34, L294–305 |
| `scanner128` | Standalone 128-bit SIMD variant (`core::simd_*`, SSE2 / wasm-simd128 bitmask), **not** the default | `parallel.cpp` L156–171, L183–243 |
| On-demand access | `Document::open(Arena&, src, size)`, `get_root()`, structural `index_count`; `Value` lazy access / spans | `include/ze_json/ondemand/document.hpp` L33–81; `value.hpp` L34–111; `src/ondemand/document.cpp` L259 |
| String / number | Lazy string decode (`escaped` flag → `unescape_string`) and separate number promotion path | `value.hpp` L34; `src/ondemand/string.cpp` L23; `src/ondemand/number.cpp`, `number.hpp` |
| Ownership / allocation | Static C-ABI slot pool `kParserSlotMax = 64`; each slot owns an `Arena` placed in static storage; bump heap with `ze_reset_heap` rewind; no free | `include/ze_json/abi/cabi.hpp` L186; `src/abi/cabi.cpp` L11–13, L35–48, L90–120, L205–243 |
| ABI | v3 on-demand parser surface plus additive v4/v5; `kAbiVersion = ZE_JSON_VERSION`; 64-bit handles packed at bit 32 | `cabi.hpp` L10–67, L127–178, L182–207 |
| JS binding | `SCANNER_MODES` exposes scanner8/64/128 explicitly; production default is library dispatch (scanner8 today); `ZeParser` uses lazy frame `(ts, cursor)` | `bindings/js/ze_json.mjs` L58–62, L169–217, L279–285, L376, L529–561 |
| Error handling | `core::Result<T, JsonErrc>`; error codes / precedence contract byte-identical to reference scan | `scalar.cpp` L38–40; `core/result.hpp`, `core/error.hpp` |
| Actual runs | Primary record: `library.abi_version = 2026000302`, `core_version = 0.3.2`, `js_version = 0.3.0`, wasm SHA-256 `9795f2e8…`, Node 26.13.1 / V8 14.6; no scanner override in `config` | `reports/nd14/zuu-20261115071747-6d87bf3-nd6-a-dev_device.record.json` (`config`, `library`, `host`) |

**Verdict PASS.** The measured configuration is `scanner8` (scalar table-driven + intra-string SWAR blocks); there is no evidence that scanner128 SIMD was used. The manuscript's terminology ("C++23 on-demand JSON parser exposed through a WebAssembly 64-bit binding", default byte-level scanner) is accurate. Any phrase implying SIMD-accelerated measurement would be unsupported.

## 2. saq-report — measured workload paths

| Path | Implementation | Measurement meaning |
|---|---|---|
| File-store `read()` | `fs.readFileSync` + `JSON.parse` + rootKey extraction | Baseline full materialization (`JsonRepository.js` L26–42) |
| File-store `readCount()` | Reads raw bytes and calls `countJsonBytes(raw, rootKey, default)` | On-demand structural count over original bytes (**not** a cache) (`JsonRepository.js` L55–87) |
| Mongo `read()` | `cloneJson(this._cache)` — full clone | Baseline clone (`MongoJsonRepository.js` L88–94) |
| Mongo `readCount()` | `countJsonBytes(this._ensureCacheBytes(), null)` | On-demand count over canonical cached bytes (`MongoJsonRepository.js` L106–112) |
| Canonical-byte cache | `_cacheBytes = Buffer.from(JSON.stringify(this._cache))`, built lazily and invalidated on `write()` | The optimization is **caching + canonical bytes + lazy count**, not parser-only (`MongoJsonRepository.js` L54–56, L114–131, L133–139) |
| ZE binding | Loads wasm64, parity contract with `read().length`; error-location parity | `repositories/zeJsonBinding.js` L4, L69–81, L100–135 |
| `/rekap` GET root | `SAQ_JSON_ENGINE === 'ze' ? readCount()×4 : read().length×4`, then `res.render('rekap-pilihan', …)` | Phase D/E measured path: four repository counts/reads + EJS render + HTTP response; `globalConfig` read occurs in later helpers, not the counted four (`routes/rekapRoutes.js` L25–47, L58) |
| App wiring | `app.use('/rekap', rekapRoutes)` | Endpoint scope is `/rekap` only (`server.js` L32, L42, L80) |

**Verdict PASS.** Phase D measures repository design (warm canonical-byte cache vs file bytes + parser access); Phase E measures the full `GET /rekap` path including rendering and HTTP serialization. Neither isolates parser latency. The manuscript's claim boundaries (D = store design + parser; E = end-to-end) are supported.

## 3. Excluded modules

`thesis-proposal` (gitlink `4059b23…`) and `submission-thesis-supervisor` (gitlink `015188c…`) were excluded per owner instruction. No experiments, implementation, or claims in this audit rely on them.

## 4. Stage 1 gate

**PASS** — both in-scope submodules were read at their pinned commits; default scanner, cache semantics, endpoint scope, ABI/version, and ownership model are verified from source. Stage 2 authorized.
