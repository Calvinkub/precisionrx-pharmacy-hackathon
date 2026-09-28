"""Run the gold-standard eval set against the engines and write a report.

    uv run python -m eval.run_eval            # prints summary, writes eval/report.md + eval/results.json
    uv run python -m eval.run_eval --sheet    # also (re)writes eval/review_sheet.csv for pharmacists

Metrics (idea.md §9):
  omission           = expected finding (from the gold label) the engine did not produce (target 0)
  false flag         = stop/action finding or NMR factor produced but not in the gold label
  risk / trend agreement with the label
  citation validity  = every cited fact id exists in the evidence store; unverified facts counted
  alert burden       = alerts to review per case vs a naive "alert on everything available" baseline
"""

import csv
import json
import sys
from pathlib import Path

import yaml

from app.assess import AssessIn, assess
from app.engines.meds import PPIS, STATINS
from app.engines.panel import catalog, facts, status

HERE = Path(__file__).resolve().parent
NORMAL = json.loads((HERE.parent / "data" / "synthetic" / "case_3.json").read_text(encoding="utf-8"))["visits"][0]["values"]
DEFAULT_PROFILE = {"age": 45, "sex": "female", "sbp": 118, "weight_kg": 55, "height_cm": 160, "waist_cm": 72,
                   "smoker": False, "diabetes": False, "hypertension": False, "family_history_dm": False}
CRITICAL = {"stop", "action"}

# naive baseline: drug-gene pairs a "show every PGx result" system would pop up
NAIVE_PGX = {"carbamazepine": "HLA-B*15:02", "oxcarbazepine": "HLA-B*15:02", "allopurinol": "HLA-B*58:01",
             "clopidogrel": "CYP2C19", **{s: "SLCO1B1" for s in STATINS}, **{p: "CYP2C19" for p in PPIS}}


def build_request(case: dict) -> AssessIn:
    visits = case.get("visits") or [{}]
    return AssessIn(
        profile={**DEFAULT_PROFILE, **case.get("profile", {})},
        meds=case.get("meds", []),
        pgx=case.get("pgx", {}),
        alcohol_drinks_per_day=0,
        activity_min_week=200,
        visits=[{"date": f"2026-0{i + 1}-01", "values": {**NORMAL, **v}} for i, v in enumerate(visits)],
    )


def naive_alerts(req: AssessIn) -> int:
    n = 0
    drugs = {m.drug.lower() for m in req.meds}
    for d in drugs:
        if NAIVE_PGX.get(d) in req.pgx:
            n += 1
    if "clopidogrel" in drugs:
        n += len(drugs & PPIS)
    cur = req.visits[-1].values
    n += sum(1 for k, v in cur.items() if k in catalog() and status(k, v) != "normal")
    return n


def evaluate(case: dict) -> dict:
    req = build_request(case)
    out = assess(req)
    exp = case.get("expected", {})
    res = {"id": case["id"], "scenario": case["scenario"], "problems": []}

    produced = {f["id"]: f["severity"] for f in out["findings"]}
    produced_critical = {k for k, s in produced.items() if s in CRITICAL}
    if "findings" in exp:
        want = set(exp["findings"])
        res["omissions"] = sorted(want - produced.keys())
        res["false_flags"] = sorted(produced_critical - want)
        res["expected_findings"] = len(want)
    factors = {f["id"] for f in out["nmr_factors"]}
    if "factors" in exp:
        want = set(exp["factors"])
        res["factor_misses"] = sorted(want - factors)
        res["factor_false"] = sorted(factors - want)
    if "risks" in exp:
        got = {r["id"]: r["category"] for r in out["risks"]}
        res["risk_mismatch"] = {k: {"expected": v, "got": got.get(k)} for k, v in exp["risks"].items() if got.get(k) != v}
    if "trend" in exp:
        got = {t["id"]: t["verdict"] for t in out["trend"]}
        res["trend_mismatch"] = {k: {"expected": v, "got": got.get(k)} for k, v in exp["trend"].items() if got.get(k) != v}
    if "advice" in exp:
        got = {a["id"] for a in out["advice"]}
        res["advice_misses"] = sorted(set(exp["advice"]) - got)

    cited = [fid for group in ("risks", "nmr_factors", "findings", "advice") for x in out[group] for fid in x["fact_ids"]]
    store = facts()["facts"]
    res["citations"] = len(cited)
    res["citations_missing"] = sorted({c for c in cited if c not in store})
    res["citations_unverified"] = sorted({c for c in cited if c in store and not store[c].get("verified")})

    res["alerts_precisionrx"] = len(produced_critical) + sum(1 for f in out["nmr_factors"] if f["severity"] == "monitor")
    res["alerts_naive"] = naive_alerts(req)

    for key in ("omissions", "false_flags", "factor_misses", "factor_false", "advice_misses", "citations_missing"):
        if res.get(key):
            res["problems"].append(f"{key}: {', '.join(res[key])}")
    for key in ("risk_mismatch", "trend_mismatch"):
        for k, v in (res.get(key) or {}).items():
            res["problems"].append(f"{key}: {k} expected {v['expected']} got {v['got']}")
    res["pass"] = not res["problems"]
    return res


