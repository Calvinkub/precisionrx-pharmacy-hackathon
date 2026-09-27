"""Medication findings for the pharmacist queue: PGx, DDI, statin response, adherence.

All rules are deterministic and cite a fact id in app/evidence/facts.yaml.
"""

from dataclasses import dataclass, field

# severity: stop (hard stop) | action (pharmacist review) | monitor | info
SEVERITY_ORDER = {"stop": 0, "action": 1, "monitor": 2, "info": 3}


@dataclass
class Medication:
    drug: str
    dose_mg: float | None = None
    pdc_pct: float | None = None  # proportion of days covered, from refill or self-report
    start_visit: int | None = None  # index of the first visit taken ON this drug

    @property
    def key(self) -> str:
        return self.drug.strip().lower()


@dataclass
class Finding:
    id: str
    category: str  # pgx | ddi | response | adherence
    severity: str
    title: str
    detail: str
    fact_ids: list[str]
    trace: list[str] = field(default_factory=list)


PPIS = {"omeprazole", "esomeprazole", "lansoprazole", "pantoprazole", "rabeprazole"}

# RCPT 2024 Table A1.1: (drug, min mg, max mg) -> intensity
STATIN_INTENSITY = [
    ("atorvastatin", 40, 80, "high"), ("rosuvastatin", 20, 40, "high"),
    ("atorvastatin", 10, 20, "moderate"), ("rosuvastatin", 5, 10, "moderate"),
    ("simvastatin", 20, 40, "moderate"), ("pitavastatin", 1, 4, "moderate"),
    ("pravastatin", 40, 40, "moderate"), ("fluvastatin", 80, 80, "moderate"),
    ("simvastatin", 10, 10, "low"), ("pravastatin", 10, 20, "low"), ("fluvastatin", 20, 40, "low"),
]
EXPECTED_MIN_LDL_DROP = {"high": 50, "moderate": 30, "low": 0}
STATINS = {s[0] for s in STATIN_INTENSITY}


def statin_intensity(med: Medication) -> str | None:
    if med.dose_mg is None:
        return None
    for drug, lo, hi, intensity in STATIN_INTENSITY:
        if med.key == drug and lo <= med.dose_mg <= hi:
            return intensity
    return None


def pgx_findings(meds: list[Medication], pgx: dict[str, str]) -> list[Finding]:
    """pgx maps gene -> phenotype/result, e.g. {"SLCO1B1": "decreased function", "HLA-B*15:02": "positive"}."""
    out = []
    keys = {m.key: m for m in meds}
    pheno = {g.upper(): v.strip().lower() for g, v in pgx.items()}

    for drug in ("carbamazepine", "oxcarbazepine"):
        if drug in keys and pheno.get("HLA-B*15:02") == "positive":
            out.append(Finding(f"pgx-hlab1502-{drug}", "pgx", "stop", f"STOP — {drug}",
                               "HLA-B*15:02 positive: ห้ามใช้ (เสี่ยง SJS/TEN) เลือกยาอื่น",
                               ["CPIC-HLAB1502"], [f"ยา: {drug}", "HLA-B*15:02 = positive"]))
    if "allopurinol" in keys and pheno.get("HLA-B*58:01") == "positive":
        out.append(Finding("pgx-hlab5801", "pgx", "stop", "STOP — allopurinol",
                           "HLA-B*58:01 positive: ห้ามใช้ (เสี่ยง SCAR) เลือกยาอื่น",
                           ["CPIC-HLAB5801"], ["ยา: allopurinol", "HLA-B*58:01 = positive"]))

    simva = keys.get("simvastatin")
    if simva and pheno.get("SLCO1B1") in {"decreased function", "poor function"}:
        dose = f"{simva.dose_mg:g} mg" if simva.dose_mg else "ไม่ทราบขนาด"
        out.append(Finding("pgx-slco1b1-simva", "pgx", "action", f"Simvastatin {dose} — SLCO1B1 {pheno['SLCO1B1']}",
                           "CPIC 2022: เปลี่ยนเป็น statin ตัวอื่น หรือถ้าจำเป็นต้องใช้ simvastatin จำกัดขนาด < 20 mg/วัน",
                           ["CPIC-SLCO1B1-2022"], [f"ยา: simvastatin {dose}", f"SLCO1B1 = {pheno['SLCO1B1']}"]))

    cyp = pheno.get("CYP2C19")
    if "clopidogrel" in keys and cyp == "poor metabolizer":
        out.append(Finding("pgx-cyp2c19-clop", "pgx", "action", "Clopidogrel — CYP2C19 poor metabolizer",
                           "CPIC 2022 (ACS/PCI): เลี่ยง clopidogrel ถ้าทำได้ ใช้ prasugrel หรือ ticagrelor ขนาดมาตรฐานถ้าไม่มีข้อห้าม",
                           ["CPIC-CYP2C19-CLOP-2022"], ["ยา: clopidogrel", "CYP2C19 = poor metabolizer"]))
    for ppi in PPIS & keys.keys():
        if cyp in {"ultrarapid metabolizer", "rapid metabolizer"}:
            out.append(Finding(f"pgx-cyp2c19-{ppi}", "pgx", "action", f"{ppi.capitalize()} — CYP2C19 {cyp}",
                               "CPIC: พิจารณาเพิ่มขนาดเริ่มต้นของ PPI ถ้ายังคุมอาการไม่ได้ (ถ้อยคำยังไม่ได้ตรวจกับต้นฉบับ)",
                               ["CPIC-CYP2C19-PPI-2020"], [f"ยา: {ppi}", f"CYP2C19 = {cyp}"]))
    return out


