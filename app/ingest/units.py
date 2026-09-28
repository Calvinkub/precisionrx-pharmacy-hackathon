"""UCUM unit standardization: every key has one canonical unit; known conversions only.

Unknown units are never guessed — they are reported as a DataIssue.
"""

# molar-mass based factors: value_in_canonical = value * factor
CANONICAL = {
    "glucose": "mmol/L", "total_c": "mmol/L", "ldl_c": "mmol/L", "hdl_c": "mmol/L", "non_hdl_c": "mmol/L",
    "tg": "mmol/L", "apob": "g/L", "creatinine": "mg/dL", "hba1c": "%", "alt": "U/L", "ast": "U/L",
    "ggt": "U/L", "platelets": "10*9/L", "albumin": "g/L", "uacr": "mg/g", "sbp": "mm[Hg]", "dbp": "mm[Hg]",
}
_ALIASES = {"mg/dl": "mg/dL", "mmol/l": "mmol/L", "g/l": "g/L", "u/l": "U/L", "iu/l": "U/L", "umol/l": "umol/L",
            "µmol/l": "umol/L", "x10^9/l": "10*9/L", "10^9/l": "10*9/L", "10*3/ul": "10*3/uL", "k/ul": "10*3/uL",
            "mmhg": "mm[Hg]", "g/dl": "g/dL", "mg/g": "mg/g", "%": "%", "mmol/mol": "mmol/mol"}
_FACTORS = {
    ("glucose", "mg/dL"): 1 / 18.016,
    ("total_c", "mg/dL"): 1 / 38.67, ("ldl_c", "mg/dL"): 1 / 38.67, ("hdl_c", "mg/dL"): 1 / 38.67,
    ("non_hdl_c", "mg/dL"): 1 / 38.67,
    ("tg", "mg/dL"): 1 / 88.57,
    ("apob", "mg/dL"): 1 / 100,
    ("creatinine", "umol/L"): 1 / 88.42,
    ("platelets", "10*3/uL"): 1.0,
    ("albumin", "g/dL"): 10.0,
}
# plausibility limits in canonical units (outside = data-entry or unit error, not disease)
PLAUSIBLE = {
    "glucose": (1.0, 40.0), "total_c": (1.0, 20.0), "ldl_c": (0.2, 15.0), "hdl_c": (0.1, 5.0), "tg": (0.1, 60.0),
    "apob": (0.1, 4.0), "creatinine": (0.1, 20.0), "hba1c": (3.0, 20.0), "alt": (1, 5000), "ast": (1, 5000),
    "ggt": (1, 5000), "platelets": (5, 2000), "albumin": (10, 60), "sbp": (60, 260), "dbp": (30, 160),
}


def ucum(unit: str) -> str:
    u = unit.strip()
    return _ALIASES.get(u.lower(), u)


def hba1c_from_ifcc(mmol_mol: float) -> float:
    """NGSP % = 0.09148 × IFCC (mmol/mol) + 2.152 (IFCC–NGSP master equation)."""
    return 0.09148 * mmol_mol + 2.152


def to_canonical(key: str, value: float, unit: str) -> tuple[float, str, bool] | None:
    """Return (value, canonical unit, converted?) or None when the unit is unknown for this key."""
    target = CANONICAL.get(key)
    u = ucum(unit)
    if target is None:
        return value, u, False
    if u == target:
        return value, target, False
    if key == "hba1c" and u == "mmol/mol":
        return round(hba1c_from_ifcc(value), 2), target, True
    f = _FACTORS.get((key, u))
    if f is None:
        return None
    return round(value * f, 4), target, True


def implausible(key: str, value: float) -> bool:
    lo, hi = PLAUSIBLE.get(key, (float("-inf"), float("inf")))
    return not lo <= value <= hi
