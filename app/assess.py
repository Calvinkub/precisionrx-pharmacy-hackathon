"""Combine NMR panel + patient profile + medications into one assessment."""

from dataclasses import asdict

from pydantic import BaseModel, Field

from app.engines import meds as m
from app.engines.meds import STATINS as m_STATINS
from app.engines.lifestyle import lifestyle_advice
from app.engines.nmr_factors import MMOL_TO_MG_DL_CHOL, nmr_factors
from app.engines.nmr_summary import summarize
from app.engines.panel import catalog, facts, status, trend
from app.engines.risk import Profile, thai_cv_risk, thai_diabetes_risk


class ProfileIn(BaseModel):
    age: int
    sex: str = "female"
    sbp: float | None = None
    smoker: bool = False
    diabetes: bool = False
    hypertension: bool = False
    family_history_dm: bool = False
    weight_kg: float | None = None
    height_cm: float | None = None
    waist_cm: float | None = None


class MedIn(BaseModel):
    drug: str
    dose_mg: float | None = None
    pdc_pct: float | None = None
    start_visit: int | None = None  # 0-based index of first visit ON the drug; None = before first visit


class VisitIn(BaseModel):
    date: str
    label: str | None = None
    values: dict[str, float]


class AssessIn(BaseModel):
    profile: ProfileIn
    meds: list[MedIn] = Field(default_factory=list)
    pgx: dict[str, str] = Field(default_factory=dict)
    alcohol_drinks_per_day: float = 0
    activity_min_week: float | None = None
    visits: list[VisitIn]


def ldl_target_finding(statin: m.Medication, ldl: float, cv_risk: float | None) -> m.Finding | None:
    if cv_risk is None or cv_risk <= 10 or ldl < 2.6:
        return None
    return m.Finding(
        f"target-{statin.key}", "response", "action", "LDL-C ยังไม่ถึงเป้าหมาย",
        f"Thai CV risk {'> 30' if cv_risk > 30 else f'{cv_risk:.0f}'}% (> 10%) เป้า LDL-C < 100 mg/dL แต่ตอนนี้ {ldl * MMOL_TO_MG_DL_CHOL:.0f} mg/dL",
        ["RCPT-2024-LDL-TARGET", "TCVRS-2021"],
        [f"Thai CV risk = {cv_risk:.1f}%", f"LDL-C = {ldl:.2f} mmol/L", "เป้า RCPT 2024 < 2.6 mmol/L"])


def next_steps(medications: list, cur: dict, risks: list, factors: list, diabetes: bool) -> list[dict]:
    """What to check next, each with its source."""
    out = []
    if any(m.key in m_STATINS for m in medications):
        out.append({"id": "recheck_lipids", "text": "ตรวจไขมันซ้ำใน 4–12 สัปดาห์หลังเริ่มหรือปรับยาลดไขมัน เพื่อดูผลของยาและการกินยา",
                    "fact_ids": ["RCPT-2024-FOLLOWUP"]})
    g = cur.get("glucose")
    dm = next((r for r in risks if r.id == "dm"), None)
    if not diabetes and ((g is not None and g >= 5.6) or (dm and dm.value is not None and dm.value >= 6)):
        out.append({"id": "confirm_glucose", "text": "ตรวจน้ำตาลขณะอดอาหาร (FPG) หรือ HbA1c เพื่อยืนยันภาวะก่อนเบาหวาน",
                    "fact_ids": ["ADA-2026-DX", "TDRS-2006"]})
    if any(f.id == "glyca_high" for f in factors):
        out.append({"id": "recheck_inflammation", "text": "ตรวจค่าการอักเสบซ้ำในช่วงที่ไม่ได้ป่วยหรือติดเชื้อ ก่อนแปลผล",
                    "fact_ids": ["GLYCA-CVD"]})
    if any(m.pdc_pct is not None and m.pdc_pct < 80 for m in medications):
        out.append({"id": "adherence_talk", "text": "คุยกับเภสัชกรเรื่องการกินยาให้สม่ำเสมอ (มียาที่กินไม่ถึง 80% ของวัน)",
                    "fact_ids": ["PQA-PDC80"]})
    return out


def assess(req: AssessIn) -> dict:
    visits = req.visits
    cur = visits[-1].values
    prev = visits[-2].values if len(visits) > 1 else None

    p = Profile(**req.profile.model_dump())
    if cur.get("total_c"):
        p.total_chol_mg_dl = cur["total_c"] * MMOL_TO_MG_DL_CHOL

    cv = thai_cv_risk(p)
    medications = [m.Medication(x.drug, x.dose_mg, x.pdc_pct, x.start_visit) for x in req.meds]
    if cv.value is not None and any(x.key in m.STATINS for x in medications):
        cv.notes.append("คำนวณจาก total cholesterol ระหว่างใช้ statin — ความเสี่ยงก่อนรักษาจะสูงกว่านี้")
    risks = [cv, thai_diabetes_risk(p)]

    findings = m.pgx_findings(medications, req.pgx) + m.ddi_findings(medications)
    now_idx = len(visits) - 1
    for med in medications:
        if med.key not in m.STATINS:
            continue
        s = med.start_visit
        if s is not None and 1 <= s <= now_idx:
            findings += m.statin_response(med, visits[s - 1].values.get("ldl_c"), cur.get("ldl_c"))
        if (s is None or s <= now_idx) and cur.get("ldl_c") is not None:
            t = ldl_target_finding(med, cur["ldl_c"], cv.value)
            if t:
                findings.append(t)
    findings += m.adherence_findings(medications, {f.id for f in findings})
    findings = m.sort_findings(findings)

    factors = nmr_factors(cur, cv.value, p.diabetes)
    high_risk = p.diabetes or (cv.value is not None and cv.value >= 20)
    summary = summarize(cur, prev, diabetes=p.diabetes, high_risk=high_risk, drugs=[x.key for x in medications])
    advice = lifestyle_advice(p, cur, req.alcohol_drinks_per_day, req.activity_min_week)
    follow_up = next_steps(medications, cur, risks, factors, p.diabetes)
    trend_rows = trend(prev, cur) if prev else []

    cat = catalog()
    panel = [{"id": k, "value": v, "status": status(k, v), "previous": (prev or {}).get(k)}
             for k, v in cur.items() if k in cat]

    used = {"UKB-NMR-REF"}
    for group in (risks, findings, factors, advice):
        for x in group:
            used.update(x.fact_ids)
    for x in follow_up:
        used.update(x["fact_ids"])
    for d in summary:
        used.update(d["fact_ids"])
    if trend_rows:
        used.update({"RCV-METHOD", "EFLM-CVI", "NIGHTINGALE-CVA"})
    store = facts()
    return {
        "snapshot": store["snapshot"],
        "panel": panel,
        "nmr_summary": summary,
        "risks": [asdict(r) for r in risks],
        "nmr_factors": [asdict(f) for f in factors],
        "findings": [asdict(f) for f in findings],
        "advice": [asdict(a) for a in advice],
        "follow_up": follow_up,
        "trend": [asdict(t) for t in trend_rows],
        "facts": {k: store["facts"][k] for k in sorted(used) if k in store["facts"]},
        "missing_facts": sorted(k for k in used if k not in store["facts"]),
    }
