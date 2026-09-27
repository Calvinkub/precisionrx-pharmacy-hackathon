# PrecisionRx — PGx ที่เตือนตอนสั่งยา + Oncology cfDNA Module

> **เวอร์ชัน 3** — รวมผลจาก `critique_PrecisionRx.md`, `market_research.md`, `business_strategy.md`, `business_case.md`, `idea_validation.md`
> ประวัติ: `idea_v1_original.md` (ไอเดียแรก) · `idea_v2.md` (แก้ตามกรรมการรอบแรก)
>
> **สถานะจริง:** ยังไม่มีบริษัท ไม่มีโรงพยาบาลหรือ lab ที่เป็นพาร์ทเนอร์ ไม่มี LOI ไม่มีข้อมูลคนไข้จริง ไม่มีรายได้ ตัวเลขที่ไม่มีแหล่งอ้างอิงเป็นสมมติฐานทั้งหมด (📊)
> สัญลักษณ์: ✅ มีแหล่งยืนยัน · 🟡 แหล่งทุติยภูมิ · 📊 สมมติฐาน · ❓ ยังยืนยันไม่ได้

---

## 0. เปลี่ยนอะไรจาก v2 และทำไม

| v2 | v3 | เหตุผล (จากรายงาน) |
|---|---|---|
| หน้าจอเภสัชกรแยก รวม 3 omics | **PGx เตือนใน HIS ตอนสั่ง/จ่ายยา** + คิวให้เภสัชกรทบทวน | ไต้หวัน: เตือน HLA-B\*15:02 ในระบบสั่งยา เพิ่มอัตราตรวจจาก 23.7% เป็น 55.6% ✅ หน้าจอแยกได้ผลแบบนี้ยาก |
| NMR เป็น data layer หลัก | **Response module ระยะ 2**: เริ่มจาก ApoB ของ lab ปกติ + RCV, NMR เมื่อมี lab คลินิก | ยังไม่พบ lab NMR ทางคลินิกในไทย ❓ Bruker B.I.-LISA ขายสถานะ research only ✅ |
| cfDNA อยู่ในหน้าจอเดียวกับทุกอย่าง | **Oncology module แยก**: ctDNA + germline DPYD/UGT1A1 + DDI ของยา TKI | เป็นจุดเดียวที่การรวมข้อมูลหลายชนิดให้การตัดสินใจใหม่จริงทางคลินิก |
| เปิด demo ด้วย clopidogrel | เปิดด้วย **HLA-B hard stop** และ **CYP2C19–PPI** | clopidogrel alert ถูกยอมรับต่ำสุดใน 6 คู่ยีน-ยา บางงาน 22% ✅; ผู้ใช้ omeprazole ไทย 55% มี CYP2C19 actionable ✅ |
| "DDI checker ไม่มี PGx" | แก้: Lexidrug มี PGx แล้ว | ✅ market research |
| ไม่รู้จัก ผูกพันธุ์ / PharmCAT | **ใช้ผูกพันธุ์เป็นแหล่งข้อมูล, PharmCAT เป็น engine** | เปลี่ยนคู่แข่งรัฐเป็น data source; engine PGx ไม่ใช่ moat |
| ตัวเลขหลายจุด "ต้องตรวจสอบ" | ใส่ตัวเลขที่ตรวจแล้ว | ดู §13 |

---

## 1. One-liner

**ผลตรวจยีนที่คนไข้ตรวจไปแล้ว ต้องถูกใช้ทุกครั้งที่มีการสั่งยาใหม่ — PrecisionRx เอาผล PGx ไปเตือนในระบบโรงพยาบาลตอนสั่งและจ่ายยา แสดงเฉพาะเรื่องที่ต้องทำ และให้เภสัชกรทบทวนก่อนถึงแพทย์ ส่วนคนไข้มะเร็ง รวมผล cfDNA, germline PGx และ interaction ของยา targeted therapy ไว้ในรายงานเดียว**

- **ไม่ใช่** AI วินิจฉัยโรค **ไม่ใช่** AI สั่งยา
- **เป็น** Clinical Decision Support ที่ทุกข้อความชี้ไปที่ rule และหลักฐานจริง เภสัชกร/แพทย์เป็นผู้ตัดสินใจ

---

## 2. ปัญหา (มีหลักฐานในไทย)

