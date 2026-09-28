"""Rule-based lifestyle advice. Each rule: trigger -> advice text (Thai) -> fact ids."""

from dataclasses import dataclass

from app.engines.risk import Profile


@dataclass
class Advice:
    id: str
    topic: str
    reason: str
    advice: str
    fact_ids: list[str]


def lifestyle_advice(
    p: Profile,
    labs: dict[str, float],
    alcohol_drinks_per_day: float = 0,
    activity_min_week: float | None = None,
) -> list[Advice]:
    """labs: analyte id -> value in panel units (ldl_c, tg, glucose in mmol/L)."""
    out = []
    if p.smoker:
        out.append(Advice("smoking", "บุหรี่", "สูบบุหรี่",
                          "เลิกสูบบุหรี่ หรือส่งต่อคลินิกเลิกบุหรี่ (รวมบุหรี่ไฟฟ้า)", ["RCPT-2024-SMOKING"]))

    bmi = p.bmi
    big_waist = p.waist_cm is not None and p.waist_cm >= (90 if p.male else 80)
    if (bmi is not None and bmi >= 23) or big_waist:
        why = []
        if bmi is not None and bmi >= 23:
            why.append(f"BMI {bmi:.1f} (เกณฑ์ไทยปกติ 18.5–22.9)")
        if big_waist:
            why.append(f"รอบเอว {p.waist_cm:g} ซม. (เกณฑ์ < {90 if p.male else 80})")
        out.append(Advice("weight", "น้ำหนัก", ", ".join(why),
                          "ลดน้ำหนักให้ BMI และรอบเอวเข้าเกณฑ์ (รอบเอวไม่เกินครึ่งหนึ่งของส่วนสูง)", ["THAI-OBESITY"]))

    glucose = labs.get("glucose")
    if glucose is not None and 5.6 <= glucose < 7.0 and not p.diabetes:
        out.append(Advice("prediabetes", "น้ำตาล", f"กลูโคส {glucose:.1f} mmol/L (ช่วง prediabetes 5.6–6.9)",
                          "ลดน้ำหนักอย่างน้อย 5–7% และออกกำลังกายระดับปานกลาง ≥ 150 นาที/สัปดาห์ "
                          "(ค่านี้มาจาก NMR ไม่ใช่ FPG มาตรฐาน — ยืนยันด้วย FPG/HbA1c)",
                          ["ADA-2026-DX", "ADA-2026-PREV"]))

    ldl = labs.get("ldl_c")
    if ldl is not None and ldl >= 3.4:  # 130 mg/dL
        out.append(Advice("ldl_diet", "อาหาร — ไขมัน", f"LDL-C {ldl:.2f} mmol/L",
                          "ลดไขมันอิ่มตัวให้ < 7% ของพลังงาน ใช้น้ำมันไม่อิ่มตัวแทน เลี่ยงไขมันทรานส์ เพิ่มใยอาหาร",
                          ["RCPT-2024-DIET"]))

    tg = labs.get("tg")
    if tg is not None and tg >= 1.7:  # 150 mg/dL
        out.append(Advice("tg_diet", "อาหาร — ไตรกลีเซอไรด์", f"TG {tg:.2f} mmol/L (≥ 1.7)",
                          "งดเครื่องดื่มแอลกอฮอล์ ลดคาร์โบไฮเดรต น้ำตาล < 10% ของพลังงาน", ["RCPT-2024-TG"]))

    if p.hypertension or (p.sbp is not None and p.sbp >= 130):
        out.append(Advice("sodium", "เกลือ", f"ความดันตัวบน {p.sbp:g} mmHg" if p.sbp else "มีโรคความดัน",
                          "โซเดียมไม่เกิน 2 กรัม/วัน (ประมาณเกลือ 1 ช้อนชา หรือน้ำปลา/ซีอิ๊ว 3 ช้อนชา)",
                          ["THAI-HT-2024-NA"]))

    limit = 2 if p.male else 1
    if alcohol_drinks_per_day > limit or (tg is not None and tg >= 1.7 and alcohol_drinks_per_day > 0):
        out.append(Advice("alcohol", "แอลกอฮอล์", f"ดื่ม {alcohol_drinks_per_day:g} ดื่มมาตรฐาน/วัน",
                          f"ไม่เกิน {limit} ดื่มมาตรฐาน/วัน และมีวันที่ไม่ดื่ม (ถ้า TG สูงควรงด)",
                          ["THAI-HT-2024-ALC"]))

    if activity_min_week is None or activity_min_week < 150:
        now = "ไม่ทราบ" if activity_min_week is None else f"{activity_min_week:g} นาที/สัปดาห์"
        out.append(Advice("activity", "ออกกำลังกาย", f"ตอนนี้ {now}",
                          "ออกกำลังกายแบบแอโรบิกระดับปานกลาง 150–300 นาที/สัปดาห์ + เวทเทรนนิ่ง ≥ 2 วัน/สัปดาห์",
                          ["WHO-PA-2020"]))
    return out
