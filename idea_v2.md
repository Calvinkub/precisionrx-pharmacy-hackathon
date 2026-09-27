# PrecisionRx — PGx-anchored Medication Review with Metabolomic + cfDNA Response Tracking

> เวอร์ชัน 2 (แก้ตามผลวิจารณ์ใน `critique_PrecisionRx.md`) — ต้นฉบับเดิมเก็บไว้ที่ `idea_v1_original.md`
> ข้อความที่ระบุ "ต้องตรวจสอบ" ต้องเช็กกับแหล่งจริงก่อนขึ้นเวที

---

## 1. One-liner

**แพลตฟอร์มช่วยเภสัชกรทบทวนยา (medication review) โดยรวม germline pharmacogenomics, NMR metabolomics และ cfDNA เข้าด้วยกัน เพื่อตอบ 3 คำถาม: ยานี้เหมาะกับพันธุกรรมคนไข้ไหม, ยาได้ผลจริงไหมเมื่อเทียบ baseline ของคนไข้เอง, และมีอะไรที่ต้องให้แพทย์ทบทวน**

- **ไม่ใช่** AI วินิจฉัยโรค **ไม่ใช่** AI สั่งยา
- **เป็น** Clinical Decision Support ที่ทุกข้อความมีหลักฐานอ้างอิง และเภสัชกร/แพทย์เป็นผู้ตัดสินใจ

---

## 2. ปัญหา (ที่เภสัชกรเจอจริง)

1. **ยาไม่เหมาะกับพันธุกรรม** — คนไข้ได้ยาที่มีหลักฐานว่า genotype ทำให้เสี่ยง ADR หรือยาไม่ได้ผล (เช่น clopidogrel ใน CYP2C19 poor metabolizer) แต่ไม่มีใครรู้เพราะไม่เคยตรวจ หรือผลตรวจไม่ถูกนำมาใช้ตอนจ่ายยา
2. **ไม่รู้ว่ายาได้ผลจริงไหม** — หมอเห็น LDL-C ครั้งเดียว ไม่เห็น trajectory และไม่รู้ว่าค่าที่ "ลดลง" เกินความแปรปรวนปกติของคนไข้หรือไม่
3. **แยกไม่ออกว่าไม่ได้ผลเพราะอะไร** — ไม่กินยา (non-adherence), ขนาดยาไม่พอ, drug interaction, หรือพันธุกรรม
4. **Alert fatigue** — ระบบ DDI เดิมแจ้งเตือนเยอะจนถูก override เป็นส่วนใหญ่
5. **มะเร็ง: ผลตรวจ molecular (cfDNA/ctDNA) กระจัดกระจาย** — รายงาน liquid biopsy, germline PGx ของยาเคมีบำบัด และ interaction ของยา targeted therapy ไม่ถูกรวมเป็นภาพเดียวให้เภสัชกรมะเร็ง

---

## 3. การตัดสินใจเรื่องยาที่ระบบเปลี่ยน (ตอบคำถามข้อ 1 ของกรรมการ)

| # | สถานการณ์ | ข้อมูลที่ใช้ | ระบบทำอะไร | ระดับหลักฐาน |
|---|---|---|---|---|
| 1 | Clopidogrel ใน CYP2C19 poor/intermediate metabolizer | Germline PGx | Flag ตาม CPIC → เสนอให้แพทย์พิจารณา antiplatelet ทางเลือก (ถ้าไม่มีข้อห้าม) | CPIC guideline (ต้องตรวจสอบถ้อยคำฉบับล่าสุด) |
| 2 | Clopidogrel + omeprazole/esomeprazole | Med list | Flag DDI (CYP2C19 inhibition) → เสนอ PPI ทางเลือก | ฉลากยา / DDI database |
| 3 | Simvastatin ใน SLCO1B1 decreased/poor function | Germline PGx | Flag ความเสี่ยง myopathy ตาม CPIC → เสนอ statin อื่นหรือทบทวนขนาด | CPIC statin guideline |
| 4 | Statin: LDL-C ถึงเป้า แต่ ApoB/LDL-P ยังสูง | NMR + lab | แสดง discordance + residual risk → เสนอทบทวนการรักษา | ESC/EAS 2019 ยอมรับ ApoB เป็นเป้าหมายได้ |
| 5 | GLP-1 RA ตอบสนองน้อย | NMR + น้ำหนัก + refill data | แยก "ไม่กินยา/ขาดยา" ออกจาก "กินแล้วไม่ตอบสนอง" ก่อนสรุป | Adherence = guideline practice; metabolomic response = research signal |
| 6 | ก่อนเริ่ม carbamazepine / allopurinol | Germline PGx | Hard stop ถ้า HLA-B\*15:02 / HLA-B\*58:01 positive | CPIC + แนวปฏิบัติไทย (ต้องตรวจสอบสิทธิ สปสช. ปัจจุบัน) |
| 7 | มะเร็งปอด (NSCLC) ดื้อยา EGFR TKI | **cfDNA** (plasma EGFR) | แสดง variant ที่มียา targeted therapy ตามฉลาก/guideline → oncologist ตัดสิน | Companion diagnostic / guideline (ต้องตรวจสอบ) |
| 8 | EGFR TKI (gefitinib/erlotinib) + PPI | Med list | Flag interaction ที่ลดการดูดซึมยา → อาจเป็นสาเหตุการตอบสนองต่ำ | ฉลากยา |
| 9 | ก่อนเริ่ม capecitabine/5-FU, irinotecan | Germline PGx | Flag DPYD / UGT1A1 → เสนอทบทวนขนาด | CPIC / DPWG |

