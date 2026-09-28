"""Tier 1 connectors (mock-grade but format-faithful): FHIR R4 Bundle, HL7 v2 ORU^R01, lab PDF,
NMR panel CSV (any size), cfDNA electropherogram CSV, wearable JSON, claims CSV.

Each returns plain objects with provenance; app/ingest/normalize.py merges and validates them.
"""

import csv
import io
import json
import re
from datetime import date, datetime

from pypdf import PdfReader

from app.engines.panel import catalog
from app.ingest.schemas import (
    CfdnaProfile, Claim, Coding, Condition, LifestyleDay, MedicationStatement, Metabolite, Provenance,
)
from app.ingest.terminology import ICD10, LOINC, icd10, key_for


def _d(s: str | None) -> date | None:
    """ISO dates (FHIR) or HL7 TS (YYYYMMDD[HHMM[SS]])."""
    if not s:
        return None
    s = s.strip()
    if re.fullmatch(r"\d{8}(\d{4}(\d{2})?)?", s):
        return datetime.strptime(s[:8], "%Y%m%d").date()
    return date.fromisoformat(s[:10])


BODY = {"29463-7": "weight_kg", "8302-2": "height_cm", "8280-0": "waist_cm"}

# raw lab tuple before unit normalization: (key|None, name, value, unit, effective, provenance, loinc|None)
RawLab = tuple[str | None, str, float, str, date | None, Provenance, str | None]


def parse_fhir_bundle(bundle: dict, doc: str) -> dict:
    out: dict = {"demographics": {}, "labs": [], "conditions": [], "medications": [], "vitals": {}}
    for i, e in enumerate(bundle.get("entry", [])):
        r = e.get("resource", {})
        prov = Provenance(source="fhir", document=doc, locator=f"entry[{i}] {r.get('resourceType')}/{r.get('id', '')}")
        rt = r.get("resourceType")
        if rt == "Patient":
            out["demographics"] = {"patient_id": r.get("id"), "sex": r.get("gender"), "birth_date": _d(r.get("birthDate"))}
        elif rt == "Observation":
            codings = r.get("code", {}).get("coding", [])
            loinc = next((c["code"] for c in codings if c.get("system") == LOINC), None)
            name = r.get("code", {}).get("text") or (codings[0].get("display") if codings else "")
            eff = _d(r.get("effectiveDateTime"))
            if loinc in BODY and "valueQuantity" in r:
                out["vitals"][BODY[loinc]] = r["valueQuantity"]["value"]
                continue
            if loinc == "72166-2":  # tobacco smoking status
                txt = (r.get("valueCodeableConcept", {}).get("text") or "").lower()
                out["vitals"]["smoker"] = "current" in txt or "every day" in txt or "some days" in txt
                continue
            if "valueQuantity" in r:
                q = r["valueQuantity"]
                out["labs"].append((key_for(loinc) if loinc else key_for(name), name, float(q["value"]),
                                    q.get("code") or q.get("unit", ""), eff, prov, loinc))
            for comp in r.get("component", []):  # blood pressure panel
                cc = comp.get("code", {}).get("coding", [{}])[0].get("code")
                if cc == "8480-6":
                    out["vitals"]["sbp"] = comp["valueQuantity"]["value"]
                elif cc == "8462-4":
                    out["vitals"]["dbp"] = comp["valueQuantity"]["value"]
        elif rt == "Condition":
            c = next((c for c in r.get("code", {}).get("coding", []) if "icd-10" in c.get("system", "")), None)
            if c:
                out["conditions"].append(Condition(coding=Coding(system=c["system"], code=c["code"],
                                                                 display=c.get("display") or (icd10(c["code"]) or {}).get("display", "")),
                                                   onset=_d(r.get("onsetDateTime")), provenance=prov))
        elif rt == "FamilyMemberHistory":
            for cond in r.get("condition", []):
                for c in cond.get("code", {}).get("coding", []):
                    if c.get("code", "").upper().startswith("E11"):
                        out["vitals"]["family_history_dm"] = True
        elif rt in ("MedicationStatement", "MedicationRequest"):
            dose = None
            for di in r.get("dosage", []) + r.get("dosageInstruction", []):
                for dr in di.get("doseAndRate", []):
                    dose = dr.get("doseQuantity", {}).get("value", dose)
            status = {"active": "active", "completed": "stopped", "stopped": "stopped", "intended": "planned", "draft": "planned"}.get(r.get("status"), "active")
            out["medications"].append(MedicationStatement(drug=r.get("medicationCodeableConcept", {}).get("text", "").lower(),
                                                          dose_mg=dose, status=status, provenance=prov))
    return out


