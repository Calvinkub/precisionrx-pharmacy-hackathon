"""NMR 'additional factors'. Shown next to the validated risk scores, never merged into them.

Most of these are association-level evidence (level: emerging) from European/US cohorts.
"""

from dataclasses import dataclass

from app.engines.panel import catalog

MMOL_TO_MG_DL_CHOL = 38.67


@dataclass
class NmrFactor:
    id: str
    title: str
    detail: str
    severity: str  # monitor | info
    level: str  # guideline | emerging
    fact_ids: list[str]


def nmr_factors(v: dict[str, float], cv_risk_pct: float | None, diabetes: bool) -> list[NmrFactor]:
    out = []
    cat = catalog()

    ldl, apob, ldl_p = v.get("ldl_c"), v.get("apob"), v.get("ldl_p")
    # Moderate-risk ESC secondary target (<100 mg/dL); tighter if Thai CV risk ≥ 20% or diabetes
    high_risk = diabetes or (cv_risk_pct is not None and cv_risk_pct >= 20)
    apob_target = 0.80 if high_risk else 1.00  # g/L
    ldl_target = 1.8 if high_risk else 2.6  # mmol/L
    if ldl is not None and apob is not None and ldl < ldl_target and apob >= apob_target:
        out.append(NmrFactor(
            "apob_discordance", "LDL-C ถึงเป้า แต่ ApoB ยังเกินเป้ารอง",
            f"LDL-C {ldl:.2f} mmol/L ({ldl * MMOL_TO_MG_DL_CHOL:.0f} mg/dL) < {ldl_target} แต่ ApoB "
            f"{apob * 100:.0f} mg/dL ≥ {apob_target * 100:.0f} mg/dL — มีอนุภาคที่ก่อหลอดเลือดแข็งเหลืออยู่ (residual risk)",
            "monitor", "guideline", ["ESC-2019-APOB"]))

    if ldl is not None and ldl_p is not None and ldl <= cat["ldl_c"]["ref_high"] and ldl_p > cat["ldl_p"]["ref_high"]:
        out.append(NmrFactor(
            "ldlp_discordance", "จำนวนอนุภาค LDL สูงกว่าที่ LDL-C บอก",
            f"LDL-P {ldl_p:.0f} nmol/L > P90 ประชากร ({cat['ldl_p']['ref_high']:.0f}) ขณะที่ LDL-C อยู่ในช่วง",
            "monitor", "emerging", ["OTVOS-2011-DISCORDANCE", "UKB-NMR-REF"]))

    glyca = v.get("glyca")
    if glyca is not None and glyca > cat["glyca"]["ref_high"]:
        out.append(NmrFactor(
            "glyca_high", "GlycA สูง — สัญญาณการอักเสบเรื้อรัง",
            f"GlycA {glyca:.2f} mmol/L > P90 ({cat['glyca']['ref_high']}) · ไม่เป็นอิสระจาก hsCRP "
            "และขึ้นได้จากการติดเชื้อเฉียบพลัน — ตรวจซ้ำก่อนแปลผล",
            "monitor", "emerging", ["GLYCA-CVD", "UKB-NMR-REF"]))

    bcaa = v.get("bcaa")
    if bcaa is not None and bcaa > cat["bcaa"]["ref_high"] and not diabetes:
        out.append(NmrFactor(
            "bcaa_high", "BCAA สูง — สัมพันธ์กับความเสี่ยงเบาหวาน",
            f"BCAA {bcaa:.0f} µmol/L > P90 ({cat['bcaa']['ref_high']:.0f}) · ใช้ประกอบ ไม่ใช่การวินิจฉัย ยืนยันด้วย FPG/HbA1c",
            "monitor", "emerging", ["BCAA-T2D", "UKB-NMR-REF"]))

    o3 = v.get("omega3_pct")
    if o3 is not None and o3 < cat["omega3_pct"]["ref_low"]:
        out.append(NmrFactor(
            "omega3_low", "Omega-3 ต่ำ",
            f"Omega-3 {o3:.1f}% < P10 ({cat['omega3_pct']['ref_low']}%) · พิจารณาเพิ่มปลาในอาหาร",
            "info", "emerging", ["OMEGA3-CVD", "UKB-NMR-REF"]))
    return out