**แกน demo** = ข้อ 1–5 (cardiometabolic) + ข้อ 7–8 (cfDNA oncology) ส่วนข้อ 6 และ 9 เป็น safety rule ที่ติดมาด้วยโดยไม่ต้องทำเพิ่มมาก

---

## 4. Data layer — 3 ชนิดข้อมูล แต่ละชนิดมีหน้าที่ชัด

**หลักการ: ระบบรับเฉพาะผลที่ lab ประมวลแล้ว — ไม่ประมวล raw spectrum และไม่ call variant เอง** (แก้ข้อขัดแย้งเดิมเรื่อง IVD)

| ชนิดข้อมูล | มาจาก | ระบบรับอะไร | ใช้ตอบคำถาม | ความถี่ |
|---|---|---|---|---|
| **Germline DNA (PGx)** | เลือด/น้ำลาย → genotyping panel ที่ lab | Genotype / diplotype ของยีน PGx (CYP2C19, CYP2C9, VKORC1, SLCO1B1, CYP2D6, HLA-B, DPYD, UGT1A1, TPMT/NUDT15, CYP3A5) | "ยานี้เหมาะกับพันธุกรรมไหม" | **ตรวจครั้งเดียว ใช้ตลอดชีวิต** |
| **NMR metabolomics** | Plasma/serum → vendor platform (เช่น Bruker IVDr หรือ Nightingale) | Quantified panel: ApoB, ApoA1, LDL-P, small LDL-P, TRL, HDL-P, GlycA, BCAA, glucose, lactate, ketones | "ยาได้ผลทาง metabolic ไหม เทียบ baseline" | ก่อนเริ่มยา + ติดตาม (เช่น 3–6 เดือน) |
| **cfDNA / ctDNA** | Plasma → liquid biopsy lab (NGS หรือ PCR panel) | Structured variant report (gene, variant, VAF, tier) | "มะเร็งมี target ที่มียาไหม, molecular response เป็นอย่างไร" | ตอนวินิจฉัย / ตอนดื้อยา / ติดตาม |
| Clinical data | HIS / FHIR | อายุ เพศ diagnosis ยา ขนาด แพ้ยา lab refill history | บริบทและ DDI | ทุก visit |

### ทำไมต้องมี cfDNA (ตอบกรรมการ bio/เภสัช)

cfDNA **ไม่ได้ใช้แทน germline PGx** — มันตอบคำถามคนละข้อ:

- **Germline DNA** = พันธุกรรมที่ติดตัวคนไข้ → ใช้ตัดสินเรื่อง metabolism และ ADR ของยา
- **cfDNA (ctDNA)** = DNA ของเนื้องอกที่หลุดในเลือด → ใช้หา target ของยา targeted therapy และติดตาม molecular response โดยไม่ต้องตัดชิ้นเนื้อซ้ำ

ในคนไข้มะเร็ง ทั้งสองอย่าง **ต้องใช้พร้อมกัน**: ctDNA บอกว่าเนื้องอกตอบสนองยาไหน, germline PGx บอกว่าคนไข้ทนยาเคมีบำบัดตัวไหนได้ (DPYD, UGT1A1) และเภสัชกรต้องเช็ก DDI ของยา TKI (CYP3A4, PPI) — นี่คือ use case ของ **oncology pharmacist** ที่ยังไม่มีเครื่องมือรวมภาพเดียว

