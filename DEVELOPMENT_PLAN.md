# PrecisionRx — แผนพัฒนาต่อ (branch `dev/prototype`)

> ต่อจาก commit `16d3e06` (idea v3 + research + judge skills)
> สถานะ: **ยืนยันแล้ว — เริ่มทำ** · demo หน้าแรก = NMR Response Dashboard (§0) · PGx ตอนสั่งยาเป็นส่วนที่สอง

---

## 0. ตัดสินใจล่าสุด: หน้าแรกของ demo = NMR Response Dashboard

ไอเดียจากทีม (28 ก.ย. 2026) ปรับให้เข้ากับหลักของ v3 (ทุก output มีแหล่ง, ไม่คิดสูตรความเสี่ยงเอง, ใช้ RCV)

```
[1] ซ้าย: ผล NMR (อัปโหลด CSV หรือเลือกเคสตัวอย่าง)
    → ภาพ spectrum จำลอง + แท่งปริมาณสารแต่ละตัวค่อย ๆ ขึ้นแบบ auto
    → แต่ละสาร: ค่าจริง + หน่วย + ช่วงอ้างอิง   (ติดป้าย SYNTHETIC / RUO)
[2] ขวา: ฟอร์มประวัติ — อายุ เพศ น้ำหนัก ส่วนสูง รอบเอว BP สูบบุหรี่ เบาหวาน ความดัน
    ประวัติครอบครัว, ยาที่ใช้ + ขนาด + ความสม่ำเสมอ (PDC), ผล PGx (ถ้ามี)
        ▼
[3] ผลลัพธ์ (ทุกข้อมี fact ID + แหล่ง + ระดับหลักฐาน)
    ├─ ความเสี่ยงรายโรค: คะแนนที่ validate แล้ว (Thai CV risk, Thai diabetes risk score)
    │    + "ปัจจัยเสริมจาก NMR" (ApoB/LDL-P discordance, GlycA, BCAA) แยกให้เห็น ไม่ผสมเข้าคะแนน
    ├─ เรื่องยา → คิวเภสัชกร (statin ลด LDL ได้ตามคาดไหม, adherence, PGx, DDI)
    └─ คำแนะนำการดูแลตัวเอง / ปรับพฤติกรรม (rule-based อิง guideline)
        ▼
[4] ตรวจครั้งใหม่: เทียบกับครั้งก่อนด้วย RCV → "ดีขึ้นจริง / แย่ลงจริง / ยังอยู่ในความแปรปรวนปกติ"
    + เช็ก adherence ก่อนสรุปว่ายาไม่ได้ผล
```

Stack ที่ใช้: Python + FastAPI (engines + API) · UI = Astro 7 + Svelte 5 islands (`web/`) · pytest

### สถานะ (28 ก.ย. 2026)

