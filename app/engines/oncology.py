"""Oncology pharmacy module: plasma cfDNA/ctDNA report + germline PGx + TKI interactions.

The lab's own variant calls and tiers are shown as reported; this engine only adds the pharmacy
layer: CHIP and possible-germline flags, the "not detected" caveat, labeled targeted therapy for
EGFR T790M, TKI + acid-reducer interactions, and DPYD / UGT1A1 dosing before chemotherapy.
Sources: docs/research_oncology.md
"""

from dataclasses import asdict, dataclass, field

# canonical clonal-hematopoiesis genes (Razavi 2019 methods list)
CHIP_GENES = {"DNMT3A", "TET2", "ASXL1", "PPM1D", "TP53", "JAK2", "RUNX1", "SF3B1", "SRSF2", "IDH1", "IDH2",
              "U2AF1", "CBL", "ATM", "CHEK2"}
# cancer-susceptibility genes that need germline confirmation (Mandelker 2019)
GERMLINE_GENES = {"BRCA1", "BRCA2", "PALB2", "MLH1", "MSH2", "MSH6", "PMS2", "ATM", "CHEK2"}
PPIS = {"omeprazole", "esomeprazole", "lansoprazole", "pantoprazole", "rabeprazole", "dexlansoprazole"}
EGFR_TKIS = {"erlotinib", "gefitinib", "afatinib", "osimertinib"}
FLUOROPYRIMIDINES = {"capecitabine", "fluorouracil", "5-fu", "tegafur"}
UGT1A1_POOR = {"*28/*28", "*6/*6", "*6/*28", "*28/*6", "poor metabolizer"}


@dataclass
class Variant:
    gene: str
    variant: str
    vaf: float
    tier: str
    lab_note: str = ""
    flags: list[dict] = field(default_factory=list)


@dataclass
class OncoFinding:
    id: str
    severity: str  # stop | action | monitor | info
    title: str
    detail: str
    fact_ids: list[str]
    audience: str  # oncologist | pharmacist | genetics


def annotate_variants(report: dict) -> list[Variant]:
    out = []
    for v in report.get("variants", []):
        var = Variant(v["gene"], v["variant"], float(v["vaf"]), v.get("tier", "ไม่ระบุ"), v.get("lab_note", ""))
        if var.gene in CHIP_GENES:
            detail = ("TP53 พบได้ทั้งในเนื้องอกและจาก clonal hematopoiesis — ยืนยันที่มาด้วยการตรวจเม็ดเลือดขาวคู่กัน"
                      if var.gene == "TP53" else
                      "variant ในยีนนี้มักมาจาก clonal hematopoiesis ไม่ใช่เนื้องอก — ยืนยันด้วยการตรวจเม็ดเลือดขาวคู่กัน")
            var.flags.append({"id": "chip", "label": "อาจมาจากเม็ดเลือด (CHIP)", "detail": detail,
                              "fact_ids": ["RAZAVI-2019-CHIP"]})
        if var.gene in GERMLINE_GENES and (30 <= var.vaf <= 70 or var.vaf >= 90):
            var.flags.append({"id": "germline", "label": "อาจเป็นยีนที่ถ่ายทอดทางพันธุกรรม",
                              "detail": f"VAF {var.vaf:g}% ใกล้ 50% หรือ 100% — ส่งตรวจ germline ยืนยัน และส่งปรึกษา genetic counselling",
                              "fact_ids": ["MANDELKER-2019-GERMLINE", "LABEL-CTDNA-GERMLINE"]})
        out.append(var)
    return out