EGFR mutation พบบ่อยในมะเร็งปอดชนิด adenocarcinoma ของคนเอเชีย รวมถึงคนไทย จึงเป็นตัวอย่างที่เกี่ยวข้องกับบริบทไทยโดยตรง (ต้องตรวจสอบตัวเลขความชุกก่อนใส่สไลด์)

### ข้อควรระวังของ cfDNA ที่ระบบต้องจัดการ (แสดงบนหน้าจอ)

1. **ผลลบ ≠ ไม่มี mutation** — เนื้องอกบางชนิดปล่อย ctDNA น้อย → ระบบแสดง "ctDNA not detected: ไม่สามารถตัดออกได้ พิจารณาตรวจชิ้นเนื้อ"
2. **Clonal hematopoiesis (CHIP)** — variant ในยีนอย่าง DNMT3A, TET2, ASXL1 อาจมาจากเม็ดเลือดขาว ไม่ใช่เนื้องอก → ระบบติดป้าย "possible CHIP origin"
3. **Incidental germline finding** — variant ที่ VAF ~50% หรือ ~100% ในยีนอย่าง BRCA1/2 อาจเป็น germline → ระบบติดป้าย "possible germline — แนะนำ genetic counselling" ไม่สรุปเอง
4. **ctDNA dynamics เพื่อติดตาม response** — ยังเป็นหลักฐานระดับ emerging ในหลายมะเร็ง → ติดป้าย "Research signal" ไม่ใช่ guideline
5. **Pre-analytics** — cfDNA ต้องใช้หลอดเฉพาะ (cfDNA stabilizing tube) หรือปั่นแยก plasma ภายในเวลาจำกัด ส่วน NMR มี SOP ของตัวเอง → **แยกหลอดเก็บตัวอย่าง** (ต้องตรวจสอบกับ lab ว่าใช้หลอดร่วมกันได้หรือไม่)

---

## 5. การตีความ NMR — ค่าจริง + RCV ไม่ใช่แถบ HIGH/LOW

เลิกใช้แถบ "Lipid metabolism ████████░░ HIGH" เพราะไม่มี reference ที่ validate แล้ว

แทนด้วย **3 สิ่งต่อ analyte**:

1. **ค่าจริง + หน่วย**
2. **เทียบ reference range** ของ panel (ระบุแหล่ง และระบุว่ามี reference ของคนไทยหรือยัง)
3. **เทียบ baseline ของคนไข้เอง ด้วย Reference Change Value (RCV)**

```
RCV = √2 × Z × √(CVa² + CVi²)

CVa = analytical variation ของ assay (จาก lab / vendor)
CVi = within-person biological variation (จาก EFLM Biological Variation Database)
Z   = 1.96 (สองทาง, 95%) หรือ 1.65 (ทางเดียว)
```

- ถ้า |%change| > RCV → แสดง "**เปลี่ยนจริง**" (↑ หรือ ↓)
- ถ้าไม่เกิน → แสดง "**ไม่ต่างจากความแปรปรวนปกติ**" (→)
- ใช้ RCV แบบ asymmetric (log-normal) ได้ถ้าค่ามีการกระจายเบ้

การจัดกลุ่ม (lipid / inflammation / amino acid) **ใช้แค่จัดหน้าจอ** ไม่เรียกเป็น "phenotype" และไม่ให้คะแนนรวม

**Inflammation**: รายงาน GlycA/GlycB ตามจริง พร้อมข้อความว่า "สะท้อน acute-phase glycoprotein; ไม่แยก acute/chronic และไม่ระบุอวัยวะ" — ถ้าจะพูดเรื่อง residual inflammatory risk ให้อ้าง hs-CRP ซึ่งเป็นตัวที่ guideline ใช้

**Pre-analytic SOP**: อดอาหาร, ชนิดหลอด, เวลาปั่น, ห้าม freeze–thaw ซ้ำ — ถ้า SOP ไม่ตรงกันระหว่าง visit ระบบเตือนว่า "เทียบ trend ไม่ได้"

---

## 6. สถาปัตยกรรม — Rule engine ทำงานหลัก, LLM แค่สรุปและตอบคำถาม

### ทำไมไม่ใช้ LLM 7 ตัว

