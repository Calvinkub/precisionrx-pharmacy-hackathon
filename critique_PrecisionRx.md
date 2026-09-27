# PrecisionRx AI — ผลวิจารณ์จากคณะกรรมการ Hackathon (จำลอง)

> ไอเดียที่ประเมิน: `idea.md` — Multi-agent AI platform สรุป NMR metabolomics + DNA/cfDNA ให้เภสัชกรและแพทย์
> คณะกรรมการ 6 ท่าน: เภสัชกรคลินิก/PGx + วิสัยทัศน์วงการยา (ประธาน) · แพทย์อายุรกรรม · นักชีววิทยา/omics · วิศวกร AI · Regulatory + Health informatics · ธุรกิจ/Health economics
> เกณฑ์: rubric มาตรฐานใน `.claude/skills/judge-panel/SKILL.md` (ถ้างานมี rubric จริง ให้เอามาแทน)
> หมายเหตุ: ตัวเลขราคาและบางข้อกฎหมายที่ระบุว่า "ต้องตรวจสอบ" ยังไม่ได้ยืนยันกับแหล่งข้อมูลจริง

---

## 0. สรุปภาพรวมใน 30 วินาที

**คำตัดสินรวม: ทิศทางถูก วาง positioning ได้ฉลาด (CDS ไม่ใช่ AI doctor) แต่ตอนนี้ยัง "กว้างเกินจนไม่มีอะไรคม"**

- จุดแข็งที่สุด: เข้าใจเรื่อง claim discipline, human-in-the-loop, evidence-backed output, และ longitudinal/personal baseline ซึ่งเป็นแนวคิดที่ถูก
- จุดอ่อนที่สุด:
  1. **ไม่มี "การตัดสินใจเรื่องยา" ที่เจาะจงสักเรื่องเดียว** — กรรมการเภสัชจะถามว่า "เปลี่ยน decision อะไร ของยาตัวไหน"
  2. **cfDNA ผิดเครื่องมือ** สำหรับ medication management นอกมะเร็ง — ส่วนที่มีหลักฐานแข็งที่สุดของ "DNA + ยา" คือ **germline pharmacogenomics (PGx)** แต่ไอเดียไม่พูดถึงเลย
  3. **"Response: Favorable/Suboptimal" และ phenotype bar (HIGH/MODERATE) ไม่มีโมเดลหรือ reference ที่ validate แล้วรองรับ**
  4. **Multi-agent 7 ตัว ยังไม่มีเหตุผลทางวิศวกรรม** — หลายส่วนควรเป็น rule engine แบบ deterministic ไม่ใช่ LLM
  5. **ยังไม่มีโมเดลธุรกิจ, ข้อจำกัดทางกฎหมาย, และแผนประเมินผล** (ท้ายไฟล์ idea.md เขียนว่าจะทำ แต่ยังไม่ได้ทำ)

**ข้อเสนอหลัก (pivot แบบคม):**
> **"PGx-first + Metabolomic Response Monitoring สำหรับยากลุ่ม cardiometabolic"**
> ใช้ germline PGx (CPIC) เป็นแกนตัดสินใจที่มีหลักฐานระดับ guideline + ใช้ NMR (ApoB, LDL-P, TRL, GlycA) ติดตาม response ของ statin / GLP-1 RA / metformin เทียบ baseline ของคนไข้เอง โดยใช้ Reference Change Value (RCV) ตัดสินว่าเปลี่ยนจริงหรือไม่ — และให้เภสัชกรเป็นผู้ review ใน pharmacist-led clinic

---

## 1. ความขัดแย้งภายในไอเดีย (เจอก่อนเริ่มให้คะแนน)