def parse_hl7_oru(text: str, doc: str) -> dict:
    """HL7 v2 ORU^R01: reads PID (id/sex/dob), OBR-7 (observation date) and OBX NM/SN segments."""
    out: dict = {"demographics": {}, "labs": []}
    eff = None
    for n, line in enumerate(re.split(r"\r\n|\r|\n", text.strip()), start=1):
        f = line.split("|")
        seg = f[0]
        if seg == "PID":
            out["demographics"] = {"patient_id": f[3].split("^")[0] if len(f) > 3 else None,
                                   "birth_date": _d(f[7]) if len(f) > 7 and f[7] else None,
                                   "sex": {"M": "male", "F": "female"}.get(f[8] if len(f) > 8 else "", None)}
        elif seg == "OBR" and len(f) > 7:
            eff = _d(f[7]) if f[7] else eff
        elif seg == "OBX" and len(f) > 6 and f[2] in ("NM", "SN"):
            ident = f[3].split("^")
            code, name = ident[0], ident[1] if len(ident) > 1 else ident[0]
            system = ident[2] if len(ident) > 2 else ""
            try:
                value = float(f[5].replace("^", "").lstrip("<>="))
            except ValueError:
                continue
            prov = Provenance(source="hl7v2", document=doc, locator=f"line {n} OBX|{f[1]}")
            loinc = code if system in ("LN", "LOINC") else None
            out["labs"].append((key_for(code) or key_for(name), name, value, f[6].split("^")[0], eff, prov, loinc))
    return out


LAB_LINE = re.compile(r"^\s*(?P<name>[A-Za-z][A-Za-z0-9 \-/().]*?)\s+(?P<value>[<>]?\d+(?:\.\d+)?)\s+(?P<unit>[A-Za-z%µ/*0-9^.\[\]]+)")
DATE_LINE = re.compile(r"(?:Collected|Collection date|Date)\s*[:：]\s*(\d{4}-\d{2}-\d{2})", re.I)


def parse_lab_pdf(data: bytes, doc: str) -> dict:
    """Text-layer lab report: 'NAME  VALUE  UNIT  [range]' lines. Scanned PDFs (no text layer) are reported, not guessed."""
    reader = PdfReader(io.BytesIO(data))
    out: dict = {"labs": [], "unmatched": [], "pages": len(reader.pages)}
    eff = None
    for p, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for ln, line in enumerate(text.splitlines(), start=1):
            if m := DATE_LINE.search(line):
                eff = _d(m.group(1))
                continue
            m = LAB_LINE.match(line)
            if not m:
                continue
            name = m.group("name").strip()
            key = key_for(name)
            if key is None:
                out["unmatched"].append(name)
                continue
            prov = Provenance(source="pdf", document=doc, locator=f"page {p} line {ln}")
            out["labs"].append((key, name, float(m.group("value").lstrip("<>")), m.group("unit"), eff, prov, None))
    return out


def _nkey(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def parse_nmr_panel(text: str, doc: str) -> dict:
    """Any-size NMR panel CSV (analyte,value[,unit]). Unknown analytes are KEPT but marked uninterpreted."""
    cat = catalog()
    alias = {k.lower(): k for k in cat} | {a["abbr"].lower(): k for k, a in cat.items()} | {a["name"].lower(): k for k, a in cat.items()}
    out: dict = {"metabolites": [], "date": None}
    for i, row in enumerate(csv.DictReader(io.StringIO(text.lstrip("﻿"))), start=2):
        name = (row.get("analyte") or "").strip()
        if not name:
            continue
        if name.lower() == "date":
            out["date"] = _d(row.get("value"))
            continue
        try:
            value = float(row.get("value", ""))
        except ValueError:
            continue
        k = alias.get(name.lower())
        prov = Provenance(source="nmr", document=doc, locator=f"row {i}")
        out["metabolites"].append(Metabolite(key=k or _nkey(name), name=cat[k]["name"] if k else name, value=value,
                                             unit=(cat[k]["unit"] if k else row.get("unit", "")) or "", interpreted=bool(k), provenance=prov))
    return out


def parse_cfdna_electropherogram(text: str, doc: str) -> CfdnaProfile:
    """CSV 'size_bp,rfu' with optional '# key: value' header lines (instrument, concentration_ng_ul)."""
    meta, rows = {}, []
    for line in text.splitlines():
        if line.startswith("#"):
            k, _, v = line[1:].partition(":")
            meta[k.strip()] = v.strip()
        elif line.strip() and not line.lower().startswith("size"):
            s, r = line.split(",")[:2]
            rows.append((float(s), float(r)))
    rows.sort()
    return CfdnaProfile(sizes_bp=[r[0] for r in rows], intensity=[r[1] for r in rows],
                        concentration_ng_ul=float(meta["concentration_ng_ul"]) if "concentration_ng_ul" in meta else None,
                        instrument=meta.get("instrument", ""), provenance=Provenance(source="cfdna", document=doc, locator=f"{len(rows)} points"))


def parse_wearable(data: dict) -> list[LifestyleDay]:
    return [LifestyleDay(day=_d(d["date"]), steps=d.get("steps"), active_minutes=d.get("active_minutes"),
                         resting_hr=d.get("resting_hr"), sleep_hours=d.get("sleep_hours")) for d in data.get("days", [])]


def parse_claims(text: str, doc: str) -> list[Claim]:
    out = []
    for i, row in enumerate(csv.DictReader(io.StringIO(text.lstrip("﻿"))), start=2):
        code = row["icd10"].strip().upper()
        out.append(Claim(service_date=_d(row["service_date"]), coding=Coding(system=ICD10, code=code,
                                                                          display=(icd10(code) or {}).get("display", "")),
                         description=row.get("description", ""), provenance=Provenance(source="claims", document=doc, locator=f"row {i}")))
    return out


def load_json(text: str) -> dict:
    return json.loads(text)
