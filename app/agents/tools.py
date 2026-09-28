"""Tier 3 tools. Same functions serve three callers: the LangGraph nodes, the Claude tool-use
loop (JSON schemas below), and the REST API (/api/v2/tools/{name})."""

from datetime import date
from pathlib import Path

from app.agents import rag
from app.engines import calculators as C
from app.engines.panel import catalog
from app.ingest.normalize import build_record
from app.ingest.terminology import resolve

PATIENTS = Path(__file__).resolve().parent.parent.parent / "data" / "synthetic" / "patients"

# clinical (non-NMR) reference intervals used by lab_reference_lookup — adult, sex-specific where it matters
CLINICAL_REF = {
    "glucose": {"any": (3.9, 5.5, "mmol/L", "ADA-2026-DX")},
    "hba1c": {"any": (4.0, 5.6, "%", "ADA-2026-DX")},
    "ldl_c": {"any": (None, 2.6, "mmol/L", "RCPT-2024-LDL-TARGET")},
    "tg": {"any": (None, 1.7, "mmol/L", "METS-HARMONIZED-2009")},
    "hdl_c": {"male": (1.0, None, "mmol/L", "METS-HARMONIZED-2009"), "female": (1.3, None, "mmol/L", "METS-HARMONIZED-2009")},
    "uacr": {"any": (None, 30, "mg/g", "KDIGO-2024")},
}


def patient_folder(patient_id: str) -> Path:
    p = (PATIENTS / patient_id).resolve()
    if p.parent != PATIENTS.resolve() or not p.is_dir():
        raise KeyError(f"unknown patient {patient_id}")
    return p


def vector_db_search(query: str, domain: str = "any", k: int = 5) -> list[dict]:
    return rag.search(query, domain, k)


def ehr_db_query(patient_id: str, date_from: str | None = None, date_to: str | None = None) -> dict:
    rec, _ = build_record(patient_folder(patient_id))
    lo = date.fromisoformat(date_from) if date_from else date.min
    hi = date.fromisoformat(date_to) if date_to else date.max
    inrange = lambda d: d is None or lo <= d <= hi
    return {
        "demographics": rec.demographics.model_dump(mode="json"),
        "conditions": [c.model_dump(mode="json") for c in rec.conditions if inrange(c.onset)],
        "medications": [m.model_dump(mode="json") for m in rec.medications],
        "labs": [o.model_dump(mode="json") for o in rec.observations if inrange(o.effective)],
        "claims": [c.model_dump(mode="json") for c in rec.claims if inrange(c.service_date)],
    }


def lab_reference_lookup(biomarker_name: str, sex: str | None = None, age: int | None = None) -> dict:
    key = biomarker_name.strip().lower()
    cat = catalog()
    out = {"biomarker": biomarker_name, "found": False}
    if key in CLINICAL_REF:
        r = CLINICAL_REF[key].get(sex or "", CLINICAL_REF[key].get("any"))
        if r:
            out |= {"found": True, "kind": "clinical", "low": r[0], "high": r[1], "unit": r[2], "fact_id": r[3]}
    elif key in cat or any(a["abbr"].lower() == key for a in cat.values()):
        a = cat.get(key) or next(a for a in cat.values() if a["abbr"].lower() == key)
        out |= {"found": True, "kind": "population (UK Biobank P10–P90)", "low": a["ref_low"], "high": a["ref_high"],
                "unit": a["unit"], "fact_id": "UKB-NMR-REF", "note": "not a Thai or clinical reference interval"}
    return out


def terminology_code_resolver(term: str, target_standard: str = "loinc") -> dict:
    return resolve(term, target_standard)


def clinical_calculator(calc_type: str, params: dict) -> dict:
    t = calc_type.lower().replace("-", "_")
    male = params.get("sex") == "male"
    if t == "egfr":
        v = C.egfr_ckd_epi_2021(params["creatinine_mg_dl"], params["age"], male)
        return {"calc": "eGFR CKD-EPI 2021", "value": round(v, 1), "unit": "mL/min/1.73m2", "fact_id": "CKD-EPI-2021"}
    if t == "fib4":
        return {"calc": "FIB-4", "value": round(C.fib4(params["age"], params["ast"], params["alt"], params["platelets"]), 2), "fact_id": "FIB4-MASLD"}
    if t == "fli":
        return {"calc": "Fatty Liver Index", "value": round(C.fli(params["tg_mg_dl"], params["bmi"], params["ggt"], params["waist_cm"]), 1), "fact_id": "FLI-2006"}
    if t == "bmi":
        return {"calc": "BMI", "value": round(params["weight_kg"] / (params["height_cm"] / 100) ** 2, 1), "unit": "kg/m2"}
    if t in ("ascvd", "thai_cv_risk", "cvd"):
        r = C.thai_cv_risk(params["age"], male, params["sbp"], params.get("diabetes", False), params["total_c_mg_dl"], params.get("smoker", False))
        return {"calc": "Thai CV Risk Score (10-year CVD)", "value": r.value, "unit": "%", "category": r.category, "fact_id": "TCVRS-2021"}
    raise ValueError(f"unknown calc_type {calc_type}")


TOOLS = {"vector_db_search": vector_db_search, "ehr_db_query": ehr_db_query, "lab_reference_lookup": lab_reference_lookup,
         "terminology_code_resolver": terminology_code_resolver, "clinical_calculator": clinical_calculator}

# Claude tool definitions (strict JSON schema)
TOOL_SCHEMAS = [
    {"name": "vector_db_search", "description": "Search the verified guideline/evidence store (ADA, KDIGO, WHO, ESC, RCPT, CPIC, drug labels). Returns citable chunks with fact_id, source and URL.",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "domain": {"type": "string", "enum": ["any", "diabetes", "cardiovascular", "kidney", "liver", "metabolic", "lifestyle", "pharmacogenomics", "drug-label", "adherence", "oncology", "cfdna", "reference", "drug-effects"]}},
                      "required": ["query", "domain"], "additionalProperties": False}},
    {"name": "ehr_db_query", "description": "Read a patient's normalized record (demographics, conditions, medications, labs, claims) for an optional ISO date range.",
     "input_schema": {"type": "object", "properties": {"patient_id": {"type": "string"}, "date_from": {"type": "string"}, "date_to": {"type": "string"}},
                      "required": ["patient_id"], "additionalProperties": False}},
    {"name": "lab_reference_lookup", "description": "Reference interval for a biomarker (clinical cut-point or NMR population band) with its source fact_id.",
     "input_schema": {"type": "object", "properties": {"biomarker_name": {"type": "string"}, "sex": {"type": "string", "enum": ["male", "female"]}, "age": {"type": "integer"}},
                      "required": ["biomarker_name"], "additionalProperties": False}},
    {"name": "terminology_code_resolver", "description": "Map a term to LOINC (labs) or ICD-10 (conditions).",
     "input_schema": {"type": "object", "properties": {"term": {"type": "string"}, "target_standard": {"type": "string", "enum": ["loinc", "icd10"]}},
                      "required": ["term", "target_standard"], "additionalProperties": False}},
    {"name": "clinical_calculator", "description": "Published clinical formulas: egfr (CKD-EPI 2021), fib4, fli, bmi, thai_cv_risk.",
     "input_schema": {"type": "object", "properties": {"calc_type": {"type": "string", "enum": ["egfr", "fib4", "fli", "bmi", "thai_cv_risk"]}, "params": {"type": "object"}},
                      "required": ["calc_type", "params"], "additionalProperties": False}},
]
