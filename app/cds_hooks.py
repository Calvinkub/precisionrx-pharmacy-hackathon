"""CDS Hooks service (order-select / order-sign) + feedback -> pharmacist queue.

Spec: https://cds-hooks.org/  (cards, suggestions, overrideReasons, feedback)
The HIS sends the draft MedicationRequest(s) in context.draftOrders and, via prefetch, the
patient's active MedicationRequests and PGx Observations. Only findings CAUSED by the draft order
are returned, so an unchanged med list never re-alerts (alert-fatigue rule, idea.md §6).
"""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.engines import meds as m
from app.engines.panel import facts

router = APIRouter()
SERVICE_ID = "precisionrx-pgx"
INDICATOR = {"stop": "critical", "action": "warning", "monitor": "info", "info": "info"}
OVERRIDE_REASONS = [
    {"code": "tolerated-before", "display": "เคยใช้ยานี้มานานโดยไม่มีอาการไม่พึงประสงค์"},
    {"code": "no-alternative", "display": "ไม่มียาทางเลือกที่เหมาะสม"},
    {"code": "benefit-outweighs", "display": "ประโยชน์มากกว่าความเสี่ยง จะติดตามใกล้ชิด"},
    {"code": "result-disputed", "display": "สงสัยผลตรวจ ขอให้เภสัชกรทบทวน"},
]
QUEUE: list[dict] = []  # in-memory pharmacist queue (demo only)
_ISSUED: dict[str, dict] = {}  # card uuid -> card + context, for feedback lookup


class HookRequest(BaseModel):
    hook: str
    hookInstance: str
    context: dict
    prefetch: dict = Field(default_factory=dict)


def _med_from_fhir(res: dict) -> m.Medication:
    name = (res.get("medicationCodeableConcept") or {}).get("text", "")
    dose = None
    for di in res.get("dosageInstruction") or []:
        for dr in di.get("doseAndRate") or []:
            dose = (dr.get("doseQuantity") or {}).get("value", dose)
    return m.Medication(name, dose)


def _entries(bundle: dict | None) -> list[dict]:
    return [e["resource"] for e in (bundle or {}).get("entry", []) if "resource" in e]


def _pgx_from_fhir(bundle: dict | None) -> dict[str, str]:
    out = {}
    for obs in _entries(bundle):
        gene = (obs.get("code") or {}).get("text")
        val = (obs.get("valueCodeableConcept") or {}).get("text")
        if gene and val:
            out[gene] = val
    return out


def _source(fact_ids: list[str]) -> dict:
    f = facts()["facts"].get(fact_ids[0], {})
    return {"label": f"PrecisionRx · {f.get('source', fact_ids[0])}", "url": f.get("url", "")}


def _suggestions(f: m.Finding, draft: list[dict], active: list[dict]) -> list[dict]:
    """Suggestions only remove/replace orders; choosing the alternative drug stays with the prescriber."""
    out = []
    draft_by_name = {(_med_from_fhir(r).key): r for r in draft}
    active_by_name = {(_med_from_fhir(r).key): r for r in active}
    drug = f.trace[0].removeprefix("ยา: ").split()[0].lower() if f.trace else ""
    if f.category == "ddi":
        orders = {**active_by_name, **draft_by_name}
        ppi = next((k for k in orders if k in m.PPIS and k in f.id), None)
        if ppi:
            out.append({"label": f"หยุด {ppi} → สั่ง pantoprazole 40 mg แทน", "uuid": str(uuid.uuid4()), "actions": [
                {"type": "delete", "description": f"หยุด {ppi}", "resourceId": [f"MedicationRequest/{orders[ppi].get('id')}"]},
                {"type": "create", "description": "สั่ง pantoprazole 40 mg วันละครั้ง", "resource": {
                    "resourceType": "MedicationRequest", "status": "draft", "intent": "order",
                    "medicationCodeableConcept": {"text": "pantoprazole"},
                    "dosageInstruction": [{"text": "วันละครั้ง ก่อนอาหารเช้า",
                                           "doseAndRate": [{"doseQuantity": {"value": 40, "unit": "mg"}}]}]}}]})
    if "untested" in f.id:
        gene = "HLA-B*15:02" if "1502" in f.id else "HLA-B*58:01"
        out.append({"label": f"ส่งตรวจ {gene} (รอผลก่อนเริ่มยา)", "uuid": str(uuid.uuid4()), "actions": [
            {"type": "create", "description": f"ส่งตรวจ {gene}", "resource": {
                "resourceType": "ServiceRequest", "status": "draft", "intent": "order", "code": {"text": f"{gene} genotyping"}}}]})
    if drug in draft_by_name and f.severity in {"stop", "action"} and f.category == "pgx":
        out.append({"label": f"ยกเลิกคำสั่ง {drug}", "uuid": str(uuid.uuid4()), "actions": [
            {"type": "delete", "description": f"ยกเลิก {drug}", "resourceId": [f"MedicationRequest/{draft_by_name[drug].get('id')}"]}]})
    return out


