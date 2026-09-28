"""Generate synthetic multi-source patient folders (FHIR, HL7 v2, lab PDF, NMR, cfDNA, wearable, claims).

    uv run python -m scripts.make_synthetic_patients
All data are synthetic.
"""

import json
import math
import random
from datetime import date, timedelta
from pathlib import Path

from app.engines.panel import catalog

OUT = Path(__file__).resolve().parent.parent / "data" / "synthetic" / "patients"


def pdf(lines: list[str]) -> bytes:
    """Minimal one-page PDF with a Helvetica text layer (enough for a text-based lab report)."""
    esc = lambda t: t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    content = "BT /F1 10 Tf 50 800 Td 14 TL " + " ".join(f"({esc(l)}) Tj T*" for l in lines) + " ET"
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            f"<< /Length {len(content)} >>\nstream\n{content}\nendstream", "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offsets = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


def fhir_bundle(pid, sex, birth, vitals, conditions, meds, family_dm, smoking):
    e = [{"resource": {"resourceType": "Patient", "id": pid, "gender": sex, "birthDate": birth}}]
    def q(code, disp, value, unit, when):
        return {"resourceType": "Observation", "id": f"{pid}-{code}", "status": "final",
                "code": {"coding": [{"system": "http://loinc.org", "code": code, "display": disp}], "text": disp},
                "effectiveDateTime": when, "valueQuantity": {"value": value, "unit": unit, "system": "http://unitsofmeasure.org", "code": unit}}
    when = vitals["date"]
    e += [{"resource": q("29463-7", "Body weight", vitals["weight"], "kg", when)},
          {"resource": q("8302-2", "Body height", vitals["height"], "cm", when)},
          {"resource": q("8280-0", "Waist circumference", vitals["waist"], "cm", when)},
          {"resource": {"resourceType": "Observation", "id": f"{pid}-bp", "status": "final", "effectiveDateTime": when,
                        "code": {"coding": [{"system": "http://loinc.org", "code": "85354-9", "display": "Blood pressure panel"}]},
                        "component": [{"code": {"coding": [{"system": "http://loinc.org", "code": "8480-6"}]}, "valueQuantity": {"value": vitals["sbp"], "unit": "mm[Hg]"}},
                                      {"code": {"coding": [{"system": "http://loinc.org", "code": "8462-4"}]}, "valueQuantity": {"value": vitals["dbp"], "unit": "mm[Hg]"}}]}},
          {"resource": {"resourceType": "Observation", "id": f"{pid}-smoke", "status": "final", "effectiveDateTime": when,
                        "code": {"coding": [{"system": "http://loinc.org", "code": "72166-2", "display": "Tobacco smoking status"}]},
                        "valueCodeableConcept": {"text": smoking}}}]
    for code, disp, onset in conditions:
        e.append({"resource": {"resourceType": "Condition", "id": f"{pid}-{code}", "onsetDateTime": onset,
                               "code": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": code, "display": disp}]}}})
    for drug, dose, status in meds:
        e.append({"resource": {"resourceType": "MedicationStatement", "id": f"{pid}-{drug}", "status": status,
                               "medicationCodeableConcept": {"text": drug}, "dosage": [{"doseAndRate": [{"doseQuantity": {"value": dose, "unit": "mg"}}]}]}})
    if family_dm:
        e.append({"resource": {"resourceType": "FamilyMemberHistory", "id": f"{pid}-fh", "status": "completed",
                               "relationship": {"text": "mother"},
                               "condition": [{"code": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": "E11"}]}}]}})
    return {"resourceType": "Bundle", "type": "collection", "entry": e}


def hl7(pid, sex, dob, when, obx):
    ts = when.replace("-", "") + "0800"
    seg = [f"MSH|^~\\&|LIS|HOSP|PRECISIONRX|HOSP|{ts}||ORU^R01|MSG{pid}|P|2.5.1",
           f"PID|1||{pid}^^^HOSP^MR||SYNTHETIC^PATIENT||{dob.replace('-', '')}|{sex}",
           f"OBR|1||LAB{pid}|24331-1^Lipid and chemistry panel^LN|||{ts}"]
    for i, (code, name, value, unit, rng) in enumerate(obx, start=1):
        seg.append(f"OBX|{i}|NM|{code}^{name}^LN||{value}|{unit}|{rng}||||F")
    return "\r".join(seg) + "\r"


def nmr_panel(known: dict, seed: int) -> str:
    """Known analytes + a Nightingale-style long tail (lipoprotein subclasses, ratios) to ~250 rows."""
    rnd = random.Random(seed)
    rows = ["analyte,value,unit", f"date,{known.pop('_date')},"]
    cat = catalog()
    for k, v in known.items():
        rows.append(f"{cat[k]['abbr']},{v},{cat[k]['unit']}")
    subclasses = ["XXL_VLDL", "XL_VLDL", "L_VLDL", "M_VLDL", "S_VLDL", "XS_VLDL", "IDL", "L_LDL", "M_LDL", "S_LDL", "XL_HDL", "L_HDL", "M_HDL", "S_HDL"]
    for sc in subclasses:
        for m, unit in [("P", "nmol/L"), ("L", "mmol/L"), ("PL", "mmol/L"), ("C", "mmol/L"), ("CE", "mmol/L"), ("FC", "mmol/L"), ("TG", "mmol/L")]:
            rows.append(f"{sc}_{m},{rnd.uniform(0.001, 0.9):.4f},{unit}")
        for m in ["PL_pct", "C_pct", "CE_pct", "FC_pct", "TG_pct"]:
            rows.append(f"{sc}_{m},{rnd.uniform(5, 60):.2f},%")
    for extra, unit in [("Total_FA", "mmol/L"), ("Omega_6", "mmol/L"), ("LA", "mmol/L"), ("PUFA", "mmol/L"), ("MUFA", "mmol/L"), ("SFA", "mmol/L"),
                        ("Ala", "umol/L"), ("Gln", "umol/L"), ("Gly", "umol/L"), ("His", "umol/L"), ("Tyr", "umol/L"),
                        ("Acetate", "umol/L"), ("Acetoacetate", "umol/L"), ("Pyruvate", "mmol/L"), ("Glycerol", "umol/L"),
                        ("VLDL_size", "nm"), ("HDL_size", "nm"), ("Total_TG", "mmol/L"), ("Total_PL", "mmol/L")]:
        rows.append(f"{extra},{rnd.uniform(0.05, 400):.3f},{unit}")
    return "\n".join(rows) + "\n"


def electropherogram(hmw: float, short_boost: float, seed: int) -> str:
    """Synthetic fragment-size trace: mono-nucleosome ~167 bp, di ~334 bp, optional HMW gDNA hump."""
    rnd = random.Random(seed)
    lines = ["# instrument: QIAxcel Connect (synthetic trace)", "# concentration_ng_ul: 0.42", "size_bp,rfu"]
    for bp in range(35, 1501, 5):
        g = lambda mu, sd, h: h * math.exp(-((bp - mu) ** 2) / (2 * sd ** 2))
        rfu = g(167, 14, 100) + g(334, 22, 14) + g(501, 30, 3) + g(135, 12, short_boost) + g(1200, 180, hmw) + rnd.uniform(0, 0.3)
        lines.append(f"{bp},{rfu:.2f}")
    return "\n".join(lines) + "\n"


def wearable(start: date, days: int, steps: int, active: int, hr: int, seed: int) -> dict:
    rnd = random.Random(seed)
    return {"device": "smartwatch (synthetic)", "days": [
        {"date": (start + timedelta(days=i)).isoformat(), "steps": max(0, int(rnd.gauss(steps, steps * .25))),
         "active_minutes": max(0, int(rnd.gauss(active, 6))), "resting_hr": int(rnd.gauss(hr, 2)), "sleep_hours": round(rnd.gauss(6.4, .6), 1)}
        for i in range(days)]}


def write(pid: str, files: dict):
    d = OUT / pid
    d.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (d / name).write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))


P1_NMR = dict(_date="2026-06-12", apob=1.04, apoa1=1.43, ldl_p=1420, s_ldl_p=205, vldl_p=196, hdl_p=14.6, total_c=4.55, ldl_c=2.50,
              hdl_c=1.20, non_hdl_c=3.35, remnant_c=0.85, tg=1.92, glyca=0.99, glucose=6.0, lactate=1.4, citrate=0.068, bcaa=498,
              leucine=133, isoleucine=69, valine=296, phenylalanine=48, omega3_pct=2.6, dha=0.15, pufa_mufa=1.35, bohb=55,
              acetone=13, creatinine=62, albumin=41)
P2_NMR = dict(_date="2026-05-06", apob=1.22, apoa1=1.20, ldl_p=1690, s_ldl_p=252, vldl_p=236, hdl_p=12.9, total_c=5.80, ldl_c=3.70,
              hdl_c=1.00, non_hdl_c=4.80, remnant_c=1.10, tg=2.50, glyca=1.12, glucose=8.1, lactate=1.6, citrate=0.07, bcaa=525,
              leucine=139, isoleucine=77, valine=309, phenylalanine=58, omega3_pct=2.8, dha=0.16, pufa_mufa=1.4, bohb=70,
              acetone=15, creatinine=118, albumin=39)

write("P001", {
    "record.fhir.json": json.dumps(fhir_bundle("P001", "female", "1974-02-15",
        {"date": "2026-06-12", "weight": 67, "height": 155, "waist": 88, "sbp": 138, "dbp": 86},
        [("E78.5", "Hyperlipidaemia, unspecified", "2026-03-10"), ("K21.9", "Gastro-oesophageal reflux disease", "2025-09-01")],
        [("simvastatin", 40, "active"), ("omeprazole", 20, "active")], True, "Never smoker"), ensure_ascii=False, indent=1),
    "lab_2026-06-12.hl7": hl7("P001", "F", "1974-02-15", "2026-06-12", [
        ("2093-3", "Cholesterol total", 176, "mg/dL", "<200"), ("13457-7", "LDL cholesterol calc", 97, "mg/dL", "<130"),
        ("2085-9", "HDL cholesterol", 46, "mg/dL", ">50"), ("2571-8", "Triglyceride", 170, "mg/dL", "<150"),
        ("1558-6", "Fasting glucose", 108, "mg/dL", "70-99"), ("4548-4", "Hemoglobin A1c", 5.9, "%", "<5.7"),
        ("2160-0", "Creatinine", 0.80, "mg/dL", "0.5-1.0"), ("99999-9", "Vitamin X (unmapped)", 12, "ng/mL", "")]),
    "lab_report_2026-06-12.pdf": pdf(["SYNTHETIC HOSPITAL LABORATORY - CLINICAL CHEMISTRY", "Patient: P001   Sex: F   DOB: 1974-02-15",
        "Collected: 2026-06-12", "", "TEST  RESULT  UNIT  REFERENCE", "ALT 48 U/L 7-35", "AST 36 U/L 13-35", "GGT 62 U/L 9-36",
        "Platelets 250 10^9/L 150-400", "Albumin 4.2 g/dL 3.5-5.2", "UACR 18 mg/g <30", "Ferritin 88 ng/mL 13-150",
        "", "This report is synthetic test data."]),
    "nmr_2026-06-12.csv": nmr_panel(dict(P1_NMR), 1),
    "cfdna_2026-06-12.csv": electropherogram(hmw=0.15, short_boost=0, seed=1),
    "wearable_2026-06.json": json.dumps(wearable(date(2026, 5, 30), 14, 4200, 12, 74, 1), indent=1),
    "claims.csv": "service_date,icd10,description\n2025-09-01,K21.9,GERD visit\n2026-03-10,E78.5,Lipid clinic\n2026-06-12,E78.5,Follow-up\n",
})
write("P002", {
    "record.fhir.json": json.dumps(fhir_bundle("P002", "male", "1965-01-20",
        {"date": "2026-05-06", "weight": 78, "height": 168, "waist": 97, "sbp": 148, "dbp": 92},
        [("E11.9", "Type 2 diabetes mellitus without complications", "2019-04-01"), ("I10", "Essential (primary) hypertension", "2018-02-01")],
        [("atorvastatin", 40, "active"), ("metformin", 1000, "active"), ("amlodipine", 5, "active")], False, "Current every day smoker"),
        ensure_ascii=False, indent=1),
    "lab_2026-05-06.hl7": hl7("P002", "M", "1965-01-20", "2026-05-06", [
        ("2093-3", "Cholesterol total", 224, "mg/dL", "<200"), ("13457-7", "LDL cholesterol calc", 143, "mg/dL", "<100"),
        ("2085-9", "HDL cholesterol", 39, "mg/dL", ">40"), ("2571-8", "Triglyceride", 221, "mg/dL", "<150"),
        ("1558-6", "Fasting glucose", 146, "mg/dL", "70-99"), ("4548-4", "Hemoglobin A1c", 7.8, "%", "<7.0"),
        ("2160-0", "Creatinine", 1.40, "mg/dL", "0.7-1.2")]),
    "lab_report_2026-05-06.pdf": pdf(["SYNTHETIC HOSPITAL LABORATORY - CLINICAL CHEMISTRY", "Patient: P002   Sex: M   DOB: 1965-01-20",
        "Collected: 2026-05-06", "", "TEST  RESULT  UNIT  REFERENCE", "ALT 62 U/L 10-40", "AST 55 U/L 10-40", "GGT 90 U/L 10-71",
        "Platelets 180 10^9/L 150-400", "Albumin 3.9 g/dL 3.5-5.2", "UACR 45 mg/g <30", "", "This report is synthetic test data."]),
    "nmr_2026-05-06.csv": nmr_panel(dict(P2_NMR), 2),
    "cfdna_2026-05-06.csv": electropherogram(hmw=22, short_boost=9, seed=2),
    "wearable_2026-05.json": json.dumps(wearable(date(2026, 4, 22), 14, 2100, 4, 82, 2), indent=1),
    "claims.csv": "service_date,icd10,description\n2018-02-01,I10,Hypertension\n2019-04-01,E11.9,Diabetes\n2026-02-02,E11.9,DM follow-up\n2026-05-06,E11.9,DM follow-up\n",
    "profile.json": json.dumps({"alcohol_drinks_per_day": 2.5}),
})
print("wrote", sorted(p.name for p in OUT.iterdir()))


# ---------------------------------------------------------------- cfDNA electropherogram run (replicates × tubes)
def ce_trace(peak: float, hmw: float, seed: int) -> tuple[list[float], list[float]]:
    """QIAxcel-style trace: 15 bp + 3000 bp alignment markers, cfDNA peak, di-nucleosome, optional HMW peak."""
    rnd = random.Random(seed)
    sizes, rfu = [], []
    bp = 10.0
    while bp <= 5000:
        g = lambda mu, sd, h: h * math.exp(-((bp - mu) ** 2) / (2 * sd ** 2))
        v = (g(15, 0.9, 0.62) + g(3000, 60, 0.55) + g(peak, peak * 0.07, 0.24) + g(peak * 2.05, 22, 0.035)
             + g(peak * 3.1, 35, 0.012) + g(1900, 230, hmw) + 0.004 + rnd.uniform(0, 0.004))
        sizes.append(round(bp, 1)); rfu.append(round(v, 4))
        bp *= 1.012
    return sizes, rfu


RUN = {"id": "E10146", "sample_label": "Case E10146 (ค่าสรุปจากสไลด์ที่ผู้ใช้ให้มา · เส้นกราฟสังเคราะห์)", "instrument": "QIAxcel Connect",
       "date": "2026-09-28", "elution_ul": 12.5, "tubes": []}
for tube, label, score, reps in [
    ("BCT", "Cell-free DNA BCT", 0.90, [(161, 2.26, 0.0), (156, 2.14, 0.0), (158, 2.21, 0.0)]),
    ("Roche", "Roche Cell-Free DNA Collection Tube", 0.86, [(163, 2.22, 0.0), (150, 2.38, 0.09), (158, 2.31, 0.0)]),
]:
    t = {"tube": tube, "tube_label": label, "replicates": [],
         "external_score": {"name": "CEliver score", "value": score, "source": "โมเดลวิจัยภายนอก (ค่าจากสไลด์)", "ruo": True}}
    for i, (pk, conc, hmw) in enumerate(reps, start=1):
        s, r = ce_trace(pk, hmw, seed=i * 7 + len(tube))
        t["replicates"].append({"name": f"replicate {i}", "main_peak_bp": pk, "conc_ng_ul": conc, "sizes_bp": s, "rfu": r})
    RUN["tubes"].append(t)
(OUT.parent / "cfdna_runs" / "E10146.json").write_text(json.dumps(RUN, ensure_ascii=False))
print("wrote cfdna run E10146")
