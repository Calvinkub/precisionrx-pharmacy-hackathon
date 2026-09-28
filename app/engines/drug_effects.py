"""Which NMR markers the patient's regular drugs are expected to move."""

from functools import cache

import yaml

from app.engines.panel import EVIDENCE, catalog

NO_EVIDENCE = "ไม่พบหลักฐานในฐานข้อมูลว่ายานี้เปลี่ยนค่า NMR ในรายงานนี้"


@cache
def _classes() -> dict:
    return yaml.safe_load((EVIDENCE / "drug_effects.yaml").read_text(encoding="utf-8"))["drugs"]


def drug_class(drug: str) -> tuple[str, dict] | None:
    d = drug.strip().lower()
    for cid, c in _classes().items():
        if d in c["members"]:
            return cid, c
    return None


def effects_for(drug: str) -> dict:
    """Per-drug view for the medications page."""
    found = drug_class(drug)
    if not found:
        return {"class": None, "label": None, "effects": [], "interpretation": NO_EVIDENCE, "fact_ids": []}
    cid, c = found
    cat = catalog()
    effects = [{"analytes": [cat[a]["abbr"] for a in e["analytes"] if a in cat], "ids": [a for a in e["analytes"] if a in cat],
                "direction": e["direction"], "note": e.get("note")} for e in c["effects"]]
    return {"class": cid, "label": c["label"], "effects": effects, "interpretation": c["interpretation"], "fact_ids": c["fact_ids"]}


def moved_by(drugs: list[str]) -> dict[str, list[dict]]:
    """analyte id -> [{drug, direction}] for drugs expected to move it (stable effects excluded)."""
    out: dict[str, list[dict]] = {}
    for drug in drugs:
        found = drug_class(drug)
        if not found:
            continue
        _, c = found
        for e in c["effects"]:
            if e["direction"] == "stable":
                continue
            for a in e["analytes"]:
                out.setdefault(a, []).append({"drug": drug.lower(), "direction": e["direction"], "fact_ids": c["fact_ids"]})
    return out
