"""Tier 3 clinical calculators + Tier 4 explanation.

Every score is a published formula — no trained model. Explanations are EXACT, not approximated:
  - Thai CV Risk: log-hazard terms relative to the calculator's own reference person
    (same age/sex, SBP 120, TC 200 mg/dL, no diabetes, non-smoker); Shapley values of a linear
    predictor against a fixed baseline equal these terms.
  - Thai Diabetes Score / metabolic syndrome: points / criteria met (additive by design).
  - Fatty Liver Index: logit terms relative to a stated lean reference.
  - eGFR / FIB-4: shown as the formula inputs (a ratio/power formula, not additive).
Uncertainty: Monte Carlo over analytical + within-person variation (CVa, CVi) of the lab inputs.
"""

import math
import random
from dataclasses import asdict, dataclass, field

MG_DL_TC = 38.67
MG_DL_TG = 88.57


@dataclass
class Contribution:
    feature: str
    label: str
    value: float | str | None
    unit: str
    contribution: float  # additive in the score's own scale (log-hazard, points, logit, criteria)
    direction: str  # up | down | none
    note: str = ""
    source: dict | None = None  # provenance of the input (document + locator)


@dataclass
class ScoreResult:
    id: str
    disease: str
    method: str
    value: float | None
    display: str
    unit: str
    category: str  # low | moderate | high | very_high | not_assessable | ...
    category_label: str
    scale: str  # what contributions are measured in
    baseline: float | None = None  # score of the reference person, same unit as value
    contributions: list[Contribution] = field(default_factory=list)
    interval: tuple[float, float] | None = None  # 95% interval from input variability
    fact_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["interval"] = list(self.interval) if self.interval else None
        return d


def _dir(x: float) -> str:
    return "up" if x > 1e-9 else "down" if x < -1e-9 else "none"


def _mc(fn, inputs: dict[str, tuple[float, float]], n: int = 2000, seed: int = 7) -> tuple[float, float] | None:
    """95% interval of fn(**sampled) when each input varies with total CV% (log-normal-ish, truncated at 0)."""
    if not inputs:
        return None
    rnd = random.Random(seed)
    vals = []
    for _ in range(n):
        s = {k: max(1e-6, v * (1 + rnd.gauss(0, cv / 100))) for k, (v, cv) in inputs.items()}
        r = fn(**s)
        if r is not None:
            vals.append(r)
    if not vals:
        return None
    vals.sort()
    return round(vals[int(0.025 * len(vals))], 2), round(vals[int(0.975 * len(vals)) - 1], 2)


# ---------------------------------------------------------------- Thai CV Risk (explained)
S0 = 0.964588
TC_COEF = {"age": 0.08183, "sex": 0.39499, "sbp": 0.02084, "dm": 0.69974, "tc": 0.00212, "smoke": 0.41916, "c": 7.04423}


def _tcvrs(age, male, sbp, dm, tc, smoke):
    lp = (TC_COEF["age"] * age + TC_COEF["sex"] * male + TC_COEF["sbp"] * sbp + TC_COEF["dm"] * dm
          + TC_COEF["tc"] * tc + TC_COEF["smoke"] * smoke) - TC_COEF["c"]
    return (1 - S0 ** math.exp(lp)) * 100


