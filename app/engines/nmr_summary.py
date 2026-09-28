"""Plain-language NMR summary: 28 analytes -> 6 health domains, each with one key marker.

Deterministic templates only (no LLM). Status uses the same reference bands as the panel,
ADA cut-points for glucose and the ESC ApoB secondary target for the atherogenic domain.
"""

from dataclasses import asdict, dataclass, field

from app.engines.drug_effects import moved_by
from app.engines.panel import catalog, status
from app.engines.rcv import compare

# status tones: good | warning | serious | none
STATUS_LABEL = {"good": "อยู่ในเกณฑ์", "warning": "ควรติดตาม", "serious": "ควรดูแล", "none": "ไม่มีข้อมูล"}
TREND_TH = {
    "improved": "ดีขึ้นจริง", "worsened": "แย่ลงจริง",
    "within_variation": "เท่าเดิม (ไม่เกินความแปรปรวนปกติ)", "changed": "เปลี่ยนจริง",
    "not_assessable": "บอกไม่ได้ว่าเปลี่ยนจริงไหม",
}

DOMAINS = [
    {"id": "atherogenic", "title": "ไขมันที่ทำให้หลอดเลือดแข็ง", "key": "apob",
     "members": ["apob", "ldl_c", "non_hdl_c", "ldl_p", "s_ldl_p", "vldl_p", "remnant_c", "tg", "total_c"],
     "what": "อนุภาคไขมันที่เข้าไปสะสมในผนังหลอดเลือด ยิ่งต่ำยิ่งดี"},
    {"id": "protective", "title": "ไขมันดี", "key": "hdl_c", "members": ["hdl_c", "apoa1", "hdl_p"],
     "what": "ช่วยขนไขมันออกจากหลอดเลือด"},
    {"id": "glucose", "title": "น้ำตาลและการเผาผลาญ", "key": "glucose",
     "members": ["glucose", "bcaa", "leucine", "isoleucine", "valine", "lactate", "citrate"],
     "what": "ระดับน้ำตาล และกรดอะมิโนที่สัมพันธ์กับความเสี่ยงเบาหวาน"},
    {"id": "inflammation", "title": "การอักเสบในร่างกาย", "key": "glyca", "members": ["glyca"],
     "what": "สัญญาณการอักเสบเรื้อรัง ขึ้นได้ชั่วคราวเมื่อติดเชื้อ"},
    {"id": "fatty_acids", "title": "กรดไขมันจากอาหาร", "key": "omega3_pct",
     "members": ["omega3_pct", "dha", "pufa_mufa", "phenylalanine"],
     "what": "สะท้อนการกินปลาและไขมันดีในอาหาร"},
    {"id": "kidney", "title": "ไตและสมดุลน้ำ", "key": "creatinine",
     "members": ["creatinine", "albumin", "bohb", "acetone"],
     "what": "ค่าพื้นฐานของไต โปรตีนในเลือด และสารคีโตน"},
]


@dataclass
class KeyMarker:
    id: str
    abbr: str
    name: str
    unit: str
    value: float
    ref_low: float | None
    ref_high: float | None
    target: float | None  # guideline target shown on the gauge, if any
    previous: float | None
    pct_change: float | None
    verdict: str | None


@dataclass
class Domain:
    id: str
    title: str
    what: str
    status: str
    status_label: str
    headline: str
    key: KeyMarker | None
    out_of_range: list[str] = field(default_factory=list)
    fact_ids: list[str] = field(default_factory=list)
    drug_note: str | None = None  # "ค่านี้ถูกยา X ลดลง" when a regular drug moves the domain's markers
    drugs: list[str] = field(default_factory=list)


def _fmt(v: float) -> str:
    a = abs(v)
    return f"{v:.0f}" if a >= 100 else f"{v:.1f}" if a >= 10 else f"{v:.2f}"


def _unfavourable(aid: str, v: float) -> bool:
    """Outside the band in the direction that matters (a low value is fine when lower is better)."""
    st, better = status(aid, v), catalog()[aid].get("better")
    if st == "normal":
        return False
    return not ((better == "lower" and st == "low") or (better == "higher" and st == "high"))