| ส่วน | สถานะ |
|---|---|
| หน้า NMR: spectrum จำลอง + แท่งปริมาณสาร 28 ตัวขึ้นแบบ auto + ช่วงอ้างอิง + ค่าครั้งก่อน | ✅ |
| ฟอร์มประวัติ / ยา / PDC / PGx | ✅ |
| ความเสี่ยงรายโรค: Thai CV Risk (สูตรจาก calculator รามาฯ) + Thai Diabetes Risk Score | ✅ test ตรงกับตัวอย่างคำนวณ |
| ปัจจัยเสริม NMR: ApoB discordance, LDL-P discordance, GlycA, BCAA, omega-3 | ✅ แยกจากคะแนน ติดป้าย EMERGING |
| เรื่องยา: HLA-B hard stop, SLCO1B1–simvastatin, CYP2C19–PPI/clopidogrel, clopidogrel+PPI, statin response, LDL target, adherence | ✅ |
| คำแนะนำพฤติกรรม 8 rules | ✅ |
| เทียบครั้งก่อนด้วย RCV (สารที่ไม่มี CVi → "ประเมินไม่ได้") | ✅ |
| อัปโหลด CSV เป็นผลตรวจครั้งใหม่ | ✅ |
| ปุ่ม Why? + fact chip แสดงแหล่ง | ✅ |
| Test | ✅ 43 ผ่าน (รวม eval gate + CDS Hooks) |
| UI ใหม่ด้วย Astro: หน้าภาพรวม + dashboard + HIS + คิว, light/dark, mobile, axe-core 0 violation ทั้ง 4 หน้า (WCAG 2.1 AA) | ✅ |
| ตรวจถ้อยคำ guideline กับต้นฉบับ | ✅ ทุก fact ที่ระบบอ้าง `verified: true` (CPIC PDF, FDA label 2026, ACR 2020) |
| Mock HIS หน้าสั่งยา + CDS Hooks service (order-select / order-sign / feedback) + คิวเภสัชกร | ✅ `/his`, `/queue` — เตือนเฉพาะที่เกิดจากคำสั่งใหม่, hard stop บล็อก sign, override ต้องมีเหตุผล |
| Eval set 46 เคส + harness + review sheet | ✅ 46/46, omission 0, false flag 0, alert −71% (`eval/`) — รอเภสัชกรตรวจเฉลย |
| Oncology module | ⏳ ยังไม่ทำ |
| LLM summarizer + verifier | ⏳ ยังไม่ทำ |

**ข้อควรระวังที่ต้องพูดบนเวที:** ช่วงอ้างอิง NMR = UK Biobank P10–P90 (ไม่ใช่คนไทย ไม่ใช่ค่าทางคลินิก) · หลักฐาน NMR → โรค เป็นระดับ association · ค่า CVi ของ LDL-P/BCAA ยังหาไม่พบ · clopidogrel rule ใช้กับ ACS/PCI (ระบบยังไม่รู้ข้อบ่งใช้ — แสดงคำแนะนำแยกตามข้อบ่งใช้ในข้อความ) · ตัวเลขอ้างอิงทั้งหมดอยู่ใน `docs/`

---

## 1. สรุปงานที่มีอยู่

| ส่วน | สถานะ |
|---|---|
| ไอเดีย | v3 (`idea.md`) ผ่านการแก้มาแล้ว 2 รอบ: เดิมเป็น "multi-agent รวม 3 omics" → ตอนนี้คือ **PGx เตือนตอนสั่งยาใน HIS (Module A)** + **Oncology pharmacy module: cfDNA + DPYD/UGT1A1 + TKI DDI (Module B)** |
| Research | market, business strategy, business case, idea validation, critique ครบ |
| Judge skills | 7 skills ใน `.claude/skills/` ใช้รีวิวซ้ำได้ |
| **โค้ด / prototype** | **ยังไม่มีเลย** |
| Synthetic data / eval set | ยังไม่มี |
| Pitch deck | ยังไม่มี |
| Checklist §14 ใน idea.md | ยังไม่ได้ตรวจ 9 ข้อ |

**ช่องว่างหลัก:** เอกสารแข็งแรงมาก แต่ roadmap แถว "Hackathon" (Module A + B บน synthetic data, 4 demo case, eval 30–50 เคส) ยังไม่ได้ทำเลย และ critique/validation ทั้งหมดประเมิน v2 — ยังไม่มีใครรีวิว v3

---

## 2. สิ่งที่จะพัฒนา (เรียงตามลำดับความสำคัญ)

### P0 — Prototype ที่ demo ได้ (แกนของ hackathon)