def thai_cv_risk(age, male: bool, sbp, diabetes: bool, tc_mg_dl, smoker: bool, cv_tc=None, sources=None) -> ScoreResult:
    sources = sources or {}
    if None in (age, sbp, tc_mg_dl):
        return ScoreResult("cvd", "โรคหัวใจและหลอดเลือด", "Thai CV Risk Score (TC)", None, "–", "% ใน 10 ปี",
                           "not_assessable", "ข้อมูลไม่พอ", "log-hazard", missing=[k for k, v in {"age": age, "sbp": sbp, "total_c": tc_mg_dl}.items() if v is None],
                           fact_ids=["TCVRS-2021"])
    ref = {"sbp": 132 if (male and age > 60) else 120 if male else 130 if age > 60 else 115, "tc": 200, "dm": 0, "smoke": 0}
    risk = _tcvrs(age, int(male), sbp, int(diabetes), tc_mg_dl, int(smoker))
    base = _tcvrs(age, int(male), ref["sbp"], 0, ref["tc"], 0)
    contribs = [
        Contribution("sbp", "ความดันตัวบน", sbp, "mmHg", TC_COEF["sbp"] * (sbp - ref["sbp"]), _dir(sbp - ref["sbp"]), f"อ้างอิง {ref['sbp']}", sources.get("sbp")),
        Contribution("total_c", "Total cholesterol", round(tc_mg_dl), "mg/dL", TC_COEF["tc"] * (tc_mg_dl - ref["tc"]), _dir(tc_mg_dl - ref["tc"]), "อ้างอิง 200", sources.get("total_c")),
        Contribution("diabetes", "เบาหวาน", "มี" if diabetes else "ไม่มี", "", TC_COEF["dm"] * int(diabetes), _dir(int(diabetes)), "", sources.get("diabetes")),
        Contribution("smoker", "สูบบุหรี่", "สูบ" if smoker else "ไม่สูบ", "", TC_COEF["smoke"] * int(smoker), _dir(int(smoker)), "", sources.get("smoker")),
    ]
    cat = "low" if risk < 10 else "moderate" if risk < 20 else "high" if risk <= 30 else "very_high"
    interval = _mc(lambda tc: _tcvrs(age, int(male), sbp, int(diabetes), tc, int(smoker)), {"tc": (tc_mg_dl, cv_tc)}) if cv_tc else None
    return ScoreResult("cvd", "โรคหัวใจและหลอดเลือด", "Thai CV Risk Score (TC)", round(risk, 2),
                       "> 30%" if risk > 30 else f"{risk:.1f}%", "% ใน 10 ปี", cat,
                       {"low": "ต่ำ", "moderate": "ปานกลาง", "high": "สูง", "very_high": "สูงมาก"}[cat], "log-hazard",
                       round(base, 2), contribs, interval, ["TCVRS-2021"],
                       [f"เทียบกับคนอายุและเพศเดียวกันที่ SBP {ref['sbp']}, TC 200, ไม่เป็นเบาหวาน, ไม่สูบบุหรี่ ({base:.1f}%)"])


# ---------------------------------------------------------------- Thai diabetes risk score (points)
def thai_diabetes_score(age, male: bool, bmi, waist, hypertension: bool, family_dm: bool, diabetes: bool, sources=None) -> ScoreResult:
    sources = sources or {}
    if diabetes:
        return ScoreResult("dm", "เบาหวานชนิดที่ 2", "Thai Diabetes Risk Score", None, "เป็นเบาหวานแล้ว", "คะแนน /17",
                           "not_applicable", "เป็นเบาหวานแล้ว", "points", fact_ids=["TDRS-2006"])
    if None in (age, bmi, waist):
        return ScoreResult("dm", "เบาหวานชนิดที่ 2", "Thai Diabetes Risk Score", None, "–", "คะแนน /17", "not_assessable",
                           "ข้อมูลไม่พอ", "points", missing=[k for k, v in {"age": age, "bmi": bmi, "waist_cm": waist}.items() if v is None], fact_ids=["TDRS-2006"])
    pts = [
        Contribution("age", "อายุ", age, "ปี", 2 if age >= 50 else 1 if age >= 45 else 0, "", "", sources.get("age")),
        Contribution("sex", "เพศชาย", "ชาย" if male else "หญิง", "", 2 if male else 0, ""),
        Contribution("bmi", "ดัชนีมวลกาย", round(bmi, 1), "kg/m²", 5 if bmi >= 27.5 else 3 if bmi >= 23 else 0, "", "", sources.get("bmi")),
        Contribution("waist", "รอบเอว", waist, "cm", 2 if waist >= (90 if male else 80) else 0, "", f"เกณฑ์ {90 if male else 80}", sources.get("waist_cm")),
        Contribution("hypertension", "ความดันโลหิตสูง", "มี" if hypertension else "ไม่มี", "", 2 if hypertension else 0, ""),
        Contribution("family_dm", "พ่อแม่/พี่น้องเป็นเบาหวาน", "มี" if family_dm else "ไม่มี", "", 4 if family_dm else 0, ""),
    ]
    for c in pts:
        c.direction = _dir(c.contribution)
    total = sum(c.contribution for c in pts)
    cat, band = ("low", "< 5%") if total <= 2 else ("moderate", "5–10%") if total <= 5 else ("high", "11–20%") if total <= 8 else ("very_high", "> 20%")
    return ScoreResult("dm", "เบาหวานชนิดที่ 2", "Thai Diabetes Risk Score", total, f"{total}/17", "คะแนน /17 (โอกาส 12 ปี)", cat,
                       {"low": "ต่ำ", "moderate": "ปานกลาง", "high": "สูง", "very_high": "สูงมาก"}[cat], "points", 0, pts, None,
                       ["TDRS-2006"], [f"โอกาสเป็นเบาหวานใน 12 ปี {band}", "AUC 0.74 ในกลุ่มพัฒนาสูตร"])