DIR_TH = {"down": "ลดลง", "up": "เพิ่มขึ้น"}


def _drug_note(members: list[str], key: str, moved: dict[str, list[dict]]) -> tuple[str | None, list[str], list[str]]:
    hits = {}
    for m in members:
        for e in moved.get(m, []):
            hits.setdefault(e["drug"], (e["direction"], e["fact_ids"]))
    if not hits:
        return None, [], []
    parts = [f"{d} ทำให้ค่าในหัวข้อนี้{DIR_TH[dr]}" for d, (dr, _) in hits.items()]
    note = " · ".join(parts)
    if any(e["direction"] == "down" for e in moved.get(key, [])):
        note += " — ค่าที่เห็นเป็นค่าระหว่างใช้ยา ความเสี่ยงก่อนรักษาสูงกว่านี้"
    facts = sorted({f for _, fs in hits.values() for f in fs})
    return note, list(hits), facts


def summarize(cur: dict[str, float], prev: dict[str, float] | None, *, diabetes: bool, high_risk: bool,
              drugs: list[str] | None = None) -> list[dict]:
    cat = catalog()
    moved = moved_by(drugs or [])
    out = []
    for d in DOMAINS:
        k = d["key"]
        members = [m for m in d["members"] if m in cur and m in cat]
        oor = [cat[m]["abbr"] for m in members if _unfavourable(m, cur[m])]
        facts = ["UKB-NMR-REF"]
        if k not in cur:
            out.append(asdict(Domain(d["id"], d["title"], d["what"], "none", STATUS_LABEL["none"],
                                     "ไม่มีค่าหลักของหัวข้อนี้ในผลตรวจ", None, oor, facts)))
            continue
        a, v = cat[k], cur[k]
        p = prev.get(k) if prev else None
        ch = compare(p, v, a.get("cva"), a.get("cvi"), a.get("better")) if p else None
        target = None

        if d["id"] == "atherogenic":
            target = 0.80 if high_risk else 1.00  # ESC secondary ApoB target, g/L
            st = "serious" if v >= target and status(k, v) == "high" else "warning" if v >= target else "good"
            head = f"{'สูงกว่า' if v >= target else 'ต่ำกว่า'}เป้า ApoB {target * 100:.0f} mg/dL (ตอนนี้ {v * 100:.0f})"
            facts.append("ESC-2019-APOB")
        elif d["id"] == "glucose":
            if v >= 7.0:
                st, head = "serious", "อยู่ในช่วงเบาหวาน" + (" (ทราบว่าเป็นเบาหวานแล้ว)" if diabetes else " — ยืนยันด้วย FPG/HbA1c")
            elif v >= 5.6:
                st, head = "warning", "ช่วงก่อนเบาหวาน — ยืนยันด้วย FPG/HbA1c"
            else:
                st, head = "good", "อยู่ในเกณฑ์ปกติ"
            facts.append("ADA-2026-DX")
        else:
            st = "warning" if _unfavourable(k, v) else "good"
            head = {"normal": "อยู่ในช่วงปกติ", "high": "สูงกว่าช่วงปกติ", "low": "ต่ำกว่าช่วงปกติ"}[status(k, v)]

        # other members out of range raise a "good" domain to "warning"
        others = [x for x in oor if x != a["abbr"]]
        if st == "good" and others:
            st = "warning"
        if ch and ch.verdict:
            head += f" · เทียบครั้งก่อน: {TREND_TH[ch.verdict]}"
            if ch.verdict in {"improved", "worsened", "changed"}:
                head += f" {ch.pct_change:+.0f}%"
            facts.append("RCV-METHOD")
        key = KeyMarker(k, a["abbr"], a["name"], a["unit"], v, a.get("ref_low"), a.get("ref_high"), target,
                        p, None if ch is None else round(ch.pct_change, 1), None if ch is None else ch.verdict)
        note, drug_names, drug_facts = _drug_note(members, k, moved)
        facts += drug_facts
        out.append(asdict(Domain(d["id"], d["title"], d["what"], st, STATUS_LABEL[st], head, key, oor, facts, note, drug_names)))
    return out
