"""Regular medications from dispensing (refill) history.

PDC (proportion of days covered): days with drug on hand / days in the window, where overlapping
supplies are shifted forward (standard PQA method). Window = last `lookback` days up to `as_of`,
starting no earlier than the first fill.
"""

from dataclasses import dataclass
from datetime import date, timedelta

LOOKBACK_DAYS = 180
STOPPED_AFTER_DAYS = 30  # supply ran out this long before as_of -> treated as stopped


@dataclass
class Fill:
    date: date
    drug: str
    dose_mg: float | None
    days_supply: int
    sig: str = ""


@dataclass
class RegularMed:
    drug: str
    dose_mg: float | None
    sig: str
    first_fill: date
    last_fill: date
    fills: int
    pdc_pct: float
    status: str  # regular | new | stopped


def parse_fills(rows: list[dict]) -> list[Fill]:
    return [Fill(date.fromisoformat(r["date"]), r["drug"].lower(), r.get("dose_mg"), int(r["days_supply"]), r.get("sig", ""))
            for r in rows]


def pdc(fills: list[Fill], start: date, end: date) -> float:
    if end <= start:
        return 100.0
    covered: set[date] = set()
    cursor = start
    for f in sorted(fills, key=lambda x: x.date):
        day = max(f.date, cursor)
        for _ in range(f.days_supply):
            if day >= end:
                break
            if day >= start:
                covered.add(day)
            day += timedelta(days=1)
        cursor = day
    return round(len(covered) / (end - start).days * 100, 1)


def regular_meds(rows: list[dict], as_of: date) -> list[RegularMed]:
    by_drug: dict[str, list[Fill]] = {}
    for f in parse_fills(rows):
        if f.date <= as_of:
            by_drug.setdefault(f.drug, []).append(f)
    out = []
    for drug, fills in by_drug.items():
        fills.sort(key=lambda x: x.date)
        first, last = fills[0], fills[-1]
        start = max(first.date, as_of - timedelta(days=LOOKBACK_DAYS))
        supply_end = last.date + timedelta(days=last.days_supply)
        if supply_end < as_of - timedelta(days=STOPPED_AFTER_DAYS):
            status = "stopped"
        elif len(fills) == 1:
            status = "new"
        else:
            status = "regular"
        out.append(RegularMed(drug, last.dose_mg, last.sig, first.date, last.date, len(fills),
                              pdc([f for f in fills if f.date + timedelta(days=f.days_supply) > start], start, as_of), status))
    return sorted(out, key=lambda m: (m.status == "stopped", m.first_fill))
