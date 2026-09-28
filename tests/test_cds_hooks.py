from fastapi.testclient import TestClient

from app.cds_hooks import QUEUE
from app.main import app

client = TestClient(app)


def mr(i, drug, dose=None):
    r = {"resourceType": "MedicationRequest", "id": i, "status": "draft", "intent": "order",
         "medicationCodeableConcept": {"text": drug}}
    if dose:
        r["dosageInstruction"] = [{"doseAndRate": [{"doseQuantity": {"value": dose, "unit": "mg"}}]}]
    return r


def bundle(resources):
    return {"resourceType": "Bundle", "type": "collection", "entry": [{"resource": r} for r in resources]}


def obs(gene, value):
    return {"resourceType": "Observation", "status": "final", "code": {"text": gene}, "valueCodeableConcept": {"text": value}}


def call(draft, active=(), pgx=(), hook="order-select", service="precisionrx-pgx"):
    body = {"hook": hook, "hookInstance": "t", "context": {"patientId": "p1", "draftOrders": bundle(draft)},
            "prefetch": {"activeMedications": bundle(list(active)), "pgxResults": bundle(list(pgx))}}
    r = client.post(f"/cds-services/{service}", json=body)
    assert r.status_code == 200
    return r.json()["cards"]


def test_discovery_lists_both_hooks():
    hooks = {s["hook"] for s in client.get("/cds-services").json()["services"]}
    assert hooks == {"order-select", "order-sign"}


def test_hla_hard_stop_is_critical_with_override_reasons():
    cards = call([mr("d1", "carbamazepine", 200)], pgx=[obs("HLA-B*15:02", "positive")])
    assert [c["indicator"] for c in cards] == ["critical"]
    assert cards[0]["extension"]["precisionrx"]["hard_stop"] is True
    assert cards[0]["overrideReasons"]
    assert any(a["type"] == "delete" for s in cards[0]["suggestions"] for a in s["actions"])


def test_only_new_findings_are_returned():
    # patient already on clopidogrel + omeprazole: ordering amlodipine must not re-alert the old DDI
    active = [mr("a1", "clopidogrel", 75), mr("a2", "omeprazole", 20)]
    assert call([mr("d1", "amlodipine", 5)], active=active) == []


def test_clopidogrel_pm_on_omeprazole_gives_pgx_and_ddi_with_ppi_swap():
    cards = call([mr("d1", "clopidogrel", 75)], active=[mr("a2", "omeprazole", 20)],
                 pgx=[obs("CYP2C19", "poor metabolizer")])
    ids = {c["extension"]["precisionrx"]["finding_id"] for c in cards}
    assert ids == {"pgx-cyp2c19-clop", "ddi-clop-omeprazole"}
    ddi = next(c for c in cards if c["extension"]["precisionrx"]["finding_id"] == "ddi-clop-omeprazole")
    acts = [a for s in ddi["suggestions"] for a in s["actions"]]
    assert {"delete", "create"} <= {a["type"] for a in acts}
    assert "MedicationRequest/a2" in acts[0]["resourceId"]


def test_untested_allopurinol_suggests_test_order():
    cards = call([mr("d1", "allopurinol", 100)])
    created = [a["resource"]["resourceType"] for c in cards for s in c["suggestions"] for a in s["actions"] if a["type"] == "create"]
    assert "ServiceRequest" in created


def test_order_sign_hook():
    cards = call([mr("d1", "carbamazepine", 200)], pgx=[obs("HLA-B*15:02", "positive")],
                 hook="order-sign", service="precisionrx-pgx-sign")
    assert cards[0]["indicator"] == "critical"


def test_override_feedback_goes_to_pharmacist_queue():
    card = call([mr("d1", "simvastatin", 40)], pgx=[obs("SLCO1B1", "decreased function")])[0]
    n = len(QUEUE)
    client.post("/cds-services/precisionrx-pgx/feedback", json={"feedback": [{
        "card": card["uuid"], "outcome": "overridden",
        "overrideReason": {"reason": {"code": "benefit-outweighs", "display": "ประโยชน์มากกว่าความเสี่ยง"}, "userComment": "test"},
        "outcomeTimestamp": "2026-09-28T10:00:00Z"}]})
    q = client.get("/api/queue").json()
    assert len(q) == n + 1 and q[0]["finding_id"] == "pgx-slco1b1-simva" and q[0]["outcome"] == "overridden"