def assess_oncology(case: dict) -> dict:
    report = case["ctdna"]
    variants = annotate_variants(report)
    current = {m["drug"].lower() for m in case.get("meds", []) if m.get("status", "current") == "current"}
    planned = {m["drug"].lower() for m in case.get("meds", []) if m.get("status") == "planned"}
    everything = current | planned
    pgx = {k.upper(): str(v).strip() for k, v in case.get("pgx", {}).items()}
    findings: list[OncoFinding] = []

    if not variants:
        findings.append(OncoFinding("ctdna-negative", "action", "ctDNA ไม่พบ variant — ยังตัดออกไม่ได้",
                                    "ผลลบจากเลือดไม่ได้แปลว่าเนื้องอกไม่มี mutation ถ้าทำได้ควรส่งตรวจชิ้นเนื้อต่อ",
                                    ["LABEL-CTDNA-NEGATIVE"], "oncologist"))

    has_t790m = any(v.gene == "EGFR" and "T790M" in v.variant for v in variants)
    on_egfr_tki = current & EGFR_TKIS
    if has_t790m and on_egfr_tki - {"osimertinib"}:
        findings.append(OncoFinding("t790m-osimertinib", "action", "พบ EGFR T790M ระหว่างใช้ EGFR TKI",
                                    "osimertinib มีข้อบ่งใช้ตามฉลากสำหรับ EGFR T790M+ ที่โรคลุกลามหลังใช้ EGFR TKI — ให้แพทย์มะเร็งพิจารณา",
                                    ["LABEL-OSIMERTINIB-T790M"], "oncologist"))

    ppis = sorted(current & PPIS)
    if ppis and "erlotinib" in current:
        findings.append(OncoFinding("ddi-erlotinib-ppi", "action", f"Erlotinib + {', '.join(ppis)}",
                                    "PPI ลดระดับ erlotinib (AUC −46%) การเว้นระยะไม่ช่วย — เลี่ยง PPI ถ้าทำได้ ถ้าจำเป็นต้องลดกรด "
                                    "ใช้ H2RA โดยกิน erlotinib 10 ชม. หลัง และอย่างน้อย 2 ชม. ก่อน H2RA มื้อถัดไป",
                                    ["LABEL-ERLOTINIB-PPI"], "pharmacist"))
    if ppis and "gefitinib" in current:
        findings.append(OncoFinding("ddi-gefitinib-ppi", "action", f"Gefitinib + {', '.join(ppis)}",
                                    "เลี่ยง PPI ถ้าทำได้ ถ้าจำเป็นให้กิน gefitinib 12 ชม. หลัง หรือ 12 ชม. ก่อน PPI",
                                    ["LABEL-GEFITINIB-PPI"], "pharmacist"))
    if ppis and "osimertinib" in everything:
        findings.append(OncoFinding("osimertinib-ppi", "info", "Osimertinib กับยาลดกรด",
                                    "omeprazole ไม่เปลี่ยนระดับ osimertinib — ถ้าเปลี่ยนเป็น osimertinib ปัญหายาลดกรดนี้หมดไป",
                                    ["LABEL-OSIMERTINIB-PPI"], "pharmacist"))

    fp = sorted(everything & FLUOROPYRIMIDINES)
    if fp:
        drug = ", ".join(fp)
        dpyd = pgx.get("DPYD")
        score = None
        if dpyd:
            try:
                score = float(dpyd.split()[0])
            except ValueError:
                score = None
        if not dpyd:
            findings.append(OncoFinding("dpyd-untested", "action", f"{drug} — ยังไม่มีผล DPYD",
                                        "ส่งตรวจ DPYD ก่อนเริ่มยา เว้นแต่ต้องเริ่มรักษาทันที",
                                        ["LABEL-DPYD-TESTING"], "pharmacist"))
        elif score is not None and score <= 0.5:
            findings.append(OncoFinding("dpyd-poor", "stop", f"{drug} — DPYD activity score {score:g}",
                                        "CPIC: หลีกเลี่ยง 5-FU และยาในกลุ่มเดียวกัน (Strong)", ["CPIC-DPYD-2017"], "oncologist"))
        elif score == 1:
            findings.append(OncoFinding("dpyd-im", "action", f"{drug} — DPYD activity score 1",
                                        "CPIC: ลดขนาดเริ่มต้น 50% แล้วปรับตามอาการข้างเคียง (Strong)", ["CPIC-DPYD-2017"], "pharmacist"))
        elif score == 1.5:
            findings.append(OncoFinding("dpyd-im", "action", f"{drug} — DPYD activity score 1.5",
                                        "CPIC: ลดขนาดเริ่มต้น 25–50% แล้วปรับตามอาการข้างเคียง (Moderate)", ["CPIC-DPYD-2017"], "pharmacist"))

    if "irinotecan" in everything and pgx.get("UGT1A1", "").lower() in {x.lower() for x in UGT1A1_POOR}:
        findings.append(OncoFinding("ugt1a1-irinotecan", "action", f"Irinotecan — UGT1A1 {pgx['UGT1A1']}",
                                    "ฉลากยา: พิจารณาลดขนาดเริ่มต้นอย่างน้อย 1 ระดับ และติดตามเม็ดเลือดขาวต่ำใกล้ชิด",
                                    ["LABEL-IRINOTECAN-UGT1A1"], "pharmacist"))

    for v in variants:
        for f in v.flags:
            sev = "action" if f["id"] == "germline" else "monitor"
            findings.append(OncoFinding(f"flag-{f['id']}-{v.gene}", sev, f"{v.gene} {v.variant} — {f['label']}", f["detail"],
                                        f["fact_ids"], "genetics" if f["id"] == "germline" else "oncologist"))

    order = {"stop": 0, "action": 1, "monitor": 2, "info": 3}
    findings.sort(key=lambda f: order[f.severity])
    return {"variants": [asdict(v) for v in variants], "findings": [asdict(f) for f in findings]}