# ---------------------------------------------------------------- Metabolic syndrome (harmonized 2009)
def metabolic_syndrome(male: bool, waist, tg_mmol, hdl_mmol, sbp, dbp, glucose_mmol, on_lipid_drug=False,
                       on_bp_drug=False, on_glucose_drug=False, sources=None) -> ScoreResult:
    sources = sources or {}
    need = {"waist_cm": waist, "tg": tg_mmol, "hdl_c": hdl_mmol, "sbp": sbp, "glucose": glucose_mmol}
    missing = [k for k, v in need.items() if v is None]
    crit = []
    def add(feature, label, value, unit, met, rule):
        crit.append(Contribution(feature, label, value, unit, 1 if met else 0, "up" if met else "none", rule, sources.get(feature)))
    if waist is not None:
        add("waist_cm", "รอบเอว", waist, "cm", waist >= (90 if male else 80), f"≥ {90 if male else 80} ซม. (เกณฑ์เอเชีย)")
    if tg_mmol is not None:
        add("tg", "ไตรกลีเซอไรด์", round(tg_mmol * MG_DL_TG), "mg/dL", tg_mmol >= 1.7 or on_lipid_drug, "≥ 150 mg/dL หรือใช้ยา")
    if hdl_mmol is not None:
        add("hdl_c", "HDL-C", round(hdl_mmol * MG_DL_TC), "mg/dL", hdl_mmol < (1.0 if male else 1.3), f"< {40 if male else 50} mg/dL")
    if sbp is not None:
        add("sbp", "ความดัน", f"{sbp:g}/{dbp:g}" if dbp else sbp, "mmHg", sbp >= 130 or (dbp or 0) >= 85 or on_bp_drug, "≥ 130/85 หรือใช้ยาลดความดัน")
    if glucose_mmol is not None:
        add("glucose", "น้ำตาลขณะอดอาหาร", round(glucose_mmol * 18.016), "mg/dL", glucose_mmol >= 5.6 or on_glucose_drug, "≥ 100 mg/dL หรือใช้ยา")
    met = sum(c.contribution for c in crit)
    if missing and met < 3:
        return ScoreResult("mets", "กลุ่มอาการเมตาบอลิก", "Harmonized criteria (2009)", met, f"{met}/5 (ข้อมูลไม่ครบ)", "เกณฑ์ที่เข้า /5",
                           "not_assessable", "ข้อมูลไม่พอ", "criteria", 0, crit, None, ["METS-HARMONIZED-2009"], missing=missing)
    cat = "present" if met >= 3 else "at_risk" if met == 2 else "absent"
    return ScoreResult("mets", "กลุ่มอาการเมตาบอลิก", "Harmonized criteria (2009)", met, f"{met}/5 เกณฑ์", "เกณฑ์ที่เข้า /5", cat,
                       {"present": "เข้าเกณฑ์", "at_risk": "ใกล้เกณฑ์", "absent": "ไม่เข้าเกณฑ์"}[cat], "criteria", 0, crit, None,
                       ["METS-HARMONIZED-2009"], ["เข้าเกณฑ์เมื่อมีอย่างน้อย 3 ใน 5 ข้อ"])