| # | ในไอเดียเขียนว่า | แต่ | ผลต่อการพิตช์ |
|---|---|---|---|
| 1 | "ไม่ต้องทำ NMR เอง" | NMR Agent มี pipeline raw spectrum → QC → peak detection → identification → quantification | กรรมการ bio/regulatory จะถามทันทีว่าทำ spectral processing เองหรือเปล่า ถ้าใช่ = ต้องพิสูจน์ analytic validity และเข้าข่าย IVD software |
| 2 | "อย่าขาย NMR + cfDNA เป็นพระเอก" | ถ้าตัด omics ออก สิ่งที่เหลือคือ DDI checker + LLM summary ซึ่งมีอยู่แล้ว | ความแตกต่างจริงคือ omics — ต้องขาย "omics ที่ตีความเป็น decision ได้" ไม่ใช่ซ่อนมัน |
| 3 | "Clinical Decision Support ไม่ใช่ AI เลือกยา" | Medication Agent ให้ label "Favorable / Suboptimal" ต่อยาแต่ละตัว | label นี้คือการประเมินการรักษา ซึ่ง regulator มองว่าเป็น treatment recommendation |
| 4 | Genomic Agent ต้องไม่ hallucinate gene→drug | ใช้ "Evidence Agent" ค้นหลักฐาน | ถ้า Evidence Agent ค้นจาก literature แบบ runtime ก็คือแหล่ง hallucination เอง |
| 5 | ท้ายไฟล์ขอ "ธุรกิจ / ข้อจำกัดคลินิก-กฎหมาย / แยกบทบาท AI" | ยังไม่มีเนื้อหาส่วนนี้ | กรรมการธุรกิจและ regulatory จะไม่มีอะไรให้ให้คะแนน |

---

## 2. กรรมการเภสัช (ประธาน) — Clinical Pharmacist + PGx + Pharma Vision

**Verdict:** "ผมชอบที่คุณเลือกเภสัชกรเป็น user แต่ตอนนี้ผมยังหาไม่เจอว่ามันเปลี่ยนการจ่ายยาตรงไหน"

### จุดแข็ง
- เลือก positioning ถูก: medication management ไม่ใช่ diagnosis — ตรงกับทิศทาง pharmacist-led care
- แนวคิด Drug Response Card และ longitudinal monitoring ตรงกับปัญหาจริง: หมอส่วนใหญ่เห็นแค่ LDL-C ครั้งเดียว ไม่เห็น trajectory
- เข้าใจว่าต้องแยก Known / Possible / Unknown

### ผิด (Wrong)
- **cfDNA สำหรับ medication management** — PGx ใช้ **germline DNA** (เลือด/น้ำลาย, genotyping panel) ส่วน cfDNA ใช้กับ liquid biopsy มะเร็ง, NIPT, transplant rejection ถ้าไม่ได้ทำ oncology ให้ตัด cfDNA ออก
- **NMR ไม่ได้วัดยา** (ยาส่วนใหญ่อยู่ต่ำกว่า detection limit ของ NMR) — จึงบอก "response" ได้แค่ผลปลายทางทาง metabolic ไม่ได้บอก exposure หรือ adherence

### อ่อน (Weak)
- Medication Agent ที่บอก interaction 2 รายการ = ของที่ Lexicomp/Micromedex/HIS ทำอยู่แล้ว และงานวิจัยด้าน CDS พบว่า alert ถูก override สูงมาก (alert fatigue) — เพิ่ม flag ไม่ได้ช่วยเภสัชกร **ลด flag ที่ไม่สำคัญ** ต่างหากที่ช่วย
- "Response: Suboptimal" ไม่แยก **non-adherence vs non-response vs dose ไม่พอ vs drug interaction** ซึ่งเป็นงานหลักของเภสัชกร
- Inflammation phenotype ยังไม่ผูกกับยาใดเลย