def summarize(results: list[dict]) -> dict:
    def total(key):
        return sum(len(r.get(key) or []) for r in results)

    expected = sum(r.get("expected_findings", 0) for r in results)
    omit = total("omissions")
    risk_checked = sum(1 for r in results if "risk_mismatch" in r)
    trend_checked = sum(1 for r in results if "trend_mismatch" in r)
    citations = sum(r["citations"] for r in results)
    naive = sum(r["alerts_naive"] for r in results)
    ours = sum(r["alerts_precisionrx"] for r in results)
    return {
        "cases": len(results),
        "passed": sum(r["pass"] for r in results),
        "expected_findings": expected,
        "omissions": omit,
        "omission_rate": round(omit / expected, 3) if expected else 0,
        "false_flags": total("false_flags") + total("factor_false"),
        "factor_misses": total("factor_misses"),
        "risk_cases_agree": f"{risk_checked - sum(1 for r in results if r.get('risk_mismatch'))}/{risk_checked}",
        "trend_cases_agree": f"{trend_checked - sum(1 for r in results if r.get('trend_mismatch'))}/{trend_checked}",
        "citations": citations,
        "citations_missing": total("citations_missing"),
        "unverified_fact_ids_cited": sorted({c for r in results for c in r["citations_unverified"]}),
        "alerts_per_case_naive": round(naive / len(results), 2),
        "alerts_per_case_precisionrx": round(ours / len(results), 2),
        "alert_reduction_pct": round((1 - ours / naive) * 100, 1) if naive else 0,
    }


def write_report(s: dict, results: list[dict]) -> str:
    lines = [
        "# PrecisionRx — Eval report (SYNTHETIC)",
        "",
        "> Gold labels written by hand from guideline/label text, **pending pharmacist review**.",
        "> Synthetic cases only — these numbers show the rules behave as specified, not clinical accuracy.",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Cases passed | {s['passed']}/{s['cases']} |",
        f"| Omissions of expected findings (target 0) | {s['omissions']} of {s['expected_findings']} ({s['omission_rate']:.1%}) |",
        f"| False flags (stop/action + NMR factors) | {s['false_flags']} |",
        f"| Risk category agreement | {s['risk_cases_agree']} |",
        f"| RCV trend verdict agreement | {s['trend_cases_agree']} |",
        f"| Citations checked / missing fact ids | {s['citations']} / {s['citations_missing']} |",
        f"| Unverified fact ids still cited | {', '.join(s['unverified_fact_ids_cited']) or '—'} |",
        f"| Alerts per case: naive baseline → PrecisionRx | {s['alerts_per_case_naive']} → {s['alerts_per_case_precisionrx']} (−{s['alert_reduction_pct']}%) |",
        "",
        "Naive baseline = alert on every drug with an available PGx result, every clopidogrel+PPI pair, and every analyte outside its reference band.",
        "",
        "## Per case",
        "",
        "| Case | Scenario | Result | Alerts (naive → ours) |",
        "|---|---|---|---|",
    ]
    for r in results:
        verdict = "✅" if r["pass"] else "❌ " + "; ".join(r["problems"])
        lines.append(f"| {r['id']} | {r['scenario']} | {verdict} | {r['alerts_naive']} → {r['alerts_precisionrx']} |")
    return "\n".join(lines) + "\n"


def write_review_sheet(cases: list[dict]) -> None:
    with open(HERE / "review_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["case", "scenario", "expected_findings", "expected_factors", "expected_risks", "expected_trend",
                    "pharmacist_1_agree(Y/N)", "pharmacist_1_note", "pharmacist_2_agree(Y/N)", "pharmacist_2_note",
                    "pharmacist_3_agree(Y/N)", "pharmacist_3_note"])
        for c in cases:
            e = c.get("expected", {})
            w.writerow([c["id"], c["scenario"], " ".join(e.get("findings", [])) if "findings" in e else "",
                        " ".join(e.get("factors", [])) if "factors" in e else "",
                        json.dumps(e.get("risks", {}), ensure_ascii=False) if "risks" in e else "",
                        json.dumps(e.get("trend", {}), ensure_ascii=False) if "trend" in e else ""])


def run() -> tuple[dict, list[dict]]:
    cases = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"]
    results = [evaluate(c) for c in cases]
    return summarize(results), results


def main() -> None:
    s, results = run()
    (HERE / "results.json").write_text(json.dumps({"summary": s, "cases": results}, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "report.md").write_text(write_report(s, results), encoding="utf-8")
    if "--sheet" in sys.argv:
        write_review_sheet(yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"])
    for k, v in s.items():
        print(f"{k:32} {v}")
    for r in results:
        if not r["pass"]:
            print(f"  ❌ {r['id']}: {'; '.join(r['problems'])}")


if __name__ == "__main__":
    main()