1. **ผล PGx ไม่ถูกใช้ตอนสั่งยา** — งานของรามาธิบดี (ข้อมูล 2011–2020) เขียนว่า *"there is currently no PGx alert system connected with the electronic health records (EHR) in Thailand"* และรายงานเคสผู้ป่วย HLA-B\*15:02 positive ที่ได้ carbamazepine เพราะไม่มีระบบเตือน แล้วเสียชีวิต ✅ [PMC9016335]
2. **ผล PGx กำลังเพิ่มขึ้นเร็ว** — การตรวจ HLA-B ที่รามาฯ เพิ่มจาก 94 ครั้ง (2011) เป็น 2,880 ครั้ง (2020) ✅ [PMC9016335]; สปสช. ครอบคลุม HLA-B\*15:02 และ HLA-B\*58:01 แล้ว ✅; และบัตรทองผ่านศูนย์จีโนมรามาฯ ครอบคลุมการตรวจ HLA-B\*15:02, CYP2C19, CYP2C9 🟡 [Hfocus ก.ค. 2026]
3. **คนไทยเกือบทุกคนมีผล PGx ที่ต้องทำอะไรสักอย่าง** — คนไทย 4,662 คน: 96% มี CPIC-actionable genotype อย่างน้อย 1 ยีน; ผู้ใช้ omeprazole มี CYP2C19 actionable 55%; ผู้ใช้ statin มี SLCO1B1 actionable ~22–23% ✅ [PLoS One 2026]
4. **Alert fatigue** — meta-analysis พบแพทย์ override DDI alert ~90% (95% CI 85–95%) ✅ [Felisberto 2024] → การเพิ่ม alert ไม่ใช่คำตอบ ต้อง **ลด** alert ที่ไม่มี action
5. **ไม่เห็น trajectory ของการรักษา** — ผู้ป่วย ACS ที่ได้ตรวจ LDL-C ซ้ำภายใน 120 วันมีแค่ 24.4% ✅ [S24 ใน market_research]
6. **มะเร็ง: ผล molecular กระจัดกระจาย** — EGFR mutation พบราว 47–56% ของ NSCLC ในงานวิจัยไทย ✅ (รามาฯ 56.3%, รพ.ตติยภูมิอีกแห่ง 47%) มะเร็งปอดรายใหม่ 23,871 ราย/ปี ✅ [GLOBOCAN 2024] รายงาน liquid biopsy, germline PGx ของยาเคมีบำบัด และ DDI ของยา TKI ไม่ถูกรวมเป็นภาพเดียวให้เภสัชกรมะเร็ง

---

## 3. การตัดสินใจเรื่องยาที่ระบบเปลี่ยน

| # | สถานการณ์ | ข้อมูลที่ใช้ | ระบบทำอะไร | ระดับหลักฐาน |
|---|---|---|---|---|
| 1 | จะสั่ง carbamazepine/oxcarbazepine ใน HLA-B\*15:02 positive | Germline PGx | **Hard stop** ตอนสั่งยา | CPIC + สิทธิ สปสช. ✅ |
| 2 | จะสั่ง allopurinol ใน HLA-B\*58:01 positive | Germline PGx | **Hard stop** | CPIC + สิทธิ สปสช. ✅ |
| 3 | Omeprazole/PPI ใน CYP2C19 ultrarapid/rapid หรือ poor metabolizer | Germline PGx | แสดงคำแนะนำ CPIC เรื่องขนาด PPI | CPIC PPI guideline (ตรวจถ้อยคำก่อนพิตช์) |
| 4 | Simvastatin 40 mg ใน SLCO1B1 decreased function | Germline PGx | CPIC 2022: "Prescribe an alternative statin… If simvastatin therapy is warranted, limit dose to <20 mg/day" | CPIC 2022, Strong ✅ |
| 5 | Clopidogrel ใน CYP2C19 PM (ACS/PCI) | Germline PGx | CPIC 2022: "Avoid clopidogrel if possible. Use prasugrel or ticagrelor at standard dose if no contraindication" | CPIC 2022, Strong ✅ |
| 6 | Clopidogrel + omeprazole/esomeprazole | Med list | Plavix label: "Avoid concomitant use" → เสนอ pantoprazole | Label ✅ |
| 7 | LDL-C ถึงเป้า แต่ ApoB ยังเกิน secondary goal | Lab (ApoB) | แสดง discordance + RCV เทียบ baseline | ESC/EAS: ApoB เป็น **secondary target** 🟡 (ตรวจกับ 2025 Focused Update) |
| 8 | NSCLC ดื้อยา EGFR TKI | **cfDNA** | แสดง variant + tier + ยาที่มีในฉลาก/guideline → oncologist ตัดสิน | Companion diagnostic / guideline |
| 9 | Gefitinib/erlotinib + PPI | Med list | IRESSA: เลี่ยง PPI หรือเว้น 12 ชม.; TARCEVA: เลี่ยง PPI (omeprazole ลด AUC 46%) | Label ✅ |
| 10 | ก่อนเริ่ม capecitabine/5-FU หรือ irinotecan | Germline PGx | Flag DPYD / UGT1A1 → เสนอทบทวนขนาด | CPIC / DPWG |

**แกน demo** = ข้อ 1, 3, 4 (PGx ตอนสั่งยา) + ข้อ 8–10 (oncology cfDNA)
ข้อ 5–6 เก็บไว้ แต่**ไม่ใช้เปิด** เพราะเป็นคู่ที่แพทย์ override มากที่สุด ✅ [PMC10726431]

---

## 4. Data layer

**หลักการ: ระบบรับเฉพาะผลที่ lab ประมวลแล้ว ไม่ประมวล raw spectrum ไม่ call variant เอง**