def _card(f: m.Finding, draft: list[dict], active: list[dict], patient_id: str) -> dict:
    store = facts()["facts"]
    lines = [f.detail, "", "**หลักฐาน**"]
    for fid in f.fact_ids:
        x = store.get(fid, {})
        flag = "" if x.get("verified") else " _(ถ้อยคำยังไม่ได้ตรวจกับต้นฉบับ)_"
        lines.append(f"- `{fid}` {x.get('text', '')} — {x.get('source', '')}{flag}")
    lines += ["", "**Why?** " + " → ".join(f.trace)]
    card = {
        "uuid": str(uuid.uuid4()),
        "summary": f.title[:140],
        "detail": "\n".join(lines),
        "indicator": INDICATOR[f.severity],
        "source": _source(f.fact_ids),
        "suggestions": _suggestions(f, draft, active),
        "selectionBehavior": "at-most-one",
        "overrideReasons": OVERRIDE_REASONS,
        "extension": {"precisionrx": {"finding_id": f.id, "fact_ids": f.fact_ids, "hard_stop": f.severity == "stop"}},
    }
    _ISSUED[card["uuid"]] = {"card": card, "patient_id": patient_id}
    return card


@router.get("/cds-services")
def discovery():
    common = {"prefetch": {"patient": "Patient/{{context.patientId}}",
                           "activeMedications": "MedicationRequest?patient={{context.patientId}}&status=active",
                           "pgxResults": "Observation?patient={{context.patientId}}&category=laboratory&code=pgx"}}
    return {"services": [
        {"hook": "order-select", "id": SERVICE_ID, "title": "PrecisionRx PGx + DDI",
         "description": "เตือนเฉพาะ PGx/DDI ที่เกิดจากคำสั่งยาใหม่ พร้อมหลักฐาน", **common},
        {"hook": "order-sign", "id": f"{SERVICE_ID}-sign", "title": "PrecisionRx PGx + DDI (sign)",
         "description": "ตรวจซ้ำตอนยืนยันคำสั่ง — hard stop สำหรับ HLA-B", **common},
    ]}


def _run(req: HookRequest) -> dict:
    if req.hook not in {"order-select", "order-sign"}:
        raise HTTPException(400, f"unsupported hook {req.hook}")
    draft = [r for r in _entries(req.context.get("draftOrders")) if r.get("resourceType") == "MedicationRequest"]
    active = [r for r in _entries(req.prefetch.get("activeMedications")) if r.get("resourceType") == "MedicationRequest"]
    pgx = _pgx_from_fhir(req.prefetch.get("pgxResults"))
    before_meds = [_med_from_fhir(r) for r in active]
    after_meds = before_meds + [_med_from_fhir(r) for r in draft]

    def run(ms):
        return {f.id: f for f in m.pgx_findings(ms, pgx) + m.ddi_findings(ms)}

    before, after = run(before_meds), run(after_meds)
    new = m.sort_findings([f for k, f in after.items() if k not in before])
    pid = req.context.get("patientId", "")
    return {"cards": [_card(f, draft, active, pid) for f in new]}


@router.post(f"/cds-services/{SERVICE_ID}")
def order_select(req: HookRequest):
    return _run(req)


@router.post(f"/cds-services/{SERVICE_ID}-sign")
def order_sign(req: HookRequest):
    return _run(req)


class FeedbackIn(BaseModel):
    feedback: list[dict]


@router.post(f"/cds-services/{SERVICE_ID}/feedback")
@router.post(f"/cds-services/{SERVICE_ID}-sign/feedback")
def feedback(body: FeedbackIn):
    for fb in body.feedback:
        issued = _ISSUED.get(fb.get("card", ""))
        if not issued:
            continue
        card = issued["card"]
        QUEUE.insert(0, {
            "time": fb.get("outcomeTimestamp") or datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "patient_id": issued["patient_id"],
            "summary": card["summary"],
            "indicator": card["indicator"],
            "finding_id": card["extension"]["precisionrx"]["finding_id"],
            "fact_ids": card["extension"]["precisionrx"]["fact_ids"],
            "outcome": fb.get("outcome"),
            "reason": ((fb.get("overrideReason") or {}).get("reason") or {}).get("display"),
            "comment": (fb.get("overrideReason") or {}).get("userComment"),
            "accepted_suggestion": [s.get("id") for s in fb.get("acceptedSuggestions", [])],
            "status": "open",
        })
    return {"ok": True}


@router.get("/api/queue")
def get_queue():
    return QUEUE


@router.post("/api/queue/{idx}/{status}")
def set_queue_status(idx: int, status: str):
    if not 0 <= idx < len(QUEUE) or status not in {"open", "reviewed", "contacted-prescriber"}:
        raise HTTPException(404)
    QUEUE[idx]["status"] = status
    return QUEUE[idx]
