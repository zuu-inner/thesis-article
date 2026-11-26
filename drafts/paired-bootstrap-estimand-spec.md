# Spesifikasi Estimand & Paired Bootstrap — Analisis Inferensial V8 vs ZE

> **Status**: spesifikasi metodologis final untuk seluruh analisis inferensial artikel
> (fase A–E, dev + server). Dokumen ini mengaudit struktur observasi dari raw data,
> mengevaluasi kandidat estimand, menetapkan estimand primer, dan menspesifikasikan
> prosedur paired bootstrap beserta confidence interval.
>
> **Verdict audit: WARN** — spesifikasi lengkap dan didukung bukti; tiga asumsi
> wajib dinyatakan (§12). Tidak ada sel `UNRESOLVED` pada tabel keputusan akhir.
>
> **Cakupan eksekusi**: dokumen ini adalah spesifikasi, bukan refactor. Tidak ada
> kode analisis, record, raw exhibit, atau working tree yang diubah saat penyusunan.
> Audit dibaca pada HEAD `a1fad918a7fccb6464722ac35723c29800ba7849`
> (branch `research/nd11-phase-d-e-synthesis`, PR #79 OPEN).
> Bahasa: catatan kerja Indonesia; simbol/path/commit tetap asli.

---

## 1. Executive summary dan keputusan metodologis

1. **Estimand primer untuk semua fase (A, B, C, D, E) adalah rasio median round-level:**

   $$\theta \;=\; \frac{\operatorname{Median}_i(T_{V8,i})}{\operatorname{Median}_i(T_{ZE,i})}, \qquad i = 1,\dots,15$$

   dengan $T_{E,i}$ = agregat dalam-ronde yang didefinisikan operasional per fase
   (§4). Arah $S = T_{V8}/T_{ZE}$ dipertahankan di seluruh tabel, chart, dan teks.

2. **Prosedur inferensi**: paired round-level bootstrap — 15 ronde diresample
   **secara joint** (indeks sama untuk kedua engine), statistik per replikasi
   **identik** dengan point estimator, $B=10{,}000$, seed `20261117`,
   `numpy default_rng` (PCG64), interval **percentile 95%** (2,5/97,5) pada skala rasio.

3. **Tiga inkonsistenan terdeteksi** di implementasi analisis lama
   (`scripts/analyze_measurement/nd_d_e_synthesis.py` + laporan sintesis):
   - **#1 (Codex P2 #1, terkonfirmasi & dikuantifikasi)**: point estimate Phase E
     dihitung dari median **150 request pooled** per engine (L475) sedangkan CI
     dihitung dari **15 median ronde** (L472). CI yang dilaporkan bukan CI untuk
     angka yang ditampilkan. Contoh: dev run 1, pooled = 1,076 vs rasio median
     ronde = 1,050 (CI 0,935–1,147).
   - **#2 (temuan audit baru)**: kolom `speedup_median` bermakna **tiga definisi
     berbeda** dalam satu script: Phase A–C = median rasio per-ronde (L600),
     Phase D = rasio median ronde (L357), Phase E = rasio median pooled (L475).
   - **#3 (Codex P2 #2, terkonfirmasi)**: verdict H₀ proposal pada
     `reports/nd11-phase-d-e-synthesis.md` L231 menyimpulkan "tertolak" dari
     boundary repository/endpoint — bukan uji parser-only; dua dari tiga dimensi
     H₀ (throughput, konsumsi memori) tidak diukur di D/E.

4. **Implementasi bootstrap eksisting (`bootstrap_median_ratio_ci`, L222–235)
   sudah benar dan deterministik** — rekalkulasi audit mereproduksi CI laporan
   persis (mis. D dev mongo 2,5724–3,0451). Yang salah bukan prosedurnya, melainkan
   **konvensi point estimate** Phase E dan **konsistensi lintas fase**.

5. **Koreksi menggeser angka dua arah, bukan pro-ZE**: dev E turun
   (1,076 → 1,050; 1,041 → 1,028), server E naik (1,134 → 1,154), D tidak berubah
   (sudah round-level). Verdict per sel tidak berubah (§9).

6. **Keputusan estimand diturunkan dari desain eksperimen** (unit ronde yang
   dideklarasikan harness + konvensi `speedup_in_run` Phase D + statistik
   bootstrap eksisting), **bukan** dari nilai yang paling menguntungkan ZE
   (§3, §4, §9).

---

## 2. Audit struktur data dan unit observasi

### 2.1 Registry eksperimen (dari bukti aktual, bukan ringkasan)

Semua record di bawah **PASS** `scripts/measurement-schema/validate.py`
(dijalankan ulang pada audit ini, 2026-11-17): 11/11 PASS.

| Eksperimen | Run (run_id) | Site | Kelas | Root/commit | Bukti raw |
|---|---|---|---|---|---|
| A dev | `zuu-20261115071747-6d87bf3` | dev_device | primary | root `6d87bf3` | `reports/nd14/raw/<rid>/nd6_phase_A.json` (+ salinan `out/raw/`) |
| A server | `server-lanjut-20261116060843-8a1324b` | saq_server | primary | root `8a1324b` | `reports/nd14/raw/<rid>/nd6_phase_A.json` |
| B dev | `zuu-20261115075332-6d87bf3` | dev_device | primary | root `6d87bf3` | `.../nd6_phase_B.json` |
| B server | `server-lanjut-20261116060900-8a1324b` | saq_server | primary | root `8a1324b` | `.../nd6_phase_B.json` |
| C dev | `zuu-20261115080838-6d87bf3` | dev_device | primary | root `6d87bf3` | `.../nd6_phase_C.json` |
| C server | `server-lanjut-20261116060915-8a1324b` | saq_server | primary | root `8a1324b` | `.../nd6_phase_C.json` |
| D dev | `zuu-20261115080840-6d87bf3` | dev_device | primary | root `6d87bf3` | `.../nd6_phase_D.json` |
| D dev | `zuu-20261115010155-3376d07` | dev_device | **supporting** (core 0.3.1) | root `3376d07` | `.../nd6_phase_D.json` |
| D server | `server-lanjut-20261116060933-8a1324b` | saq_server | primary | root `8a1324b` | `.../nd6_phase_D.json` |
| E dev run 1 | `zuu-20261116101458-8556513` | dev_device | primary | root `8556513` | `reports/nd11/raw/<rid>/nd11_phase_e.json` |
| E dev re-run | `zuu-20261117000112-6979e3f` | dev_device | primary | root `6979e3f` | `.../nd11_phase_e.json` |
| E server | `server-lanjut-20261117003513-530f751` | saq_server | primary | root `530f751` | `.../nd11_phase_e.json` |
| E pilot | `zuu-20261116235636-ab255f5` | dev_device | **pilot — excluded** | root `ab255f5` | protokol beda: 2 ronde × 3 request **TOTAL** (v8: 1+2, ze: 2+1), warmup 2 |

Commit `ze_json`/`saq-report` per run tercantum di `record.library.version`
(terverifikasi untuk D: `6d87bf3` → core 0.3.2; E server: `530f751`); identitas
wasm per run = `record.library.artifact_sha256`. Era lama
(`zuu-20261112063944-0dcb418`, Node v24.19.0, ze_json `14592a0` — sumber
`reports/charts/nd6-phase-*.csv` yang tak terlacak) **tidak comparable** dan
dikecualikan dari semua analisis inferensial.

### 2.2 Struktur observasi per fase (verifikasi harness, bukan asumsi)

**Fase A/B/C** (`scripts/bench/nd6_bench.mjs`, `--phase A|B|C`):

- Jalur per fase (L244–313): A = `v8-parse`, `v8-clone` (referensi), `ze-parse`;
  B = `v8-selective`, `ze-project-selective`; C = `v8-selective`, `ze-l1-traversal`.
- `reps = targetReps(bytes) = max(1, min(30, floor(200000/bytes)))` (L379–380) —
  **reps per dokumen**: 30 (courses, assistants, lecturers, globalConfig),
  5 (schedules, reports); diverifikasi dari exhibit `raw_rounds[].reps`.
- `runPathRound` (L387–392): satu nilai ronde = `dt/reps` =
  **rata-rata `reps` iterasi** (timing `performance.now()` di luar loop iterasi).
- `measureBlock` (L394–423): warmup 3 iterasi/jalur untimed (L396–398); 15 ronde
  (L399–410); **urutan jalur dirotasi per ronde** `off = r % paths.length`
  (L400–402) — kontrol bias urutan/thermal; exhibit menyimpan `rounds_ms` per
  jalur **dalam urutan ronde** (push per iterasi ronde, L406).
- Pasangan round-level: `rounds_ms[i]` jalur V8 vs jalur ZE pada indeks ronde yang
  sama — pasangan **by construction** (kedua engine diukur dalam ronde yang sama,
  urutan eksekusi dirotasi). **Tidak ada pairing iterasi-level**: iterasi dibatch
  per jalur (loop `reps` di dalam satu jalur, satu demi satu).
- `pushResult` (L425–465): `seconds_mean` = mean antar-ronde; `extras.seconds_median`
  = **median antar-ronde**; `seconds_p95` = interpolasi linier; `stddev` = populasi
  (ddof=0); **tanpa trimming**.

**Fase D** (jalur `--phase D`, L316–362 + L480–494):

- Empat jalur: `D-file-store-v8`, `D-file-store-ze`, `D-mongo-cache-v8`,
  `D-mongo-cache-ze`. Satu iterasi = satu "request `/rekap`" = sweep 4 repo
  (courses, assistants, schedules, reports; `globalConfig` di luar iterasi `.length`).
- `reps = targetReps(BYTES_TOTAL)` = **2** (diverifikasi dari exhibit:
  `reps=2`, dan record `extras.reps_per_round=2`, `config.iterations=2`).
- Nilai ronde = mean 2 iterasi. **Catatan matematis**: untuk n=2, mean ≡ median —
  agregasi "mean of reps" dan "median of reps" koinsiden.
- Mongo-cache = warm cache steady-state (state pasca-`init()` direplikasi tanpa
  MongoDB, L322–326; stringify bytes kanonik pertama jatuh di warmup untimed).
- Keempat jalur diukur dalam ronde yang sama (rotasi `off = r % 4`); pasangan
  analisis = jalur V8 vs jalur ZE **dalam store yang sama**. Perbandingan
  antar-store (mongo vs file) **bukan** pasangan hipotesis — dilaporkan terpisah.

**Fase E** (`scripts/bench/nd11_phase_e.mjs`):

- Dua instance aplikasi byte-identik di localhost (v8 port A, ze port B, toggle
  `SAQ_JSON_ENGINE`), load generator satu host (L1–54, L180–202).
- Warmup 3 request/jalur untimed, bergantian (L410–420).
- Ronde terukur (L422–438): `r = 1..15`, `k = 0..19` — **20 request per ronde
  TOTAL**, engine dipilih `(r+k)%2 === 0 ? 'v8' : 'ze'` → **10 V8 + 10 ZE per
  ronde**; eksekusi **sekuensial** (`await requestOnce`); start-engine bergantian
  per ronde (r ganjil mulai ze, r genap mulai v8). n = 150/engine, 300 total
  (diverifikasi dari exhibit: `r1..r15` masing-masing 10/10 per engine).
- Latensi per request = `performance.now()` di sekitar `fetch` + pembacaan body
  (`requestOnce`, L320–331). **Parity gate**: seluruh 300 body byte-identik
  (1 hash unik; mismatch = run void, tanpa record, L442–450).
- `speedup_in_run` harness (L492–493) = rasio **median pooled 150 request** per
  engine — konvensi deskriptif harness (lihat §10 #1).
- Exhibit menyimpan **raw per-request** `{round, seconds, body_bytes, body_sha256}`
  (L589–594) — agregasi dalam-ronde apa pun dapat dihitung ulang.
- **Pairing request-level TIDAK didesain**: alternasi bersifat posisional (urutan
  slot), semua request workload-nya identik (parity), dan tidak ada identitas
  workload per request yang membedakan pasangan. Kedekatan temporal request
  bersebelahan (posisi k vs k+1) bisa menjadi *diagnostik* opsional, bukan pasangan
  yang didesain → bukan dasar estimand primer.

### 2.3 Kelengkapan, kegagalan, dan keadaan khusus

- **Tidak ada data hilang/terbuang/retry** di record yang diterima: harness tanpa
  retry (`requestOnce` throw pada status ≠ 200 → run gagal tanpa record;
  parity mismatch / child death = run void instan). Mode kegagalan menghasilkan
  **void**, bukan data parsial.
- **Semua ronde workload sebanding**: A–C (dokumen & konsumen sama per ronde),
  D (sweep 4 repo sama per ronde; warm cache steady-state), E (endpoint, store,
  dan respons byte-identik; parity gate). Tidak ada trimming; seluruh 15 ronde
  masuk analisis.
- **Perbedaan antar-run yang relevan**: dev vs server = host, runtime, commit
  `saq-report`, dan store berbeda (E server = store LIVE + koeksistensi produksi);
  D dev `3376d07` = core 0.3.1 (supporting). Semua dilarang dipooling (AGENTS §4).
- **Konvensi nama ambigu** (sudah didisambiguasi sintesis, dipertahankan di sini):
  `reps_per_round` pada record **D** = iterasi per engine per ronde (2);
  pada record **E** = request per ronde **TOTAL dua engine** (20).

### 2.4 Tabel unit

| Konsep | Fase A–C | Fase D | Fase E |
|---|---|---|---|
| Observasi mentah | timing `reps` iterasi per jalur-ronde (tidak dipertahankan per-iterasi; tersimpan agregat mean) | timing 2 iterasi sweep 4-repo (agregat mean tersimpan) | latensi per request (raw tersimpan penuh) |
| Unit eksperimen | satu pengukuran jalur dalam satu ronde | satu pengukuran jalur dalam satu ronde | satu request HTTP |
| Unit pairing | ronde (indeks ronde sama V8–ZE) | ronde (indeks ronde sama per store) | ronde (10+10 request, alternasi posisional) |
| Unit resampling | ronde (diambil bersama) | ronde (diambil bersama) | ronde (diambil bersama) |
| Unit inferensi | 15 ronde berpasangan per run per dokumen | 15 ronde berpasangan per run per store | 15 ronde berpasangan per run |

300 request Phase E **bukan** 300 observasi independen; nilai inferensial hanya
pada 15 pasangan ronde (dokumen sintesis L30–31; harness `nd11_phase_e.mjs`).

---

## 3. Tabel perbandingan kandidat estimand

Kandidat dievaluasi terhadap: kesesuaian dengan unit inferensi (ronde),
kemampuan dipasangkan dengan prosedur bootstrap yang mempertahankan pairing,
robustness, dan kesesuaian dengan konvensi repo (definisi $S=T_{V8}/T_{ZE}$
yang sudah dipakai laporan sebelumnya).

| Kandidat | Definisi | Pairing dipertahankan? | Kelebihan | Kekurangan | Peran |
|---|---|---|---|---|---|
| **A — median rasio per-ronde** | $\theta_A = \operatorname{Median}_i(S_r)$, $S_r = T_{V8,r}/T_{TZE,r}$ | Ya (rasio per pasangan) | statistik paired sejati; interpretasi "speedup ronde tipikal" | bukan konvensi repo; menyimpang dari semua laporan D sebelumnya; bootstrap-nya berbeda dari implementasi eksisting | **sekunder deskriptif berlabel** (`paired_median_ratio`) |
| **B — geometric mean rasio per-ronde** | $\theta_B = \exp(\overline{\log S_r})$ | Ya | efek multiplicative rata-rata; sensitif ke semua ronde | tidak robust: seluruh ronde (termasuk outlier) memengaruhi hasil; interpretasi kurang cocok untuk "speedup tipikal" | sensitivitas saja |
| **C — rasio statistik agregat (pooled / round)** | $\theta_C = \operatorname{Median}(T_{V8})/\operatorname{Median}(T_{ZE})$ | **C′ (round): ya — unit resampling = pasangan ronde; C-pooled: tidak pada level point** | robust (median); konvensi repo & `speedup_in_run` D; cocok dengan bootstrap eksisting | pooled mengabaikan struktur ronde di point (E); harus dilabeli eksplisit | **C′ = PRIMER**; C-pooled = deskriptif (E) |
| **D — rasio request/iterasi individual** | rasio observasi individual per pasangan buatan | Tidak — pasangan tidak didesain | — | pasangan buatan (posisional/array) tanpa bukti desain; E: identitas request tidak ada; A–D: iterasi dibatch per jalur | **tidak layak sebagai primer** |
| **E — cluster bootstrap atas pooled-request** | point pooled, bootstrap = resample ronde lalu hitung pooled dari request ronde ter-sample | Ya (cluster) | membuat point E lama konsisten dengan CI | mempertahankan estimand marginal (bukan round-level) yang melanggar unit inferensi yang dideklarasikan; konvensi beda dari D | alternatif yang sah secara internal, ditolak sebagai primer (alasan §4.7) |
| **F — diagnostik adjacent-pair (E)** | rasio pasangan request bersebelahan dalam ronde | sebagian (kedekatan temporal) | deteksi bias urutan mikro | bukan pairing yang didesain | diagnostik opsional, bukan primer |

**Kesimpulan**: satu estimand primer untuk semua fase = **C′ (rasio median
round-level)**; A dan B dipertahankan sebagai deskriptif/sensitivitas; C-pooled
untuk E didemosi ke deskriptif; D dan F tidak layak primer.

---

## 4. Definisi estimand primer (verbal, matematis, operasional)

### 4.1 Definisi verbal

> Untuk satu run pengukuran, estimand adalah **rasio antara latensi round-tipikal
> jalur V8 dan latensi round-tipikal jalur ZE**, di mana "latensi round" adalah
> agregat yang terdefinisi operasional dari seluruh observasi engine tersebut
> dalam satu ronde pengukuran yang sama. Nilai θ = 1 berarti kedua jalur
> setara pada level ronde; θ > 1 berarti ZE lebih cepat pada ronde tipikal;
> θ < 1 berarti V8 lebih cepat. Estimand ini terbatas pada satu run_id:
> tidak ada pooling lintas run, site, commit, atau boundary.

### 4.2 Definisi matematis

Untuk satu run dengan $R = 15$ ronde berpasangan dan agregat dalam-ronde
$T_{V8,i}, T_{ZE,i}$ (definisi operasional di §4.3):

$$\boxed{\;\theta \;=\; \frac{\operatorname{Median}\{T_{V8,1},\dots,T_{V8,15}\}}{\operatorname{Median}\{T_{ZE,1},\dots,T_{ZE,15}\}}\;}$$

- Bobot ronde setara: median tidak membobot; tiap ronde kontribusinya setara.
- Median pembilang dan penyebut dihitung dari **masing-masing marginal round-level**
  pada pasangan ronde yang sama (resampling joint menjaga pasangan tetap utuh
  dalam inferensi; median adalah fungsi marginal, dan itu dinyatakan eksplisit
  sebagai properti estimand, bukan penyamaran).
- Estimand ini adalah **fungsi dari distribusi round-level** — sesuai unit
  inferensi yang dideklarasikan desain (§2.4).

### 4.3 Definisi operasional $T_{E,i}$ per fase

| Fase | $T_{E,i}$ (agregat dalam-ronde) | Sumber | Dapat dihitung ulang? |
|---|---|---|---|
| A | $T_{E,i} = \frac{1}{\text{reps}}\sum \text{latensi iterasi}$ = nilai `rounds_ms[i]` harness (reps 30/5 per dokumen) | `rounds_ms` exhibit | Ya, dari exhibit (nilai sudah tersimpan); median dalam-ronde **tidak** dapat dihitung (raw iterasi tidak dipertahankan) |
| B | idem A | `rounds_ms` exhibit | idem |
| C | idem A | `rounds_ms` exhibit | idem |
| D | $T_{E,i}$ = mean 2 iterasi = `rounds_ms[i]` (mean ≡ median utk n=2) | `rounds_ms` exhibit | idem |
| E | $T_{E,i} = \operatorname{median}$ dari 10 request engine E pada ronde $i$ | exhibit `requests` | **Ya penuh** — raw per-request tersimpan; median dipilih sebagai nilai pusat robust (pilihan analisis, dinyatakan; sensitivitas mean-of-10 di §9) |

Perbedaan agregasi antar fase **adalah bagian dari definisi operasional** dan
diwariskkan dari desain harness (A–D: mean-of-reps terkunci di harness; E: data
raw utuh sehingga analisis memilih median). Keduanya dinyatakan, tidak
disamarkan.

### 4.4 Pasangan jalur analisis per fase

| Fase | Jalur V8 (pembilang) | Jalur ZE (penyebut) | Catatan |
|---|---|---|---|
| A | `v8-parse` | `ze-parse` | `v8-clone` dilaporkan **hanya sebagai referensi deskriptif** (semantik `MongoJsonRepository.read()`), bukan sisi pasangan inferensial A |
| B | `v8-selective` | `ze-project-selective` | konsumen subset identik |
| C | `v8-selective` | `ze-l1-traversal` | konsumen subset identik |
| D | `D-mongo-cache-v8` / `D-file-store-v8` | `D-mongo-cache-ze` / `D-file-store-ze` | analisis **per store**, tidak digabung |
| E | request `v8` | request `ze` (instance `wasm64_cabi`) | endpoint `GET /rekap`, respons byte-identik |

### 4.5 Mengapa estimand ini sesuai desain

1. Unit inferensi yang dideklarasikan desain dan harness adalah **ronde**
   (dokumen sintesis L19–31; `docs/measurement/nd6-benchmark-plan.md` §3
   "ronde independen"; AGENTS §6).
2. Konvensi repo yang sudah dipakai **semua** hasil D sebelumnya adalah rasio
   median round-level (`speedup_in_run` D; laporan ND-6 §10 "speedup =
   baseline/ze dalam run yang sama"). Mengadopsi estimand yang sama untuk E dan
   A–C menyatukan seluruh artikel di bawah satu definisi $S$.
3. Statistik bootstrap eksisting yang **sudah teruji reproduksi** menghitung
   persis estimand ini (§6).
4. Ratio of medians robust terhadap ronde ekstrem (satu ronde menggeser median
   ≤ 1/15), sejalan dengan disiplin pelaporan Hoefler & Belli (2015).

### 4.6 Mengapa kandidat lain tidak menjadi primer

- **A** (`median(S_r)`): estimand yang sah dan paired, tetapi menjawab pertanyaan
  berbeda ("speedup pada ronde tipikal" vs "rasio latensi round-tipikal") dan
  memaksakan perubahan konvensi pada seluruh laporan D tanpa alasan desain.
  Dipertahankan sebagai deskriptif berlabel — divergence A vs C′ sendiri adalah
  informasi diagnostik (§9).
- **B**: melanggar prinsip robustness untuk laporan utama.
- **C-pooled (E)**: point-nya fungsi marginal atas 150 request yang **mengabaikan
  unit inferensi ronde** yang dideklarasikan; CI round-level atas point pooled
  adalah inkonsistensi #1 yang diaudit.
- **E (cluster bootstrap pooled)**: internally konsisten, tetapi mempertahankan
  estimand marginal sebagai target inferensi — tidak perlu ketika estimand
  round-level tersedia dan lebih sesuai desain; ditolak demi kesatuan estimand
  lintas fase.
- **D & F**: pairing tidak didesain (§2.2, §3).

### 4.7 Keterbatasan interpretasi estimand primer

- θ menjawab "seberapa besar rasio latensi round-tipikal", **bukan** "probabilitas
  ronde acak memiliki S_r > 1" (itu dijawab sign test) dan **bukan** "efek
  multiplicative rata-rata" (itu θ_B).
- θ adalah estimand **dalam-run**: tidak mengkuantifikasi variabilitas antar-run
  atau antar-site (§12).
- Untuk fase D, θ mencakup **desain repository** (canonical-byte cache pada
  `readCount()`), bukan parser murni (AGENTS §6); untuk E, θ mencakup seluruh
  latensi endpoint.

---

## 5. Rumus point estimator

$$\hat{\theta} \;=\; \frac{\operatorname{median}(v_1,\dots,v_{15})}{\operatorname{median}(z_1,\dots,z_{15})}$$

dengan $v_i = T_{V8,i}$, $z_i = T_{ZE,i}$ sesuai §4.3. Implementasi numpy:

```python
theta_hat = float(np.median(v) / np.median(z))   # v, z = array 15 nilai ronde
```

Properti yang relevan:

1. **Identitas point–bootstrap**: fungsi yang sama dipakai pada data asli dan pada
   setiap sampel bootstrap (§6) — syarat konsistensi #1.
2. **Median untuk n=15** = nilai ke-8 urut (n ganjil); untuk n=2 (mean of reps D)
   mean ≡ median.
3. **Robustness**: satu ronde ekstrem menggeser median paling banyak 1/15
   dari posisinya.

---

## 6. Algoritma paired bootstrap

### 6.1 Parameter

| Parameter | Nilai | Catatan |
|---|---|---|
| $B$ | 10.000 | resolusi Monte Carlo, bukan tambahan unit eksperimen |
| seed | `20261117` | RNG = `numpy.random.default_rng(20261117)` (PCG64) |
| confidence level | 95% | percentile 2,5/97,5 |
| unit resampling | 1 ronde = pasangan utuh $(v_i, z_i)$ | indeks sama untuk kedua engine |
| jumlah unit per replikasi | 15 (dengan replacement, duplikat dihitung) | iid atas ronde |
| statistik replikasi | `median(v*)/median(z*)` | identik dengan point estimator |

### 6.2 Populasi empiris

Populasi resampling = **15 pasangan ronde teramati** $(v_1,z_1),\dots,(v_{15},z_{15})$
dari **satu run**. Aproksimasi: ronde adalah sampel iid dari distribusi ronde
kondisi host tersebut (asumsi desain: warmup + alternasi + rotasi urutan
mengontrol drift dalam-run; tidak ada trimming).

### 6.3 Pseudocode (kerangka final — estimand identik di kedua tahap)

```text
INPUT:
    v = [T_V8,1 .. T_V8,15]      # agregat dalam-ronde jalur V8 (§4.3)
    z = [T_ZE,1 .. T_ZE,15]      # agregat dalam-ronde jalur ZE (pasangan ronde sama)
    B = 10000
    seed = 20261117

STATISTIC(pairs):                # satu fungsi, dipakai di SEMUA tahap
    return median(v of pairs) / median(z of pairs)

point = STATISTIC(pairs)         # estimand yang sama

rng = default_rng(seed)
FOR b = 1 .. B:
    idx = rng.integers(0, 15, size=15)        # ronde diambil BERSAMA (pasangan utuh)
    boot_v = v[idx]; boot_z = z[idx]          # TIDAK boleh resample v dan z terpisah
    theta_b = STATISTIC(zip(boot_v, boot_z))  # estimand yang sama
COLLECT theta_1..theta_B

CI95 = [percentile(theta, 2.5), percentile(theta, 97.5)]   # skala rasio
```

Implementasi referensi (eksisting, terverifikasi reproduksi audit):
`bootstrap_median_ratio_ci(v8, ze)` di `scripts/analyze_measurement/nd_d_e_synthesis.py`
L222–235 — `idx = rng.integers(0, a.size, size=(b, a.size))`;
`stat = np.median(a[idx], axis=1) / np.median(z[idx], axis=1)`; percentile 2,5/97,5.

### 6.4 Mengapa resampling pasangan ronde precomputed ≡ resample ronde utuh

Jika satu replikasi memilih ronde $r^* = r$, maka seluruh observasi engine pada
ronde itu ikut, dan agregat dalam-ronde (mean-of-reps A–D / median-of-10 E)
adalah **statistik intra-ronde** — nilainya ditentukan sepenuhnya oleh data ronde
tersebut. Karena itu resampling tuple $(T_{V8,i}, T_{ZE,i})$ yang sudah dihitung
menghasilkan distribusi bootstrap **identik** dengan resample ronde utuh lalu
menghitung ulang agregat. (Relevan untuk E yang raw per-requestnya tersimpan:
kedua jalur implementasi ekuivalen; gunakan jalur tuple demi kesederhanaan.)

### 6.5 Perlakuan ronde tidak valid / data hilang

- Pada bukti saat ini: **nol** — tidak ada ronde hilang, gagal, atau dibuang
  (tanpa trimming; kegagalan fatal menghasilkan run void tanpa record, §2.3).
- Aturan normatif ke depan: ronde hanya boleh dikeluarkan **dari kedua engine
  sekaligus** (pasangan tetap utuh), alasannya didokumentasikan; bila kegagalan
  berasal dari desain (parity/child death), run adalah void dan seluruh analisis
  dibatalkan. Tidak ada imputasi; tidak ada pembuangan satu sisi pasangan.

### 6.6 Hal yang dilarang dalam bootstrap

- Resampling V8 dan ZE secara **independen** (merusak pairing).
- Resampling request/iterasi sebagai unit (melanggar unit inferensi; menghasilkan
  CI semu yang terlalu sempit).
- Mengganti statistik antara point dan replikasi (inkonsistensi #1 yang diaudit).
- Mencampur ronde dari run, commit, site, store, dokumen, atau boundary berbeda.
- Mengubah seed/B untuk mengubah kesimpulan (seed/B tetap; §9 sensitivitas).

---

## 7. Pemilihan metode confidence interval

### 7.1 Metode primer: percentile bootstrap 95%

**Alasan**:

1. Interval percentile dibentuk langsung dari distribusi bootstrap **estimand
   yang sama** dengan point estimate — syarat konsistensi inti.
2. Percentile bersifat **transform-equivariant**: untuk transformasi monoton $h$,
   persentil interval di skala $h(\theta)$ kembali ke skala rasio persis sama
   ($\exp$ dari persentil log = persentil dari $\theta^*$). Artinya: jika CI
   dihitung pada skala log-ratio lalu ditransform balik dengan $\exp$, hasilnya
   **identik** dengan percentile pada skala rasio — tidak ada keputusan skala
   yang bisa mengubah interval.
3. Sederhana, transparan, dan sudah menjadi konvensi implementasi + laporan
   sebelumnya (reproduksi audit persis, §9).
4. $B=10{,}000$ menekan error Monte Carlo pada persentil ke level jauh di bawah
   lebar interval yang dilaporkan.

### 7.2 Sensitivitas: BCa

BCa (bias-corrected and accelerated; Efron & Tibshirani 1993, §14) dievaluasi
pada **skala log** lalu ditransform balik (praktik standar untuk rasio), dengan
jackknife leave-one-round-out untuk acceleration $a$ dan $z_0$ dari proporsi
bootstrap di bawah point. Hasil pada semua sel audit (§9): **tidak membalik
verdict**, meskipun batas interval bergeser (contoh: dev E run 1 percentile
0,935–1,147 vs BCa 0,969–1,168; file-store server 0,971–1,039 vs 0,957–1,008).

**Alasan BCa bukan primer**: (a) dengan $n=15$, estimasi jackknife acceleration
tidak stabil (sel file-store server: $z_0=-0{,}411$ — koreksi besar dari data
kecil); (b) coverage BCa pada median dengan n kecil tidak dijamin lebih baik;
(c) pergeseran batas antar metode justru dilaporkan sebagai bagian analisis
sensitivitas, bukan disembunyikan di metode primer.

### 7.3 Keterbatasan 15 ronde — wajib dinyatakan

- $n=15$ unit independen per run. **10.000 replikasi memperbaiki resolusi
  simulasi, bukan menambah unit eksperimen.**
- Coverage percentile CI pada median dengan $n=15$ tidak persis 95% — interval
  dibaca sebagai **aproximasi**; kesimpulan signifikansi selalu dikombinasikan
  dengan uji round-level eksak (§8) dan tidak pernah bersandar pada satu CI.
- Distribusi bootstrap median pada $n=15$ bersifat diskrit (nilai median dari
  multiset ter-sample); lebar interval dan posisinya tetap valid sebagai
  interval empirical, tetapi granularitasnya kasar — jangan menafsirkan selisih
  kecil antar batas.
- Satu run per sel (kecuali E dev ×2) → CI mengukur variabilitas **antar-ronde
  dalam-run**; bukti bahwa antar-run bisa bergeser ada pada sendirinya (dev E
  1,076 → 1,041 lama / 1,050 → 1,028 terkoreksi, dua run independen).

---

## 8. Interpretasi statistik dan batas klaim

### 8.1 Nilai kesetaraan dan pembacaan CI

$S = T_{V8}/T_{ZE}$; kesetaraan = 1. Pembacaan CI 95% estimand θ:

| CI | Interpretasi yang sah |
|---|---|
| seluruh interval di atas 1 | bukti dalam-run bahwa ZE lebih cepat pada estimand round-tipikal (per boundary, per run) |
| seluruh interval di bawah 1 | bukti dalam-run bahwa V8 lebih cepat (kasus file-store) |
| interval mencakup 1 | **data tidak dapat membedakan dari kesetaraan** — TIDAK boleh ditulis "H₀ diterima" / "ZE tidak lebih cepat"; yang benar: "keunggulan tidak terdeteksi" pada ketelitian desain ini |

### 8.2 Uji hipotesis pelengkap (round-level, eksak)

- **Exact sign test** dua-sisi: jumlah ronde dengan $S_r > 1$ vs Binomial(15, 0,5)
  (`scipy.stats.binomtest`). Menguji $P(S_r>1)$ = 0,5 pada ronde acak.
- **Exact Wilcoxon signed-rank** dua-sisi pada selisih ronde
  $d_i = T_{V8,i} - T_{ZE,i}$ (ms), `zero_method='wilcox'` (tidak ada nol yang
  diharapkan). Menguji lokasi distribusi selisih.
- Keduanya **sudah round-level** di implementasi lama — konsisten, dipertahankan
  sebagai pelengkap. **P-value tidak diambil dari CI**; keduanya menguji hipotesis
  round-level yang **terkait namun berbeda** dari estimand θ (rasio median) —
  selalu dilaporkan sebagai komplementer, bukan pengganti.

### 8.3 Batas klaim (disiplin boundary)

1. **A–C**: estimand per dokumen per fase pada boundary binding — biaya
   open/arena, proyeksi L2, traversal L1; **bukan** parser murni dan **bukan**
   prediksi angka D/E.
2. **D**: boundary repository (`read().length` vs `readCount()` atas bytes
   kanonik warm-cache); gabungan desain repository + jalur parser; **bukan**
   request HTTP dan **bukan** pengukuran parser-only. Klaim ≥1,5× (acceptance
   protokol ND-6 §7) hanya berlaku pada path yang diukur (mongo-cache).
3. **E**: boundary endpoint `GET /rekap` end-to-end (middleware → handler 4 repo
   → render EJS → respons); **bukan** `/rekap/asisten`, export, `express.json()`
   body parsing, atau seluruh aplikasi SAQ.
4. **Tidak ada verdict H₀ parser-only dari D/E.** H₀ proposal menyentuh tiga
   dimensi (latensi parser, throughput, konsumsi memori); memori/CPU tidak diukur
   di D/E → H₀ proposal **belum diputuskan** oleh data ini; yang dilaporkan hanya
   hasil latensi per boundary (temuan Codex P2 #2).
5. Tidak ada klaim CPU/memori tanpa data; tidak ada indeks kompresi lintas-boundary
   yang dibaca sebagai estimasi share parser (C = S_D/S_E deskriptif saja).
6. Dev vs server selalu **narasi kontekstual** — tidak ada pooling, tidak ada
   perbandingan langsung sebagai bukti kausal.

---

## 9. Analisis sensitivitas (terhitung dari raw exhibit — read-only)

Semua angka dihitung ulang dari exhibit raw pada audit ini dengan prosedur §5–§6
(seed `20261117`, B=10000). Angka ini **ilustrasi audit**; rekalkulasi formal
untuk artikel dilakukan di Stage 2 (`drafts/evidence-ledger.csv`) dengan
provenance sha256.

### 9.1 Phase E — tiga run primary

| Run | Pooled (lama dilaporkan) | A = med(S_r) [CI_pct] | B = geo | **C′ = ratio(med) [CI_pct]** | CI_BCa(log) | ze wins |
|---|---:|---:|---:|---:|---:|---|
| dev run 1 `8556513` | 1,0762 | 1,0477 [0,9883–1,0909] | 1,0355 | **1,0501 [0,9347–1,1473]** | 0,9687–1,1675 | 9/15 |
| dev re-run `6979e3f` | 1,0405 | 1,0286 [0,9740–1,1109] | 1,0478 | **1,0278 [0,9740–1,1143]** | 0,9729–1,1143 | 10/15 |
| server `530f751` | 1,1338 | 1,1327 [1,0779–1,1793] | 1,1255 | **1,1544 [1,0845–1,1751]** | 1,1099–1,1862 | 15/15 |

- CI E dev run 1 (0,935–1,147) di tabel laporan = CI untuk C′ — angka 1,076 yang
  ditampilkan bersebelahan bukan estimand CI itu (inkonsistensi #1).
- Koreksi konvensi menggeser point **dua arah** (dev −2,4/−1,2%; server +1,8%);
  **verdict tidak berubah**: dev CI memuat 1 (sign test p = 0,612 / 0,424);
  server CI di atas 1 (15/15, sign p = 6,1e-5; Wilcoxon konsisten).

### 9.2 Phase D — dua run primary × dua store

| Run/store | A = med(S_r) [CI_pct] | B = geo | **C′ = ratio(med) [CI_pct]** | CI_BCa(log) | ze wins |
|---|---:|---:|---:|---:|---|
| dev `6d87bf3` mongo | 2,8499 [2,4414–3,0664] | 2,8757 | **2,8802 [2,5724–3,0451]** | 2,6921–3,3950 | 15/15 |
| dev `6d87bf3` file | 0,9511 [0,8674–1,0518] | 0,9630 | **0,9526 [0,7673–1,1093]** | 0,7679–1,1304 | — |
| server `8a1324b` mongo | 2,7556 [2,4686–2,8734] | 2,6431 | **2,6654 [2,5083–2,8573]** | 2,5083–2,8573 | 15/15 |
| server `8a1324b` file | 0,9977 [0,9639–1,0166] | 0,9973 | **0,9871 [0,9705–1,0387]** | 0,9574–1,0080 | — |

- Angka D yang beredar (2,880×; 2,665×; 0,953×; 0,987×) **sudah C′** —
  konsisten dengan estimand primer; CI ter-reproduksi persis → implementasi
  bootstrap eksisting benar.
- BCa menggeser batas (terbesar: dev mongo 2,572→2,692 bawah; server file
  0,971→0,957) namun **tidak mengubah verdict** mana pun.

### 9.3 Phase A–C — divergensi A vs C′ per dokumen (36 sel)

Nilai A (median rasio ronde — konvensi lama `nd-phase-abcd-stats.csv`) vs
C′ (rasio median — estimand primer baru). Tabel lengkap:

| Phase | Site | Dokumen | A = med(rasio) | C′ = rasio(med) | (A/C′ − 1) |
|---|---|---|---:|---:|---:|
| A | dev | courses | 0,0486 | 0,0494 | −1,55% |
| A | dev | assistants | 0,0497 | 0,0544 | −8,55% |
| A | dev | lecturers | 0,0443 | 0,0428 | +3,44% |
| A | dev | schedules | 0,0452 | 0,0446 | +1,31% |
| A | dev | reports | 0,0521 | 0,0613 | −15,06% |
| A | dev | globalConfig | 0,0443 | 0,0445 | −0,41% |
| B | dev | courses | 0,1131 | 0,1229 | −7,95% |
| B | dev | assistants | 0,1088 | 0,1059 | +2,75% |
| B | dev | lecturers | 0,0770 | 0,0755 | +1,97% |
| B | dev | schedules | 0,1250 | 0,1287 | −2,88% |
| B | dev | reports | 0,1521 | 0,1594 | −4,58% |
| B | dev | globalConfig | 0,1205 | 0,0987 | **+22,12%** |
| C | dev | courses | 0,8888 | 0,9223 | −3,64% |
| C | dev | assistants | 1,0152 | 1,1680 | −13,08% |
| C | dev | lecturers | 1,0140 | 1,0455 | −3,01% |
| C | dev | schedules | 1,6403 | 1,6454 | −0,31% |
| C | dev | reports | 0,2774 | 0,2861 | −3,05% |
| C | dev | globalConfig | 0,0444 | 0,0452 | −1,79% |
| A | server | courses | 0,0506 | 0,0493 | +2,60% |
| A | server | assistants | 0,0595 | 0,0669 | −10,93% |
| A | server | lecturers | 0,0520 | 0,0520 | +0,11% |
| A | server | schedules | 0,0570 | 0,0569 | +0,19% |
| A | server | reports | 0,0577 | 0,0576 | +0,26% |
| A | server | globalConfig | 0,0497 | 0,0501 | −0,80% |
| B | server | courses | 0,1219 | 0,1228 | −0,79% |
| B | server | assistants | 0,1109 | 0,1130 | −1,86% |
| B | server | lecturers | 0,0915 | 0,0828 | +10,46% |
| B | server | schedules | 0,1322 | 0,1282 | +3,09% |
| B | server | reports | 0,1436 | 0,1436 | 0,00% |
| B | server | globalConfig | 0,1199 | 0,1043 | +14,95% |
| C | server | courses | 0,8021 | 0,8561 | −6,30% |
| C | server | assistants | 1,3794 | 1,4194 | −2,82% |
| C | server | lecturers | 0,9600 | 0,9562 | +0,39% |
| C | server | schedules | 1,4930 | 1,4983 | −0,36% |
| C | server | reports | 0,3227 | 0,3087 | +4,53% |
| C | server | globalConfig | 0,0458 | 0,0469 | −2,31% |

Ringkas: |A/C′ − 1| mean = 4,45%, maks = 22,12% (B dev `globalConfig`).
Perbedaan material pada sel-sel tertentu → kolom `speedup_median` A–C **wajib
diseragamkan** ke C′ (perubahan implementasi §11); nilai A tetap dilaporkan
sebagai `paired_median_ratio`.

### 9.4 Sensitivitas agregasi dalam-ronde (E)

Median-of-10 (primer, robust) vs mean-of-10: raw per-request tersimpan sehingga
keduanya dapat dihitung; pergeseran yang diharapkan kecil (rata-rata request
dalam ronde hampir seimbang 10/10). Rekomendasi: laporkan median-of-10 primer;
mean-of-10 hanya bila pembaca butuh kepekaan terhadap request ekstrem. Tidak
mengubah unit inferensi.

### 9.5 Aturan sensitivitas

Sensitivitas (A, B, BCa, mean-of-10) **tidak boleh** dipakai untuk mengganti
estimand primer secara post hoc karena hasilnya lebih menguntungkan; semua
divergensi dilaporkan, dan estimand primer tetap §4.

---

## 10. Audit ketidakkonsistenan implementasi lama

Bukti pada commit `a1fad918a7` (file tidak diubah oleh audit ini).

| # | Lokasi | Estimator lama | Estimand yang benar-benar dihitung | Mengapa tidak konsisten | Perbaikan (§11) |
|---|---|---|---|---|---|
| 1 | `nd_d_e_synthesis.py` **L475** `med_speedup = float(sv["median"] / sz["median"])` dengan `sv, sz = describe_ms(v8), describe_ms(ze)` **L465** — `v8, ze` = **150 request pooled** (L455 `phase_e_arrays`) | rasio median **pooled-request** (konvensi harness `speedup_in_run`, L492–493 `nd11_phase_e.mjs`) | CI **L472** `bootstrap_median_ratio_ci(vm, zm)` dihitung atas **15 median ronde** → CI untuk **C′** | dua estimand berbeda: populasi request marginal vs distribusi round-level; mislabel eksplisit di `infer_rows` **L538–550** ("statistic": "median(T_v8,i)/median(T_ze,i) over 15 paired rounds", "point": pooled) | point E = C′ (satu baris); pooled tetap ada sebagai deskriptif berlabel |
| 2 | `nd_d_e_synthesis.py` **L600** (`abcd_rows`): `"speedup_median": g(float(np.median(ratio)))` — `ratio = v8 / ze` per-ronde (L594) | median **rasio per-ronde** (kandidat A) | estimand primer C′ | kolom `speedup_median` sama, makna beda dari baris D (L357 `sv["median"]/sz["median"]`) dalam satu script; divergensi hingga 22% (§9.3) | A–C `speedup_median` → C′; nilai A pindah ke `paired_median_ratio` |
| 3 | `nd_d_e_synthesis.py` **L357** (baris D) | rasio median **round-level** | C′ | — konsisten — (referensi konvensi yang benar) | tetap |
| 4 | `reports/nd11-phase-d-e-synthesis.md` **L231** | verdict "H₀ tertolak" dari D/E | H₀ proposal mencakup latensi parser + throughput + **memori**; D = boundary repository (gabungan desain cache), E = boundary endpoint; memori/CPU tidak diukur | kesimpulan melampaui boundary yang diukur (temuan Codex P2 #2; AGENTS §6) | laporan artikel: hasil per-boundary; H₀ proposal tidak diputuskan oleh D/E |
| 5 | `nd_d_e_synthesis.py` **L222–235** `bootstrap_median_ratio_ci` | — | — | **benar**: seed tetap, resample joint, statistik = C′; reproduksi audit identik (D dev mongo CI 2,5724–3,0451 = laporan 2,572–3,045) | dipertahankan apa adanya |

Kesimpulan audit: **prosedur bootstrap sudah benar; kesalahan terletak pada
(1) pilihan estimand point Phase E dan (2) ketidaksinkronan definisi kolom
lintas fase** — keduanya perubahan analisis, bukan perubahan data.

---

## 11. Rencana perubahan implementasi (minimal, TIDAK dieksekusi di tahap ini)

Prinsip: perubahan hanya di lapisan **analisis** (`scripts/analyze_measurement/
nd_d_e_synthesis.py` + turunan CSV/figure). **Tidak ada** perubahan raw exhibit,
record, harness, validator, atau hasil eksperimen; tidak ada pengukuran ulang.

1. **Phase E block** (`main()`, bagian E):
   - Tambahkan `round_point = float(np.median(vm) / np.median(zm))`.
   - `infer_rows` Phase E: `"point": g(round_point)` (estimand = label yang sudah
     tertulis).
   - `e_stats_rows`: ganti/labelkan — `speedup_median` (pooled, konvensi harness)
     tetap sebagai **deskriptif**; tambah kolom `speedup_round_median = round_point`
     sebagai **primary**; caption/figure menggunakan `round_point`.
   - `check()` terhadap `speedup_in_run` (pooled) tetap — reconciliasi harness
     tidak berubah.
2. **Phase A–C block** (`abcd_rows`):
   - `speedup_median` ← `g(sv["median"] / sz["median"])` (C′).
   - Tambah kolom `paired_median_ratio` ← `g(float(np.median(ratio)))` (nilai lama
     tidak hilang, hanya di-relabel).
3. **Kolom sensitivitas** (opsional tapi direkomendasikan): `boot_ci_bca_lo/hi`
   (BCa skala log, back-transform) untuk D/E; disimpan sebagai kolom terpisah.
4. **Figur/caption**: `nd-de-speedup-comparison` menampilkan `round_point` untuk E;
   catatan kaki menjelaskan perubahan konvensi dan referensi spesifikasi ini.
5. **Provenance**: `provenance.json.inference.headline_statistic` diperbarui:
   "ratio of round-level medians (same estimator for point and bootstrap);
   pooled-request ratio retained as descriptive (`speedup_in_run` harness
   convention)".
6. **Dokumentasi**: catat perubahan di `drafts/source-audit.md` (artikel) +
   changelog repo; resolve dua thread review PR #79 dengan menautkan spesifikasi
   ini.
7. **Rekalkulasi angka artikel** (Stage 2): seluruh angka inferensial artikel
   diregenerasi dari estimand ini; angka lama di laporan committed **tidak
   disentuh** (immutable); perbedaan konvensi dijelaskan eksplisit di naskah.

Estimasi dampak angka artikel: D tidak berubah; E dev 1,076→1,050 dan
1,041→1,028; E server 1,134→1,154; A–C menyesuaikan maksimum hingga ±22% pada
sel individual (tabel §9.3). Verdict tidak berubah di sel mana pun.

---

## 12. Unresolved issues dan risiko metodologis

1. **(asumsi dinyatakan)** Agregasi dalam-ronde Phase E = median-of-10 adalah
   **pilihan analisis** (raw tersimpan penuh). Alternatif mean-of-10 tersedia;
   dipilih median demi robustness. Dinyatakan di naskah.
2. **(asumsi dinyatakan)** Agregasi dalam-ronde A–C/D = mean-of-reps **terkunci
   di harness** (raw per-iterasi tidak dipertahankan di exhibit). Median
   dalam-ronde tidak dapat dihitung ulang untuk data yang ada.
3. **(asumsi dinyatakan)** Coverage percentile CI pada n=15 approximatif;
   BCa tidak stabil pada beberapa sel ($z_0$ hingga −0,411) — dilaporkan sebagai
   sensitivitas, bukan primer.
4. **Single-run per sel**: inferensi terbatas pada variabilitas antar-ronde
   dalam-run; replikasi antar-run tidak tersedia (kecuali E dev ×2, yang justru
   menunjukkan shift antar-run 1,050→1,028). Klaim lintas-run/site tetap narasi.
5. **H₀ proposal tiga-dimensi** (latensi parser, throughput, memori): dua
   dimensi tidak diukur di D/E; throughput ≈ invers latensi hanya untuk jalur
   yang diukur; kesimpulan H₀ dibiarkan per-boundary, bukan parser-only.
6. **Dua run dev Phase E**: diperlakukan sebagai dua estimasi independen yang
   dilaporkan terpisah; tidak digabung (tidak ada pooling lintas run).
7. **Kandidat F (adjacent-pair)** dan diagnostik lain (distribusi request,
   ECDF) boleh ditambahkan sebagai deskriptif; tidak pernah menjadi dasar
   kesimpulan primer.
8. **Istilah `reps_per_round`** bermakna berbeda antar record D (2) dan E (20
   TOTAL) — setiap tabel artikel wajib menuliskan maknanya eksplisit.

---

## 13. Referensi metodologis

**Internal (bukti desain & konvensi):**

- `AGENTS.md` §4 (hukum komparasi satu run_id) dan §6 (metodologi gate; L201–205:
  Phase D menggabungkan optimasi repository, bukan parser murni).
- `docs/measurement/nd6-benchmark-plan.md` §2–§3, §7 (protokol A–D; acceptance
  ≥1,5×).
- `docs/measurement/nd11-phase-e-http.md` §3, §6, §8 (protokol E; as-built 20
  request/ronde TOTAL; alternasi per-request).
- `scripts/bench/nd6_bench.mjs` (harness A–D; L379–392, L394–423, L425–465).
- `scripts/bench/nd11_phase_e.mjs` (harness E; L320–331, L422–438, L442–450,
  L492–493).
- `scripts/analyze_measurement/nd_d_e_synthesis.py` (analisis; L222–235, L353–360,
  L465–475, L538–550, L594–601).
- `reports/nd11-phase-d-e-synthesis.md` (L19–47 unit/statistik; L231 verdict H₀).
- Review PR #79 (chatgpt-codex-connector[bot], commit `a1fad918a7`): P2 #1
  (konsistensi point/CI Phase E) dan P2 #2 (verdict H₀ boundary).
- `@cite 10.1002/spe.3313` (on-demand JSON; disiplin boundary & provenance),
  `@cite 10.14778/3115404.3115416` (Mison; structural index) — @cite yang
  terbawa di harness/record.

**Eksternal:**

- B. Efron (1979). *Bootstrap Methods: Another Look at the Jackknife*.
  The Annals of Statistics 7(1):1–26.
- B. Efron & R. J. Tibshirani (1993). *An Introduction to the Bootstrap*.
  Chapman & Hall/CRC. (percentile & BCa; jackknife acceleration)
- A. Georges, D. Buytaert, L. Eeckhout (2007). *Statistically rigorous Java
  performance evaluation*. OOPSLA 2007. (desain paired + CI pada benchmark VM;
  DOI `10.1145/1297027.1297035` — **kandidat verifikasi Crossref di Stage 3**)
- T. Mytkowicz, T. Diwan, M. Hauswirth, P. F. Sweeney (2009). *Producing wrong
  data without doing anything obviously wrong!* ASPLOS 2009. (bias pengukuran &
  alternasi; DOI `10.1145/1508284.1508275` — **kandidat verifikasi Crossref di
  Stage 3**)
- T. Hoefler & R. Belli (2015). *Scientific benchmarking of parallel computing
  systems*. SC 2015. DOI `10.1145/2807591.2807644` (terverifikasi di
  `assets/bib/cites.bib`; fondasi disiplin pelaporan median/CI).

---

## 14. Tabel keputusan akhir

| Eksperimen | Unit inferensi | Estimand primer | Point estimator | Bootstrap unit | CI method |
|---|---|---|---|---|---|
| **A — full materialization** (per dokumen × site × run; pasangan `v8-parse` ↔ `ze-parse`) | 15 ronde berpasangan | $\operatorname{median}(v_i)/\operatorname{median}(z_i)$, $v_i$/$z_i$ = mean-of-reps | fungsi yang sama | ronde, joint (B=10.000, seed `20261117`) | percentile 95% (BCa = sensitivitas) |
| **B — L2 projection** (per dokumen × site × run; `v8-selective` ↔ `ze-project-selective`) | idem | idem | idem | idem | idem |
| **C — L1 traversal** (per dokumen × site × run; `v8-selective` ↔ `ze-l1-traversal`) | idem | idem | idem | idem | idem |
| **D — repository** (per store × site × run; mongo-cache & file-store dilaporkan terpisah) | idem | idem ($v_i$/$z_i$ = mean-of-2 ≡ median) | idem | idem | idem |
| **E — HTTP endpoint** (per run; `8556513`, `6979e3f`, `530f751`) | idem | idem ($v_i$/$z_i$ = median-of-10 request) | idem | idem | idem |

Sekunder deskriptif (berlabel, non-inferensial): `paired_median_ratio`
(kandidat A), `speedup_in_run` pooled (kandidat C-pooled, E), rasio mean, rasio
p95, B geometric-mean, A–C sweep per dokumen, v8-clone (fase A), indeks
kompresi C = S_D/S_E.

Tidak ada sel `UNRESOLVED`.

---

## 15. Acceptance criteria checklist (status audit)

- [x] Struktur observasi dan pairing terverifikasi dari raw data (§2 — harness
      code + exhibit fields + record config; 11/11 record PASS validator).
- [x] Unit inferensi tiap eksperimen didefinisikan (§2.4, §14).
- [x] Estimand primer dinyatakan verbal dan matematis (§4.1–§4.2).
- [x] Point estimator diturunkan langsung dari estimand (§5).
- [x] Prosedur paired bootstrap dijelaskan algoritmik (§6).
- [x] Bootstrap mempertahankan struktur pairing yang benar (§6.3, §6.6).
- [x] CI mengestimasi estimand yang sama dengan point estimate (§5, §6.3, §7).
- [x] Pemilihan metode CI berjustifikasi (§7.1–§7.2).
- [x] Keterbatasan 15 ronde dibahas (§7.3, §12).
- [x] Perbedaan estimand antar-fase dijelaskan (agregasi dalam-ronde §4.3;
      estimand primer satu keluarga dengan definisi operasional per fase).
- [x] Tidak ada klaim inferensial di luar batas eksperimen (§8).
- [x] Seluruh keputusan didukung referensi file/fungsi/record/bukti (§2, §10, §13).

**Provenance perhitungan §9**: dihitung read-only dari exhibit raw
(`out/raw/...` — byte-identik dengan arsip committed) dengan numpy/scipy:
statistik §5, bootstrap §6 (seed `20261117`, B=10000, `default_rng`), BCa §7.2
(skala log, jackknife). Script audit tidak menyimpan file; rekalkulasi formal +
provenance sha256 masuk Stage 2 (`drafts/evidence-ledger.csv`).