def ddi_findings(meds: list[Medication]) -> list[Finding]:
    keys = {m.key for m in meds}
    out = []
    if "clopidogrel" in keys:
        for ppi in sorted(keys & {"omeprazole", "esomeprazole"}):
            out.append(Finding(f"ddi-clop-{ppi}", "ddi", "action", f"Clopidogrel + {ppi}",
                               "ฉลาก Plavix: หลีกเลี่ยงการใช้ร่วมกัน พิจารณาเปลี่ยนเป็น pantoprazole",
                               ["LABEL-CLOP-PPI"], ["ยา: clopidogrel", f"ยา: {ppi}"]))
    return out


def statin_response(med: Medication, ldl_before: float | None, ldl_now: float | None) -> list[Finding]:
    """ldl values in mmol/L: before = last result before start, now = latest result on the statin."""
    intensity = statin_intensity(med)
    if intensity is None or ldl_before is None or ldl_now is None:
        return []
    drop = (ldl_before - ldl_now) / ldl_before * 100
    expected = EXPECTED_MIN_LDL_DROP[intensity]
    trace = [f"ยา: {med.drug} {med.dose_mg:g} mg = {intensity} intensity",
             f"LDL-C {ldl_before:.2f} → {ldl_now:.2f} mmol/L (ลด {drop:.0f}%)",
             f"คาดว่าลด ≥ {expected}%"]

    if med.pdc_pct is not None and med.pdc_pct < 80:
        trace.append(f"PDC {med.pdc_pct:.0f}% (< 80%)")
        return [Finding(f"adh-{med.key}", "adherence", "action",
                        f"{med.drug.capitalize()} — ทบทวนการใช้ยาก่อน",
                        f"PDC {med.pdc_pct:.0f}% ต่ำกว่าเกณฑ์ 80% — ทบทวนการกินยาก่อนสรุปว่ายาไม่ได้ผล "
                        f"(LDL-C ลด {drop:.0f}% คาด ≥ {expected}%)",
                        ["PQA-PDC80", "RCPT-2024-FOLLOWUP", "RCPT-2024-STATIN"], trace)]
    if med.pdc_pct is not None:
        trace.append(f"PDC {med.pdc_pct:.0f}% (≥ 80%)")
    if drop < expected:
        return [Finding(f"resp-{med.key}", "response", "action",
                        f"{med.drug.capitalize()} — LDL-C ลดน้อยกว่าที่คาด",
                        f"ลด {drop:.0f}% แต่ยา {intensity} intensity คาดว่าลด ≥ {expected}% "
                        "— ทบทวนขนาดยา ยาที่ใช้ร่วม และผล PGx",
                        ["RCPT-2024-STATIN", "RCPT-2024-FOLLOWUP"], trace)]
    return [Finding(f"resp-{med.key}", "response", "info",
                    f"{med.drug.capitalize()} — LDL-C ลดตามที่คาด",
                    f"ลด {drop:.0f}% (คาด ≥ {expected}% สำหรับ {intensity} intensity)",
                    ["RCPT-2024-STATIN"], trace)]


def adherence_findings(meds: list[Medication], already: set[str]) -> list[Finding]:
    """PDC < 80% for any drug not already covered by a response/adherence finding."""
    out = []
    for med in meds:
        if med.pdc_pct is None or med.pdc_pct >= 80 or f"adh-{med.key}" in already:
            continue
        out.append(Finding(f"adh-{med.key}", "adherence", "action", f"{med.drug.capitalize()} — กินยาไม่สม่ำเสมอ",
                           f"PDC {med.pdc_pct:.0f}% ต่ำกว่าเกณฑ์ 80% — คุยหาสาเหตุ (ลืม ผลข้างเคียง ค่าใช้จ่าย) ก่อนปรับยา",
                           ["PQA-PDC80"], [f"ยา: {med.drug}", f"PDC {med.pdc_pct:.0f}% (< 80%)"]))
    return out


def sort_findings(findings: list[Finding]) -> list[Finding]:
    return sorted(findings, key=lambda f: SEVERITY_ORDER[f.severity])