การเทียบตาราง CPIC, กฎ DDI, การคำนวณ RCV และการจัด tier ของ variant **ต้องได้ผลเหมือนเดิมทุกครั้ง** และต้องทดสอบได้ → เขียนเป็นโค้ด
LLM ใช้เฉพาะงานที่ต้องใช้ภาษา: **เรียบเรียงรายงาน** และ **ตอบคำถามแพทย์** โดยห้ามสร้าง fact ใหม่

```
Inputs (FHIR-like JSON: meds, labs, refill, PGx genotype, NMR panel, cfDNA variant report)
   │
   ├─ 1. Deterministic engines (Python, unit-tested)
   │    ├─ PGx engine: diplotype → phenotype → CPIC/DPWG recommendation
   │    ├─ DDI engine: rules จาก drug label / DDI database
   │    ├─ NMR engine: reference comparison + RCV change detection + SOP check
   │    ├─ cfDNA engine: variant → tier (AMP/ASCO/CAP) + labeled therapy
   │    │                + CHIP flag + possible-germline flag + "not detected" caveat
   │    └─ Adherence engine: refill gap → proportion of days covered (PDC)
   │
   ├─ 2. Evidence store (versioned snapshot; ทุก fact มี ID + แหล่ง + evidence level)
   │       CPIC, PharmGKB, drug labels, ClinVar, variant knowledge base (เช่น OncoKB — ต้องเช็ก license)
   │
   ├─ 3. LLM layer (2 agents เท่านั้น)
   │    ├─ Summarizer: เขียน Clinical Brief จาก fact ID เท่านั้น
   │    └─ Q&A agent: ตอบคำถามแพทย์/เภสัชกร โดย query evidence store ได้ และต้องอ้าง fact ID
   │
   ├─ 4. Verifier (code): ทุกประโยค ↔ fact ID ที่มีอยู่จริง; ตัดประโยคที่ไม่มีหลักฐานทิ้ง
   │
   └─ 5. Pharmacist review UI → accept / modify / reject → รายงานถึงแพทย์ (+ audit log)
```

**ทำไมเรียกว่า agent ได้**: Q&A agent มี tool (query evidence store, เรียก engine) และ decision loop จริง ส่วน Summarizer เป็น constrained generation ที่ถูก verifier คุม — ส่วนอื่นทั้งหมดเป็นโค้ด ไม่เรียกว่า agent

**ปุ่ม "Why?"** แสดง trace จริง: ข้อสรุป → engine ที่ให้ผล → rule/fact ID → ข้อมูลคนไข้ที่ใช้ → แหล่งหลักฐาน — ไม่ใช่ให้ LLM เล่าเหตุผลย้อนหลัง

**ระดับความเชื่อมั่น 3 ชั้น** (ติดทุก finding):
- **Guideline** — CPIC A/B, ฉลากยา, companion diagnostic
- **Emerging** — มีงานวิจัยแต่ยังไม่อยู่ใน guideline (เช่น ctDNA dynamics, pharmacometabolomics)
- **Unknown** — VUS, variant ที่ไม่มีข้อมูล

**Determinism + audit**: fix version ของ model, prompt และ evidence snapshot; ใช้ temperature 0; log ทุก input/output

**Privacy**: ข้อมูล genome ไม่ส่งออกนอกประเทศ — ใช้ LLM ที่ host ในไทยหรือ on-prem หรือส่งเฉพาะ fact ที่ลบตัวบ่งชี้ตัวตนแล้ว; กรอง free-text note ก่อนเข้า LLM (ป้องกัน prompt injection)

---

## 7. หน้าจอเภสัชกร (1 หน้า)

```
┌─ ACTION NEEDED (2) ─────────────────────────────────────────┐
│ ⚠ Clopidogrel — CYP2C19 *2/*2 (poor metabolizer)   [Guideline] │
│   CPIC: consider alternative antiplatelet if no contraindication │
│   + omeprazole co-prescribed (CYP2C19 inhibitor)    [Label]     │
│   [Why?] [Accept] [Modify] [Reject]                              │
│                                                                   │
│ ⚠ Statin response — LDL-C at goal, ApoB above goal  [Guideline]  │
│   ApoB change vs baseline: −6% (RCV ±X%) → not a real change     │
│   Adherence PDC 92%  →  adherence not the explanation            │
│   [Why?] [Accept] [Modify] [Reject]                              │
├─ MONITOR ────────────────────────────────────────────────────┤
│ GlycA: no change beyond RCV            [Emerging]              │
├─ NO ACTION ──────────────────────────────────────────────────┤
│ 7 other checks passed (collapsed)                              │
└──────────────────────────────────────────────────────────────┘
```

