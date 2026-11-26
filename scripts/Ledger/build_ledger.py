#!/usr/bin/env python3
"""Build article/drafts/evidence-ledger.csv — 16-column evidence ledger.

Recomputes every ledger statistic from validator-PASS measurement records and
raw exhibits using the locked estimand of
`article/drafts/paired-bootstrap-estimand-spec.md`:

  theta = median_i(T_V8,i) / median_i(T_ZE,i)   over 15 paired rounds
  paired round-level bootstrap: B=10000, seed=20261117, percentile 95% CI

Read-only with respect to all repository evidence: records, raw exhibits,
schemas, and harnesses are never modified. Deterministic; no wall-clock input
(the run date is a constant header field, not a generated timestamp).

Outputs:
  article/data/csv/evidence-ledger.csv              16-column ledger
  article/data/json/evidence-ledger.provenance.json  full sha256 + method metadata
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import os
from pathlib import Path

import numpy as np

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()  # article/scripts/Ledger -> v5
ART = ROOT / "article"
SEED = 20261117
B = 10000
CONF = 0.95
AUDIT_DATE = "2026-11-18"

SPEC_REF = "article/drafts/paired-bootstrap-estimand-spec.md"
METRIC = (
    "S = T_V8/T_ZE; ratio of round-level medians over 15 paired rounds; "
    f"paired bootstrap B={B}, seed={SEED}, percentile {int(CONF * 100)}%"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(rel: str) -> tuple[dict, str, str]:
    """Load evidence file preferring out/raw copy, fallback to committed copy.

    Returns (data, relpath_used, sha256).
    """
    p = Path(rel)
    candidates = [
        ROOT / "out" / "raw" / p.parent.name / p.name,
        ROOT / p,
    ]
    for cand in candidates:
        if cand.is_file():
            with open(cand, encoding="utf-8") as f:
                data = json.load(f)
            return data, str(cand.relative_to(ROOT)), sha256(cand)
    raise FileNotFoundError(rel)


def record_and_exhibit(record_rel: str) -> tuple[dict, dict, str, str, str, str]:
    """Load a record plus its sibling raw exhibit from the record's path.

    Record rel: reports/<dir>/<file>.record.json
    Exhibit:    reports/<dir>/raw/<run_id>/<exhibit_name>.json
    Returns (record, exhibit, rec_rel, rec_sha, exh_rel, exh_sha).
    """
    rec_rel = record_rel
    rec, rec_rel_used, rec_sha = load_json(rec_rel)
    run_id = rec["run_id"]
    # exhibit name from the record filename convention
    if "nd11" in Path(rec_rel).name:
        exhibit_name = "nd11_phase_e.json"
    else:
        # phase letter from record filename: ...-nd6-<x>-...
        m = re.search(r"nd6-([a-d])-", Path(rec_rel).name)
        exhibit_name = f"nd6_phase_{m.group(1).upper()}.json"
    exh_rel = str(Path(rec_rel).parent / "raw" / run_id / exhibit_name)
    exh, exh_rel_used, exh_sha = load_json(exh_rel)
    return rec, exh, rec_rel_used, rec_sha, exh_rel_used, exh_sha


def boot_ci(v: np.ndarray, z: np.ndarray) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, v.size, size=(B, v.size))
    stats = np.median(v[idx], axis=1) / np.median(z[idx], axis=1)
    lo, hi = np.percentile(stats, [(1 - CONF) / 2 * 100, (1 + CONF) / 2 * 100])
    return float(lo), float(hi)


def runtime_short(rec: dict) -> str:
    tc = rec.get("host", {}).get("toolchain", "")
    m = re.search(r"node v([0-9.]+) \(v8 ([0-9.]+)", tc)
    if m:
        return f"Node {m.group(1)}/V8 {m.group(2)}"
    return tc or "UNRECORDED"


def lib_short(rec: dict) -> str:
    lib = rec.get("library", {})
    return (
        f"core {lib.get('core_version')} / js {lib.get('js_version')} "
        f"/ ABI {lib.get('abi_version')}"
    )


def corpus_short(rec: dict) -> str:
    c = rec.get("corpus", {})
    if not c:
        return "UNRECORDED"
    return f"{c.get('name')} ({c.get('document_count')} docs, {c.get('total_bytes')} B)"


def phase_ac_rows(phase: str, record_rel: str, ev_class: str,
                  pairs: dict[str, tuple[str, str]], rows: list, files: dict):
    rec, exh, rec_rel, rec_sha, exh_rel, exh_sha = record_and_exhibit(record_rel)
    site = rec["site"]
    rid = rec["run_id"]
    commit = rec["git_commit"]["hash"]
    wasm = rec.get("library", {}).get("artifact_sha256", "")
    by_doc: dict[str, dict[str, list[float]]] = {}
    for r in exh["raw_rounds"]:
        by_doc.setdefault(r["doc"], {})[r["path"]] = [float(x) for x in r["rounds_ms"]]
    for doc, (v_path, z_path) in pairs.items():
        if doc not in by_doc:
            raise KeyError(f"{phase} {rid}: missing doc {doc}")
        v = np.array(by_doc[doc][v_path])
        z = np.array(by_doc[doc][z_path])
        assert v.size == z.size == 15, f"{phase} {rid} {doc}: rounds != 15"
        point = float(np.median(v) / np.median(z))
        lo, hi = boot_ci(v, z)
        rows.append({
            "evidence_id": f"{phase}-{ev_class}-{site}-{doc}",
            "phase": phase,
            "site": site,
            "evidence_class": ev_class,
            "run_id": rid,
            "git_root_commit": commit,
            "boundary_detail": doc,
            "comparison_pair": f"{v_path}/{z_path}",
            "runtime": runtime_short(rec),
            "library_version": lib_short(rec),
            "corpus": corpus_short(rec),
            "metric": METRIC,
            "point_estimate": f"{point:.4f}",
            "ci95_lower": f"{lo:.4f}",
            "ci95_upper": f"{hi:.4f}",
            "provenance": f"record={rec_rel}#{rec_sha[:16]}; exhibit={exh_rel}#{exh_sha[:16]}",
        })
        files[f"record {ev_class} {phase} {site} {doc} {rid}"] = rec_rel
        files[f"exhibit {ev_class} {phase} {site} {doc} {rid}"] = exh_rel


def phase_d_rows(record_rel: str, ev_class: str, rows: list, files: dict):
    rec, exh, rec_rel, rec_sha, exh_rel, exh_sha = record_and_exhibit(record_rel)
    site = rec["site"]
    rid = rec["run_id"]
    commit = rec["git_commit"]["hash"]
    wasm = rec.get("library", {}).get("artifact_sha256", "")
    paths = {r["path"]: np.array([float(x) for x in r["rounds_ms"]])
             for r in exh["raw_rounds"]}
    for store, vp, zp in (("mongo-cache", "D-mongo-cache-v8", "D-mongo-cache-ze"),
                          ("file-store", "D-file-store-v8", "D-file-store-ze")):
        v, z = paths[vp], paths[zp]
        assert v.size == z.size == 15, f"D {rid} {store}: rounds != 15"
        point = float(np.median(v) / np.median(z))
        lo, hi = boot_ci(v, z)
        rows.append({
            "evidence_id": f"D-{ev_class}-{site}-{store}",
            "phase": "D",
            "site": site,
            "evidence_class": ev_class,
            "run_id": rid,
            "git_root_commit": commit,
            "boundary_detail": f"repository/{store}",
            "comparison_pair": f"{vp}/{zp}",
            "runtime": runtime_short(rec),
            "library_version": lib_short(rec),
            "corpus": corpus_short(rec),
            "metric": METRIC,
            "point_estimate": f"{point:.4f}",
            "ci95_lower": f"{lo:.4f}",
            "ci95_upper": f"{hi:.4f}",
            "provenance": f"record={rec_rel}#{rec_sha[:16]}; exhibit={exh_rel}#{exh_sha[:16]}",
        })
        files[f"record {ev_class} D {site} {store} {rid}"] = rec_rel
        files[f"exhibit {ev_class} D {site} {store} {rid}"] = exh_rel


def phase_e_rows(record_rel: str, ev_class: str, rows: list, files: dict):
    rec, exh, rec_rel, rec_sha, exh_rel, exh_sha = record_and_exhibit(record_rel)
    site = rec["site"]
    rid = rec["run_id"]
    commit = rec["git_commit"]["hash"]
    req = exh["requests"]
    v8 = np.array([x["seconds"] * 1000.0 for x in req["v8"]])
    v8r = np.array([int(x["round"]) for x in req["v8"]])
    ze = np.array([x["seconds"] * 1000.0 for x in req["ze"]])
    zer = np.array([int(x["round"]) for x in req["ze"]])
    v = np.array([float(np.median(v8[v8r == r])) for r in range(1, 16)])
    z = np.array([float(np.median(ze[zer == r])) for r in range(1, 16)])
    assert v.size == z.size == 15, f"E {rid}: rounds != 15"
    # parity check: exactly one unique response hash per run
    hashes = {x["body_sha256"] for x in req["v8"]} | {x["body_sha256"] for x in req["ze"]}
    assert len(hashes) == 1, f"E {rid}: parity mismatch ({len(hashes)} hashes)"
    point = float(np.median(v) / np.median(z))
    lo, hi = boot_ci(v, z)
    rows.append({
        "evidence_id": f"E-{ev_class}-{site}-rekap-{rid}",
        "phase": "E",
        "site": site,
        "evidence_class": ev_class,
        "run_id": rid,
        "git_root_commit": commit,
        "boundary_detail": "http GET /rekap end-to-end",
        "comparison_pair": "v8-instance/ze-instance (20 req/round TOTAL: 10+10)",
        "runtime": runtime_short(rec),
        "library_version": lib_short(rec),
        "corpus": corpus_short(rec),
        "metric": METRIC,
        "point_estimate": f"{point:.4f}",
        "ci95_lower": f"{lo:.4f}",
        "ci95_upper": f"{hi:.4f}",
        "provenance": f"record={rec_rel}#{rec_sha[:16]}; exhibit={exh_rel}#{exh_sha[:16]}",
    })
    files[f"record {ev_class} E {site} {rid}"] = rec_rel
    files[f"exhibit {ev_class} E {site} {rid}"] = exh_rel


def main() -> None:
    rows: list[dict] = []
    files: dict[str, str] = {}

    pairs = {
        "A": {
            "courses": ("v8-parse", "ze-parse"),
            "assistants": ("v8-parse", "ze-parse"),
            "lecturers": ("v8-parse", "ze-parse"),
            "schedules": ("v8-parse", "ze-parse"),
            "reports": ("v8-parse", "ze-parse"),
            "globalConfig": ("v8-parse", "ze-parse"),
        },
        "B": {
            "courses": ("v8-selective", "ze-project-selective"),
            "assistants": ("v8-selective", "ze-project-selective"),
            "lecturers": ("v8-selective", "ze-project-selective"),
            "schedules": ("v8-selective", "ze-project-selective"),
            "reports": ("v8-selective", "ze-project-selective"),
            "globalConfig": ("v8-selective", "ze-project-selective"),
        },
        "C": {
            "courses": ("v8-selective", "ze-l1-traversal"),
            "assistants": ("v8-selective", "ze-l1-traversal"),
            "lecturers": ("v8-selective", "ze-l1-traversal"),
            "schedules": ("v8-selective", "ze-l1-traversal"),
            "reports": ("v8-selective", "ze-l1-traversal"),
            "globalConfig": ("v8-selective", "ze-l1-traversal"),
        },
    }

    # primary dev (core 0.3.2)
    phase_ac_rows("A", "reports/nd14/zuu-20261115071747-6d87bf3-nd6-a-dev_device.record.json", "primary", pairs["A"], rows, files)
    phase_ac_rows("B", "reports/nd14/zuu-20261115075332-6d87bf3-nd6-b-dev_device.record.json", "primary", pairs["B"], rows, files)
    phase_ac_rows("C", "reports/nd14/zuu-20261115080838-6d87bf3-nd6-c-dev_device.record.json", "primary", pairs["C"], rows, files)
    phase_d_rows("reports/nd14/zuu-20261115080840-6d87bf3-nd6-d-dev_device.record.json", "primary", rows, files)
    # primary server
    phase_ac_rows("A", "reports/nd14/server-lanjut-20261116060843-8a1324b-nd6-a-saq_server.record.json", "primary", pairs["A"], rows, files)
    phase_ac_rows("B", "reports/nd14/server-lanjut-20261116060900-8a1324b-nd6-b-saq_server.record.json", "primary", pairs["B"], rows, files)
    phase_ac_rows("C", "reports/nd14/server-lanjut-20261116060915-8a1324b-nd6-c-saq_server.record.json", "primary", pairs["C"], rows, files)
    phase_d_rows("reports/nd14/server-lanjut-20261116060933-8a1324b-nd6-d-saq_server.record.json", "primary", rows, files)
    # primary E
    phase_e_rows("reports/nd11/zuu-20261116101458-8556513-nd11-phase-e-dev_device.record.json", "primary", rows, files)
    phase_e_rows("reports/nd11/zuu-20261117000112-6979e3f-nd11-phase-e-dev_device.record.json", "primary", rows, files)
    phase_e_rows("reports/nd11/server-lanjut-20261117003513-530f751-nd11-phase-e-saq_server.record.json", "primary", rows, files)
    # supporting dev (core 0.3.1)
    phase_ac_rows("A", "reports/nd14/zuu-20261115005811-3376d07-nd6-a-dev_device.record.json", "supporting", pairs["A"], rows, files)
    phase_ac_rows("B", "reports/nd14/zuu-20261115010151-3376d07-nd6-b-dev_device.record.json", "supporting", pairs["B"], rows, files)
    phase_ac_rows("C", "reports/nd14/zuu-20261115010153-3376d07-nd6-c-dev_device.record.json", "supporting", pairs["C"], rows, files)
    phase_d_rows("reports/nd14/zuu-20261115010155-3376d07-nd6-d-dev_device.record.json", "supporting", rows, files)

    out_csv = ART / "data" / "csv" / "evidence-ledger.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    cols = ["evidence_id", "phase", "site", "evidence_class", "run_id",
            "git_root_commit", "boundary_detail", "comparison_pair", "runtime",
            "library_version", "corpus", "metric", "point_estimate",
            "ci95_lower", "ci95_upper", "provenance"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    prov = {
        "schema_version": "1.0.0",
        "kind": "evidence_ledger_provenance",
        "date": AUDIT_DATE,
        "estimand_spec": SPEC_REF,
        "estimand": "theta = median_i(T_V8,i)/median_i(T_ZE,i) over 15 paired rounds",
        "bootstrap": {"B": B, "seed": SEED, "ci": "percentile", "conf": CONF},
        "phase_e_aggregation": "T_E,i = median of 10 requests per engine per round",
        "phase_abc_d_aggregation": "T_E,i = mean of reps (harness-stored rounds_ms)",
        "files": {k: {"path": v, "sha256": None} for k, v in files.items()},
    }
    # fill sha256 for every referenced file
    for k in list(prov["files"]):
        rel = prov["files"][k]["path"]
        p_root = ROOT / rel
        p_out = ROOT / "out" / "raw" / Path(rel).parent.name / Path(rel).name
        actual = p_out if p_out.is_file() else p_root
        prov["files"][k]["sha256"] = sha256(actual)
        prov["files"][k]["path"] = str(actual.relative_to(ROOT))
    out_prov = ART / "data" / "json" / "evidence-ledger.provenance.json"
    out_prov.parent.mkdir(parents=True, exist_ok=True)
    with open(out_prov, "w", encoding="utf-8") as f:
        json.dump(prov, f, indent=2, ensure_ascii=False)

    print(f"ledger rows: {len(rows)}  -> {out_csv.relative_to(ROOT)}")
    print(f"provenance : {len(prov['files'])} files -> {out_prov.relative_to(ROOT)}")
    print()
    print(f"{'evidence_id':<38}{'point':>9}{'ci_lo':>9}{'ci_hi':>9}")
    for r in rows:
        print(f"{r['evidence_id']:<38}{r['point_estimate']:>9}{r['ci95_lower']:>9}{r['ci95_upper']:>9}")


if __name__ == "__main__":
    main()
