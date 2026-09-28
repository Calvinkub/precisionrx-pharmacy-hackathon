"""Build ai_audit_log.csv from the real engine output on the synthetic demo data.

Run from a checkout of branch dev/prototype (needs app/engines/oncology.py):
    uv run python scripts/make_ai_audit_log.py ai_audit_log.csv

The AI decisions and reasons come from the engines. Timestamps, user IDs and clinician
outcomes are simulated for the demo and are labelled "simulated" in the outcome column.
"""

import csv
import json
import sys
import uuid
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.engines.panel import facts
from app.main import app

client = TestClient(app)
FACTS = facts()["facts"]
START = datetime(2026, 9, 28, 9, 0, 0)
RISK = {"stop": "critical", "critical": "critical", "action": "high", "warning": "high", "monitor": "medium", "info": "low"}
DECISION = {"stop": "hard_stop", "critical": "hard_stop", "action": "flag_for_review", "warning": "flag_for_review",
            "monitor": "monitor", "info": "inform"}
rows: list[dict] = []


def confidence(fact_ids: list[str]) -> str:
    """Evidence confidence of the cited facts (rules are deterministic; this is not a model probability)."""
    levels = [(FACTS.get(f) or {}).get("level", "missing") for f in fact_ids]
    verified = all((FACTS.get(f) or {}).get("verified", False) for f in fact_ids)
    if not fact_ids or "missing" in levels or "assumption" in levels or not verified:
        return "low"
    if "emerging" in levels:
        return "medium"
    return "high"


def outcome_for(severity: str, i: int) -> str:
    if severity in ("stop", "critical"):
        return "simulated: order blocked; prescriber chose alternative drug"
    if severity in ("action", "warning"):
        return ["simulated: accepted by pharmacist", "simulated: overridden with reason - sent to pharmacist queue",
                "simulated: modified dose after pharmacist review"][i % 3]
    return "simulated: acknowledged"


def add(user: str, action: str, sev: str, title: str, fact_ids: list[str], i: int):
    rows.append({
        "timestamp": (START + timedelta(minutes=4 * len(rows))).isoformat(timespec="seconds") + "+07:00",
        "user_id": user,
        "action": action,
        "ai_decision": f"{DECISION.get(sev, sev)}: {title}",
        "confidence": confidence(fact_ids),
        "risk_level": RISK.get(sev, "low"),
        "reason": "evidence: " + "; ".join(f"{f} ({(FACTS.get(f) or {}).get('source', 'missing')})" for f in fact_ids),
        "outcome": outcome_for(sev, i),
    })


def no_alert(user: str, action: str):
    rows.append({
        "timestamp": (START + timedelta(minutes=4 * len(rows))).isoformat(timespec="seconds") + "+07:00",
        "user_id": user, "action": action, "ai_decision": "no_alert: no new PGx or interaction finding",
        "confidence": "high", "risk_level": "low", "reason": "rule engine: order causes no new finding (alert-fatigue rule)",
        "outcome": "simulated: order signed",
    })


# 1) Prescribing-time CDS Hooks (doctor)
bundle = lambda rs: {"resourceType": "Bundle", "type": "collection", "entry": [{"resource": r} for r in rs]}


def med_req(pid: str, rid: str, drug: str, dose, status="active"):
    return {"resourceType": "MedicationRequest", "id": rid, "status": status, "intent": "order",
            "subject": {"reference": f"Patient/{pid}"}, "medicationCodeableConcept": {"text": drug},
            "dosageInstruction": [{"text": "", "doseAndRate": [{"doseQuantity": {"value": dose, "unit": "mg"}}] if dose else []}]}


ORDERS = {"HN-0001": [("carbamazepine", 200)], "HN-0002": [("simvastatin", 40), ("amlodipine", 5)],
          "HN-0003": [("clopidogrel", 75)], "HN-0004": [("allopurinol", 100)]}
for p in client.get("/api/his/patients").json():
    for drug, dose in ORDERS.get(p["id"], []):
        body = {"hook": "order-select", "hookInstance": str(uuid.uuid4()),
                "context": {"userId": "Practitioner/MD-demo-01", "patientId": p["id"],
                            "draftOrders": bundle([med_req(p["id"], "draft-1", drug, dose, "draft")])},
                "prefetch": {"activeMedications": bundle([med_req(p["id"], f"a{i}", m["drug"], m.get("dose_mg"))
                                                          for i, m in enumerate(p["active"])]),
                             "pgxResults": bundle([{"resourceType": "Observation", "status": "final", "code": {"text": g["gene"]},
                                                    "valueCodeableConcept": {"text": g["result"]}} for g in p["pgx"]])}}
        cards = client.post("/cds-services/precisionrx-pgx", json=body).json()["cards"]
        act = f"order-select {p['id']}: {drug} {dose} mg"
        if not cards:
            no_alert("MD-demo-01", act)
        for i, cd in enumerate(cards):
            ext = cd["extension"]["precisionrx"]
            add("MD-demo-01", act, cd["indicator"], cd["summary"], ext["fact_ids"], i)

# 2) Pharmacist medication review on the NMR dashboard cases (every visit)
for c in client.get("/api/cases").json():
    case = client.get(f"/api/cases/{c['id']}").json()
    for v in range(len(case["visits"])):
        res = client.post("/api/assess", json={"profile": case["profile"], "meds": case["meds"], "pgx": case["pgx"],
                                                "visits": case["visits"][: v + 1]}).json()
        act = f"assess case {c['id']} visit {v + 1}"
        for i, f in enumerate(res["findings"]):
            add("RPh-demo-01", act, f["severity"], f["title"], f["fact_ids"], i)
        for r in res["risks"]:
            add("RPh-demo-01", act, "info", f"{r['score_name']} = {r['display']} ({r['category']})", r["fact_ids"], 0)

# 3) Oncology pharmacy report (cfDNA + germline PGx + TKI interactions)
for o in client.get("/api/oncology/cases").json():
    res = client.get(f"/api/oncology/cases/{o['id']}").json()
    for i, f in enumerate(res["findings"]):
        add("RPh-onc-demo-01", f"oncology report {o['id']}", f["severity"], f["title"], f["fact_ids"], i)

out = sys.argv[1] if len(sys.argv) > 1 else "ai_audit_log.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=["timestamp", "user_id", "action", "ai_decision", "confidence", "risk_level", "reason", "outcome"])
    w.writeheader()
    w.writerows(rows)
print(json.dumps({"rows": len(rows), "file": out}))