# ---------------------------------------------------------------- CKD (CKD-EPI 2021 + KDIGO)
def egfr_ckd_epi_2021(scr_mg_dl, age, male: bool):
    k, a = (0.9, -0.302) if male else (0.7, -0.241)
    return 142 * min(scr_mg_dl / k, 1) ** a * max(scr_mg_dl / k, 1) ** -1.200 * 0.9938 ** age * (1 if male else 1.012)


def ckd(scr_mg_dl, age, male: bool, uacr=None, cv_scr=None, sources=None) -> ScoreResult:
    sources = sources or {}
    if scr_mg_dl is None or age is None:
        return ScoreResult("ckd", "โรคไตเรื้อรัง", "eGFR CKD-EPI 2021 + KDIGO", None, "–", "mL/min/1.73m²", "not_assessable", "ข้อมูลไม่พอ",
                           "inputs", missing=["creatinine"], fact_ids=["CKD-EPI-2021", "KDIGO-2024"])
    e = egfr_ckd_epi_2021(scr_mg_dl, age, male)
    g = "G1" if e >= 90 else "G2" if e >= 60 else "G3a" if e >= 45 else "G3b" if e >= 30 else "G4" if e >= 15 else "G5"
    a = None if uacr is None else "A1" if uacr < 30 else "A2" if uacr <= 300 else "A3"
    # KDIGO heat map (low / moderate / high / very high)
    heat = {"G1": ["low", "moderate", "high"], "G2": ["low", "moderate", "high"], "G3a": ["moderate", "high", "very_high"],
            "G3b": ["high", "very_high", "very_high"], "G4": ["very_high"] * 3, "G5": ["very_high"] * 3}
    cat = heat[g][{"A1": 0, "A2": 1, "A3": 2}[a]] if a else ("low" if g in ("G1", "G2") else heat[g][0])
    contribs = [Contribution("creatinine", "Creatinine", scr_mg_dl, "mg/dL", 0, "none", "ใช้ในสมการ eGFR", sources.get("creatinine")),
                Contribution("age", "อายุ", age, "ปี", 0, "none", "ใช้ในสมการ eGFR")]
    if uacr is not None:
        contribs.append(Contribution("uacr", "Albumin/creatinine ratio", uacr, "mg/g", 0, "up" if uacr >= 30 else "none", a or "", sources.get("uacr")))
    notes = ["การวินิจฉัย CKD ต้องมีความผิดปกตินานกว่า 3 เดือน — ตรวจยืนยันซ้ำ"]
    if a is None:
        notes.append("ยังไม่มีผล UACR — ประเมินได้แค่ครึ่งเดียวของ KDIGO")
    interval = _mc(lambda s: egfr_ckd_epi_2021(s, age, male), {"s": (scr_mg_dl, cv_scr)}) if cv_scr else None
    label = {"low": "ต่ำ", "moderate": "ปานกลาง", "high": "สูง", "very_high": "สูงมาก"}[cat]
    return ScoreResult("ckd", "โรคไตเรื้อรัง", "eGFR CKD-EPI 2021 + KDIGO", round(e, 1), f"{e:.0f} ({g}{'/' + a if a else ''})",
                       "mL/min/1.73m²", cat, label, "inputs", None, contribs, interval, ["CKD-EPI-2021", "KDIGO-2024"], notes)


# ---------------------------------------------------------------- MASLD / NAFLD: FLI (steatosis) + FIB-4 (fibrosis)
FLI_REF = {"tg": 100.0, "bmi": 22.0, "ggt": 20.0, "waist": 80.0}


def fli(tg_mg_dl, bmi, ggt, waist):
    y = 0.953 * math.log(tg_mg_dl) + 0.139 * bmi + 0.718 * math.log(ggt) + 0.053 * waist - 15.745
    return math.exp(y) / (1 + math.exp(y)) * 100


def fib4(age, ast, alt, plt):
    return age * ast / (plt * math.sqrt(alt))


