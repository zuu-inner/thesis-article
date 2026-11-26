#!/usr/bin/env python3
"""Stage 2 evidence verification (read-only on all raw evidence).

Verifies primary A-E metadata, recomputes point estimates from raw exhibits,
checks Phase E request structure, and compares corpus per-file SHA-256 against
the corpus manifest. Derived output only:
  article/data/json/final-audit-evidence.json
"""
from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import Counter
import os
from pathlib import Path

ROOT = Path(os.environ.get("THESIS_WORKSPACE_ROOT", Path(__file__).resolve().parents[3])).resolve()
LEDGER = ROOT / "article" / "data" / "csv" / "evidence-ledger.csv"
OUT = ROOT / "article" / "data" / "json" / "final-audit-evidence.json"
MANIFEST = ROOT / "corpus" / "benchmarks" / "saq_payload_v1" / "MANIFEST.json"

RUNS = {
    "A": ["zuu-20261115071747-6d87bf3",
          "server-lanjut-20261116060843-8a1324b"],
    "B": ["zuu-20261115075332-6d87bf3",
          "server-lanjut-20261116060900-8a1324b"],
    "C": ["zuu-20261115080838-6d87bf3",
          "server-lanjut-20261116060915-8a1324b"],
    "D": ["zuu-20261115080840-6d87bf3",
          "server-lanjut-20261116060933-8a1324b"],
    "E": ["zuu-20261116101458-8556513",
          "zuu-20261117000112-6979e3f",
          "server-lanjut-20261117003513-530f751"],
}
PAIRS = {
    "A": ("v8-parse", "ze-parse"),
    "B": ("v8-selective", "ze-project-selective"),
    "C": ("v8-selective", "ze-l1-traversal"),
    "D": (("D-mongo-cache-v8", "D-mongo-cache-ze"),
          ("D-file-store-v8", "D-file-store-ze")),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def record(rid: str) -> dict:
    hits = list((ROOT / "reports" / "nd14").glob(f"{rid}*.record.json"))
    hits += list((ROOT / "reports" / "nd11").glob(f"{rid}*.record.json"))
    if len(hits) != 1:
        raise FileNotFoundError(f"record for {rid}: {len(hits)} hits")
    return load_json(hits[0])


def exhibit(rid: str, phase: str) -> dict:
    name = (f"nd11_phase_e.json" if phase == "E"
            else f"nd6_phase_{phase}.json")
    p = ROOT / "out" / "raw" / rid / name
    if not p.is_file():
        raise FileNotFoundError(p)
    return load_json(p)


def main() -> None:
    with open(LEDGER, encoding="utf-8") as f:
        ledger = {r["evidence_id"]: r for r in csv.DictReader(f)}
    manifest = load_json(MANIFEST)
    man_hashes = {d["file"]: d["sha256"] for d in manifest["documents"]}
    summary: dict = {"metadata": [], "checks": [], "corpus": []}

    for phase, rids in RUNS.items():
        for rid in rids:
            rec = record(rid)
            lib = rec.get("library", {})
            summary["metadata"].append({
                "phase": phase, "run_id": rid, "site": rec["site"],
                "runtime": rec.get("host", {}).get("toolchain", ""),
                "core_version": lib.get("core_version"),
                "js_version": lib.get("js_version"),
                "abi_version": lib.get("abi_version"),
                "artifact_sha256": lib.get("artifact_sha256"),
                "corpus": rec.get("corpus", {}).get("name"),
                "rounds": rec.get("config", {}).get("repeats"),
                "warmup": rec.get("config", {}).get("warmup_runs"),
                "config_iterations": rec.get("config", {}).get("iterations"),
            })
            raw = exhibit(rid, phase)
            if phase in ("A", "B", "C"):
                pairs = PAIRS[phase]
                by = {(r["doc"], r["path"]): [float(x) for x in r["rounds_ms"]]
                      for r in raw["raw_rounds"]}
                for doc, (vp, zp) in ((d, pairs) for d in sorted(
                        {k[0] for k in by})):
                    v, z = by[(doc, vp)], by[(doc, zp)]
                    assert len(v) == len(z) == 15
                    point = statistics.median(v) / statistics.median(z)
                    key = f"{phase}-primary-{rec['site']}-{doc}"
                    ledger_point = float(ledger[key]["point_estimate"])
                    summary["checks"].append({
                        "key": key, "run_id": rid,
                        "recomputed": round(point, 4),
                        "ledger": ledger_point,
                        "status": "MATCH" if abs(point - ledger_point) <= 5e-5
                                  else "MISMATCH"})
            elif phase == "D":
                by = {r["path"]: [float(x) for x in r["rounds_ms"]]
                      for r in raw["raw_rounds"]}
                for vp, zp in PAIRS["D"]:
                    v, z = by[vp], by[zp]
                    assert len(v) == len(z) == 15
                    point = statistics.median(v) / statistics.median(z)
                    store = vp[2:-3]  # strip 'D-' and '-v8'
                    key = f"D-primary-{rec['site']}-{store}"
                    ledger_point = float(ledger[key]["point_estimate"])
                    summary["checks"].append({
                        "key": key, "run_id": rid,
                        "recomputed": round(point, 4),
                        "ledger": ledger_point,
                        "status": "MATCH" if abs(point - ledger_point) <= 5e-5
                                  else "MISMATCH"})
            else:
                req = raw["requests"]
                counts = {eng: Counter(int(x["round"]) for x in req[eng])
                          for eng in ("v8", "ze")}
                ok = (len(req["v8"]) == len(req["ze"]) == 150 and
                      set(counts["v8"]) == set(counts["ze"]) ==
                      set(range(1, 16)) and
                      all(counts["v8"][r] == counts["ze"][r] == 10
                          for r in range(1, 16)))
                hashes = {x["body_sha256"] for x in
                          req["v8"] + req["ze"]}
                v = [statistics.median(x["seconds"] * 1000 for x in req["v8"]
                                       if int(x["round"]) == r)
                     for r in range(1, 16)]
                z = [statistics.median(x["seconds"] * 1000 for x in req["ze"]
                                       if int(x["round"]) == r)
                     for r in range(1, 16)]
                point = statistics.median(v) / statistics.median(z)
                key = f"E-primary-{rec['site']}-rekap-{rid}"
                ledger_point = float(ledger[key]["point_estimate"])
                summary["checks"].append({
                    "key": key, "run_id": rid,
                    "structure_15x20_10_10": ok,
                    "n_v8": len(req["v8"]), "n_ze": len(req["ze"]),
                    "unique_body_hashes": len(hashes),
                    "recomputed": round(point, 4), "ledger": ledger_point,
                    "status": "MATCH" if abs(point - ledger_point) <= 5e-5
                              else "MISMATCH"})
                store_hashes = rec["results"][0]["extras"].get("store_sha256")
                if store_hashes:
                    summary["corpus"].append({
                        "run_id": rid, "site": rec["site"],
                        "store_label": rec["corpus"]["name"],
                        "all_six_match_manifest":
                            all(store_hashes.get(f) == h
                                for f, h in man_hashes.items()),
                        "per_file": {f: store_hashes.get(f) == h
                                     for f, h in man_hashes.items()}})

    # on-disk corpus files vs manifest
    cdir = ROOT / "corpus" / "benchmarks" / "saq_payload_v1"
    summary["corpus"].append({
        "run_id": "ON-DISK", "site": "-", "store_label": "corpus files",
        "all_six_match_manifest":
            all(sha256(cdir / f) == h for f, h in man_hashes.items()),
        "per_file": {f: sha256(cdir / f) == h for f, h in man_hashes.items()}})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    statuses = Counter(c["status"] for c in summary["checks"])
    print(f"metadata rows: {len(summary['metadata'])}")
    print(f"point checks: {dict(statuses)}")
    print("E structure:", [(c["key"], c.get("structure_15x20_10_10"),
                            c.get("unique_body_hashes"))
                           for c in summary["checks"] if c["key"].startswith("E")])
    print("corpus:", [(c["run_id"], c["all_six_match_manifest"])
                      for c in summary["corpus"]])
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