| ชนิดข้อมูล | มาจาก | ระบบรับอะไร | ระยะ |
|---|---|---|---|
| **Germline PGx** | **ผูกพันธุ์** (กรมวิทย์ฯ + มหิดล), lab PGx (Rama PPM, N Health, Bangkok Hospital ฯลฯ) | Genotype/diplotype หรือ VCF → PharmCAT | **ระยะ 1 (แกน)** |
| Clinical data | HIS (HOSxP ฯลฯ) ผ่าน FHIR | ยา ขนาด แพ้ยา lab refill | ระยะ 1 |
| **cfDNA / ctDNA** | Lab liquid biopsy | Structured variant report (gene, variant, VAF, tier) | **ระยะ 1 (oncology module)** |
| ApoB / lipid ปกติ | Lab clinical chemistry | ค่าจริง + หน่วย | ระยะ 2 |
| NMR metabolomics | Lab ที่ได้ accreditation เมื่อมีในไทย (ติดตาม Nightingale × Innoquest ซึ่งมีข้อตกลงครอบคลุมไทย ✅ แต่ยังไม่ยืนยันว่าให้บริการแล้ว ❓) | Quantified panel | ระยะ 2–3 (ก่อนหน้านั้นใช้ในงานวิจัยเท่านั้น ติดป้าย RUO) |

### 4.1 ทำไม cfDNA ยังอยู่ และอยู่ตรงไหน

cfDNA **ไม่ได้ใช้แทน germline PGx** มันตอบคำถามอื่น:

- **Germline DNA** → คนไข้ทนยาไหนได้ ยาไหนเสี่ยง ADR (DPYD, UGT1A1, CYP2C19…)
- **ctDNA** → เนื้องอกมี target ของยาไหน และดื้อยาด้วยกลไกอะไร โดยไม่ต้องตัดชิ้นเนื้อซ้ำ

ในคนไข้มะเร็ง ต้องใช้ทั้งสองอย่างพร้อมกับ DDI ของยา TKI ซึ่งเป็นงานประจำของ oncology pharmacist **นี่คือจุดเดียวที่การรวมข้อมูลหลายชนิดสร้างการตัดสินใจใหม่จริง** — ไม่ใช่แค่วางผลไว้ข้างกัน

**ขายยังไง:** license "oncology pharmacy module" ต่อศูนย์มะเร็ง ครอบคลุมคนไข้มะเร็งทุกคน (DPYD/UGT1A1 + DDI ของยา TKI/เคมีบำบัด + อ่านผล ctDNA เมื่อมี) ไม่เก็บเงินเฉพาะรายงาน cfDNA เพราะปริมาณในไทยเล็ก (TAM ราว ฿11–27 ล้าน/ปี 📊)

### 4.2 ข้อควรระวังของ cfDNA ที่ระบบแสดงบนหน้าจอ

1. **ผลลบไม่ได้แปลว่าไม่มี mutation** — เนื้องอกบางชนิดปล่อย ctDNA น้อย → "ctDNA not detected: ตัดออกไม่ได้ พิจารณาตรวจชิ้นเนื้อ"
2. **Clonal hematopoiesis (CHIP)** — variant ใน DNMT3A, TET2, ASXL1 อาจมาจากเม็ดเลือดขาว → ติดป้าย "possible CHIP origin"
3. **Incidental germline finding** — VAF ~50% หรือ ~100% ในยีนอย่าง BRCA1/2 อาจเป็น germline → "แนะนำ genetic counselling" ระบบไม่สรุปเอง
4. **ctDNA dynamics** ใช้ติดตาม response ได้ในระดับ emerging → ติดป้าย "Emerging"
5. **Pre-analytics** — cfDNA ใช้หลอด stabilizing หรือปั่นแยก plasma ในเวลาจำกัด ใช้หลอดแยกจากการตรวจอื่น

---

## 5. Response module (ระยะ 2) — ApoB ก่อน, NMR ทีหลัง

ไม่ใช้แถบ HIGH/LOW ใช้ **3 สิ่งต่อ analyte**:

1. ค่าจริง + หน่วย
2. เทียบ reference / เป้าหมายตาม guideline (ApoB เป็น secondary target)
3. เทียบ baseline ของคนไข้เอง ด้วย **Reference Change Value**

```
RCV = √2 × Z × √(CVa² + CVi²)
CVa = analytical variation (จาก lab)
CVi = within-person biological variation (จาก EFLM Biological Variation Database)
Z   = 1.96 (สองทาง 95%) หรือ 1.65 (ทางเดียว)
```

- |%change| > RCV → "เปลี่ยนจริง"
- ไม่เกิน → "ไม่ต่างจากความแปรปรวนปกติ"
- ❓ ต้องเช็กว่า EFLM มี CVi ของ ApoB (น่าจะมี) และของ LDL-P/GlycA หรือไม่ ถ้าไม่มี ห้ามแสดงลูกศรสำหรับ analyte นั้น

**Adherence ก่อนสรุปว่ายาไม่ได้ผล** — คำนวณ proportion of days covered (PDC) จาก refill; ถ้า PDC ต่ำ ระบบบอก "ทบทวนการใช้ยาก่อน"

**NMR** เพิ่ม LDL-P, TRL, GlycA ได้เมื่อมี lab คลินิกในไทย จนกว่าจะถึงตอนนั้นใช้ในโครงการวิจัยเท่านั้น (เช่น ร่วมกับ lab phenome ในมหาวิทยาลัย) และติดป้าย RUO

---

## 6. สถาปัตยกรรม

**หลักการ:** การเทียบตาราง CPIC, กฎ DDI, RCV, PDC และการจัด tier ของ variant **ต้องได้ผลเหมือนเดิมทุกครั้ง** → เขียนเป็นโค้ด LLM ใช้เฉพาะงานภาษา และห้ามสร้าง fact ใหม่