### ขาด (Missing) — จุดที่กรรมการเภสัชที่รู้ vision จะเสียดายที่สุด
1. **Pharmacogenomics (PGx) ที่มี guideline จริง** — CPIC / DPWG / PharmGKB level 1A ตัวอย่างที่เกี่ยวกับคนไทยโดยตรง:
   - HLA-B\*15:02 – carbamazepine/oxcarbazepine (SJS/TEN) — พบบ่อยในคนไทย/เอเชียตะวันออกเฉียงใต้ และมีสิทธิประโยชน์ตรวจก่อนใช้ยาในไทย (ต้องตรวจสอบรายละเอียดสิทธิ สปสช. ปัจจุบัน)
   - HLA-B\*58:01 – allopurinol
   - CYP2C19 – clopidogrel, PPI, SSRI
   - SLCO1B1 – simvastatin (myopathy) → **เชื่อมกับ lipid story ได้ตรงเลย**
   - CYP2C9 + VKORC1 – warfarin; TPMT/NUDT15 – thiopurine; DPYD – 5-FU/capecitabine; UGT1A1 – irinotecan; CYP2D6 – codeine/tramadol/tamoxifen
   - หลักฐานระดับ RCT: **PREPARE trial (Swen et al., Lancet 2023)** — ใช้ 12-gene PGx panel แบบ preemptive ลด clinically relevant ADR ได้ราว 30%
2. **Adherence** — ตัวแปรใหญ่สุดของ "drug response" ต้องมี input (refill data, pill count, self-report) ก่อนสรุปว่ายาไม่ได้ผล
3. **Polypharmacy / deprescribing ในผู้สูงอายุ** — ไทยเป็นสังคมสูงวัยแล้ว (Beers criteria, STOPP/START) เป็น use case ที่เภสัชกรทำอยู่ทุกวัน
4. **Pharmacist workflow** — เภสัชกรเห็นผลตอนไหน (ก่อนพบแพทย์? คลินิก MTM? ร้านยา?) และทำอะไรได้ตามกฎหมาย (เสนอแนะ, แพทย์ลงนาม)

### Vision ของวงการยาที่ควรเอามาผูก (เพิ่มคะแนน "impact")
- Preemptive PGx ระดับประเทศ / บัตรแพ้ยาพันธุกรรม
- Model-informed precision dosing (MIPD) และ TDM
- GLP-1 RA (semaglutide/tirzepatide) — ยาแพง ใครตอบสนอง ใครควรหยุด → **metabolomic response monitoring มี story ที่ทันยุคมาก**
- Residual risk หลัง statin: LDL-C ถึงเป้าแล้วแต่ ApoB/LDL-P ยังสูง (discordance) และ residual inflammatory risk (CANTOS, LoDoCo2, COLCOT → low-dose colchicine) — ระวัง: guideline ใช้ hs-CRP ไม่ใช่ GlycA
- Pharmacist-led chronic disease clinic และ telepharmacy

### Killer questions
1. บอกมาหนึ่ง prescribing decision ที่ระบบคุณเปลี่ยนได้พรุ่งนี้ พร้อม evidence level
2. cfDNA ใช้ตัดสินใจเรื่องยาตัวไหน นอกเหนือจากมะเร็ง?
3. "Suboptimal response" validate กับ outcome อะไร ใน cohort ไหน?
4. ถ้า metabolome ไม่ดีขึ้น คุณแยก "ไม่กินยา" กับ "กินแล้วไม่ตอบสนอง" ยังไง?
5. ระบบคุณเพิ่มหรือลด alert fatigue?

### คะแนน
| Clinical need | Med-decision impact | Evidence grounding | Workflow fit | Safety | Pharma vision |
|---|---|---|---|---|---|
| 7 | 4 | 4 | 5 | 6 | 6 |

---

## 3. กรรมการแพทย์ — Internal Medicine / Cardiometabolic

**Verdict:** "หน้าจอสวย แต่ผมมีเวลา 3–5 นาทีต่อคน และตอนนี้ครึ่งหนึ่งของหน้าจอผมทำอะไรต่อไม่ได้"

### จุดแข็ง
- หน้าแรกไม่ยาว มี AI Clinical Brief — เข้าใจ time pressure ของ OPD
- ตัวอย่าง "LDL ลดแล้วแต่ particle ยังไม่ดี" เป็น clinical insight ที่จริง (LDL-C/ApoB discordance; ESC/EAS 2019 ยอมรับ ApoB เป็นเป้าหมายการรักษาได้)