**หลักการลด alert fatigue**: แสดงเฉพาะ finding ที่มี action; ที่เหลือพับไว้

---

## 8. Demo — 4 เคส (ข้อมูล synthetic ติดป้ายชัด)

| เคส | เรื่อง | สิ่งที่โชว์ |
|---|---|---|
| **A** | ชาย 58 ปี post-PCI, clopidogrel + omeprazole, CYP2C19 poor metabolizer | PGx + DDI รวมเป็น 1 action card |
| **B** | หญิง 52 ปี simvastatin 40 mg, SLCO1B1 decreased function, LDL-C ถึงเป้าแต่ ApoB ยังสูง | PGx + NMR discordance + RCV |
| **C** | หญิง 45 ปี GLP-1 RA 6 เดือน น้ำหนักลดน้อย, refill gap | Adherence engine แยก "ขาดยา" ก่อนสรุปว่าไม่ตอบสนอง |
| **D (cfDNA)** | ชาย 64 ปี NSCLC EGFR+ ได้ gefitinib + PPI, โรคลุกลาม; plasma ctDNA พบ resistance mutation + DNMT3A variant | cfDNA tier + labeled therapy → oncologist; DDI TKI+PPI; CHIP flag; DPYD check ก่อนเคมีบำบัด |

แต่ละเคส: หน้าจอ 1 หน้า → "Why?" → เภสัชกร accept/modify/reject → รายงาน PDF ถึงแพทย์

**ถ้าเวลาพิตช์สั้น**: โชว์ B (ครบ PGx + NMR + RCV) และ D (cfDNA) — A และ C ไว้ตอบคำถาม

---

## 9. แผนประเมินผล (Evaluation)

### ใน hackathon
- **Gold-standard case set**: 30–50 เคส synthetic ที่ครอบคลุมทั้ง 9 สถานการณ์ในข้อ 3 เฉลยโดยเภสัชกร 2–3 คน
- **Metrics**:
  - Critical-omission rate (finding สำคัญที่ระบบพลาด) — เป้า 0
  - False-flag rate (flag ที่เภสัชกรไม่เห็นด้วย)
  - Citation precision (ทุกประโยคมี fact ID ที่ถูกและรองรับจริง)
  - Concordance กับ CPIC (ความถูกต้องของ PGx engine) — ควร 100% เพราะเป็นโค้ด
  - จำนวน alert ต่อเคส เทียบ DDI checker ปกติ (โชว์การลด noise)
  - Inter-rater agreement ระหว่างเภสัชกร (เป็นเพดานของระบบ)
- **Regression test**: รันทุกครั้งที่เปลี่ยน prompt/model/evidence snapshot

### หลัง hackathon (pilot)
- Retrospective: ผู้ป่วยจริงที่มีผล PGx/NMR/cfDNA อยู่แล้ว (ผ่าน IRB) — วัด % recommendation ที่เภสัชกรยอมรับ และจำนวน actionable finding ต่อ 100 คน
- Prospective pilot 6 เดือนในคลินิกเดียว — วัดเวลาทบทวนยาต่อราย, ADR ที่ป้องกันได้, การเปลี่ยนยาที่เกิดขึ้นจริง

**ห้าม claim**: ความแม่นยำทำนายโรค หรือผลลัพธ์ทางคลินิก จากข้อมูล synthetic

---

## 10. ข้อจำกัดทางคลินิก

- ไม่วินิจฉัยโรค ไม่เลือกยาแทนแพทย์ — ทุก recommendation ต้องผ่านเภสัชกรและแพทย์
- NMR ไม่วัดระดับยา และไม่ระบุตำแหน่งการอักเสบ
- Reference range ของ NMR ส่วนใหญ่มาจากประชากรยุโรป — ต้องมีข้อมูลคนไทยก่อนใช้ cut-off
- หลักฐาน pharmacometabolomics และ ctDNA dynamics ยังเป็นระดับ emerging
- ctDNA ผลลบไม่ตัดการมี mutation ออก; variant บางตัวอาจเป็น CHIP หรือ germline
- PGx ครอบคลุมเฉพาะยีนใน panel; ผลลบไม่ได้แปลว่าปลอดภัยทุกยา
- VUS และ incidental germline finding ต้องส่ง genetic counselling ระบบไม่สรุปเอง