```
ผูกพันธุ์ / PGx lab ──┐
Liquid biopsy lab ────┤
HIS (HOSxP ฯลฯ) ──────┤  FHIR (Patient, MedicationRequest, Observation,
                      │        DiagnosticReport, Genomics Reporting IG)
                      ▼
 1. Deterministic engines (unit-tested)
    ├─ PGx: PharmCAT (open source) → CPIC/DPWG + Thai drug mapping (TMT)
    ├─ DDI: rules จากฉลากยา / DDI database ที่มี license
    ├─ Alert filter: แสดงเฉพาะ finding ที่มี action
    ├─ Oncology: variant → tier (AMP/ASCO/CAP) + labeled therapy
    │            + CHIP flag + possible-germline flag + "not detected" caveat
    ├─ Response: guideline target + RCV change detection   (ระยะ 2)
    └─ Adherence: refill → PDC
                      ▼
 2. Evidence store (versioned snapshot; ทุก fact มี ID + แหล่ง + ระดับหลักฐาน)
    CPIC, PharmGKB/ClinPGx, drug labels, ClinVar, OncoKB (ต้องจ่าย license เชิงพาณิชย์ ✅)
                      ▼
 3. จุดส่งมอบ
    ├─ CDS Hooks: order-sign / order-select → card ในหน้าจอสั่งยาของ HIS
    │   (hard stop สำหรับ HLA-B; card แนะนำสำหรับอย่างอื่น)
    └─ Pharmacist queue: finding ที่ต้องทบทวน → accept / modify / reject
                      ▼
 4. LLM layer (2 agent เท่านั้น)
    ├─ Summarizer: เขียน brief / oncology report จาก fact ID เท่านั้น
    └─ Q&A agent: ตอบคำถามแพทย์/เภสัชกร โดย query evidence store และเรียก engine ได้
                      ▼
 5. Verifier (code): ทุกประโยค ↔ fact ID ที่มีจริง; ตัดประโยคที่ไม่มีหลักฐาน
                      ▼
 6. Audit log + sign-off
```

- **ทำไมเรียก agent ได้:** Q&A agent มี tool และ decision loop จริง ส่วนอื่นเป็นโค้ด ไม่เรียก agent
- **ปุ่ม "Why?"** แสดง trace จริง: ข้อสรุป → engine → rule/fact ID → ข้อมูลคนไข้ → แหล่ง ไม่ใช่ให้ LLM เล่าย้อนหลัง
- **ระดับหลักฐาน 3 ชั้น** ติดทุก finding: **Guideline** (CPIC A/B, ฉลาก, companion Dx) · **Emerging** (ctDNA dynamics, pharmacometabolomics) · **Unknown** (VUS)
- **Determinism:** fix version ของ model, prompt, evidence snapshot; temperature 0; regression test ทุกครั้งที่เปลี่ยน
- **Privacy:** ข้อมูล genome ไม่ออกนอกประเทศ ใช้ LLM ที่ host ในไทยหรือ on-prem หรือส่งเฉพาะ fact ที่ลบตัวบ่งชี้แล้ว; กรอง free-text note ก่อนเข้า LLM (ป้องกัน prompt injection)
- **ต้นทุน AI ~35 บาท/รายงาน** 📊 ต้นทุนหลักคือ curation และ support [business_case]

---

## 7. หน้าจอ

### 7.1 Card ในหน้าจอสั่งยาของแพทย์ (CDS Hooks)
```
┌──────────────────────────────────────────────────────────────┐
│ ⛔ STOP — Carbamazepine                                        │
│   HLA-B*15:02 POSITIVE (ผลจาก ผูกพันธุ์, 2024-03-12)           │
│   CPIC: do not use (risk of SJS/TEN)            [Guideline]    │
│   [Why?]  [เลือกยาอื่น]  [Override + เหตุผล → แจ้งเภสัชกร]     │
└──────────────────────────────────────────────────────────────┘
```