### ผิด
- **Inflammation แยกเป็น acute / chronic low-grade / lipid-associated / metabolic / oxidative stress** — NMR (GlycA/GlycB) แยกแบบนี้ไม่ได้ เป็น overclaim แม้จะใช้คำว่า "associated with"

### อ่อน
- **Phenotype bar "Lipid dysregulation HIGH"** — HIGH เทียบกับประชากรไหน cut-off เท่าไร ปรับอายุ/เพศไหม มี reference ของคนไทยไหม
- **"Amino-acid metabolism HIGH"** — แพทย์ทำอะไรต่อ? ไม่มี action = noise
- ยังไม่แยก clinical validity (สัมพันธ์กับโรค) vs clinical utility (ทำตามแล้วผลลัพธ์ดีขึ้น)

### ขาด
- ไม่มีตัวอย่างผู้ป่วยที่ระบบนำไปสู่การตัดสินใจที่ **ต่างและดีกว่า** lipid panel มาตรฐาน
- ไม่มีแผนจัดการ VUS / secondary genomic findings / genetic counselling
- ไม่เทียบกับสิ่งที่ใช้อยู่: Thai CV risk score, Lp(a), hs-CRP, eGFR/UACR

### Killer questions
1. อะไรบนหน้าจอแรกที่เปลี่ยนการรักษาผมวันนี้?
2. "HIGH" ใช้ cut-off อะไร?
3. ถ้าเจอ VUS ใครคุยกับคนไข้?

### คะแนน
| Clinical problem | Actionability | Clinical validity | Workflow/time | Safety | Evidence of utility |
|---|---|---|---|---|---|
| 7 | 4 | 4 | 6 | 6 | 3 |

---

## 4. กรรมการชีววิทยา / Omics

**Verdict:** "วิทยาศาสตร์ส่วน lipoprotein ใช้ได้ แต่ inflammation, cfDNA และลูกศร ↓↓ ยังไม่มีฐานทางชีววิทยา"

### จุดแข็ง
- เลือก NMR ถูกงาน: quantitative, reproducible, ถูกเมื่อทำจำนวนมาก, lipoprotein subclass เป็นจุดแข็งจริงของ NMR
- เข้าใจว่า NMR ไม่ระบุตำแหน่งอวัยวะ

### ผิด
- **cfDNA** ไม่ใช่ data layer ที่เหมาะกับ PGx/germline risk (ดูข้อ 2)
- **Pipeline raw spectrum ที่เขียนไว้** — ในทางปฏิบัติ vendor platform (เช่น Bruker IVDr, Nightingale) ให้ quantified panel ที่ validate แล้ว การเขียน peak detection เองทำให้ต้องพิสูจน์ analytic validity ใหม่ทั้งหมด

### อ่อน
- **ลูกศร ↓ / ↓↓ / → ไม่มี model ของ variability** — การเปลี่ยนแปลงจะนับว่า "จริง" ได้ต้องเกิน Reference Change Value:
  `RCV = √2 × Z × √(CVa² + CVi²)` (CVa = analytical variation, CVi = within-person biological variation)
  → **นี่คือของที่ทำให้ Personal Baseline Agent น่าเชื่อถือขึ้นทันที** และโชว์ความรู้ lab medicine ต่อหน้ากรรมการ
- **Pre-analytics** — การอดอาหาร, ชนิดหลอด (EDTA/serum), เวลาปั่น, freeze-thaw, batch — เปลี่ยน metabolite ได้มากกว่าผลของยา ต้องมี SOP
- **"Phenotype" ที่จัดกลุ่มเอง** (lipid/inflammatory/amino acid/energy) — เป็น hand-defined grouping ไม่ใช่ entity ทางชีววิทยา ต้องบอกให้ชัด

