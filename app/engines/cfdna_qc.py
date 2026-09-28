"""cfDNA electropherogram (capillary electrophoresis) — pre-analytical QC + research-only fragment metrics.

What this does NOT do: call cancer. Fragment-size-only profiles from CE are not a validated cancer
screening test; validated fragmentomics (e.g. DELFI) uses genome-wide sequencing. So the output is
"sample quality" (can this sample be sent for ctDNA sequencing?) plus a clearly labelled RUO number.
"""

from dataclasses import asdict, dataclass, field


@dataclass
class CfdnaQC:
    main_peak_bp: float
    di_peak_bp: float | None
    mono_fraction: float  # 100–250 bp share of signal
    short_fraction: float  # 90–150 bp share of the 90–250 bp region (RUO)
    hmw_fraction: float  # >700 bp share of signal (genomic DNA from lysed leukocytes)
    concentration_ng_ul: float | None
    status: str  # pass | warning | fail
    findings: list[dict] = field(default_factory=list)


def _area(sizes, rfu, lo, hi):
    return sum(r for s, r in zip(sizes, rfu) if lo <= s < hi)


def analyse(sizes: list[float], rfu: list[float], concentration: float | None) -> dict:
    # subtract instrument baseline (10th percentile of the trace) so noise does not accumulate as "HMW"
    base = sorted(rfu)[len(rfu) // 10] if rfu else 0
    rfu = [max(0.0, r - base) for r in rfu]
    total = sum(rfu) or 1
    main = max(zip(sizes, rfu), key=lambda x: x[1] if 100 <= x[0] <= 250 else -1)[0]
    di_candidates = [(s, r) for s, r in zip(sizes, rfu) if 280 <= s <= 400]
    di = max(di_candidates, key=lambda x: x[1])[0] if di_candidates else None
    mono = _area(sizes, rfu, 100, 250) / total
    core = _area(sizes, rfu, 90, 250) or 1
    short = _area(sizes, rfu, 90, 150) / core
    hmw = _area(sizes, rfu, 700, 1e9) / total
    findings = []
    status = "pass"
    if hmw > 0.20:
        status = "fail"
        findings.append({"id": "cfdna-hmw", "severity": "action", "title": "ปนเปื้อน DNA จากเม็ดเลือดขาว (fragment > 700 bp)",
                         "detail": f"สัญญาณ > 700 bp {hmw:.0%} ของทั้งหมด — ตัวอย่างอาจไม่เหมาะส่งตรวจ ctDNA ควรเก็บเลือดใหม่ด้วยหลอด cfDNA และปั่นแยกพลาสมาตามเวลา",
                         "fact_ids": ["CFDNA-HMW-QC"]})
    elif hmw > 0.10:
        status = "warning"
        findings.append({"id": "cfdna-hmw", "severity": "monitor", "title": "มี DNA ขนาดใหญ่ปนเล็กน้อย",
                         "detail": f"สัญญาณ > 700 bp {hmw:.0%} — ตรวจขั้นตอนเก็บตัวอย่าง", "fact_ids": ["CFDNA-HMW-QC"]})
    if not 155 <= main <= 180:
        status = "warning" if status == "pass" else status
        findings.append({"id": "cfdna-peak", "severity": "monitor", "title": f"จุดยอดหลักที่ {main:.0f} bp ไม่อยู่ในช่วงปกติของ cfDNA",
                         "detail": "cfDNA ปกติมีจุดยอดประมาณ 166–167 bp (หนึ่งนิวคลีโอโซม)", "fact_ids": ["CFDNA-NUCLEOSOME"]})
    findings.append({"id": "cfdna-short-ruo", "severity": "info", "title": f"สัดส่วน fragment สั้น 90–150 bp: {short:.0%} (RUO)",
                     "detail": "ค่าสำหรับงานวิจัยเท่านั้น — fragment สั้นพบมากขึ้นใน DNA จากเนื้องอก แต่การวัดขนาดด้วย CE อย่างเดียวยังไม่ใช่การคัดกรองมะเร็งที่ validate แล้ว ไม่ใช้ตัดสินใจทางคลินิก",
                     "fact_ids": ["CFDNA-SHORT-FRAGMENTS", "CFDNA-FRAGMENTOMICS-SEQ"]})
    qc = CfdnaQC(main, di, round(mono, 3), round(short, 3), round(hmw, 3), concentration, status, findings)
    return asdict(qc)