**2.1 Deterministic PGx engine**
- Input: diplotype/phenotype ต่อยีน (HLA-B, CYP2C19, SLCO1B1, CYP2C9, DPYD, UGT1A1) — ไม่รับ VCF ในรอบแรก
- Rule table เป็นไฟล์ข้อมูล (JSON/YAML) ที่มี `fact_id`, แหล่ง (CPIC 2022 ฯลฯ), ระดับหลักฐาน, ถ้อยคำคำแนะนำ
- ครอบคลุม 10 สถานการณ์ใน `idea.md` §3
- Alert filter: แสดงเฉพาะ finding ที่มี action → นับ "alert ที่ถูกซ่อน" เพื่อโชว์การลด noise
- Unit test ทุก rule
- PharmCAT: ใส่เป็น adapter ทีหลัง (ต้องใช้ Java + VCF) — บนเวทีพูดได้ว่า "engine เปลี่ยนเป็น PharmCAT ได้"

**2.2 DDI rules เฉพาะที่ใช้ใน demo**
- clopidogrel + omeprazole/esomeprazole, gefitinib/erlotinib + PPI (จากฉลากยา)

**2.3 CDS Hooks service (mock)**
- Endpoint `order-select` / `order-sign` รับ FHIR `MedicationRequest` + context คนไข้ → คืน card
- HLA-B = hard stop, อย่างอื่น = card แนะนำ, override ต้องใส่เหตุผลและส่งเข้าคิวเภสัชกร

**2.4 หน้าจอ 2 หน้า**
- **Mock หน้าสั่งยา (HIS)**: เลือกคนไข้ → พิมพ์ชื่อยา → card เด้ง (ตาม §7.1)
- **คิวเภสัชกร**: ACTION NEEDED / MONITOR / NO ACTION + Accept/Modify/Reject (ตาม §7.2)
- ปุ่ม **"Why?"** แสดง trace จริง: ข้อสรุป → rule → fact_id → ข้อมูลคนไข้ → แหล่ง

**2.5 Synthetic patients**
- 4 demo case (A–D ใน §8) เป็น FHIR bundle, ติดป้าย SYNTHETIC ทุกหน้าจอ

### P1 — หลักฐานว่าระบบถูก (คะแนน technical + validity)

**2.6 Gold-standard eval set + harness**
- 30–50 เคส synthetic ครอบคลุม 10 สถานการณ์ + เคสที่ไม่ควรเตือน (negative control)
- สคริปต์คำนวณ: critical-omission rate, false-flag rate, concordance กับ CPIC, alert ต่อเคสเทียบ "เตือนทุกอย่าง", citation precision
- ต้องมีเภสัชกร 2–3 คนเฉลย (งานคน ไม่ใช่โค้ด) — ระหว่างนี้ใช้เฉลยจาก rule table ติดป้ายว่า "ยังไม่ผ่านเภสัชกร"

**2.7 Oncology module (Module B)**
- รับ structured ctDNA report (gene, variant, VAF, tier)
- Flag: CHIP (DNMT3A/TET2/ASXL1), possible germline (VAF ~50%/~100%), "not detected ≠ ไม่มี", DPYD/UGT1A1 ก่อน capecitabine/irinotecan, TKI + PPI
- ใช้ tier จากข้อมูลในเคส ไม่เรียก OncoKB จริง (ติด license)

### P2 — ส่วนเสริม

**2.8 LLM summarizer + verifier**
- Summarizer เขียน brief ภาษาไทยจาก list ของ fact_id เท่านั้น
- Verifier (โค้ด) เช็กว่าทุกประโยคอ้าง fact_id ที่มีจริง ตัดประโยคที่ไม่มี
- ถ้าไม่มี API key → fallback เป็น template ให้ demo รันได้เสมอ

**2.9 Response module (ระยะ 2)**: RCV + PDC — เป็นสูตร deterministic ทำได้เร็ว ใช้กับเคส C

**2.10 Q&A agent** — ทำเป็นอย่างสุดท้าย หรือไม่ทำ (เสี่ยงที่สุดบนเวที)

### งานที่ไม่ใช่โค้ด (ทำคู่ขนาน)