---

## 11. ข้อจำกัดทางกฎหมายและ regulatory

**Intended use (ร่าง)**
> "PrecisionRx summarises existing accredited laboratory results (germline pharmacogenomic genotypes, NMR lipoprotein/metabolite panels, and cfDNA variant reports), current medications and prior visits into a structured, evidence-linked report to support pharmacist and physician medication review. It does not diagnose disease or select treatment; all recommendations require clinician review."

| ประเด็น | แนวทาง |
|---|---|
| **เครื่องมือแพทย์ (SaMD)** | ซอฟต์แวร์ที่ตีความข้อมูลรายบุคคลเพื่อการรักษามีแนวโน้มเป็นเครื่องมือแพทย์ตาม พ.ร.บ.เครื่องมือแพทย์ — ต้องปรึกษา อย. เรื่อง class (ต้องตรวจสอบ) · ลดความเสี่ยงโดย: ไม่ประมวล raw spectrum/raw sequencing, แสดงพื้นฐานของทุกคำแนะนำให้ clinician ตรวจเองได้ (สอดคล้องแนวคิด non-device CDS ใน US FDA CDS guidance 2022) |
| **Lab** | รับผลจาก lab ที่ได้ ISO 15189 เท่านั้น; ผล research-use-only ต้องติดป้าย; cfDNA ใช้ assay ที่ validate แล้ว |
| **PDPA** | ข้อมูลสุขภาพและพันธุกรรมเป็นข้อมูลอ่อนไหว (มาตรา 26) → explicit consent แยกสำหรับ PGx / NMR / cfDNA, ระบุวัตถุประสงค์, ระยะเวลาเก็บ, สิทธิ์ถอนความยินยอม, มี DPO, ไม่ส่งข้อมูลข้ามประเทศโดยไม่มีฐานทางกฎหมาย |
| **วิชาชีพ** | เภสัชกรเสนอแนะ แพทย์เป็นผู้สั่ง — ระบบบันทึก sign-off ทุกครั้ง |
| **Liability + governance** | Audit log, change control เมื่อแก้ rule/model, ช่องทางรายงาน incident, ข้อตกลงความรับผิดกับโรงพยาบาล |
| **Research** | ใช้ข้อมูลผู้ป่วยจริงต้องผ่าน IRB/EC |
| **Integration** | ส่งรายงานเข้า HIS (เช่น HOSxP) ผ่าน HL7 FHIR (Observation, MedicationStatement, DiagnosticReport, Genomics Reporting IG); ใช้ LOINC และ TMT |

---

## 12. โมเดลธุรกิจ

### ใครใช้ ใครจ่าย
| | Module A: Cardiometabolic | Module B: Oncology (cfDNA) |
|---|---|---|
| ผู้ใช้ | เภสัชกรคลินิก cardiometabolic / anticoagulation | เภสัชกรมะเร็ง + oncologist |
| ผู้จ่าย (beachhead) | โรงพยาบาลเอกชนที่มี preventive / lipid clinic | ศูนย์มะเร็ง / lab ที่ทำ liquid biopsy (partnership) |
| ผู้จ่ายระยะยาว | ประกันสุขภาพ, สวัสดิการองค์กร, รัฐ (ถ้ามีหลักฐาน cost-effectiveness) | โรงพยาบาล, ประกัน |

### รายได้ (เสนอ ต้อง validate กับลูกค้า)
- **SaaS ต่อโรงพยาบาล** (ค่าติดตั้ง + รายปี) สำหรับ Module A
- **ค่าบริการต่อรายงาน** สำหรับ Module B — แบ่งรายได้กับ lab liquid biopsy / PGx
- **เราไม่ขายการตรวจ lab** — เป็น interpretation layer ที่ต่อกับ lab หลายเจ้า (lab-agnostic)

### ทำไมคุ้ม (story สำหรับ buyer)
- **PGx ตรวจครั้งเดียวใช้ตลอดชีวิต** — ยิ่งคนไข้ได้ยาหลายตัว ยิ่งคุ้ม; PREPARE trial (Swen et al., Lancet 2023) พบ preemptive 12-gene panel ลด clinically relevant ADR ได้ราว 30%
- **ลดค่ายาแพงที่ไม่ได้ผล** — เช่น GLP-1 RA, targeted therapy: รู้เร็วว่าไม่ตอบสนอง หรือรู้ว่าเป็นเพราะขาดยา
- **ลดเวลาเภสัชกร** — รวมข้อมูล 3 แหล่งเป็นหน้าเดียว และลด alert ที่ไม่มี action