### ขาด
- ไม่ระบุ panel/vendor และ analyte ที่ใช้จริง
- ไม่พูดถึงการ transfer หลักฐานจาก UK Biobank/ยุโรปมาคนไทย (เช่น metabolomic risk scores แบบ Buergel et al., Nature Medicine 2022) — population shift เป็นคำถามที่กรรมการชีวะชอบถาม
- โอกาส novelty ที่พลาด: genotype × metabolite (genetically influenced metabotypes, pharmacometabolomics) — เป็น "เหตุผลทางวิทยาศาสตร์" ที่ทำให้การรวม DNA + NMR มีความหมายมากกว่าแค่วางคู่กัน

### คะแนน
| Plausibility | Assay fit | Variability/confounding | Honest limits | Novelty |
|---|---|---|---|---|
| 6 | 5 | 3 | 6 | 6 |

---

## 5. กรรมการ AI / Tech

**Verdict:** "Diagram สวย แต่ถ้าผมลบ multi-agent ออกแล้วเหลือ pipeline เดียว ผมยังไม่เห็นว่าอะไรพัง"

### จุดแข็ง
- เข้าใจ risk hallucination และต้องการ evidence ทุก statement
- มี "Why?" drill-down — ถูกทิศถ้าทำเป็น trace จริง

### ผิด / เสี่ยง
- **Evidence Agent ที่ค้นหลักฐานแบบ runtime** คือแหล่ง hallucination ต้องใช้ **curated knowledge base snapshot** (CPIC, PharmGKB, ClinVar, drug label, formulary ไทย) และมี verifier ตรวจว่า citation มีอยู่จริงและรองรับ claim
- **"Explainability" ถ้าให้ LLM เล่าเหตุผลย้อนหลัง** = post-hoc narrative ไม่ใช่ explanation — "Why?" ต้องชี้ไปที่ rule/data point จริงที่ทำให้เกิดข้อสรุป

### อ่อน
- 7 agents ส่วนใหญ่คือ prompt ต่างกันบน LLM เดียว — ไม่มี tool/data source/failure mode ที่แยกกันชัด
- สิ่งที่ควรเป็น **deterministic code ไม่ใช่ LLM**: CPIC lookup (genotype → phenotype → recommendation), DDI rules, reference range, RCV, trend calculation
- LLM ควรอยู่แค่ 2 ที่: (1) สรุป/เรียบเรียง fact ที่ถูก ground แล้ว (2) ตอบคำถามแพทย์โดยอ้าง fact เดิม

### ขาด
- **แผนประเมินผล** — ตัวอย่าง metric: critical-omission rate, false-flag rate, citation precision, ความสอดคล้องกับ CPIC, inter-rater agreement กับเภสัชกร บน gold-standard case set (เช่น 30–50 เคสจำลองที่เภสัชกรเฉลยไว้)
- Determinism / versioning / audit log (prompt, model, KB version)
- Privacy: ข้อมูล genome ส่งไป cloud LLM ไหม? cross-border transfer ตาม PDPA? prompt injection จาก free-text note?
- ถ้าจะมี ML risk model ต้องบอกว่า train กับข้อมูลอะไร — ถ้าไม่มีข้อมูลจริง อย่า claim โมเดลทำนาย และติดป้าย "synthetic demo" ชัดเจน

### Reference architecture ที่เสนอ (เรียบกว่า แต่หนักแน่นกว่า)
```
Inputs (FHIR-like JSON: meds, labs, NMR panel, PGx genotype)
   │
   ├─ Deterministic layer (code, testable)
   │    ├─ PGx engine: genotype → phenotype → CPIC recommendation
   │    ├─ DDI / dose rules
   │    ├─ NMR reference + RCV change detection
   │    └─ Adherence signal (refill gap)
   │
   ├─ Evidence store (versioned KB snapshot, every fact has ID)
   │
   ├─ LLM layer
   │    ├─ Summarizer: writes brief ONLY from fact IDs
   │    └─ Q&A agent: answers clinician questions, must cite fact IDs
   │
   ├─ Verifier: every sentence ↔ fact ID; drop unsupported sentences
   │
   └─ Pharmacist review UI → sign-off → report to physician
```
เรียก "agent" ได้เฉพาะส่วนที่มี tool และ decision loop จริง (เช่น Q&A agent ที่ query KB ได้) — กรรมการ tech จะเคารพความซื่อตรงนี้มากกว่า 7 กล่อง