def liver(tg_mmol, bmi, ggt, waist, age, ast, alt, plt, cv_tg=None, sources=None) -> ScoreResult:
    sources = sources or {}
    notes, contribs, facts = [], [], ["FLI-2006", "FIB4-MASLD"]
    f = fl = None
    if None not in (tg_mmol, bmi, ggt, waist):
        tg = tg_mmol * MG_DL_TG
        fl = fli(tg, bmi, ggt, waist)
        terms = {"tg": 0.953 * (math.log(tg) - math.log(FLI_REF["tg"])), "bmi": 0.139 * (bmi - FLI_REF["bmi"]),
                 "ggt": 0.718 * (math.log(ggt) - math.log(FLI_REF["ggt"])), "waist": 0.053 * (waist - FLI_REF["waist"])}
        contribs += [Contribution("tg", "ไตรกลีเซอไรด์", round(tg), "mg/dL", terms["tg"], _dir(terms["tg"]), "อ้างอิง 100", sources.get("tg")),
                     Contribution("bmi", "ดัชนีมวลกาย", round(bmi, 1), "kg/m²", terms["bmi"], _dir(terms["bmi"]), "อ้างอิง 22", sources.get("bmi")),
                     Contribution("ggt", "GGT", ggt, "U/L", terms["ggt"], _dir(terms["ggt"]), "อ้างอิง 20", sources.get("ggt")),
                     Contribution("waist", "รอบเอว", waist, "cm", terms["waist"], _dir(terms["waist"]), "อ้างอิง 80", sources.get("waist_cm"))]
    if None not in (age, ast, alt, plt):
        f = fib4(age, ast, alt, plt)
        hi_cut = 2.67
        lo_cut = 2.0 if age > 65 else 1.3
        notes.append(f"FIB-4 {f:.2f}: " + ("พังผืดน้อย" if f < lo_cut else "ตรวจเพิ่ม (elastography)" if f <= hi_cut else "เสี่ยงพังผืดสูง ส่งต่อแพทย์ตับ"))
        contribs.append(Contribution("fib4", "FIB-4 (อายุ, AST, ALT, เกล็ดเลือด)", round(f, 2), "", 0, "up" if f >= lo_cut else "none",
                                     f"< {lo_cut} ต่ำ · > {hi_cut} สูง", sources.get("ast")))
    if fl is None and f is None:
        return ScoreResult("masld", "ไขมันพอกตับ (MASLD)", "Fatty Liver Index + FIB-4", None, "–", "", "not_assessable", "ข้อมูลไม่พอ",
                           "logit", missing=["tg/bmi/ggt/waist", "ast/alt/platelets"], fact_ids=facts)
    if f is not None and f > 2.67:
        cat = "very_high"
    elif f is not None and f >= (2.0 if age > 65 else 1.3):
        cat = "high"
    elif fl is not None and fl >= 60:
        cat = "moderate"
    else:
        cat = "low"
    label = {"low": "ต่ำ", "moderate": "มีไขมันพอกตับ", "high": "ต้องตรวจพังผืดเพิ่ม", "very_high": "เสี่ยงพังผืดสูง"}[cat]
    if fl is not None:
        notes.insert(0, f"FLI {fl:.0f}: " + ("ไม่น่ามีไขมันพอกตับ" if fl < 30 else "ไขมันพอกตับน่าจะมี" if fl >= 60 else "ก้ำกึ่ง"))
    interval = _mc(lambda tg: fli(tg, bmi, ggt, waist), {"tg": (tg_mmol * MG_DL_TG, cv_tg)}) if (cv_tg and fl is not None) else None
    base = fli(FLI_REF["tg"], FLI_REF["bmi"], FLI_REF["ggt"], FLI_REF["waist"]) if fl is not None else None
    return ScoreResult("masld", "ไขมันพอกตับ (MASLD)", "Fatty Liver Index + FIB-4", None if fl is None else round(fl, 1),
                       f"FLI {fl:.0f}" if fl is not None else f"FIB-4 {f:.2f}", "FLI 0–100", cat, label, "logit",
                       None if base is None else round(base, 1), contribs, interval, facts, notes)