### คู่แข่งและ moat
| คู่แข่ง | เขาทำ | เราต่างตรงไหน |
|---|---|---|
| DDI checker (Lexicomp, Micromedex) | Interaction ทั่วไป | รวม PGx + response monitoring + adherence และลด noise |
| บริษัท PGx report | รายงาน PGx ครั้งเดียว | ใช้ PGx ซ้ำทุกครั้งที่สั่งยาใหม่ + เชื่อม response |
| Vendor NMR / liquid biopsy | รายงานของ assay ตัวเอง | Lab-agnostic, รวมหลาย assay, มุมมองเรื่องยา |
| CDS ใน HIS | Rule เดี่ยว ๆ | Evidence store ที่ version ได้ + longitudinal RCV + pharmacist workflow |

**Moat**: evidence store ที่ curate สำหรับบริบทไทย (TMT mapping, สิทธิการรักษา, allele frequency ของคนไทย), workflow ที่ฝังใน HIS, และข้อมูล pilot ที่พิสูจน์ผล

### Why now
- ไทยเป็นสังคมสูงวัย → polypharmacy เพิ่ม
- Preemptive PGx มีหลักฐานระดับ RCT แล้ว
- ยา GLP-1 RA และ targeted therapy แพง → ผู้จ่ายต้องการรู้ว่าใครได้ประโยชน์
- Liquid biopsy ราคาลดลงและใช้แพร่หลายขึ้น (ต้องตรวจสอบตัวเลข)
- LLM พร้อมใช้สำหรับการสรุปที่มีหลักฐานกำกับ

### Pilot success criteria (6 เดือน, 1 คลินิก)
- ≥ X% ของ recommendation ที่เภสัชกรยอมรับ
- จำนวน actionable PGx finding ต่อ 100 คน
- เวลาทบทวนยาต่อราย ลดลง Y%
- Critical omission = 0
(กำหนด X, Y ร่วมกับโรงพยาบาลก่อนเริ่ม)

---

## 13. Roadmap

| ระยะ | สิ่งที่ทำ |
|---|---|
| Hackathon | Module A + B บน synthetic data, 4 demo cases, eval 30–50 เคส |
| 0–6 เดือน | Retrospective validation กับข้อมูลจริง (IRB), หา pilot site, ปรึกษา อย. เรื่อง class |
| 6–12 เดือน | Prospective pilot 1 คลินิก, FHIR integration กับ HIS, PDPA compliance ครบ |
| 12 เดือน+ | ขยาย drug classes, สร้าง reference NMR ของคนไทยร่วมกับ lab/มหาวิทยาลัย, cost-effectiveness study |

---

## 14. อธิบายให้เพื่อนฟัง (สั้น ๆ)

เราไม่ได้ทำเครื่องตรวจ เราเอาผลตรวจ 3 อย่างที่ lab ทำเสร็จแล้วมารวมให้เภสัชกร:

- **DNA พันธุกรรม (PGx)** → ยานี้เหมาะกับคนนี้ไหม เช่น CYP2C19 ไม่ดี = clopidogrel อาจไม่ได้ผล
- **NMR** → ยาได้ผลทาง metabolic จริงไหม เทียบกับค่าเดิมของคนไข้เอง โดยใช้ RCV ดูว่าเปลี่ยนจริงหรือแค่แกว่ง
- **cfDNA** → ในคนไข้มะเร็ง ดูว่าเนื้องอกมี mutation ที่มียารักษาไหม และติดตามการตอบสนองโดยไม่ต้องตัดชิ้นเนื้อ

การเทียบ guideline เขียนเป็นโค้ดทั้งหมด AI ใช้แค่เรียบเรียงรายงานและตอบคำถาม ทุกประโยคต้องมีหลักฐานอ้างอิง เภสัชกรกดยอมรับหรือแก้ก่อนส่งให้หมอ

**ประโยคขาย**: "เราช่วยเภสัชกรตอบว่า ยานี้เหมาะกับคนไข้ไหม ได้ผลจริงไหม และถ้าไม่ได้ผล เป็นเพราะอะไร"