### คะแนน
| Architecture justification | Grounding/safety | Eval plan | Hackathon feasibility | Engineering depth | Privacy |
|---|---|---|---|---|---|
| 4 | 5 | 2 | 7 | 5 | 3 |

---

## 6. กรรมการ Regulatory + Health Informatics

**Verdict:** "Claim discipline ดีกว่าทีมส่วนใหญ่ แต่ตัว product บางส่วนยังทำเกินกว่า claim"

### จุดแข็ง
- หลีกเลี่ยงคำ AI Diagnosis / AI Prescribing / Biohacking — ถูกต้อง
- ให้แพทย์/เภสัชกรเป็นผู้ตัดสินใจ

### ประเด็นเสี่ยง
- **SaMD**: ซอฟต์แวร์ที่ตีความข้อมูลผู้ป่วยรายบุคคลเพื่อการรักษามีแนวโน้มเป็นเครื่องมือแพทย์ตาม พ.ร.บ.เครื่องมือแพทย์ (ต้องตรวจสอบการจัด class กับ อย.) — เทียบ US FDA CDS guidance (2022): ซอฟต์แวร์ที่ประมวล signal/pattern จาก IVD ถือเป็น device และ CDS ที่จะไม่เป็น device ต้องให้ clinician ตรวจสอบพื้นฐานของคำแนะนำได้เอง → **ถ้า NMR Agent ประมวล raw spectrum = เข้าข่าย device ชัดขึ้น** / ถ้ารับ quantified panel จาก lab ที่ accredited แล้ว ความเสี่ยงลดลง
- **PDPA**: ข้อมูลสุขภาพและพันธุกรรมเป็นข้อมูลอ่อนไหว (มาตรา 26) ต้องมี explicit consent, purpose limitation, การส่งข้ามประเทศ, ระยะเวลาเก็บ
- **Lab**: ผล NMR/genotype ที่ใช้ทางคลินิกต้องมาจาก lab ที่ได้ ISO 15189 ถ้าเป็น research-use-only ต้องติดป้าย
- **Integration**: ส่งรายงานเข้า HIS (เช่น HOSxP) หรือเป็น web app แยก? ถ้าแยก แพทย์ไม่เปิด — ควรพูดถึง HL7 FHIR (Observation, MedicationStatement, DiagnosticReport, Genomics Reporting IG) และ terminology (LOINC, TMT)
- **Liability**: ถ้าระบบพลาด interaction ร้ายแรง ใครรับผิด — ต้องมี audit trail และ sign-off

### Intended-use sentence ที่เสนอ
> "PrecisionRx summarises existing laboratory results (accredited NMR lipoprotein/metabolite panel and germline pharmacogenomic genotypes), current medications and prior visits into a structured, evidence-linked report to support pharmacist and physician medication review. It does not diagnose disease or select treatment; all recommendations require clinician review."

### คะแนน
| Regulatory awareness | Claim discipline | Data protection | Integration | Governance |
|---|---|---|---|---|
| 6 | 7 | 3 | 3 | 4 |

---

## 7. กรรมการธุรกิจ / Health Economics

**Verdict:** "ผมยังไม่รู้ว่าใครจ่ายเงิน"