### 7.2 คิวเภสัชกร
```
┌─ ACTION NEEDED (2) ──────────────────────────────────────────┐
│ ⚠ Simvastatin 40 mg — SLCO1B1 decreased function [Guideline] │
│   CPIC 2022: alternative statin, or limit to <20 mg/day       │
│   [Why?] [Accept] [Modify] [Reject]                            │
│ ⚠ Omeprazole — CYP2C19 ultrarapid metabolizer    [Guideline]  │
│   CPIC: consider dose increase (ตรวจถ้อยคำ)                    │
│   [Why?] [Accept] [Modify] [Reject]                            │
├─ MONITOR ────────────────────────────────────────────────────┤
│ ApoB: −6% vs baseline (RCV ±X%) → ไม่ต่างจากความแปรปรวนปกติ   │
├─ NO ACTION ──────────────────────────────────────────────────┤
│ 7 other checks passed (collapsed)                             │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Demo — 4 เคส (synthetic ติดป้ายชัด)

| เคส | เรื่อง | สิ่งที่โชว์ |
|---|---|---|
| **A (เปิด)** | ชาย 34 ปี โรคลมชัก แพทย์กำลังสั่ง carbamazepine ผล HLA-B\*15:02 positive อยู่ในผูกพันธุ์ | Hard stop ในหน้าจอสั่งยา — เล่าคู่กับเคสจริงที่เสียชีวิตเพราะไม่มีระบบเตือน |
| **B** | หญิง 52 ปี simvastatin 40 mg + omeprazole, SLCO1B1 decreased + CYP2C19 ultrarapid | 2 PGx finding ใน card เดียว, "Why?" trace, เภสัชกร accept |
| **C** | เคส B ผ่านไป 3 เดือน: LDL-C ถึงเป้า ApoB ยังเกิน secondary goal, PDC 92% | Response module + RCV + adherence (ระยะ 2) |
| **D (cfDNA)** | ชาย 64 ปี NSCLC EGFR+ ได้ erlotinib + omeprazole โรคลุกลาม; ctDNA พบ resistance mutation + DNMT3A variant; แผนถัดไปมี capecitabine | ctDNA tier + ยาในฉลาก → oncologist; TKI+PPI interaction; CHIP flag; DPYD check |

ถ้าเวลาพิตช์สั้น: A + D เคส B และ C ไว้ตอบคำถาม

---

## 9. แผนประเมินผล

### ใน hackathon
- **Gold-standard case set** 30–50 เคส synthetic ครอบคลุม 10 สถานการณ์ใน §3 เฉลยโดยเภสัชกร 2–3 คน
- **Metrics**
  - Critical-omission rate — เป้า 0
  - False-flag rate
  - Citation precision ≥ 99%
  - Concordance กับ CPIC (PharmCAT + mapping) — ควร 100%
  - จำนวน alert ต่อเคส เทียบ DDI checker ปกติ (โชว์การลด noise)
  - Inter-rater agreement ระหว่างเภสัชกร (เพดานของระบบ)
- Regression test ทุกครั้งที่เปลี่ยน prompt/model/evidence

### Pilot 6 เดือน, 1 โรงพยาบาล [business_strategy]
- **เดือน 0–2:** รันย้อนหลังกับเวชระเบียนเดิม ไม่แตะการรักษา (n ≥ 300)
- **เดือน 3–6:** ใช้จริง ~150–200 reviews
- **เป้า (กำหนดก่อนเริ่ม):**
  - Critical omission = 0 (go/no-go)
  - เภสัชกรยอมรับ ≥ 70%, แพทย์ยอมรับ ≥ 50%
  - Alert ต่อ review ลด ≥ 50%, เวลาทบทวนลด ≥ 30%
  - Actionable PGx finding ต่อ 100 คน (คาดตามข้อมูลไทย: ~55 ในผู้ใช้ omeprazole, ~22 ในผู้ใช้ statin)
- **Kill criteria:** ยอมรับ < 50% หรือโรงพยาบาลมีผู้ป่วยที่มีผล PGx < 200 ราย
- **ไม่ claim** ว่าลด ADR จาก pilot นี้

**ห้าม claim** ความแม่นยำหรือผลลัพธ์ทางคลินิกจากข้อมูล synthetic

---

## 10. ข้อจำกัดทางคลินิก

- ไม่วินิจฉัย ไม่เลือกยาแทนแพทย์ ทุก recommendation ผ่านเภสัชกร/แพทย์
- PGx ครอบคลุมเฉพาะยีนที่ตรวจ ผลลบไม่ได้แปลว่าปลอดภัยทุกยา
- หลักฐาน PREPARE มาจากยุโรป (97.7% ผู้เข้าร่วมเป็นคนยุโรป/เมดิเตอร์เรเนียน/ตะวันออกกลาง ใช้ DPWG) ยังไม่มีข้อมูลผลลัพธ์ในคนไทย
- แพทย์ยอมรับ PGx alert เฉลี่ยราว 63% และการกดยอมรับตรงกับการเปลี่ยนการรักษาจริงแค่ 47% ✅ [PMC10726431]
- ยังไม่มี NMR ทางคลินิกในไทย ❓ reference range NMR ส่วนใหญ่มาจากยุโรป
- ctDNA ผลลบไม่ตัดการมี mutation; variant อาจเป็น CHIP หรือ germline; ctDNA dynamics ยังเป็น emerging
- VUS และ incidental germline finding ต้องส่ง genetic counselling

---

## 11. กฎหมายและ regulatory

**Intended use (ร่าง)**
> "PrecisionRx applies published pharmacogenomic guidelines and drug-label rules to existing accredited laboratory results (germline pharmacogenomic genotypes and, for oncology, cfDNA variant reports) and current medications, and presents evidence-linked alerts and summaries to support prescribing and pharmacist medication review. It does not diagnose disease or select treatment; all recommendations require clinician review."

| ประเด็น | แนวทาง |
|---|---|
| **SaMD** | มีแนวโน้มเป็นเครื่องมือแพทย์ตาม พ.ร.บ.เครื่องมือแพทย์ ต้องปรึกษา อย. เรื่อง class ❓ · คู่แข่งในภูมิภาค (Nalagenetics) ต้องได้ CE mark ก่อนขาย PGx CDS ✅ · ตัวเทียบ: **US FDA CDS guidance ฉบับ 6 ม.ค. 2026** (แทนฉบับ 2022) — ซอฟต์แวร์ที่ประมวล signal จาก IVD ยังเป็น device การรับเฉพาะผลที่ lab ประมวลแล้วจึงสอดคล้อง แต่ guidance ไม่พูดถึง LLM และไม่มีผลทางกฎหมายในไทย ✅ · บทเรียน: Translational Software ในสหรัฐฯ หยุดบริการ PGx CDS หลังไม่ผ่าน FDA 510(k) 🟡 |
| **Lab** | รับผลจาก lab ที่ได้ ISO 15189; NMR ที่ยังเป็น RUO ใช้ได้แค่ในงานวิจัยและติดป้าย |
| **PDPA** | ม.26 ข้อมูลสุขภาพและพันธุกรรมเป็นข้อมูลอ่อนไหว ✅ → explicit consent แยกสำหรับ PGx และ cfDNA, purpose limitation, ระยะเวลาเก็บ, ถอนความยินยอมได้, DPO, ไม่ส่งข้ามประเทศ · ใช้ consent ของผูกพันธุ์ (ThaiD) เป็นทางเข้าข้อมูล · ข้อยกเว้นตาม ม.26(5) ต้องให้ทนายตรวจก่อนอ้าง |
| **ประกัน/ผู้จ่าย** | ผู้จ่ายประกันไม่เห็นข้อมูลพันธุกรรมรายบุคคล เห็นเฉพาะผลรวม |
| **วิชาชีพ** | เภสัชกรเสนอ แพทย์สั่ง ระบบบันทึก sign-off และเหตุผลการ override |
| **Governance** | Audit log, change control ของ rule/evidence, incident reporting, ข้อตกลงความรับผิดกับโรงพยาบาล |
| **Research** | ข้อมูลผู้ป่วยจริงต้องผ่าน IRB/EC |
| **License** | OncoKB เชิงพาณิชย์ต้องจ่าย annual license ✅; DDI database ต้องมี license |

---

## 12. โมเดลธุรกิจ

### 12.1 ใครใช้ ใครจ่าย
| | Module A: PGx ตอนสั่งยา (+ Response ระยะ 2) | Module B: Oncology pharmacy (cfDNA) |
|---|---|---|
| ผู้ใช้ | แพทย์ (card ใน HIS), เภสัชกร (คิวทบทวน) | Oncology pharmacist + oncologist |
| ผู้ซื้อ | ผู้บริหารโรงพยาบาล; อนุมัติโดย PTC (คณะกรรมการเภสัชกรรมและการบำบัด), IT, DPO | ศูนย์มะเร็ง |
| ผู้ได้ประโยชน์ | คนไข้ (ADR ลดลง), โรงพยาบาล (ผลตรวจที่ขายไปแล้วถูกใช้จริง) | คนไข้, ศูนย์มะเร็ง |

### 12.2 Beachhead
**โรงพยาบาลเอกชนที่ขาย PGx อยู่แล้ว** — ประโยคขาย: "ผลตรวจยีนที่คนไข้จ่ายไปแล้ว ถูกใช้ทุกครั้งที่สั่งยาใหม่"
- Bangkok Hospital (PGx NGS 500+ ยา), BNH (PGx 126 ยา), Samitivej (Genomics Center), Bumrungrad, N Health (PGx panel ฿14,751) ✅ — **ยังไม่ได้คุยกับที่ไหนเลย**
- เครือ BDMS มีครบทั้ง lipid clinic, PGx lab และศูนย์ genetics ✅ ได้ 1 แห่งขยายในเครือได้
- โรงพยาบาลมหาวิทยาลัยและคณะเภสัชฯ = พาร์ทเนอร์ validation ไม่ใช่ลูกค้าจ่ายเงินรายแรก
- ระยะถัดไป: **PGx CDS connector สำหรับโรงพยาบาลรัฐที่ใช้ HOSxP** สำหรับยีนที่บัตรทองจ่าย (ผู้ซื้ออาจเป็น vendor HIS หรือหน่วยงานรัฐ)

### 12.3 รายได้ (📊 สมมติฐาน ต้อง validate)
| ช่องทาง | ราคา | หมายเหตุ |
|---|---|---|
| Module A: ค่าติดตั้ง | ฿250,000 ครั้งเดียว | |
| Module A: ต่อผู้ป่วยที่มีผล PGx และได้ยาในปีนั้น | **฿300–480/คน/ปี** ขั้นต่ำ 1,000 คน | base ฿480; ถ้า ฿300 LTV:CAC ลดจาก 3.4 เหลือ 1.6 |
| Module B: license ต่อศูนย์มะเร็ง หรือ ฿3,000/รายงาน | | ต่ำกว่า 5% ของค่า osimertinib 1 เดือน ✅ |
| Lab revenue share | ฿500/ผลตรวจ | lab ได้ประโยชน์เพราะผลตรวจมีค่าขึ้น |

**เราไม่ขายการตรวจ lab** เป็น interpretation layer แบบ lab-agnostic

### 12.4 Unit economics และ ROI (จาก business_case.md 📊)
- Contribution margin ~67% · CAC ~฿400k · LTV ~฿1.36M · LTV:CAC ~3.4 · payback ~13 เดือน (รวม curation ปีที่ 3: ~2.0 และ ~23 เดือน)
- **ROI ของโรงพยาบาล ~2.2 เท่า เฉพาะเมื่อโรงพยาบาลเก็บค่า pharmacist PGx review ได้** (~฿700 × ≥510 ครั้ง/ปี หรือรวมในราคาแพ็กเกจ PGx) ถ้านับแค่เวลาเภสัชกรที่ประหยัด + ADR ที่ป้องกัน ได้คืนแค่ ~0.37 เท่า → **สมมติฐานสำคัญที่สุด ต้อง validate กับโรงพยาบาลก่อน**
- ต้นทุน ADR admission ในไทย ฿7,215/ครั้ง ✅; เวลาเภสัชกร 24 นาที/PGx consult ✅ (Mayo)

### 12.5 ประมาณการ 3 ปี (base case 📊)
- รายได้: ฿0.5M → ฿3.4M → ฿9.6M (12 โรงพยาบาล + 3 ศูนย์มะเร็งในปีที่ 3) ทีม 5 → 11 คน
- **คุ้มทุนรายเดือนราวเดือนที่ 45–50** ต้องใช้เงินราว ฿25–30M (ปีแรก ~฿7M)
- Downside: ขาดทุนราว ฿27M และไม่คุ้มทุน → มี kill/pivot rule ที่เดือน 12 และ 24

### 12.6 ขนาดตลาด (📊 จาก market_research.md)
- Module A: TAM ~฿0.4–0.8 พันล้าน/ปี · SAM ~฿20–60 ล้าน · SOM ปีที่ 3 ~฿2–6 ล้าน
- Module B: TAM ~฿11–27 ล้าน/ปี · SOM < ฿1 ล้าน → **Module B เป็นจุดต่างและหลักฐานว่าสถาปัตยกรรมขยายได้ ไม่ใช่รายได้หลัก**

### 12.7 คู่แข่ง
| ผู้เล่น | ทำอะไร | เราต่างตรงไหน / วางเป็นอะไร |
|---|---|---|
| **ไม่ทำอะไร** (ผล PGx เป็น PDF/บัตร) | ฟรี | **คู่แข่งอันดับ 1** — ขายด้วยความเสี่ยงของการไม่ทำ |
| **ผูกพันธุ์** (กรมวิทย์ฯ + มหิดล) | เก็บผลยีนแพ้ยาตลอดชีวิต, ThaiD, เชื่อม 11 รพ. ✅ | **แหล่งข้อมูล ไม่ใช่คู่แข่ง** — เขาเป็นแอปดูผล เราเป็น CDS ตอนสั่งยา |
| PGxCard / กินอยู่ดี × ม.บูรพา | บัตรแพ้ยาอิเล็กทรอนิกส์ ✅ | ต้องดูระบบจริงก่อนพิตช์ |
| Rama PPM + PGx ID card | Reference lab + บัตร ✅ | พาร์ทเนอร์ |
| **PharmCAT** | Open-source CPIC engine ✅ | เราใช้เป็น engine — PGx engine ไม่ใช่ moat |
| Lexidrug / Micromedex | DDI + มี PGx database ✅ | ไม่ผูก genotype คนไข้รายคน ไม่ลด alert |
| Epic genomics | CPIC alert ใน EHR | ไม่มีในโรงพยาบาลไทยส่วนใหญ่ |
| **Nalagenetics** | PGx CDS (CE mark) ขยายใน SEA ✅ | **คู่แข่งตรงที่สุดในภูมิภาค** — เราต่างที่ mapping ไทย + HOSxP + oncology |
| Tabula Rasa MedWise | PGx + DDI + pharmacist workflow (US) ✅ | แนวคิดเดียวกัน ไม่อยู่ในไทย |
| Translational Software, RxGenomix | PGx CDS / pharmacist program (US) | ไม่อยู่ในไทย |
| QIAGEN QCI, Roche navify, OncoKB, Tempus, Guardant | Oncology interpretation | ไม่มี germline PGx + DDI สำหรับเภสัชกร |
| Nightingale Health | NMR + report; มีข้อตกลงกับ Innoquest ครอบคลุมไทย ✅ | Lab partner ในอนาคต |
| HOSxP (BMS) | HIS ที่ใช้ในโรงพยาบาลส่วนใหญ่ มี alert แพ้ยาทั่วไป | **ช่องทาง** — ถ้าเขาเพิ่ม PGx เอง เราต้องเป็น module ของเขา |

**"ทำไม HIS vendor ไม่ทำเอง?"** — เขาทำได้ Epic ทำแล้ว ต้นทุนจริงไม่ใช่การเขียน rule ครั้งแรก แต่เป็นการดูแล evidence ที่ CPIC อัปเดตเรื่อย ๆ, map กับรหัสยาไทย, รับ liability และภาระ อย. ของ clinical interpretation และ rule เดี่ยวใน HIS จะ**เพิ่ม** alert ในขณะที่แพทย์ override อยู่แล้ว ~90% เราขายการ**ลด** alert — และวางตัวเป็น module ที่ต่อเข้า HIS ไม่ใช่แข่งกับ HIS

**Moat (พูดตรง ๆ):** ได้เปรียบด้านเวลาและโฟกัส ไม่ใช่สิ่งที่ลอกไม่ได้ — evidence store ที่ curate สำหรับไทย (TMT, สิทธิการรักษา, allele frequency ไทย), การต่อ HIS จริง และข้อมูล pilot

### 12.8 Why now
- สังคมสูงวัยโดยสมบูรณ์: 60+ = 21.82% (2568) ✅; polypharmacy 59.5% ในผู้สูงอายุ OPD รพ.ทุติยภูมิเขต 8 ✅
- ผล PGx เพิ่มเร็ว + สิทธิ สปสช./บัตรทองขยาย ✅
- ผูกพันธุ์สร้างชั้นข้อมูล PGx ระดับชาติแล้ว → ขาดแค่จุดเตือนตอนสั่งยา
- PREPARE (Lancet 2023): ในผู้ป่วยที่มี actionable result, clinically relevant ADR 21.0% vs 27.7%, **OR 0.70 (95% CI 0.54–0.91)** ✅ — หลักฐานยุโรป ยังไม่มีข้อมูลไทย และมีจดหมายใน Lancet แย้งว่าประโยชน์ยังไม่ชัด
- ยาแพง (targeted therapy) → ศูนย์มะเร็งต้องการใช้ผล molecular ให้คุ้ม

### 12.9 Partnership (ตามลำดับ)
คณะเภสัชฯ (validate) → โรงพยาบาลเอกชน 1 แห่ง (pilot) → lab PGx → vendor HIS → lab liquid biopsy / ศูนย์มะเร็ง → lab NMR (วิจัย) → ประกัน / สปสช. (18 เดือนขึ้นไป)

---

## 13. Roadmap

| ระยะ | สิ่งที่ทำ |
|---|---|
| **Hackathon** | Module A (PGx + CDS Hooks mock + คิวเภสัชกร) + Module B (oncology) บน synthetic data, 4 demo case, eval 30–50 เคส |
| **ก่อนพิตช์** | สัมภาษณ์เภสัชกรโรงพยาบาล 5–10 คน (รัฐที่ใช้ HOSxP + เอกชน) — ยังไม่มีหลักฐานเชิงปริมาณเรื่องความต้องการ |
| **0–3 เดือน** | LOI จากโรงพยาบาล 1 แห่ง + คุยกับทีมผูกพันธุ์และ BMS-HOSxP · **Kill:** ถ้าไม่ได้ทั้งสองอย่างใน 3 เดือน หยุดหรือ pivot |
| **3–9 เดือน** | Pilot 6 เดือน (§9) + IRB + ปรึกษา อย. |
| **9–18 เดือน** | ขยายในเครือ, oncology module ที่ศูนย์มะเร็ง 1 แห่ง, Response module (ApoB + RCV) |
| **18 เดือน+** | NMR เมื่อมี lab คลินิก + สร้าง reference คนไทยร่วมกับมหาวิทยาลัย, PGx connector สำหรับโรงพยาบาลรัฐ, cost-effectiveness study |

---

## 14. สิ่งที่ยังต้องตรวจก่อนขึ้นเวที

- [ ] ถ้อยคำ CPIC CYP2C19–PPI ฉบับล่าสุด (เคส B)
- [ ] ESC/EAS 2025 Focused Update เรื่อง ApoB
- [ ] ผูกพันธุ์มี API/FHIR หรือ alert ตอนสั่งยาแล้วหรือยัง และเชื่อมกี่ รพ. ในปี 2026
- [ ] HOSxP มี PGx field หรือ module แล้วหรือยัง
- [ ] EFLM มี CVi ของ ApoB / LDL-P / GlycA หรือไม่
- [ ] Label ของ osimertinib เรื่อง PPI
- [ ] ตัวเลขเภสัชกร 46.3% ความรู้ PGx ต่ำ และ 7% เคยแปลผล (มาจาก abstract) [PubMed 32187156]
- [ ] ราคา cfDNA / EGFR plasma ในไทย
- [ ] ข่าวบัตรทองครอบคลุม CYP2C19/CYP2C9 (Hfocus ก.ค. 2026) — ยืนยันกับประกาศ สปสช.

---

## 15. อธิบายให้เพื่อนฟัง

คนไทยตรวจยีนแพ้ยากันมากขึ้นทุกปี สปสช. ก็จ่ายให้ แต่ผลอยู่ในบัตรหรือ PDF พอหมอสั่งยาไม่มีอะไรเตือน เคยมีคนตายเพราะแบบนี้

เราทำตัวเชื่อม: ดึงผลยีนจากผูกพันธุ์หรือ lab → เทียบ guideline CPIC ด้วยโค้ด → **เด้งเตือนในหน้าจอสั่งยาของหมอ** เฉพาะเรื่องที่ต้องทำจริง → ส่งเรื่องที่ต้องคิดต่อให้เภสัชกรทบทวน

คนไข้มะเร็งมีอีก module: รวมผล **cfDNA** (เนื้องอกดื้อยาเพราะอะไร มียาตัวไหน) + **ยีนของคนไข้เอง** (ทนยาเคมีตัวไหนได้) + **ยาตีกัน** (เช่น TKI กับยาลดกรด) เป็นรายงานเดียวให้เภสัชกรมะเร็ง

AI ใช้แค่เรียบเรียงและตอบคำถาม ทุกประโยคต้องชี้ไปที่หลักฐาน

**ประโยคขาย:** "ผลตรวจยีนที่คนไข้จ่ายไปแล้ว ต้องถูกใช้ทุกครั้งที่หมอสั่งยา"