- [ ] รัน `judge-panel` กับ `idea.md` v3 → `critique_v3.md` (ยังไม่มีใครรีวิว v3)
- [ ] ตรวจ checklist §14 ใน `idea.md` (ถ้อยคำ CPIC PPI, ESC/EAS 2025, ผูกพันธุ์ API, HOSxP PGx field, EFLM CVi ฯลฯ)
- [ ] สคริปต์สัมภาษณ์เภสัชกร 5–10 คน
- [ ] Pitch deck 3 นาที (โครงอยู่ใน `business_strategy.md` §8)

---

## 3. Stack ที่เสนอ

| ชั้น | เลือก | เหตุผล |
|---|---|---|
| Backend / engines | **Python + FastAPI** | ทีม health/bio คุ้นเคย, test ง่าย (pytest), ทำ CDS Hooks endpoint ได้ตรง ๆ |
| ข้อมูล rule/evidence | JSON/YAML ใน repo (versioned) | ตรงกับหลัก "evidence snapshot มี version" |
| FHIR | `fhir.resources` (pydantic) | validate bundle ของเคส synthetic |
| Frontend | **หน้าเว็บเดียวแบบเบา** (HTML + htmx หรือ React/Vite) | demo ต้องเร็วและไม่พัง |
| LLM (P2) | Claude API ผ่าน env var, มี template fallback | |
| Test / eval | pytest + `eval/run_eval.py` | |

โครงโฟลเดอร์ที่เสนอ:
```
app/
  engines/      pgx.py, ddi.py, oncology.py, response.py, alert_filter.py
  evidence/     rules_pgx.yaml, rules_ddi.yaml, sources.yaml
  cds_hooks/    service.py
  web/          ordering.html, pharmacist_queue.html
data/synthetic/ case_A.json … case_D.json
eval/           cases/, run_eval.py
tests/
```

---

## 4. ลำดับการทำ (milestones)

| # | งาน | ผลลัพธ์ที่เห็นได้ |
|---|---|---|
| M1 | Scaffold + PGx engine + rule table + unit test | `pytest` ผ่าน, เคส A และ B ให้ finding ถูก |
| M2 | CDS Hooks service + mock หน้าสั่งยา | demo เคส A (hard stop) ได้ |
| M3 | คิวเภสัชกร + ปุ่ม Why? | demo เคส B ได้ |
| M4 | Oncology module | demo เคส D ได้ |
| M5 | Eval set 30–50 เคส + harness | ตัวเลข metric สำหรับสไลด์ |
| M6 | Response module (RCV/PDC) + LLM summarizer + verifier | demo เคส C + brief ภาษาไทย |

ถ้าเวลาน้อย: M1–M3 + M5 คือขั้นต่ำที่พิตช์ได้ (เคส A + B + ตัวเลข eval)

---

## 5. ความเสี่ยง / ข้อควรระวัง

- **ถ้อยคำ CPIC** ใน rule table ต้องคัดจากแหล่งจริง ห้ามแต่งเอง — ข้อไหนยังไม่ได้ตรวจ ติด `verified: false` และแสดงบนหน้าจอ
- **Synthetic เท่านั้น** — ห้ามใช้ข้อมูลคนไข้จริงจนกว่าจะผ่าน IRB
- **ห้าม claim ความแม่นยำ** จาก eval synthetic ว่าเป็นผลทางคลินิก
- OncoKB / DDI database เชิงพาณิชย์ต้องมี license → ใช้ข้อมูลที่เขียนในเคสเองเท่านั้น

---

## 6. คำถามที่ต้องตัดสินใจก่อนเริ่ม

1. Hackathon วันไหน เหลือเวลาเท่าไร และมี rubric จริงไหม (จะได้ตัด scope ให้พอดี)
2. ทีมถนัด stack อะไร (Python/JS) — ถ้าไม่มีความเห็นจะใช้ตามข้อ 3
3. จะทำ Module B (oncology) ใน prototype ด้วยไหม หรือทำ Module A ให้แน่นก่อน
4. มีเภสัชกรในทีม/คนรู้จักที่ช่วยเฉลย eval set ได้ไหม
