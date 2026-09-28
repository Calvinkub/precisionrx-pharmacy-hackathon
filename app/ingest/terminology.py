"""Terminology mapping: internal key <-> LOINC, free-text lab names -> key, ICD-10 lookups.

Codes live in app/evidence/terminology.yaml (versioned, each with a verified flag).
"""

import re
from functools import cache

import yaml

from app.engines.panel import EVIDENCE

LOINC = "http://loinc.org"
ICD10 = "http://hl7.org/fhir/sid/icd-10"
ICD10CM = "http://hl7.org/fhir/sid/icd-10-cm"


@cache
def _data() -> dict:
    return yaml.safe_load((EVIDENCE / "terminology.yaml").read_text(encoding="utf-8"))


def loinc_for(key: str) -> dict | None:
    return _data()["labs"].get(key)


@cache
def _name_index() -> dict[str, str]:
    idx = {}
    for key, e in _data()["labs"].items():
        for n in [key, e["display"], *e.get("aliases", [])]:
            idx[_norm(n)] = key
        if e.get("code"):
            idx[e["code"]] = key
    return idx


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def key_for(name_or_code: str) -> str | None:
    """Resolve a lab name, alias or LOINC code to an internal key."""
    return _name_index().get(name_or_code.strip()) or _name_index().get(_norm(name_or_code))


def icd10(code: str) -> dict | None:
    c = code.upper().strip()
    table = _data()["conditions"]
    while c:
        if c in table:
            return {"code": code.upper(), **table[c]}
        c = c[:-1].rstrip(".")
    return None


def resolve(term: str, target: str) -> dict:
    """terminology_code_resolver tool: term -> {system, code, display} or a not-found result."""
    if target.lower() == "loinc":
        k = key_for(term)
        e = loinc_for(k) if k else None
        return {"found": bool(e), "key": k, "system": LOINC, **(e or {})}
    hits = [{"code": c, **v} for c, v in _data()["conditions"].items()
            if _norm(term) in _norm(v["display"]) or term.upper().startswith(c)]
    return {"found": bool(hits), "system": ICD10, "matches": hits}