### ประเด็น
- **Payer ≠ user**: เภสัชกรใช้ แต่ใครจ่าย — โรงพยาบาลเอกชน (preventive/lipid clinic), สปสช., ประกัน, องค์กร, หรือคนไข้เอง?
- **Unit economics**: NMR + genotype + compute ต่อคนต่อ visit — ถ้าต้องตรวจ NMR ทุก visit ต้นทุนคูณตามจำนวนครั้ง (ราคาจริงในไทย ต้องตรวจสอบ) — PGx ข้อดีคือ **ตรวจครั้งเดียวใช้ตลอดชีวิต** ซึ่งเป็น story ทางเศรษฐศาสตร์ที่ดีกว่า
- **คู่แข่ง**: DDI checker (Lexicomp, Micromedex), บริษัท PGx report, vendor metabolomics ที่มีรายงานของตัวเอง, CDS ใน HIS — moat คืออะไร?
- **Beachhead ที่แนะนำ**: pharmacist-led cardiometabolic clinic ในโรงพยาบาลเอกชน หรือ บริการ PGx ในโรงพยาบาลที่มีอยู่แล้ว
- **Outcome ที่ buyer อยากเห็น**: ADR ที่ป้องกันได้, admission ที่ลดลง, ค่ายาที่ลด (เช่น หยุด GLP-1 ในคนไม่ตอบสนอง) — ไม่ใช่ AUC
- **Why now**: สังคมสูงวัย + polypharmacy, preemptive PGx มีหลักฐาน RCT แล้ว, GLP-1 cost pressure, LLM พร้อมใช้

### คะแนน
| Market need | Business model | Differentiation | GTM | Impact metric |
|---|---|---|---|---|
| 7 | 2 | 4 | 3 | 3 |

---

## 8. ตารางคะแนนรวม (ประธานสรุป)

| เกณฑ์ (น้ำหนัก) | เภสัช | แพทย์ | Bio | Tech | Reg | Biz | เฉลี่ย |
|---|---|---|---|---|---|---|---|
| Problem significance (20%) | 7 | 7 | 6 | 6 | 6 | 7 | 6.5 |
| Innovation / differentiation (20%) | 5 | 5 | 6 | 5 | 5 | 4 | 5.0 |
| Scientific/clinical validity (20%) | 4 | 4 | 4 | 4 | 5 | 4 | 4.2 |
| Technical feasibility & demo (15%) | 6 | 6 | 5 | 6 | 5 | 5 | 5.5 |
| Safety, ethics, regulation (10%) | 6 | 6 | 6 | 4 | 5 | 5 | 5.3 |
| Business & impact (15%) | 5 | 4 | 4 | 4 | 4 | 2 | 3.8 |
| **รวมถ่วงน้ำหนัก** | | | | | | | **≈ 5.1 / 10** |

อ่านผล: ไอเดียนี้ "ผ่านรอบแรก" ได้เพราะ positioning ดี แต่ **เข้ารอบชิงยาก** ถ้ายังไม่มี decision ที่เจาะจงและแผนประเมินผล ถ้าทำตาม pivot ในข้อ 10 คาดว่าขยับไป 7–7.5 ได้

---

## 9. Kill-shot questions 3 ข้อที่ต้องเตรียมคำตอบก่อนขึ้นเวที

1. **"บอกหนึ่งการตัดสินใจเรื่องยาที่ระบบเปลี่ยน และ evidence level ของมัน"** (เภสัช + แพทย์)
   → คำตอบที่ดี: "ผู้ป่วยได้ simvastatin, SLCO1B1 decreased function → CPIC แนะนำเลี่ยง simvastatin ขนาดสูง/พิจารณา statin อื่น; ระบบเห็น LDL-C ถึงเป้าแต่ ApoB ยังเกิน RCV จาก baseline → flag residual risk ให้เภสัชกร review" (ต้องตรวจสอบถ้อยคำ CPIC ฉบับล่าสุดก่อนพิตช์)
2. **"ทำไมต้อง cfDNA และทำไมต้อง 7 agents?"** (Bio + Tech)
   → ตัด cfDNA เป็น germline PGx; ตอบว่า agent มีแค่ส่วนที่มี tool จริง ส่วนอื่นเป็น deterministic engine
3. **"ใครจ่าย และคุณวัดความสำเร็จด้วยอะไร?"** (Biz + Reg)
   → ระบุ buyer หนึ่งราย + outcome ของ pilot (เช่น % รายงานที่เภสัชกรเห็นด้วย, จำนวน actionable PGx finding ต่อ 100 คน, เวลาทบทวนยาที่ลดลง)

---

