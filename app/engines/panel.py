"""NMR panel: analyte catalog, CSV import, per-analyte status and visit-to-visit trend.

The system only accepts quantified results from the lab. It never processes raw spectra.
"""

import csv
import io
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml

from app.engines.rcv import compare

EVIDENCE = Path(__file__).resolve().parent.parent / "evidence"


@cache
def catalog() -> dict[str, dict]:
    data = yaml.safe_load((EVIDENCE / "analytes.yaml").read_text(encoding="utf-8"))
    return {a["id"]: a for a in data["analytes"]}


@cache
def facts() -> dict:
    return yaml.safe_load((EVIDENCE / "facts.yaml").read_text(encoding="utf-8"))


def _aliases() -> dict[str, str]:
    out = {}
    for a in catalog().values():
        for k in (a["id"], a["abbr"], a["name"]):
            out[k.strip().lower()] = a["id"]
    return out


def parse_csv(text: str) -> tuple[dict[str, float], list[str], str | None]:
    """CSV with columns analyte,value (header required; 'date' row optional).

    Returns (values, unknown analyte names, date).
    """
    aliases = _aliases()
    values, unknown, date = {}, [], None
    for row in csv.DictReader(io.StringIO(text.lstrip("﻿"))):
        name = (row.get("analyte") or "").strip()
        raw = (row.get("value") or "").strip()
        if not name:
            continue
        if name.lower() == "date":
            date = raw
            continue
        aid = aliases.get(name.lower())
        if aid is None:
            unknown.append(name)
            continue
        try:
            values[aid] = float(raw)
        except ValueError:
            unknown.append(name)
    return values, unknown, date


def status(analyte_id: str, value: float) -> str:
    a = catalog()[analyte_id]
    if a.get("ref_high") is not None and value > a["ref_high"]:
        return "high"
    if a.get("ref_low") is not None and value < a["ref_low"]:
        return "low"
    return "normal"


@dataclass
class TrendRow:
    id: str
    abbr: str
    unit: str
    previous: float
    current: float
    pct_change: float
    rcv_pct: float | None
    verdict: str


def trend(previous: dict[str, float], current: dict[str, float]) -> list[TrendRow]:
    rows = []
    for aid, a in catalog().items():
        if aid not in previous or aid not in current:
            continue
        c = compare(previous[aid], current[aid], a.get("cva"), a.get("cvi"), a.get("better"))
        rows.append(TrendRow(aid, a["abbr"], a["unit"], c.previous, c.current,
                             round(c.pct_change, 1), None if c.rcv_pct is None else round(c.rcv_pct, 1), c.verdict))
    return rows
