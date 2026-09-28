"""Doctor-in-the-loop care plan: candidate interventions by risk tier -> edited/approved by the
clinician -> exported as a FHIR R4 CarePlan + ServiceRequest bundle for the HIS/EHR order sheet."""

import hashlib
import json
import uuid
from datetime import date, datetime, timedelta, timezone


def _item(id, category, title, detail, weeks, why, facts, selected=True):
    return {"id": id, "category": category, "title": title, "detail": detail, "interval_weeks": weeks,
            "rationale": why, "fact_ids": facts, "selected": selected}


def propose(risks: dict[str, dict], features: dict, flags: list[dict]) -> list[dict]:
    out = []
    cvd, dm, mets, ckd, liver = (risks.get(k, {}) for k in ("cvd", "dm", "mets", "ckd", "masld"))
    if mets.get("category") in ("present", "at_risk") or dm.get("category") in ("high", "very_high"):
        out.append(_item("nutrition", "nutrition", "โภชนบำบัดรายบุคคล", "ลดน้ำหนัก 5–7% ใน 6 เดือน ลดไขมันอิ่มตัว < 7% ของพลังงาน ลดน้ำตาล < 10%",
                         12, "กลุ่มอาการเมตาบอลิก / เสี่ยงเบาหวานสูง", ["ADA-2026-PREV", "RCPT-2024-DIET", "RCPT-2024-TG"]))
    if features.get("active_minutes_week") is not None and features["active_minutes_week"] < 150:
        out.append(_item("exercise", "exercise", "ใบสั่งออกกำลังกาย", "แอโรบิกระดับปานกลาง 150–300 นาที/สัปดาห์ + เวทเทรนนิ่ง 2 วัน/สัปดาห์ (ติดตามจาก smartwatch)",
                         4, f"กิจกรรมจาก smartwatch เฉลี่ย {features['active_minutes_week']:.0f} นาที/สัปดาห์", ["WHO-PA-2020"]))
    if features.get("on_statin"):
        out.append(_item("lipid_recheck", "lab", "ตรวจไขมันซ้ำ (lipid + ApoB)", "ติดตามผลยาลดไขมันและการกินยา", 8,
                         "ใช้ยาลดไขมันอยู่", ["RCPT-2024-FOLLOWUP"]))
    if dm.get("category") in ("high", "very_high") or features.get("prediabetes"):
        out.append(_item("glucose_confirm", "lab", "ตรวจ FPG / HbA1c ยืนยัน", "ยืนยันภาวะก่อนเบาหวาน", 12,
                         "คะแนนเสี่ยงเบาหวานสูง หรือน้ำตาลอยู่ในช่วงก่อนเบาหวาน", ["ADA-2026-DX", "TDRS-2006"]))
    if ckd.get("category") in ("moderate", "high", "very_high"):
        out.append(_item("ckd_confirm", "lab", "ตรวจ creatinine + UACR ซ้ำ", "ยืนยันความผิดปกติของไตที่คงอยู่เกิน 3 เดือน", 12,
                         f"eGFR/UACR อยู่ในกลุ่มเสี่ยง KDIGO {ckd.get('category_label', '')}", ["KDIGO-2024"]))
    if liver.get("category") in ("high", "very_high"):
        out.append(_item("elastography", "imaging", "ส่งตรวจความแข็งตับ (elastography)", "FIB-4 อยู่ในช่วงต้องตรวจเพิ่ม", 6,
                         "ประเมินพังผืดในตับต่อจาก FIB-4", ["FIB4-MASLD"]))
    elif liver.get("category") == "moderate":
        out.append(_item("liver_us", "imaging", "อัลตราซาวด์ตับ (พิจารณา)", "FLI บ่งชี้ไขมันพอกตับ", 12, "Fatty Liver Index ≥ 60", ["FLI-2006"], selected=False))
    for f in flags:
        if f["id"] == "cfdna-hmw" and f["severity"] == "action":
            out.append(_item("cfdna_recollect", "lab", "เก็บตัวอย่าง cfDNA ใหม่", "หลอด cfDNA stabilizing + ปั่นแยกพลาสมาภายในเวลาที่กำหนด", 2,
                             "ตัวอย่างเดิมปนเปื้อน genomic DNA", ["CFDNA-HMW-QC"]))
        if f["id"] == "adherence":
            out.append(_item("adherence", "medication", "ทบทวนการกินยากับเภสัชกร", f["detail"], 4, "PDC ต่ำกว่า 80%", ["PQA-PDC80"]))
    if cvd.get("category") in ("high", "very_high"):
        out.append(_item("cvd_review", "medication", "ทบทวนการรักษาความเสี่ยงหัวใจ", "เป้า LDL-C และความดันตาม guideline", 4,
                         f"Thai CV risk {cvd.get('display')}", ["RCPT-2024-LDL-TARGET", "TCVRS-2021"]))
    return out


def export_fhir(patient_id: str, items: list[dict], approver: str, note: str = "") -> dict:
    """FHIR R4 transaction-style Bundle: one CarePlan + one ServiceRequest per selected item."""
    now = datetime.now(timezone.utc)
    sel = [i for i in items if i.get("selected")]
    reqs = []
    for i in sel:
        rid = str(uuid.uuid4())
        due = date.today() + timedelta(weeks=int(i.get("interval_weeks") or 0))
        reqs.append({"fullUrl": f"urn:uuid:{rid}", "resource": {
            "resourceType": "ServiceRequest", "id": rid, "status": "active", "intent": "order",
            "category": [{"text": i["category"]}], "code": {"text": i["title"]}, "subject": {"reference": f"Patient/{patient_id}"},
            "occurrenceDateTime": due.isoformat(), "note": [{"text": i.get("detail", "")}],
            "reasonCode": [{"text": i.get("rationale", "")}], "supportingInfo": [{"display": fid} for fid in i.get("fact_ids", [])],
            "requester": {"display": approver}}})
    cp_id = str(uuid.uuid4())
    careplan = {"fullUrl": f"urn:uuid:{cp_id}", "resource": {
        "resourceType": "CarePlan", "id": cp_id, "status": "active", "intent": "plan", "title": "แผนป้องกันโรค NCDs",
        "subject": {"reference": f"Patient/{patient_id}"}, "created": now.isoformat(timespec="seconds"),
        "author": {"display": approver}, "note": [{"text": note}] if note else [],
        "activity": [{"reference": {"reference": r["fullUrl"]}} for r in reqs]}}
    bundle = {"resourceType": "Bundle", "type": "collection", "timestamp": now.isoformat(timespec="seconds"), "entry": [careplan, *reqs]}
    digest = hashlib.sha256(json.dumps(bundle, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    bundle["meta"] = {"tag": [{"system": "urn:precisionrx:approval", "code": "approved", "display": f"{approver} · sha256:{digest[:16]}"}]}
    return bundle
