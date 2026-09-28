"""Compute the consumer app's numbers from the validated engines (no hand-typed risks).

    uv run python -m scripts.build_consumer_data     # writes web/src/data/computed.json
"""

import json
from pathlib import Path

from app.engines import calculators as C
from app.engines.panel import facts

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "web" / "src" / "data" / "mockPatient.json"
OUT = ROOT / "web" / "src" / "data" / "computed.json"


def build() -> dict:
    m = json.loads(SRC.read_text(encoding="utf-8"))
    p, L = m["profile"], m["labs"]
    male = p["sex"] == "male"
    bmi = p["weight_kg"] / (p["height_cm"] / 100) ** 2
    glucose = L["glucose_mg_dl"] / 18.016
    tg = L["tg_mg_dl"] / 88.57
    hdl = L["hdl_mg_dl"] / 38.67
    family_dm = any("เบาหวาน" in f["condition"] for f in p["family_history"])

    # Thai CV Risk, non-lab version (waist/height) — no total cholesterol in this profile
    from app.engines.risk import Profile, thai_cv_risk
    cv = thai_cv_risk(Profile(age=p["age"], sex=p["sex"], sbp=p["sbp"], smoker=p["smoking"] == "current",
                              diabetes=False, waist_cm=p["waist_cm"], height_cm=p["height_cm"]))
    dm = C.thai_diabetes_score(p["age"], male, bmi, p["waist_cm"], False, family_dm, False)
    mets = C.metabolic_syndrome(male, p["waist_cm"], tg, hdl, p["sbp"], p["dbp"], glucose)
    liver = C.liver(tg, bmi, L["ggt"], p["waist_cm"], p["age"], L["ast"], L["alt"], L["platelets"])
    prediabetes = 5.7 <= L["hba1c_pct"] < 6.5 or 5.6 <= glucose < 7.0

    nmr_high = [k for k, v in m["nmr"].items() if v["value"] > v["high_above"]]
    bcaa_high = [k for k in ("valine", "isoleucine", "leucine") if k in nmr_high]
    used = {"TCVRS-2021", "TDRS-2006", "METS-HARMONIZED-2009", "FLI-2006", "FIB4-MASLD", "ADA-2026-DX", "BCAA-T2D",
            "WHO-PA-2020", "ADA-2026-PREV", "RCPT-2024-DIET", "RCPT-2024-TG", "THAI-HT-2024-NA", "THAI-OBESITY",
            "CFDNA-FRAGMENTOMICS-SEQ", "OTVOS-2011-DISCORDANCE", "RCPT-2024-SMOKING", "WHO-2005-PREVENTABLE",
            "ESC-2021-DIET", "WHO-SEDENTARY-2020", "RCPT-2024-FOLLOWUP"}
    store = facts()["facts"]
    return {
        "bmi": round(bmi, 1),
        "prediabetes": prediabetes,
        "risks": {
            "diabetes": {"method": dm.method, "value": dm.value, "display": dm.display, "category": dm.category, "label": dm.category_label,
                         "band": dm.notes[0], "contributions": [{"label": c.label, "points": c.contribution} for c in dm.contributions if c.contribution],
                         "fact_ids": ["TDRS-2006"]},
            "cvd": {"method": f"{cv.score_name} ({cv.method})", "value": cv.value, "display": cv.display, "category": cv.category,
                    "label": {"low": "ต่ำ", "moderate": "ปานกลาง", "high": "สูง", "very_high": "สูงมาก"}.get(cv.category, "–"), "fact_ids": ["TCVRS-2021"]},
            "liver": {"method": liver.method, "fli": liver.value, "category": liver.category, "label": liver.category_label, "notes": liver.notes,
                      "fact_ids": ["FLI-2006", "FIB4-MASLD"]},
            "mets": {"met": mets.value, "category": mets.category, "label": mets.category_label,
                     "criteria": [{"label": c.label, "value": c.value, "unit": c.unit, "met": bool(c.contribution), "rule": c.note} for c in mets.contributions],
                     "fact_ids": ["METS-HARMONIZED-2009"]},
        },
        "nmr_high": nmr_high,
        "insulin_resistance_pattern": bool(bcaa_high) and prediabetes,
        "bcaa_high": bcaa_high,
        "facts": {k: store[k] for k in sorted(used) if k in store},
    }


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", OUT)
