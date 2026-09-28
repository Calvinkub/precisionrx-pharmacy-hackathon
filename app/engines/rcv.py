"""Reference Change Value: is the change between two results larger than normal variation?

RCV = sqrt(2) * Z * sqrt(CVa^2 + CVi^2)
  CVa = analytical CV (%), CVi = within-subject biological CV (%).
If CVi is unknown for an analyte we refuse to judge the change (idea.md §5).
"""

from dataclasses import dataclass
from math import sqrt

Z_TWO_SIDED_95 = 1.96


@dataclass(frozen=True)
class Change:
    previous: float
    current: float
    pct_change: float
    rcv_pct: float | None
    verdict: str  # improved | worsened | within_variation | changed | not_assessable


def rcv_percent(cva: float, cvi: float, z: float = Z_TWO_SIDED_95) -> float:
    return sqrt(2) * z * sqrt(cva**2 + cvi**2)


def compare(
    previous: float,
    current: float,
    cva: float | None,
    cvi: float | None,
    better: str | None = None,
    z: float = Z_TWO_SIDED_95,
) -> Change:
    """better: "lower", "higher" or None (no preferred direction)."""
    pct = (current - previous) / previous * 100 if previous else 0.0
    if cva is None or cvi is None or previous == 0:
        return Change(previous, current, pct, None, "not_assessable")

    rcv = rcv_percent(cva, cvi, z)
    if abs(pct) <= rcv:
        verdict = "within_variation"
    elif better is None:
        verdict = "changed"
    elif (pct < 0) == (better == "lower"):
        verdict = "improved"
    else:
        verdict = "worsened"
    return Change(previous, current, pct, rcv, verdict)
