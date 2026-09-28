"""Compute the consumer app's numbers from the validated engines (no hand-typed risks).

    uv run python -m scripts.build_consumer_data     # writes web/src/data/computed.json
"""

import json
import math
from pathlib import Path

from app.engines import calculators as C
from app.engines.cfdna_run import summarize_run
from app.engines.panel import facts
from app.engines.risk import Profile, thai_cv_risk

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
    cv = thai_cv_risk(Profile(age=p["age"], sex=p["sex"], sbp=p["sbp"], smoker=p["smoking"] == "current",
                              diabetes=False, waist_cm=p["waist_cm"], height_cm=p["height_cm"]))
    # reference person for the explanation: same age/sex, SBP 120, waist = half the height, non-smoker
    cv_ref = thai_cv_risk(Profile(age=p["age"], sex=p["sex"], sbp=120, waist_cm=p["height_cm"] / 2, height_cm=p["height_cm"]))
    dm = C.thai_diabetes_score(p["age"], male, bmi, p["waist_cm"], False, family_dm, False)
    mets = C.metabolic_syndrome(male, p["waist_cm"], tg, hdl, p["sbp"], p["dbp"], glucose)
    liver = C.liver(tg, bmi, L["ggt"], p["waist_cm"], p["age"], L["ast"], L["alt"], L["platelets"])
    prediabetes = 5.7 <= L["hba1c_pct"] < 6.5 or 5.6 <= glucose < 7.0

    nmr_high = [k for k, v in m["nmr"].items() if v["value"] > v["high_above"]]
    bcaa_high = [k for k in ("valine", "isoleucine", "leucine") if k in nmr_high]
    used = {"TCVRS-2021", "TDRS-2006", "METS-HARMONIZED-2009", "FLI-2006", "FIB4-MASLD", "ADA-2026-DX", "BCAA-T2D",
            "WHO-PA-2020", "ADA-2026-PREV", "RCPT-2024-DIET", "RCPT-2024-TG", "THAI-HT-2024-NA", "THAI-OBESITY",
            "CFDNA-FRAGMENTOMICS-SEQ", "OTVOS-2011-DISCORDANCE", "RCPT-2024-SMOKING", "WHO-2005-PREVENTABLE",
            "ESC-2021-DIET", "WHO-SEDENTARY-2020", "RCPT-2024-FOLLOWUP", "CFDNA-NUCLEOSOME", "CFDNA-HMW-QC"}
    store = facts()["facts"]
    src = {f: s["no"] for s in m["sources"] for f in s["fields"]}
    run = summarize_run(json.loads((ROOT / next(s for s in m["sources"] if s["id"] == "ce")["run_file"]).read_text(encoding="utf-8")))
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
        "traces": traces(m, src, bmi, family_dm, cv, cv_ref, dm, mets, liver, prediabetes, bcaa_high),
        "cfdna_run": cfdna_view(run),
        "nmr_high": nmr_high,
        "insulin_resistance_pattern": bool(bcaa_high) and prediabetes,
        "bcaa_high": bcaa_high,
        "facts": {k: store[k] for k in sorted(used) if k in store},
    }


def _x(term: float) -> str:
    return f"×{math.exp(term):.2f}"


