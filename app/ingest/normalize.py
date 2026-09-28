"""Merge all connector outputs into one PatientRecord (Structured Patient JSON) and validate it.

Rules: convert to canonical UCUM units; never guess unknown units; flag implausible values; when
the same lab arrives from several sources on the same day keep the most structured one
(FHIR > HL7 v2 > PDF); report missing inputs per downstream score instead of imputing them.
"""

import json
from datetime import date
from pathlib import Path

from app.ingest import parsers as P
from app.ingest.schemas import DataIssue, Demographics, Observation, PatientRecord
from app.ingest.terminology import LOINC, loinc_for
from app.ingest.units import implausible, to_canonical

SOURCE_RANK = {"fhir": 0, "hl7v2": 1, "pdf": 2, "manual": 3}
# inputs each downstream calculator needs (reported, not imputed)
REQUIRED = {
    "Thai CV Risk": ["age", "sex", "sbp", "total_c|waist_cm"],
    "Thai Diabetes Score": ["age", "sex", "bmi", "waist_cm"],
    "Metabolic syndrome": ["waist_cm", "tg", "hdl_c", "sbp", "glucose"],
    "eGFR (CKD-EPI 2021)": ["creatinine", "age", "sex"],
    "KDIGO albuminuria": ["uacr"],
    "FIB-4": ["age", "ast", "alt", "platelets"],
    "Fatty Liver Index": ["tg", "bmi", "ggt", "waist_cm"],
}
STALE_DAYS = 365


def _age(birth: date | None, on: date) -> int | None:
    if not birth:
        return None
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def build_record(folder: Path, as_of: date | None = None) -> tuple[PatientRecord, dict]:
    """Read every known file in a patient folder. Returns (record, raw_data summary)."""
    as_of = as_of or date.today()
    raw: dict = {}
    labs, conditions, meds, demo, vitals = [], [], [], {}, {}
    metabolites, cfdna, lifestyle, claims, issues = [], None, [], [], []
    sources = []

    def add(name: str):
        sources.append(name)
        raw[name] = (folder / name).stat().st_size

    for f in sorted(folder.iterdir()):
        n = f.name
        if n.endswith(".fhir.json"):
            r = P.parse_fhir_bundle(json.loads(f.read_text(encoding="utf-8")), n)
            demo |= {k: v for k, v in r["demographics"].items() if v}
            labs += r["labs"]; conditions += r["conditions"]; meds += r["medications"]; vitals |= r["vitals"]
        elif n.endswith(".hl7"):
            r = P.parse_hl7_oru(f.read_text(encoding="utf-8"), n)
            demo = {**{k: v for k, v in r["demographics"].items() if v}, **demo}
            labs += r["labs"]
        elif n.endswith(".pdf"):
            r = P.parse_lab_pdf(f.read_bytes(), n)
            labs += r["labs"]
            for u in r["unmatched"]:
                issues.append(DataIssue(field=u, kind="unmapped", detail=f"{n}: lab name not in terminology map", severity="info"))
        elif n.startswith("nmr") and n.endswith(".csv"):
            r = P.parse_nmr_panel(f.read_text(encoding="utf-8"), n)
            metabolites += r["metabolites"]
            raw["nmr_date"] = str(r["date"]) if r["date"] else None
        elif n.startswith("cfdna") and n.endswith(".csv"):
            cfdna = P.parse_cfdna_electropherogram(f.read_text(encoding="utf-8"), n)
        elif n.startswith("wearable") and n.endswith(".json"):
            lifestyle = P.parse_wearable(json.loads(f.read_text(encoding="utf-8")))
        elif n.startswith("claims") and n.endswith(".csv"):
            claims = P.parse_claims(f.read_text(encoding="utf-8"), n)
        elif n == "profile.json":
            demo |= json.loads(f.read_text(encoding="utf-8"))
        else:
            continue
        add(n)

    # --- labs: canonical units, plausibility, de-duplication
    best: dict[tuple[str, date | None], Observation] = {}
    for key, name, value, unit, eff, prov, loinc in labs:
        if key is None:
            issues.append(DataIssue(field=name, kind="unmapped", detail=f"{prov.document} {prov.locator}: no terminology match", severity="info"))
            continue
        conv = to_canonical(key, value, unit)
        if conv is None:
            issues.append(DataIssue(field=key, kind="unit_unknown", detail=f"{value} {unit} ({prov.document} {prov.locator}) — not converted", severity="warning"))
            continue
        v, u, converted = conv
        e = loinc_for(key) or {}
        obs = Observation(key=key, name=e.get("display", name), value=v, unit=u,
                          original_value=value if converted else None, original_unit=unit if converted else None,
                          coding={"system": LOINC, "code": loinc or e.get("code", ""), "display": e.get("display", name)},
                          effective=eff, provenance=prov, flags=["converted"] if converted else [])
        if implausible(key, v):
            obs.flags.append("implausible")
            issues.append(DataIssue(field=key, kind="implausible", detail=f"{v} {u} outside plausible range — excluded from scores", severity="blocking"))
        slot = (key, eff)
        if slot in best:
            keep = best[slot]
            if SOURCE_RANK[prov.source] < SOURCE_RANK[keep.provenance.source]:
                best[slot] = obs
            issues.append(DataIssue(field=key, kind="duplicate", detail=f"{key} on {eff} from {keep.provenance.source} and {prov.source}; kept the more structured source", severity="info"))
        else:
            best[slot] = obs
    observations = sorted(best.values(), key=lambda o: (o.key, o.effective or date.min))
    for o in observations:
        if o.effective and (as_of - o.effective).days > STALE_DAYS:
            o.flags.append("stale")
            issues.append(DataIssue(field=o.key, kind="stale", detail=f"result from {o.effective} is older than 12 months", severity="info"))

    demo |= {k: v for k, v in vitals.items() if v}
    if not demo.get("age"):
        demo["age"] = _age(demo.get("birth_date") if isinstance(demo.get("birth_date"), date) else
                           (date.fromisoformat(demo["birth_date"]) if demo.get("birth_date") else None), as_of)
    record = PatientRecord(demographics=Demographics(**demo), observations=observations, conditions=conditions,
                           medications=meds, metabolomics=metabolites, cfdna=cfdna, lifestyle=lifestyle,
                           claims=claims, issues=issues, sources=sources)
    record.issues += missing_inputs(record)
    raw["n_metabolites"] = len(metabolites)
    raw["n_interpreted_metabolites"] = sum(m.interpreted for m in metabolites)
    return record, raw


def _has(record: PatientRecord, field: str) -> bool:
    d = record.demographics
    if field == "bmi":
        return bool(d.weight_kg and d.height_cm)
    if hasattr(d, field) and field != "patient_id":
        return getattr(d, field) is not None
    usable = [o for o in record.observations if o.key == field and "implausible" not in o.flags]
    if usable:
        return True
    return any(m.key == field and m.interpreted for m in record.metabolomics)


def missing_inputs(record: PatientRecord) -> list[DataIssue]:
    out = []
    for score, fields in REQUIRED.items():
        miss = [f for f in fields if not any(_has(record, alt) for alt in f.split("|"))]
        if miss:
            out.append(DataIssue(field=score, kind="missing", detail=f"missing {', '.join(miss)} — not computed (no imputation)", severity="warning"))
    return out
