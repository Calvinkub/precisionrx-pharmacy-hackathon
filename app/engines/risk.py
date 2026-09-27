"""Validated Thai risk scores. No home-made risk models (idea.md §5, critique §4).

- Thai CV Risk Score 2.5 (Rama-EGAT), equations copied from the official Ramathibodi
  calculator script (formular.js, 2021). Fact: TCVRS-2021.
- Thai diabetes risk score (Aekplakorn et al., Diabetes Care 2006). Fact: TDRS-2006.
See docs/research_risk_lifestyle.md for sources.
"""

from dataclasses import dataclass, field
from math import exp

TCVRS_S0 = 0.964588  # official calculator; MOPH/HDC spec uses 0.978296


@dataclass
class Profile:
    age: int
    sex: str  # "male" | "female"
    sbp: float | None = None
    smoker: bool = False
    diabetes: bool = False
    hypertension: bool = False
    family_history_dm: bool = False
    total_chol_mg_dl: float | None = None
    weight_kg: float | None = None
    height_cm: float | None = None
    waist_cm: float | None = None

    @property
    def male(self) -> int:
        return 1 if self.sex == "male" else 0

    @property
    def bmi(self) -> float | None:
        if self.weight_kg and self.height_cm:
            return self.weight_kg / (self.height_cm / 100) ** 2
        return None


@dataclass
class RiskResult:
    id: str
    disease: str
    score_name: str
    value: float | None
    display: str
    category: str  # low | moderate | high | very_high | not_assessable
    method: str
    fact_ids: list[str]
    notes: list[str] = field(default_factory=list)


def _tcvrs_category(risk: float) -> str:
    if risk < 10:
        return "low"
    if risk < 20:
        return "moderate"
    if risk <= 30:
        return "high"
    return "very_high"


def thai_cv_risk(p: Profile) -> RiskResult:
    notes = []
    if p.sbp is None:
        return RiskResult("cvd", "โรคหัวใจและหลอดเลือด (10 ปี)", "Thai CV Risk Score", None,
                          "ต้องมีความดันตัวบน (SBP)", "not_assessable", "-", ["TCVRS-2021"])
    if not 30 <= p.age <= 70:
        notes.append("อายุอยู่นอกช่วงที่สูตรรองรับ (30–70 ปี) ตีความด้วยความระวัง")

    smoke, dm, sex = int(p.smoker), int(p.diabetes), p.male
    if p.total_chol_mg_dl:
        score = (0.08183 * p.age + 0.39499 * sex + 0.02084 * p.sbp + 0.69974 * dm
                 + 0.00212 * p.total_chol_mg_dl + 0.41916 * smoke) - 7.04423
        method = "สูตรใช้ total cholesterol"
    elif p.waist_cm and p.height_cm:
        score = (0.079 * p.age + 0.128 * sex + 0.019350987 * p.sbp + 0.58454 * dm
                 + 3.512566 * (p.waist_cm / p.height_cm) + 0.459 * smoke) - 7.712325
        method = "สูตรไม่ใช้ผลเลือด (รอบเอว/ส่วนสูง)"
    elif p.waist_cm:
        score = (0.08372 * p.age + 0.05988 * sex + 0.02034 * p.sbp + 0.59953 * dm
                 + 0.01283 * p.waist_cm + 0.459 * smoke) - 7.31047
        method = "สูตรไม่ใช้ผลเลือด (รอบเอว)"
    else:
        return RiskResult("cvd", "โรคหัวใจและหลอดเลือด (10 ปี)", "Thai CV Risk Score", None,
                          "ต้องมี total cholesterol หรือรอบเอว", "not_assessable", "-", ["TCVRS-2021"])

    risk = (1 - TCVRS_S0 ** exp(score)) * 100
    display = "> 30%" if risk > 30 else f"{risk:.1f}%"
    return RiskResult("cvd", "โรคหัวใจและหลอดเลือด (10 ปี)", "Thai CV Risk Score", round(risk, 2),
                      display, _tcvrs_category(risk), method, ["TCVRS-2021"], notes)


def thai_diabetes_risk(p: Profile) -> RiskResult:
    name = ("dm", "เบาหวานชนิดที่ 2 (12 ปี)", "Thai Diabetes Risk Score")
    if p.diabetes:
        return RiskResult(*name, None, "เป็นเบาหวานแล้ว — ไม่ใช้คะแนนคัดกรอง", "not_assessable",
                          "-", ["TDRS-2006"])
    if p.bmi is None or p.waist_cm is None:
        return RiskResult(*name, None, "ต้องมีน้ำหนัก ส่วนสูง และรอบเอว", "not_assessable",
                          "-", ["TDRS-2006"])
    notes = []
    if not 35 <= p.age <= 55:
        notes.append("คะแนนพัฒนาจากกลุ่มอายุ 35–55 ปี")

    pts = 2 if p.age >= 50 else 1 if p.age >= 45 else 0
    pts += 2 if p.male else 0
    pts += 5 if p.bmi >= 27.5 else 3 if p.bmi >= 23 else 0
    pts += 2 if p.waist_cm >= (90 if p.male else 80) else 0
    pts += 2 if p.hypertension else 0
    pts += 4 if p.family_history_dm else 0

    if pts <= 2:
        cat, band = "low", "< 5%"
    elif pts <= 5:
        cat, band = "moderate", "5–10%"
    elif pts <= 8:
        cat, band = "high", "11–20%"
    else:
        cat, band = "very_high", "> 20%"
    if pts >= 6:
        notes.append("คะแนน ≥ 6: ควรตรวจน้ำตาลในเลือด")
    return RiskResult(*name, pts, f"{pts}/17 คะแนน (โอกาส {band})", cat, "ตารางคะแนน", ["TDRS-2006"], notes)