def traces(m, src, bmi, family_dm, cv, cv_ref, dm, mets, liver, prediabetes, bcaa_high) -> dict:
    """Input → effect → result for every headline number. effect is in the score's own scale."""
    p, L, n = m["profile"], m["labs"], m["nmr"]
    ex = {"ex-smoker": "เลิกแล้ว", "current": "สูบ", "never": "ไม่สูบ"}[p["smoking"]]
    # Thai CV Risk (waist/height formula): log-hazard vs the reference person
    t_sbp = 0.019350987 * (p["sbp"] - 120)
    t_whtr = 3.512566 * (p["waist_cm"] / p["height_cm"] - 0.5)
    t_smk = 0.459 * (p["smoking"] == "current")
    pts = {c.feature: c.contribution for c in dm.contributions}
    fli_terms = {c.feature: c.contribution for c in liver.contributions if c.feature != "fib4"}
    fib4 = next(c.value for c in liver.contributions if c.feature == "fib4")
    return {
        "diabetes": {"scale": "คะแนน", "base": None, "result": dm.display, "inputs": [
            {"label": "อายุ", "value": f"{p['age']} ปี", "src": src["age"], "effect": pts["age"], "show": f"+{pts['age']}"},
            {"label": "เพศ", "value": "ชาย" if p["sex"] == "male" else "หญิง", "src": src["sex"], "effect": pts["sex"], "show": f"+{pts['sex']}"},
            {"label": "BMI", "value": f"{bmi:.1f}", "src": src["weight_kg"], "effect": pts["bmi"], "show": f"+{pts['bmi']}"},
            {"label": "รอบเอว", "value": f"{p['waist_cm']} ซม.", "src": src["waist_cm"], "effect": pts["waist"], "show": f"+{pts['waist']}"},
            {"label": "โรคความดัน (วินิจฉัยแล้ว)", "value": "ไม่มี", "src": src["medications"], "effect": pts["hypertension"], "show": f"+{pts['hypertension']}"},
            {"label": "ครอบครัวเป็นเบาหวาน", "value": "พ่อ" if family_dm else "ไม่มี", "src": src["family_history"], "effect": pts["family_dm"], "show": f"+{pts['family_dm']}"}]},
        "cvd": {"scale": "เท่าของความเสี่ยง", "base": f"{cv_ref.value:.1f}%", "base_label": f"คนอายุ {p['age']} เพศเดียวกัน ค่าปกติ",
                "result": cv.display, "inputs": [
            {"label": "ความดันตัวบน", "value": f"{p['sbp']} mmHg", "src": src["sbp"], "effect": round(t_sbp, 3), "show": _x(t_sbp), "ref": "เทียบ 120"},
            {"label": "รอบเอว ÷ ส่วนสูง", "value": f"{p['waist_cm'] / p['height_cm']:.2f}", "src": src["waist_cm"], "effect": round(t_whtr, 3), "show": _x(t_whtr), "ref": "เทียบ 0.50"},
            {"label": "บุหรี่", "value": ex, "src": src["smoking"], "effect": round(t_smk, 3), "show": _x(t_smk)},
            {"label": "เบาหวาน", "value": "ไม่มี", "src": src["glucose_mg_dl"], "effect": 0.0, "show": _x(0)}]},
        "liver": {"scale": "เท่าของ odds", "base": "FLI " + str(round(liver.baseline)), "base_label": "ค่าอ้างอิง TG 100 · BMI 22 · GGT 20 · เอว 80",
                  "result": f"FLI {liver.value:.0f}", "inputs": [
            {"label": "ไตรกลีเซอไรด์", "value": f"{L['tg_mg_dl']} mg/dL", "src": src["tg_mg_dl"], "effect": round(fli_terms["tg"], 3), "show": _x(fli_terms["tg"])},
            {"label": "BMI", "value": f"{bmi:.1f}", "src": src["weight_kg"], "effect": round(fli_terms["bmi"], 3), "show": _x(fli_terms["bmi"])},
            {"label": "GGT", "value": f"{L['ggt']} U/L", "src": src["ggt"], "effect": round(fli_terms["ggt"], 3), "show": _x(fli_terms["ggt"])},
            {"label": "รอบเอว", "value": f"{p['waist_cm']} ซม.", "src": src["waist_cm"], "effect": round(fli_terms["waist"], 3), "show": _x(fli_terms["waist"])}]},
        "fib4": {"formula": "อายุ × AST ÷ (เกล็ดเลือด × √ALT)", "result": f"{fib4:.2f}", "cut": 2.0 if p["age"] > 65 else 1.3, "inputs": [
            {"label": "อายุ", "value": f"{p['age']}", "src": src["age"]}, {"label": "AST", "value": f"{L['ast']}", "src": src["ast"]},
            {"label": "เกล็ดเลือด", "value": f"{L['platelets']}", "src": src["platelets"]}, {"label": "ALT", "value": f"{L['alt']}", "src": src["alt"]}]},
        "mets": {"result": f"{mets.value}/5", "inputs": [
            {"label": c.label, "value": f"{c.value} {c.unit}".strip(), "src": src[k], "met": bool(c.contribution), "rule": c.note}
            for c, k in zip(mets.contributions, ["waist_cm", "tg_mg_dl", "hdl_mg_dl", "sbp", "glucose_mg_dl"])]},
        "insulin_resistance": {"rule": "BCAA สูง ≥ 1 ตัว และ น้ำตาลช่วงก่อนเบาหวาน", "result": bool(bcaa_high) and prediabetes, "inputs": [
            *[{"label": n[k]["label"], "value": f"{n[k]['value']}", "unit": n[k]["unit"], "src": src[k], "met": k in bcaa_high, "rule": f"> {n[k]['high_above']:g}"}
              for k in ("valine", "isoleucine", "leucine")],
            {"label": "น้ำตาลขณะอดอาหาร", "value": f"{L['glucose_mg_dl']}", "unit": "mg/dL", "src": src["glucose_mg_dl"], "met": 100 <= L["glucose_mg_dl"] < 126, "rule": "100–125"},
            {"label": "HbA1c", "value": f"{L['hba1c_pct']}", "unit": "%", "src": src["hba1c_pct"], "met": 5.7 <= L["hba1c_pct"] < 6.5, "rule": "5.7–6.4"}]},
    }


def cfdna_view(run: dict) -> dict:
    """The BCT tube (the one the patient's report uses): replicate traces, downsampled, markers kept for display."""
    t = next(x for x in run["tubes"] if x["tube"] == "BCT")
    reps = [{"name": r["name"], "peak": r["main_peak_bp"], "hmw": r["hmw_fraction"], "qc": r["qc_status"],
             "pts": [[s, round(v, 4)] for s, v in zip(r["sizes_bp"][::2], r["rfu"][::2])]} for r in t["replicates"]]
    return {"instrument": run["instrument"], "date": run["date"], "tube": t["tube_label"], "elution_ul": run["elution_ul"],
            "average_size_bp": t["average_size_bp"], "peak_cv_pct": t["peak_cv_pct"], "mean_conc_ng_ul": t["mean_conc_ng_ul"],
            "total_ng": t["total_ng"], "hmw_max": max(r["hmw"] for r in reps), "qc_status": t["qc_status"],
            "markers_bp": [15, 3000], "replicates": reps}


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", OUT)