## 10. ข้อเสนอ Pivot: "PrecisionRx — PGx-anchored Medication Review with Metabolomic Response Tracking"

### เปลี่ยนอะไร
| เดิม | ใหม่ |
|---|---|
| DNA/cfDNA risk | **Germline PGx panel** (CPIC level A/B) + optional Lp(a)/FH ถ้ามี |
| NMR raw spectrum pipeline | รับ **quantified NMR panel** จาก lab (ApoB, LDL-P, small LDL-P, TRL, HDL-P, GlycA, BCAA, glucose/lactate) |
| Phenotype bars HIGH/MOD/LOW | **ค่าจริง + reference + RCV-based change จาก baseline คนไข้เอง** |
| Response: Favorable/Suboptimal | "**Change beyond expected variation: yes/no**" + สาเหตุที่ต้องทบทวน (adherence, dose, PGx, DDI) |
| 7 LLM agents | Deterministic engines + LLM summarizer + Q&A agent + verifier |
| ทุกโรค ทุกยา | **3 กลุ่มยา**: statin, GLP-1 RA, antiplatelet (clopidogrel) — + HLA safety check เป็น bonus |
| User ไม่ชัด | **เภสัชกรใน cardiometabolic clinic** review ก่อนพบแพทย์ |

### Demo ที่แนะนำ (ทำได้ในเวลา hackathon) — 3 patient stories (synthetic, ติดป้ายชัด)
1. **คุณ A – statin + SLCO1B1**: LDL-C ถึงเป้า แต่ ApoB/LDL-P ยังสูงเกิน RCV → residual risk + PGx flag → เภสัชกรเสนอทบทวน statin
2. **คุณ B – GLP-1 RA 6 เดือน**: น้ำหนักลดน้อย, refill gap พบ → ระบบบอก "ทบทวน adherence ก่อนสรุปว่าไม่ตอบสนอง"
3. **คุณ C – post-PCI ได้ clopidogrel + CYP2C19 poor metabolizer + ได้ omeprazole** → CPIC flag + DDI → เสนอพิจารณาทางเลือก (แพทย์ตัดสิน)

แต่ละเคส: หน้าจอ 1 หน้า → ปุ่ม "Why?" ที่ชี้ไป rule/fact ID จริง → เภสัชกรกด accept/modify/reject → export รายงานให้แพทย์

### Metric ที่โชว์ได้บนเวที
- Concordance กับคำตอบเภสัชกร 2–3 คนบน 30 เคสจำลอง
- Citation precision (ทุกประโยคมี fact ID ที่ถูกต้อง)
- จำนวน alert ต่อเคส เทียบกับ DDI checker ปกติ (โชว์ว่า **ลด noise**)

---

## 11. Checklist ก่อนพิตช์

- [ ] ตัดหรืออธิบาย cfDNA (แนะนำตัด)
- [ ] เพิ่มสไลด์ PGx พร้อม CPIC/PharmGKB level และตัวอย่างที่เกี่ยวกับคนไทย (HLA-B\*15:02, HLA-B\*58:01, CYP2C19)
- [ ] เปลี่ยน phenotype bar เป็นค่าจริง + reference + RCV
- [ ] ระบุ vendor/panel NMR ที่สมมติว่าใช้ และบอกว่าไม่ทำ spectral processing เอง
- [ ] แยก rule engine vs LLM บน architecture slide
- [ ] มี eval plan + ตัวเลขจากเคสจำลอง (ติดป้าย synthetic)
- [ ] Intended-use sentence 1 ประโยค
- [ ] สไลด์ PDPA + consent + ที่เก็บข้อมูล genome
- [ ] โมเดลธุรกิจ: buyer, ราคาต่อคน, pilot outcome
- [ ] ตรวจทุก citation ในสไลด์ (PREPARE, CPIC wording, สิทธิ สปสช.) กับแหล่งจริงก่อนขึ้นเวที

---

*สร้างด้วย judge skills ใน `.claude/skills/` — รันซ้ำได้ด้วย skill `judge-panel` เมื่อแก้ไอเดียแล้ว*
