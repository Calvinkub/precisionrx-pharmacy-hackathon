# PrecisionRx — Business & Go-to-Market Strategy

> เอกสารกลยุทธ์ธุรกิจสำหรับ hackathon (ประกอบ `idea.md` v2 และ `critique_PrecisionRx.md`)
> ขนาดตลาดและราคาคู่แข่งแบบละเอียดอยู่ในไฟล์แยก `market_research.md` (อีก agent ทำ) — เอกสารนี้เน้น **กลยุทธ์** ไม่ทำ market sizing ซ้ำ
> วันที่: 27 ก.ย. 2026

## ข้อควรรู้ก่อนอ่าน (พูดตรง ๆ)

> PrecisionRx ตอนนี้ **ยังไม่มีบริษัท ไม่มีโรงพยาบาลหรือ lab ที่เป็นพาร์ทเนอร์ ไม่มี LOI ไม่มีข้อมูลผู้ป่วยจริง และไม่มีรายได้** ตัวเลขเศรษฐศาสตร์ทุกตัวในเอกสารนี้ที่ไม่มี URL กำกับเป็น **สมมติฐานของทีม** เพื่อแสดงวิธีคิด ไม่ใช่ผลลัพธ์ บนเวทีให้พูดแบบนี้ก่อนที่กรรมการจะถาม

**สัญลักษณ์**
- ✅ **verified** — มีแหล่งอ้างอิงหลัก (URL กำกับ)
- 🟡 **secondary** — มีแหล่งแต่ยังไม่ได้อ่านต้นฉบับเต็ม / ต้องยืนยันก่อนขึ้นสไลด์
- 📊 **recommendation / assumption** — การวิเคราะห์หรือสมมติฐานของทีม ไม่ใช่ข้อเท็จจริง

---

## 0. คำแนะนำหลักใน 5 บรรทัด

1. **Beachhead = "เปิดใช้ผล PGx ที่โรงพยาบาลขายไปแล้ว"** ในโรงพยาบาลเอกชนที่มีบริการ PGx อยู่แล้ว — เริ่มที่คลินิก cardiometabolic / anticoagulation ที่เภสัชกรเป็นผู้ทบทวนยา 📊
2. **Module A เริ่มจาก PGx + DDI + adherence ก่อน** แล้วค่อยเพิ่ม NMR response monitoring เป็น add-on (NMR ต้องตรวจซ้ำทุก visit และยังไม่มี reference ของคนไทย → ต้นทุนและหลักฐานยังไม่พร้อมเป็นตัวนำ) 📊
3. **Module B (cfDNA oncology) ขายผ่าน lab** แบบ per-report / revenue share ไม่ขายตรงให้โรงพยาบาลในปีแรก 📊
4. **โมเดลรายได้ที่แนะนำ**: ค่าบริการต่อ "ผู้ป่วยที่มีผล PGx ที่ active ต่อปี" (per-active-patient-per-year) + ค่าติดตั้งครั้งเดียว — ไม่ใช่ SaaS เหมาจ่ายก้อนใหญ่ 📊
5. **ตัวชี้วัด pilot หลัก**: ≥70% ของ recommendation ที่เภสัชกรยอมรับ และ critical omission = 0 บนเคสที่ตรวจคู่ — ตั้งไว้ก่อนเริ่ม และตกลงร่วมกันว่าผลแบบไหนคือ "หยุด" 📊

---

## 1. แผนที่ลูกค้าและผู้จ่าย (Customer & payer map)

หลักคิด: แยก 3 คำถามที่มักถูกรวมกัน — **ใครใช้**, **ใครจ่าย (งบบรรทัดไหน)**, **ใครได้ประโยชน์** — ถ้าตอบรวมกันเป็นคำเดียว ("โรงพยาบาล") กรรมการธุรกิจจะรู้ทันทีว่ายังไม่ได้คุยกับลูกค้า

### Module A — Cardiometabolic (PGx + DDI + adherence → + NMR ภายหลัง)

| บทบาท | ใคร | หมายเหตุ |
|---|---|---|
| **User (ผู้ใช้ทุกวัน)** | เภสัชกรคลินิกใน lipid / anticoagulation / DM clinic, เภสัชกรจ่ายยา OPD | ต้องการ: รู้ว่าคนไข้มีผล PGx, ลด alert ที่ไม่มี action, เอกสารส่งแพทย์ |
| **Secondary user** | แพทย์อายุรกรรม / cardiology | อ่านรายงาน 1 หน้า ตัดสินใจ |
| **Buyer (คนเซ็น PO)** | ผู้อำนวยการฝ่ายเภสัชกรรม + ผู้บริหารศูนย์ genomic / precision medicine ของโรงพยาบาล | ศูนย์ genomic มีแรงจูงใจชัด: ผล PGx ที่ขายไปแล้วถูกใช้ซ้ำ = คุณค่าของบริการ PGx สูงขึ้น |
| **Budget line** | (1) งบ IT / clinical software ของฝ่ายเภสัช หรือ (2) ต้นทุนบริการของแพ็กเกจ PGx (บวกเข้าราคาขายให้ผู้ป่วย self-pay) | 📊 แนะนำทาง (2) ในปีแรก — ไม่ต้องรอรอบงบ IT ประจำปี |
| **Decision maker / gatekeeper** | คณะกรรมการเภสัชกรรมและการบำบัด (PTC), ฝ่าย IT (integration กับ HIS), ฝ่ายกฎหมาย/DPO (PDPA ข้อมูลพันธุกรรม) | PTC เป็นคนอนุมัติ rule ทางคลินิก — ต้องมีเภสัชกรอาวุโสเป็น champion |
| **Beneficiary** | ผู้ป่วย (ADR น้อยลง, ไม่ได้ยาที่ไม่ได้ผล), โรงพยาบาล (ความเสี่ยงทางกฎหมายจาก ADR ที่ป้องกันได้ลดลง, รายได้บริการ PGx) | |
| **Long-term payer** | ประกันสุขภาพเอกชน / สวัสดิการองค์กร (ยาแพง เช่น GLP-1 RA), สปสช. (ต้องมี cost-effectiveness ก่อน) | ไม่ใช่ beachhead — ดูข้อ 6 |

### Module B — Oncology (cfDNA + germline PGx + TKI DDI)

| บทบาท | ใคร | หมายเหตุ |
|---|---|---|
| **User** | เภสัชกรมะเร็ง (oncology pharmacist) + oncologist | |
| **Buyer** | **lab ที่ทำ liquid biopsy / NGS** (ใช้การตีความเชิงยาเป็นจุดขายของรายงาน) — รองลงมาคือศูนย์มะเร็งของโรงพยาบาลเอกชน | |
| **Budget line** | ต้นทุนต่อรายงานของ lab (COGS) — ผู้ป่วยจ่าย self-pay เป็นส่วนใหญ่ | ✅ แนวทางผู้เชี่ยวชาญไทยระบุว่า "financial considerations are a major barrier... NGS which require patients to self-pay" ([Shuangshoti et al., TLCR](https://tlcr.amegroups.org/article/view/103441/html)) |
| **Decision maker** | ผู้อำนวยการ lab / medical director ของ lab, หัวหน้าหน่วยมะเร็ง | |
| **Beneficiary** | ผู้ป่วย NSCLC EGFR+ (ไม่ต้องตัดชิ้นเนื้อซ้ำ, หลีกเลี่ยง TKI+PPI interaction), oncologist | |
| **Long-term payer** | โรงพยาบาล, ประกันมะเร็ง (ยา targeted therapy แพง) | |

**บริบทที่ยืนยันแล้วสำหรับ Module B**
- ✅ ผู้ป่วย metastatic NSCLC 681 รายที่โรงพยาบาลตติยภูมิที่ใหญ่ที่สุดของไทย มี EGFR mutation 317 ราย (47.0%) ช่วงปี 2014–2018 ([PubMed 36895484](https://pubmed.ncbi.nlm.nih.gov/36895484/)) — ใช้แทนข้อความ "ต้องตรวจสอบตัวเลขความชุก" ใน idea.md ได้
- ✅ แนวทางไทยแนะนำ liquid biopsy เมื่อไม่มีชิ้นเนื้อพอ หรือตรวจ EGFR T790M ตอนดื้อยา TKI รุ่น 1–2; NGS ในไทยใช้เวลา 10–30 วัน ([TLCR](https://tlcr.amegroups.org/article/view/103441/html))
- ⚠️ แพ็กเกจ "ctDNA cancer screening" ของโรงพยาบาลเอกชนบางแห่ง (เช่น [Phyathai](https://www.phyathai.com/en/pyt2/package/ctdna-program-pt2), [Samitivej](https://www.samitivejhospitals.com/package/detail/Circulating-Tumor-DNA)) เป็น **การคัดกรองมะเร็งในคนสุขภาพดี** ไม่ใช่การเลือกยาในผู้ป่วยมะเร็ง — อย่านับเป็นตลาดของ Module B

---

## 2. Beachhead — เลือกอะไร และทำไม

### ตัวเลือกที่พิจารณา

| ตัวเลือก | ข้อดี | ข้อเสีย | คำตัดสิน 📊 |
|---|---|---|---|
| **A1. โรงพยาบาลเอกชนที่ขาย PGx อยู่แล้ว → คลินิก cardiometabolic** | ผล PGx มีอยู่แล้ว (ไม่มีต้นทุนตรวจเพิ่ม); ผู้ป่วย self-pay ยอมจ่าย; ตัดสินใจเร็วกว่ารัฐ; มีศูนย์ genomic เป็น champion | จำนวนผู้ป่วยที่มีผล PGx ต่อโรงพยาบาลยังไม่ทราบ [DATA REQUIRED]; แต่ละแห่งใช้ HIS ต่างกัน | **✅ เลือก** |
| A2. โรงพยาบาลมหาวิทยาลัย (มี PGx lab เอง) | มีข้อมูลและผู้เชี่ยวชาญ; เหมาะ validate | มักสร้างเครื่องมือเอง; จัดซื้อช้า | เป็น **clinical/validation partner** ไม่ใช่ลูกค้าจ่ายเงินรายแรก |
| A3. สปสช. / โรงพยาบาลรัฐทั่วประเทศ | ขนาดใหญ่มาก; HLA-B screening อยู่ในสิทธิประโยชน์แล้ว | ต้องมี cost-effectiveness; จัดซื้อยาวหลายปี | ระยะยาว (12–36 เดือน+) |
| A4. ประกัน / สวัสดิการองค์กร (GLP-1 program) | งบยาแพงเป็นแรงจูงใจ | ยังไม่มีหลักฐาน NMR response ในคนไทย; ข้อมูลพันธุกรรมกับประกันเสี่ยงเรื่องความไว้วางใจ | หลังมีข้อมูล pilot |
| B1. Lab liquid biopsy (Module B) | lab ต้องการความต่างของรายงาน; ขายเป็นต่อรายงาน | ตลาดเล็กกว่า (เฉพาะผู้ป่วยมะเร็งที่ตรวจ NGS); ต้องใช้ knowledge base ที่อาจติด license (เช่น OncoKB) | **ช่องทางที่สอง** ขนานกันแบบเบา ๆ |

### ทำไม A1 (เหตุผลที่ยืนยันได้)

1. **ปัญหามีหลักฐานจริงในไทย: ผล PGx ไม่ถูกใช้ตอนสั่งยา** — ✅ งานวิจัยย้อนหลัง 10 ปีของไทย (13,985 tests, 2011–2020) ระบุว่า "there is currently no PGx alert system connected with the electronic health records (EHR) in Thailand" และรายงานเคสผู้ป่วย HLA-B\*15:02 positive ที่ได้ carbamazepine เพราะไม่มี alert แล้วเสียชีวิต ([PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/)) — 🟡 บทความนี้ตีพิมพ์ปี 2022 ต้องเช็กว่าหลังจากนั้นมีโรงพยาบาลไหนทำ PGx-CDS แล้วบ้าง (เช่น บทความ ["Clinical pharmacogenomics implementation in Thailand: a dream come true" (2023)](https://pubmed.ncbi.nlm.nih.gov/37222126/) ที่ยังไม่ได้อ่านฉบับเต็ม)
2. **ความต้องการตรวจโตเร็ว** — ✅ HLA-B tests เพิ่มจาก 94 (2011) เป็น 2,880 (2020) ([PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/))
3. **ยาที่เรา demo คือยาที่คนไทยใช้จริงและ actionable บ่อย** — ✅ ในผู้ใหญ่ไทย 4,662 คน (Siriraj) 95.99% มีผล CPIC-actionable อย่างน้อย 1 ยีน; ในผู้ที่ใช้ omeprazole มี CYP2C19 phenotype ที่ actionable 55.02%; ในผู้ใช้ statin มี SLCO1B1 actionable ~22–23% ([PLOS One 2026, PMC13432136](https://pmc.ncbi.nlm.nih.gov/articles/PMC13432136/)) → ตรงกับเคส A และ B ใน demo
4. **โรงพยาบาลเอกชนขาย PGx อยู่แล้ว** (ดูรายชื่อด้านล่าง) → เราไม่ต้องขายการตรวจ แค่ทำให้ผลที่มีอยู่ทำงาน
5. **PGx ตรวจครั้งเดียวใช้ตลอดชีวิต** → คุณค่าต่อผู้ป่วยสะสมทุกครั้งที่สั่งยาใหม่ ขณะที่ NMR ต้องตรวจซ้ำ → ต้นทุนคูณตาม visit (ตรงกับคำวิจารณ์ของกรรมการธุรกิจ)

### ลูกค้า 3 ประเภทแรกในไทย

| ลำดับ | ประเภท | ตัวอย่างที่ยืนยันว่ามีบริการที่เกี่ยวข้องจริง | บทบาท |
|---|---|---|---|
| **1** | **โรงพยาบาลเอกชนที่มีบริการ PGx / genomic center** (design partner + ลูกค้าจ่ายเงินรายแรก) | ✅ Bumrungrad — มี Pharmacogenomics and Precision Medicine division ([bumrungrad.com](https://www.bumrungrad.com/en/centers/preventive-genomics-integrative-medicine), [HLA-B lab guide](https://www.bumrungrad.com/lab-service-guide/labs/pharmacogenomics-in-hla-b)) · ✅ Bangkok Hospital — ตรวจ PGx ด้วย NGS "Drug-Gene Profile" ([bangkokhospital.com](https://www.bangkokhospital.com/en/content/pharmacogenomics)) · ✅ Samitivej — Genomics and Lifestyle Wellness Center ([samitivejhospitals.com](https://www.samitivejhospitals.com/center/detail/Samitivej-Genomic-and-Life-Style-Wellness-Center)) | ขาย: "ผล PGx ของคนไข้คุณถูกใช้ทุกครั้งที่สั่งยา" |
| **2** | **Lab PGx / liquid biopsy** (ช่องทางจัดจำหน่าย + Module B) | ✅ Ramathibodi Pharmacogenomics and Personalized Medicine laboratory ([rama.mahidol.ac.th](https://www.rama.mahidol.ac.th/postgrad/clinicalpatho/Lab/Pharmacogenomics)); lab NGS ภาครัฐ/เอกชนมีหลายแห่ง ([Cancer Biol Med 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10875286/)) — ยังไม่ระบุชื่อ lab liquid biopsy เอกชนเพราะยังไม่ได้ยืนยัน | รายงาน lab + "interpretation layer เชิงยา" |
| **3** | **โรงพยาบาลมหาวิทยาลัย / คณะเภสัชศาสตร์** (clinical + validation partner, ไม่ใช่ลูกค้าจ่ายเงิน) | ✅ Ramathibodi (PGx card, TPGxD database) ([Sukasem et al.](https://www.tandfonline.com/doi/full/10.2217/pgs-2015-0009)); ✅ Siriraj (cohort PGx 4,662 ราย) ([PMC13432136](https://pmc.ncbi.nlm.nih.gov/articles/PMC13432136/)) | gold-standard case set, IRB, retrospective validation, ความน่าเชื่อถือ |

📊 **สิ่งที่ห้ามพูดบนเวที**: "เรากำลังคุยกับ Bumrungrad/Bangkok Hospital" — ยังไม่มีการคุย ให้พูดว่า "เป้าหมายคือโรงพยาบาลเอกชนที่ **มีบริการ PGx อยู่แล้ว** เช่น ... (มีบริการจริงตามเว็บไซต์) — pipeline ตอนนี้ = ศูนย์"

---

## 3. Positioning และความแตกต่าง

### Positioning statement (📊)

> **สำหรับ** เภสัชกรคลินิกในโรงพยาบาลที่มีผลตรวจ PGx / NMR / cfDNA ของผู้ป่วยอยู่แล้ว
> **ที่** ต้องทบทวนยาแต่ผลตรวจเหล่านั้นกระจายอยู่ใน PDF และบัตร ไม่ได้ถูกใช้ตอนสั่งยา และจมอยู่ใต้ alert DDI ที่ถูก override เกือบหมด
> **PrecisionRx คือ** ชั้นตีความ (interpretation layer) ที่เป็นอิสระจาก lab
> **ที่** เปลี่ยนผลตรวจทุกแหล่งให้เป็น "action card" ไม่กี่ใบต่อผู้ป่วย พร้อมหลักฐานตรวจสอบได้ทุกบรรทัด
> **ต่างจาก** DDI checker และรายงาน lab ตรงที่เราใช้ผลพันธุกรรมซ้ำทุกครั้งที่สั่งยาใหม่ แยกสาเหตุ "ยาไม่ได้ผล" (ขาดยา / ขนาด / DDI / พันธุกรรม) และลด alert แทนที่จะเพิ่ม

**ประโยคเดียว (Thai)**: "ผลตรวจยีนที่คนไข้จ่ายไปแล้ว ถูกใช้ทุกครั้งที่หมอสั่งยาใหม่ — และเภสัชกรเห็นเฉพาะสิ่งที่ต้องทำ"

### ทำไม "ลด alert" คือจุดขาย (ยืนยันแล้ว)
✅ Meta-analysis พบอัตรา override ของ DDI alert โดยแพทย์ ~90% (95% CI 85–95%) จาก 16 การศึกษา ([Felisberto et al., Health Informatics J 2024](https://journals.sagepub.com/doi/10.1177/14604582241263242)) และ systematic review อีกชิ้นพบช่วง override 46–96% ([PMC7400042](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7400042/))

### เทียบคู่แข่งตามสิ่งที่ผู้ซื้อจะทำแทนการซื้อเรา

| ทางเลือกของผู้ซื้อ | ทำอะไรได้ | ช่องว่าง | เราต่างตรงไหน |
|---|---|---|---|
| **ไม่ทำอะไร (status quo)** — ผล PGx เป็น PDF/บัตร, เภสัชกรจำเอง | ฟรี | ✅ ไม่มี PGx alert ใน EHR ไทย (2022) + เคสเสียชีวิต ([PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/)) | **คู่แข่งอันดับ 1 จริง ๆ** — ต้องขายด้วยความเสี่ยงของการไม่ทำ |
| **DDI checker** (Lexicomp, Micromedex) | ฐานข้อมูล interaction ทั่วไป | ไม่รู้ genotype ของผู้ป่วย, ไม่มี longitudinal response, alert fatigue | ผสาน PGx + DDI เป็น card เดียว (เช่น clopidogrel + CYP2C19 PM + omeprazole), พับ alert ที่ไม่มี action |
| **PGx report vendor / lab** | รายงานครั้งเดียวตอนตรวจ (+ บัตร) | ไม่ถูกเรียกใช้ตอนสั่งยาปีต่อมา; ไม่เชื่อมยาปัจจุบัน/adherence | ผล PGx "ตื่น" ทุกครั้งที่มีใบสั่งยาใหม่ |
| **Liquid biopsy vendor report** | variant + tier + ยาตามฉลาก ของ assay ตัวเอง | ไม่รวม germline PGx (DPYD/UGT1A1) และ DDI ของ TKI; vendor-locked | lab-agnostic, มุมมองเภสัชกร, CHIP/germline flag |
| **CDS ใน HIS** | rule เดี่ยว (drug-allergy, dose) | ส่วนใหญ่ยังไม่รับ genotype แบบ structured; ไม่มี RCV/trend; ไม่มี evidence versioning | evidence store versioned + RCV + pharmacist workflow + audit |
| **PGx-CDS ต่างประเทศ** (เช่น GenXys TreatGx, Epic Genomics module) | PGx-CDS ครบ | ไม่มีบริบทไทย (TMT, สิทธิการรักษา, allele ไทย); Epic ไม่ใช่ HIS หลักของไทย | Thai-first evidence store + ต่อ HIS ไทย |

✅ หลักฐานว่า PGx-CDS เป็นหมวดสินค้าที่มีจริง: Epic Genomics module มี "Genomic Indicators" สำหรับ PGx alerts ([Frontiers Pharmacol 2024](https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2024.1458095/full)); GenXys ขาย TreatGx ให้ health systems ([genxys.com](https://www.genxys.com/clinical-decision-support-system/))

### "ทำไมโรงพยาบาลใหญ่หรือ HIS vendor ไม่สร้างเอง?"

**คำตอบที่ซื่อตรง: เขาสร้างได้ และบางเจ้าจะสร้าง** — Epic ทำแล้ว (ด้านบน) และ Ramathibodi ทำ PGx card เอง ดังนั้น "เขาทำไม่ได้" เป็นคำตอบที่ผิด ความได้เปรียบของเราคือ **เวลาและโฟกัส** ไม่ใช่ความเป็นไปไม่ได้ ใช้ test 3 ข้อ:

| คำถาม | HIS vendor ไทย | โรงพยาบาลเอกชนใหญ่ |
|---|---|---|
| ซื้อ/สร้าง capability ได้ไหม? | ได้ | ได้ |
| กินรายได้เดิมไหม? | ไม่ | ไม่ |
| ต้องเปลี่ยนสิ่งที่เปลี่ยนเร็วไม่ได้ไหม? | **ใช่** — ต้องสร้างและ **ดูแลต่อเนื่อง** evidence store (CPIC อัปเดตเรื่อย ๆ), รับภาระ SaMD/อย. และ liability ทางคลินิก ซึ่งไม่ใช่ธุรกิจหลัก | **ใช่** — ต้องมีทีม informatics + เภสัชกร curate ถาวร, และทำซ้ำทุกโรงพยาบาลในเครือที่ใช้ HIS ต่างกัน |

เหตุผลเฉพาะที่ใช้ได้ (📊 แต่มีหลักฐานประกอบ):
1. **ภาระ regulatory เป็นต้นทุนจริง** — ✅ Translational Software หยุดให้บริการ PGx decision support ในสหรัฐหลังไม่ผ่าน 510(k) ([Precision Medicine Online](https://www.precisionmedicineonline.com/business-news/pgx-labs-searching-new-result-reporting-options-after-translational-softwares-failed)) → HIS vendor ที่ขายระบบให้โรงพยาบาลหลายร้อยแห่งไม่อยากแบกความเสี่ยง SaMD ของ clinical interpretation ในผลิตภัณฑ์หลัก
2. **HIS vendor ไทยมีลำดับความสำคัญอื่น** — ✅ Bangkok Medical Software (HOSxP) ระบุว่าระบบของตน serve "more than 90% of hospitals" ในไทย และ AI ที่เปิดตัวล่าสุดคือ documentation (PresScribe ใน 35 โรงพยาบาล) ไม่ใช่ PGx ([Microsoft Source Asia, พ.ค. 2025](https://news.microsoft.com/source/asia/features/bangkok-medical-software-utilizes-presscribeai-by-looloo-health-to-enhance-healthcare-services-across-35-hospitals-in-thailand/)) — 🟡 ตัวเลข 90% เป็นคำกล่าวของบริษัท
3. **ผู้ป่วย PGx ส่วนใหญ่ตอนนี้อยู่ในโรงพยาบาลเอกชน/มหาวิทยาลัย** ไม่ใช่กลุ่มหลักของ HOSxP → HIS vendor ยังไม่มีแรงกดดันจากลูกค้า

**กลยุทธ์ที่ถูกต้อง: อย่าแข่งกับ HIS — เป็น module ที่เสียบเข้า HIS** (FHIR / HL7) และให้ HIS vendor เป็น channel ในระยะ 2 ถ้า HIS vendor ตัดสินใจสร้างเอง เราต้องมีสิ่งที่เขาต้องมาซื้อ/ขอ license: **Thai evidence store ที่ curate + validation dataset + regulatory file**

**Moat ที่เป็นไปได้จริง (ไม่ใช่เทคโนโลยี)**
1. Evidence store สำหรับไทย (CPIC ↔ TMT mapping, สิทธิการรักษา, allele frequency ไทย เช่น TPGxD) — ✅ มีฐานข้อมูลไทยให้ต่อยอด ([TPGxD-1](https://ascpt.onlinelibrary.wiley.com/doi/10.1111/cts.13830))
2. Gold-standard case set + ผล retrospective validation กับข้อมูลจริง (สร้างได้เฉพาะคนที่มีพาร์ทเนอร์)
3. Integration ที่ติดตั้งแล้ว (switching cost)
4. เอกสาร regulatory / intended use ที่ผ่าน อย. (ถ้าต้องขึ้นทะเบียน)

---

## 4. โมเดลธุรกิจ

### ตัวเลือก

| โมเดล | ใครจ่าย | ข้อดี | ข้อเสีย |
|---|---|---|---|
| **(1) SaaS ต่อโรงพยาบาล** (ค่าติดตั้ง + รายปีเหมา) | งบ IT โรงพยาบาล | รายได้คาดการณ์ได้ | ต้องเข้ารอบงบประจำปี; ราคาก้อนใหญ่ต้องผ่านหลายชั้น; ขายยากตอนยังไม่มีหลักฐาน |
| **(2) Per-report / per-review fee** | โรงพยาบาลหรือผู้ป่วย (ผ่านบิล) | ตรงกับคุณค่า; เริ่มเล็กได้ | รายได้ผันผวน; อาจสร้างแรงจูงใจให้สั่ง review เกินจำเป็น |
| **(3) Lab revenue share** (ฝังในรายงาน lab) | lab (ส่งต่อให้ผู้ป่วยในราคาตรวจ) | ใช้ช่องทางขายของ lab; ไม่ต้องขายทีละโรงพยาบาล | ผูกกับ volume ของ lab; lab อาจสร้างเองเมื่อ volume สูง; ความเป็น lab-agnostic ลดลงถ้าผูกเจ้าเดียว |
| **(4) Insurer / corporate program** | ประกัน / HR | งบใหญ่ (ยาแพง) | ยังไม่มีหลักฐานผลลัพธ์; ข้อมูลพันธุกรรม + ประกัน = ความเสี่ยงความไว้วางใจ/PDPA; รอบขายยาว |
| **(5) Per-active-PGx-patient-per-year (แนะนำ)** | โรงพยาบาล (ส่งต่อในแพ็กเกจ PGx ได้) | ราคาขึ้นกับจำนวนผู้ป่วยที่ได้ประโยชน์จริง; เริ่มเล็ก; ผูกกับคุณค่า "PGx ใช้ซ้ำตลอดชีวิต" | ต้องนิยาม "active" ชัด (เช่น มีใบสั่งยาอย่างน้อย 1 ครั้ง/ปี) |

### คำแนะนำ 📊

- **Module A**: **(5) + ค่าติดตั้งครั้งเดียว** — โรงพยาบาลจ่ายต่อผู้ป่วยที่มีผล PGx ในระบบและมีการสั่งยาในปีนั้น; มี tier ขั้นต่ำต่อปีเพื่อให้คุ้มค่า integration; NMR response monitoring เป็น add-on คิดต่อ NMR report ที่ประมวล
- **Module B**: **(3) lab revenue share / per-report** — lab จ่ายต่อรายงานที่ใช้ interpretation layer
- **ระยะ 2**: HIS vendor เป็น reseller (revenue share) — ขยายไปโรงพยาบาลรัฐเมื่อมี cost-effectiveness
- **ระยะ 3**: insurer/corporate program เฉพาะ "ยาแพง" (GLP-1 RA, targeted therapy) โดยประกันเห็นแค่ **ผลรวม aggregate** ไม่เห็นผลพันธุกรรมรายบุคคล
- **ไม่ขายการตรวจ lab เอง** (คงหลักการ lab-agnostic จาก idea.md)

### Unit economics แบบสาธิต (ทุกตัวเลขเป็นสมมติฐาน — ห้ามอ้างเป็นข้อมูล)

> ⚠️ ตัวเลขด้านล่างเป็น **placeholder เพื่อแสดงโครงสร้าง** ทีมยังไม่มีข้อมูลราคาที่ลูกค้ายอมจ่ายจริง ต้นทุน cloud/LLM จริง หรือจำนวนผู้ป่วย PGx ต่อโรงพยาบาล — ให้แทนด้วยข้อมูลจาก `market_research.md` และการสัมภาษณ์ลูกค้า

| ตัวแปร | ค่าสมมติ | สถานะ |
|---|---|---|
| ผู้ป่วยที่มีผล PGx และ active ต่อโรงพยาบาลต่อปี (N) | 1,000 | 📊 ASSUMPTION [DATA REQUIRED] |
| ราคาต่อ active patient ต่อปี (P) | ฿300 | 📊 ASSUMPTION — ต้อง validate ว่าต่ำกว่าส่วนต่างราคาแพ็กเกจ PGx มาก |
| ค่าติดตั้ง/integration ครั้งเดียว | ฿300,000 | 📊 ASSUMPTION |
| ต้นทุนผันแปรต่อ active patient ต่อปี (compute + LLM + storage + support) | ฿40 | 📊 ASSUMPTION — LLM ใช้แค่สรุปรายงาน ต้นทุนต่ำ แต่ต้อง host ในไทย/on-prem ซึ่งแพงขึ้น |
| ต้นทุนดูแล evidence store + clinical governance ต่อปี (fixed, ทั้งบริษัท) | ฿2,000,000 | 📊 ASSUMPTION (เภสัชกร curate 1 คน + QA) |

**สูตร**
- รายได้ต่อโรงพยาบาลต่อปี = N × P = 1,000 × 300 = **฿300,000** (+ ค่าติดตั้งปีแรก)
- Contribution margin ต่อโรงพยาบาล = N × (P − ต้นทุนผันแปร) = 1,000 × 260 = **฿260,000/ปี**
- จำนวนโรงพยาบาลที่ต้องมีเพื่อจ่าย fixed cost ของ evidence store = 2,000,000 / 260,000 ≈ **8 โรงพยาบาล** (ยังไม่รวมเงินเดือนทีม engineering/sales)

**สิ่งที่ตัวเลขนี้บอก (📊)**: ที่ราคาสมมตินี้ ธุรกิจจะอยู่ได้ต่อเมื่อ (ก) มีผู้ป่วย PGx ต่อโรงพยาบาลมากพอ หรือ (ข) ขายผ่าน lab/HIS ที่รวม volume หลายโรงพยาบาล — ดังนั้น **คำถามสำคัญที่สุดสำหรับการสัมภาษณ์ลูกค้าคือ "ตอนนี้มีผู้ป่วยที่มีผล PGx ในระบบกี่คน และเพิ่มปีละเท่าไร"** ถ้าคำตอบคือหลักร้อย โมเดลต่อโรงพยาบาลเดี่ยวไม่พอ → ต้องไปทาง lab channel

**ทำไมต้นทุนผู้ป่วยไม่ใช่ปัญหาของเรา (สำหรับ Module A beachhead)**: ต้นทุนการตรวจ PGx ถูกจ่ายไปแล้ว (sunk) โดยผู้ป่วย/โรงพยาบาล — เราขายการใช้ผลซ้ำ ไม่ได้ขายการตรวจใหม่ ส่วน NMR ที่ต้องตรวจซ้ำทุก visit เป็นต้นทุนที่ต้องมีผู้จ่ายชัดก่อนจะเป็นตัวนำ

**ข้อมูลอ้างอิงเรื่อง "ผู้จ่ายยอมจ่ายสำหรับ PGx" ในไทย** — ✅ HLA-B\*15:02 screening ก่อน carbamazepine ถูกผลักดันเป็นนโยบายระดับประเทศโดย สปสช. ปี 2018 ([PMC9294359](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9294359/)); การศึกษา cost-effectiveness ปี 2013 พบ ICER 130,000 บาท/QALY ในผู้ป่วย neuropathic pain เทียบเพดาน 120,000 บาท/QALY ในขณะนั้น ([Rattanavipapong et al., Epilepsia 2013](https://pubmed.ncbi.nlm.nih.gov/23895569/)) — ใช้เป็นหลักฐานว่า "รัฐไทยจ่ายเงินให้ PGx เมื่อมี economic evaluation" ไม่ใช่หลักฐานว่าจะจ่ายให้ซอฟต์แวร์เรา
- 🟡 มีรายงานว่า HLA-B\*58:01 เบิก สปสช. ได้ที่ราคา 1,000 บาท/test (จาก snippet ผลค้นหา; ยังเปิดต้นฉบับไม่ได้ — [ACR Open Rheumatology 2025](https://acrjournals.onlinelibrary.wiley.com/doi/10.1002/acr2.70093)) — ต้องยืนยันก่อนใช้

---

## 5. การออกแบบ Pilot

**หลักการ**: ตั้งเกณฑ์สำเร็จ **ก่อน** เริ่มเก็บข้อมูล เป็นภาษาของผู้ซื้อ (ความปลอดภัย, เวลาเภสัชกร, การใช้ผล PGx ซ้ำ) — **pilot 6 เดือนพิสูจน์การลด ADR ไม่ได้** (PREPARE ใช้ผู้ป่วยราว 7,000 คนใน 7 ประเทศ [ดูข้อ 8]) อย่าสัญญาสิ่งนั้น

### Site และโครงสร้าง (📊)

| ส่วน | รายละเอียด |
|---|---|
| **Site** | โรงพยาบาลเอกชน 1 แห่งที่มีบริการ PGx อยู่แล้ว — หน่วยงาน: คลินิก cardiometabolic / anticoagulation ที่มีเภสัชกรทบทวนยา; + คณะเภสัชศาสตร์/โรงพยาบาลมหาวิทยาลัย 1 แห่งเป็นผู้เฉลย gold standard และยื่น IRB ร่วม |
| **ระยะเวลา** | 6 เดือน: เดือน 0–2 retrospective (shadow mode), เดือน 3–6 prospective |
| **Phase 1 — Retrospective shadow (เดือน 0–2)** | ผู้ป่วยที่มีผล PGx + ประวัติยาในระบบ **n ≥ 300** (ถ้ามีไม่ถึง ใช้ทั้งหมด) → รันระบบย้อนหลัง, เภสัชกร 2 คน review แยกกันบนตัวอย่างสุ่ม 100 ราย เพื่อวัด omission / false flag / inter-rater agreement — ไม่มีผลต่อการรักษาจริง |
| **Phase 2 — Prospective (เดือน 3–6)** | ทุกผู้ป่วยที่มาคลินิกและมีผล PGx → เภสัชกรใช้ระบบก่อนพบแพทย์; เป้า **n ≈ 150–200 medication reviews** (📊 ประมาณจากคลินิกเดียว ~10 ราย/สัปดาห์ × 16 สัปดาห์ — ต้องปรับตาม volume จริง) |
| **ตัวเปรียบเทียบ** | เวลา review และจำนวน alert ช่วง 4 สัปดาห์ก่อนเริ่ม (baseline แบบเดิม) vs ระหว่างใช้ระบบ; ในเคส retrospective เทียบกับ DDI checker ที่โรงพยาบาลใช้อยู่ |
| **NMR / cfDNA** | ไม่อยู่ใน pilot แรก ยกเว้นโรงพยาบาลมีข้อมูล NMR อยู่แล้ว (ใช้เป็น exploratory เท่านั้น) — ลดความซับซ้อนและต้นทุน |

### ตัวชี้วัดความสำเร็จ (ตั้งไว้ล่วงหน้า — 📊 เป้าเป็นข้อเสนอ ต้องตกลงกับโรงพยาบาลก่อนเริ่ม)

| ตัวชี้วัด | เป้า | ประเภท |
|---|---|---|
| **Critical omission** (finding สำคัญที่เภสัชกรผู้เฉลยเจอแต่ระบบพลาด) บนเคสที่ review คู่ | **0** | Safety — gate |
| **Pharmacist acceptance rate** (accept + modify เล็กน้อย) | **≥ 70%** | Primary |
| **Physician acceptance** ของคำแนะนำที่เภสัชกรส่งต่อ | **≥ 50%** | Secondary |
| **Alert ต่อ review** (ที่ต้องอ่าน) เทียบ DDI checker เดิม | **ลดลง ≥ 50%** โดยไม่มี omission | Secondary — ตรงกับปัญหา alert fatigue |
| **เวลา review ต่อราย** | **ลดลง ≥ 30%** จาก baseline | Secondary |
| **Actionable drug-gene finding ต่อ 100 ผู้ป่วยที่มีผล PGx** | **รายงานค่าจริง** (คาดการณ์ ≥ 10/100 — 📊 ASSUMPTION; อ้างอิงบริบท: ผู้ใช้ omeprazole 55% มี CYP2C19 actionable ใน cohort Siriraj [PMC13432136](https://pmc.ncbi.nlm.nih.gov/articles/PMC13432136/)) | Descriptive — ขนาดของปัญหา |
| **Citation precision** (ทุกประโยคในรายงานมี fact ID ที่ถูก) | **≥ 99%** | Technical quality |
| **Inter-rater agreement** ระหว่างเภสัชกรผู้เฉลย | รายงาน (Cohen's κ) | เพดานของระบบ |
| **ความตั้งใจซื้อ** | โรงพยาบาลตอบรับข้อเสนอราคาเชิงพาณิชย์ภายในเดือน 7 | Business |

### สิ่งที่ผู้ซื้อเห็นในเดือนที่ 6 (1-page dashboard)
1. **จำนวนผู้ป่วยที่ผล PGx ถูกใช้ซ้ำ** และจำนวนใบสั่งยาที่ถูกตรวจกับ genotype
2. **รายการ "near-miss" ที่ถูกจับได้** (เช่น simvastatin ขนาดสูงใน SLCO1B1 poor function, clopidogrel ใน CYP2C19 PM + omeprazole) พร้อมการตัดสินใจของแพทย์ — เป็นรายเคส ไม่ extrapolate เป็นจำนวน ADR ที่ป้องกันได้
3. **Alert burden ก่อน/หลัง** และเวลาเภสัชกรต่อราย
4. **ผล safety audit**: critical omission, false flag, citation precision
5. **ข้อเสนอเชิงพาณิชย์** คำนวณจาก N จริงของโรงพยาบาล พร้อมสมมติฐานที่ระบุชัด
6. **สิ่งที่ pilot นี้ไม่ได้พิสูจน์**: การลด ADR/admission (ต้องศึกษาขนาดใหญ่กว่า) — เขียนไว้ชัดเจน

### Kill criteria ของ pilot (ตกลงล่วงหน้า)
- มี critical omission ที่เกิดจาก logic ของระบบ (ไม่ใช่ข้อมูลขาด) แล้วแก้ไม่ได้ภายใน 2 สัปดาห์ → หยุด prospective
- Acceptance < 50% หลังปรับ rule 1 รอบ → คุณค่าไม่พอ ทบทวน use case
- เวลา review ไม่ลดลงเลย → workflow ไม่ fit
- ผู้ป่วยที่มีผล PGx ในโรงพยาบาล < 200 คน → โมเดลต่อโรงพยาบาลไม่พอ เปลี่ยนไป lab channel

---

## 6. กลยุทธ์พาร์ทเนอร์และลำดับ

**หลักการ**: คอขวดคือ **พาร์ทเนอร์ 1 ราย ไม่ใช่เงิน** — ขอ pilot ไม่ใช่ขอเงินลงทุน; ขอแค่สิ่งที่คนคนเดียวเซ็นได้

| ลำดับ | พาร์ทเนอร์ | ขออะไร | ให้อะไร | ช่วงเวลา |
|---|---|---|---|---|
| **1** | **คณะเภสัชศาสตร์ / อาจารย์ PGx ในมหาวิทยาลัย** | เภสัชกร 2–3 คนเฉลย gold-standard 30–50 เคส, ที่ปรึกษาคลินิก, ร่วมยื่น IRB | ผลงานวิจัย/ตีพิมพ์, เครื่องมือสอน | ทันทีหลัง hackathon (เดือน 0–1) |
| **2** | **โรงพยาบาลเอกชน 1 แห่งที่มีบริการ PGx** (design partner) | ข้อมูล retrospective (de-identified, ผ่าน IRB), คลินิก 1 แห่ง, champion เภสัชกรอาวุโส | ใช้ฟรีตลอด pilot + ส่วนลดปีแรก + co-branding/publication | เดือน 1–3 เซ็น LOI → pilot เดือน 3–9 |
| **3** | **Lab PGx** (ต้นทางข้อมูล genotype) | รูปแบบไฟล์ผลแบบ structured (diplotype), สิทธิ์เชื่อมข้อมูล | ทำให้รายงาน lab "ถูกใช้ต่อ" = เหตุผลให้แพทย์สั่งตรวจเพิ่ม | ขนานกับข้อ 2 |
| **4** | **HIS vendor** (เช่น HOSxP/BMS หรือ HIS ที่โรงพยาบาล pilot ใช้) | FHIR/API endpoint, sandbox | module เสริมที่ไม่แข่งกับเขา, revenue share ภายหลัง | เดือน 6–12 |
| **5** | **Lab liquid biopsy / NGS** (Module B) | variant report แบบ structured, pilot per-report 1 ศูนย์มะเร็ง | interpretation เชิงยาใส่ในรายงาน | เดือน 6–12 (หลัง Module A มี traction) |
| **6** | **Lab NMR / มหาวิทยาลัย** (เช่น ✅ KKU International Phenome Laboratory มี NMR 400/600 MHz [kkuipl](https://kkuipl.wordpress.com/about-us/)) | โครงการวิจัย Thai reference interval + CVi สำหรับ RCV | ใช้เป็น use case ทางคลินิกของ panel | track วิจัยขนาน (ขอทุน) — **ไม่ใช่ critical path ของรายได้** |
| **7** | **ประกัน / สวัสดิการองค์กร / สปสช.** | program ยาแพง (GLP-1 RA, targeted) / economic evaluation | ข้อมูล aggregate outcome | 18 เดือน+ หลังมีข้อมูล pilot |

📊 **ข้อควรระวัง**: รายการด้านบนเป็น **target list ไม่ใช่ pipeline** — pipeline ตอนนี้ = 0 ขั้นแรกที่ต้องทำคือหา warm introduction ไปที่ **หนึ่ง** โรงพยาบาล ไม่ใช่ส่งอีเมลไป 5 แห่ง

### มุมประกัน (สั้น ๆ)
- ประกันไม่ได้ซื้อ "การตรวจ" แต่ซื้อ **เคลมที่ไม่ต้องจ่าย** — ADR ที่ต้องนอนโรงพยาบาล และค่ายาแพงที่ไม่ได้ผล ต้องมีข้อมูลผลลัพธ์ก่อนคุยเรื่องเงิน
- ✅ บรรทัดฐานต่างประเทศ: PREPARE พบ ADR ลดลงในกลุ่มที่มี actionable result (ดูข้อ 8) — เป็นหลักฐานของ **PGx-guided prescribing** ไม่ใช่ของซอฟต์แวร์เรา
- 📊 **กฎเหล็ก**: ข้อมูลพันธุกรรมรายบุคคล **ไม่ส่งให้ประกัน** และไม่ใช้ในการคิดเบี้ย — ประกันเห็นเฉพาะ aggregate (PDPA มาตรา 26 + ความไว้วางใจของผู้ป่วย) ถ้าจะทำ program กับประกันต้องให้ `thai-healthtech-legal` ตรวจโครงสร้างก่อน
- การคิดราคาต่อสมาชิกที่ประกันจะยอมจ่ายเป็นงานของ actuarial — ยังไม่ควรมีตัวเลขในเอกสารนี้จนกว่าจะมีข้อมูล ADR/เคลมจาก pilot

---

## 7. ความเสี่ยงและ Kill criteria ระดับบริษัท

| ความเสี่ยง | ระดับ | การลดความเสี่ยง | Kill / pivot trigger |
|---|---|---|---|
| **ผู้ป่วยที่มีผล PGx ต่อโรงพยาบาลน้อยเกินไป** | สูง | สัมภาษณ์ 5 โรงพยาบาลเรื่อง volume ก่อนเขียนโค้ดเพิ่ม | ถ้าทุกแห่ง < 200 ราย → pivot เป็น lab channel หรือขายเป็นส่วนหนึ่งของแพ็กเกจ PGx ใหม่ |
| **HIS vendor / โรงพยาบาลสร้าง PGx alert เอง** | กลาง | เป็นพาร์ทเนอร์ของ HIS; สร้าง Thai evidence store + validation data ที่ต้อง license | ถ้า HIS หลักเปิด PGx-CDS ฟรีก่อนเรามีลูกค้า 3 ราย → pivot เป็น evidence-store licensing |
| **Regulatory (SaMD/อย.)** | กลาง-สูง | intended use แคบ, ไม่ประมวล raw data, แสดงพื้นฐานทุกคำแนะนำ, ปรึกษา อย. ช่วง 0–6 เดือน | ถ้า อย. จัดเป็น class ที่ต้องมี clinical study ก่อนขาย → ขายเฉพาะ research-use / ใน pilot ที่มี IRB จนกว่าจะขึ้นทะเบียน |
| **Clinical error / liability** | สูง | deterministic engine + unit test, verifier, pharmacist sign-off, audit log | critical omission ที่เกิดจาก logic ใน pilot → หยุด |
| **PDPA / ข้อมูลพันธุกรรม** | สูง | consent แยก, host ในไทย, DPA กับโรงพยาบาล | โรงพยาบาลไม่ยอมให้ข้อมูลออกนอก → ต้องทำ on-prem (ต้นทุนติดตั้งสูงขึ้น) |
| **ความรู้ PGx ของเภสัชกร** | กลาง | 🟡 มีรายงานว่าเภสัชกรโรงพยาบาลไทย 46.3% มีคะแนนความรู้ PGx ต่ำ ([PubMed 32187156](https://pubmed.ncbi.nlm.nih.gov/32187156/), จาก abstract) → ระบบต้องอธิบาย "Why?" ได้ + มีโมดูลอบรม | — (เป็นโอกาสด้วย: เครื่องมือช่วยปิด gap) |
| **NMR ไม่มีผู้จ่าย / ไม่มี Thai reference** | สูง | NMR เป็น add-on + track วิจัย ไม่ใช่ตัวนำรายได้ | ถ้าภายใน 18 เดือนไม่มีผู้จ่าย NMR ซ้ำ → ตัด NMR ออกจากผลิตภัณฑ์เชิงพาณิชย์ เหลือ research module |
| **Module B กระจายโฟกัส** | กลาง | ทำเป็น demo + lab partnership เบา ๆ; ไม่จ้างทีมแยก | ถ้า lab ไม่มีใครสนใจ per-report ภายใน 12 เดือน → พัก Module B |
| **License knowledge base (เช่น OncoKB)** | กลาง | ตรวจ license ก่อน; ใช้แหล่งเปิด (CPIC, PharmGKB, ClinVar, ฉลากยา) | ค่า license เชิงพาณิชย์เกิน margin → ใช้ tier จากรายงาน lab แทน |

---

## 8. Pitch narrative — 3 นาที

### โครงเรื่อง (map กับเกณฑ์ตัดสิน)

| เวลา | ช่วง | เนื้อหา | เกณฑ์ที่ได้คะแนน |
|---|---|---|---|
| 0:00–0:25 | **Hook — คนไข้หนึ่งคน** | "คนไข้คนนี้ตรวจยีนแล้ว ผลบอกว่าเสี่ยงแพ้ carbamazepine รุนแรง แต่ผลอยู่ในกระดาษ ระบบโรงพยาบาลไม่เตือน — เขาได้ยานั้นและเสียชีวิต" (เคสจริงที่รายงานใน [PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/) — เล่าแบบไม่ระบุตัวตน และอ้างแหล่ง) | Problem significance |
| 0:25–0:50 | **ปัญหา 2 ชั้น** | (1) ผล PGx ไม่ถูกใช้ตอนสั่งยา — ไม่มี PGx alert ใน EHR ไทย (2) ระบบ DDI เตือนจนแพทย์ override ~90% ([meta-analysis](https://journals.sagepub.com/doi/10.1177/14604582241263242)) → เพิ่ม alert ไม่ใช่คำตอบ | Problem + clinical need |
| 0:50–1:50 | **Demo — เคส B + D** | เคส B: simvastatin + SLCO1B1 + LDL-C ถึงเป้าแต่ ApoB ไม่เปลี่ยนเกิน RCV → 1 action card → กด "Why?" เห็น rule/fact ID → เภสัชกร accept. เคส D: cfDNA + CHIP flag + TKI+PPI | Innovation, technical feasibility, safety |
| 1:50–2:10 | **ทำไมเชื่อได้** | Rule engine ทำงานหลัก, LLM แค่สรุปพร้อม fact ID; eval บน 30–50 เคส synthetic (ติดป้าย) — critical omission, citation precision, alert ต่อเคส | Scientific validity, safety |
| 2:10–2:40 | **ใครจ่าย + beachhead** | "ลูกค้าแรก: โรงพยาบาลเอกชนที่ **ขาย PGx อยู่แล้ว** — เราทำให้ผลที่คนไข้จ่ายไปแล้วถูกใช้ทุกครั้งที่สั่งยา คิดราคาต่อผู้ป่วย active ต่อปี; oncology ขายผ่าน lab ต่อรายงาน" | Business model, GTM |
| 2:40–3:00 | **Pilot + ask** | "Pilot 6 เดือน 1 คลินิก: เป้า acceptance ≥70%, critical omission 0, alert ลด ≥50% — ตั้งเกณฑ์ไว้แล้วก่อนเริ่ม สิ่งที่เราขอ: โรงพยาบาล 1 แห่งและเภสัชกร 3 คนเป็นผู้เฉลย" + ประโยคปิด: "ยานี้เหมาะกับคนไข้ไหม ได้ผลจริงไหม และถ้าไม่ได้ผล เป็นเพราะอะไร" | Impact metric |

📊 **ตัดออกจากพิตช์ 3 นาที**: market size ก้อนใหญ่ (ให้ไว้ใน appendix พร้อม methodology จาก `market_research.md`), ความเป็นสังคมสูงวัยเกิน 1 ประโยค, รายละเอียด NMR analyte ทั้งหมด

### คำตอบ Killer questions ของกรรมการธุรกิจ

**Q1. ใครจ่าย จ่ายเท่าไรต่อคน และสูงกว่าต้นทุนไหม?**
> "ปีแรก: โรงพยาบาลเอกชนที่มีบริการ PGx จ่ายต่อผู้ป่วยที่มีผล PGx และมีการสั่งยาในปีนั้น — ตัวเลขราคาตอนนี้เป็นสมมติฐาน (ในเอกสารเราใช้ ฿300/คน/ปี เป็น placeholder) ต้นทุนผันแปรของเราต่ำเพราะ rule engine เป็นโค้ด LLM ใช้แค่สรุป ความเสี่ยงจริงไม่ใช่ margin ต่อคน แต่คือ **volume ผู้ป่วยที่มีผล PGx ต่อโรงพยาบาล** — นั่นคือคำถามแรกที่เราจะถามลูกค้า ถ้าไม่พอ เราไปผ่าน lab ที่รวม volume หลายโรงพยาบาล ส่วนต้นทุนการตรวจ PGx ถูกจ่ายไปแล้ว เราไม่ได้เพิ่มต้นทุนตรวจ"

**Q2. ลูกค้าจ่ายเงินรายแรกคือใคร และผู้ป่วย 100 คนแรกมาจากไหน?**
> "ประเภทลูกค้าคือโรงพยาบาลเอกชนที่มีศูนย์ PGx อยู่แล้ว — ตามเว็บไซต์ Bumrungrad, Bangkok Hospital, Samitivej มีบริการนี้ เรายังไม่ได้คุยกับใคร pipeline ตอนนี้คือศูนย์ ผู้ป่วย 100 คนแรกคือ **ผู้ป่วยที่มีผล PGx อยู่แล้วในระบบ** ของโรงพยาบาล pilot — รันแบบ retrospective ก่อน ไม่ต้องหาคนตรวจใหม่"

**Q3. ทำไมโรงพยาบาลซื้อเรา แทนที่จะเพิ่ม PGx rule ใน HIS เอง?**
> "เขาทำได้ และ Epic ในต่างประเทศทำแล้ว แต่ต้นทุนจริงไม่ใช่การเขียน rule ครั้งแรก — คือการ **ดูแล** evidence ที่ CPIC อัปเดตเรื่อย ๆ, map กับรหัสยาไทย, รับ liability และภาระ อย. ของ clinical interpretation (บริษัท PGx-CDS ในสหรัฐเคยต้องหยุดบริการเพราะไม่ผ่าน FDA) และ rule เดี่ยวใน HIS จะเพิ่ม alert ในขณะที่แพทย์ override อยู่แล้ว ~90% เราขายการ **ลด** alert และรวม PGx + DDI + adherence เป็น card เดียว และเราตั้งใจเป็น module ที่เสียบเข้า HIS ไม่ใช่แข่งกับ HIS"

**Q4. หลัง pilot 6 เดือน จะโชว์ผลอะไรให้ผู้ซื้อ?**
> "Dashboard 1 หน้า: ผล PGx ถูกใช้ซ้ำกี่ครั้ง, near-miss ที่จับได้รายเคสพร้อมการตัดสินใจของแพทย์, alert ต่อ review ก่อน/หลัง, เวลาเภสัชกร, และผล safety audit เกณฑ์ที่ตั้งไว้ล่วงหน้า: acceptance ≥70%, omission 0, alert ลด ≥50%, เวลาลด ≥30% — และเราบอกตรง ๆ ว่า 6 เดือนพิสูจน์การลด ADR ไม่ได้ PREPARE ต้องใช้ผู้ป่วยหลายพันคน"

**คำถามต่อเนื่องที่ควรเตรียม**

| คำถาม | คำตอบสั้น |
|---|---|
| หลักฐานว่า PGx-guided prescribing ได้ผล? | ✅ PREPARE (Lancet 2023): ในผู้ป่วยที่มี actionable result, ADR ที่สำคัญทางคลินิก 21% vs 28%, OR 0.70 (95% CI 0.54–0.91) ([PMC10213803](https://pmc.ncbi.nlm.nih.gov/articles/PMC10213803)) — ✅ มีจดหมายโต้แย้งใน Lancet ว่าประโยชน์ยังไม่ชัด ([Lancet correspondence](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(23)00855-3/fulltext)) → พูดว่า "หลักฐานระดับ RCT ในยุโรป ยังไม่มีในไทย" |
| ทำไมไม่ขายตรงให้ผู้ป่วย? | ผู้ป่วยไม่ใช่คนสั่งยา; คุณค่าเกิดตอนเภสัชกร/แพทย์ใช้ผล — B2C ไม่ผ่าน workflow |
| cfDNA ทำให้โฟกัสกระจายไหม? | Module B เป็น channel ผ่าน lab ต่อรายงาน ไม่แยกทีมขาย ใช้ engine เดียวกัน (PGx + DDI) — ถ้าไม่มี lab สนใจใน 12 เดือนเราพักไว้ |
| NMR ใครจ่าย? | ยังไม่มีคำตอบที่มั่นใจ — จึงเป็น add-on และ track วิจัย ไม่ใช่ตัวนำรายได้; ต้องมี Thai reference + CVi ก่อน |
| Moat? | ไม่ใช่เทคโนโลยี — Thai evidence store, validation dataset จาก pilot, integration ที่ติดตั้งแล้ว, regulatory file; ความได้เปรียบคือ **เวลาและโฟกัส** |
| ขนาดตลาด? | อ้าง `market_research.md` พร้อมวิธีคำนวณ bottom-up และบอกว่า input ไหนเป็นสมมติฐาน |

---

## 9. ข้อเสนอแก้ไข `idea.md` ข้อ 12 (diff-style — ไม่ได้แก้ไฟล์เอง)

```diff
 ## 12. โมเดลธุรกิจ

+> สถานะ: ยังไม่มีบริษัท พาร์ทเนอร์ LOI หรือรายได้ — ตัวเลขทุกตัวที่ไม่มีแหล่งอ้างอิงเป็นสมมติฐาน

 ### ใครใช้ ใครจ่าย
-| ผู้จ่าย (beachhead) | โรงพยาบาลเอกชนที่มี preventive / lipid clinic | ศูนย์มะเร็ง / lab ที่ทำ liquid biopsy (partnership) |
+| ผู้ซื้อ (beachhead) | ฝ่ายเภสัชกรรม + ศูนย์ genomic ของโรงพยาบาลเอกชนที่ **ขาย PGx อยู่แล้ว** (เริ่มคลินิก cardiometabolic/anticoagulation) | **lab liquid biopsy/NGS** (per-report) |
+| งบบรรทัดไหน | ต้นทุนบริการของแพ็กเกจ PGx (ส่งต่อผู้ป่วย self-pay) หรืองบ clinical software ฝ่ายเภสัช | COGS ต่อรายงานของ lab (ผู้ป่วยส่วนใหญ่ self-pay NGS) |
+| ผู้อนุมัติ/gatekeeper | PTC, IT (HIS integration), DPO | Medical director ของ lab |
+| ผู้ได้ประโยชน์ | ผู้ป่วย, โรงพยาบาล (ลดความเสี่ยง ADR, คุณค่าบริการ PGx) | ผู้ป่วย NSCLC, oncologist |

+### Beachhead (ใหม่)
+- "เปิดใช้ผล PGx ที่ขายไปแล้ว": ไม่มี PGx alert ใน EHR ไทย (PMC9016335), 95.99% ของผู้ใหญ่ไทยมีผล CPIC-actionable (Siriraj, PMC13432136)
+- ลำดับ: PGx + DDI + adherence ก่อน → NMR เป็น add-on → Module B ผ่าน lab
+- มหาวิทยาลัย = clinical/validation partner ไม่ใช่ลูกค้าจ่ายเงินรายแรก

 ### รายได้ (เสนอ ต้อง validate กับลูกค้า)
-- **SaaS ต่อโรงพยาบาล** (ค่าติดตั้ง + รายปี) สำหรับ Module A
+- **Module A: ค่าติดตั้งครั้งเดียว + ค่าบริการต่อผู้ป่วยที่มีผล PGx และ active ต่อปี** (ราคาเป็นสมมติฐาน); NMR = add-on ต่อรายงาน
-- **ค่าบริการต่อรายงาน** สำหรับ Module B — แบ่งรายได้กับ lab liquid biopsy / PGx
+- **Module B: per-report / revenue share กับ lab liquid biopsy**
+- ระยะ 2: HIS vendor เป็น reseller; ระยะ 3: program ยาแพงกับประกัน/องค์กร (ประกันเห็นเฉพาะ aggregate ไม่เห็นผลพันธุกรรมรายบุคคล)
+- Unit economics: ดู business_strategy.md §4 — ตัวแปรที่ตัดสินคือจำนวนผู้ป่วยที่มีผล PGx ต่อโรงพยาบาล

 ### ทำไมคุ้ม (story สำหรับ buyer)
-- **PGx ตรวจครั้งเดียวใช้ตลอดชีวิต** — ... PREPARE trial (Swen et al., Lancet 2023) พบ preemptive 12-gene panel ลด clinically relevant ADR ได้ราว 30%
+- **PGx ตรวจครั้งเดียวใช้ตลอดชีวิต** — PREPARE (Lancet 2023): ในผู้ป่วยที่มี actionable result, ADR 21% vs 28%, OR 0.70 (95% CI 0.54–0.91); หลักฐานจากยุโรป ยังไม่มีในไทย และมีข้อโต้แย้งใน Lancet correspondence
+- **ลด alert แทนเพิ่ม** — DDI alert ถูก override ~90% (meta-analysis, Felisberto 2024)
-- **ลดค่ายาแพงที่ไม่ได้ผล** — เช่น GLP-1 RA, targeted therapy ...
+- **ลดค่ายาแพงที่ไม่ได้ผล** — (ระยะยาว, ยังไม่มีหลักฐาน — ไม่ใช่ข้อเสนอหลักของ beachhead)

 ### คู่แข่งและ moat
+| ไม่ทำอะไร (status quo: PDF/บัตร PGx) | ฟรี | คู่แข่งอันดับ 1 — ขายด้วยความเสี่ยงของการไม่ทำ |
+| PGx-CDS ต่างประเทศ (Epic Genomics, GenXys) | PGx alerts | ไม่มีบริบทไทย/ไม่ต่อ HIS ไทย |
-**Moat**: evidence store ที่ curate สำหรับบริบทไทย ...
+**Moat (ซื่อตรง)**: เทคโนโลยีลอกได้ — ความได้เปรียบคือเวลาและโฟกัส: Thai evidence store, validation dataset, integration, regulatory file
+**ทำไม HIS/โรงพยาบาลไม่สร้างเอง**: สร้างได้ แต่ต้นทุนคือการดูแล evidence + liability + ภาระ อย. (Translational Software หยุดบริการหลังไม่ผ่าน 510(k)); กลยุทธ์: เป็น module ใน HIS ไม่แข่งกับ HIS

 ### Why now
-- Liquid biopsy ราคาลดลงและใช้แพร่หลายขึ้น (ต้องตรวจสอบตัวเลข)
+- ความต้องการ PGx โต: HLA-B tests 94 (2011) → 2,880 (2020) ในไทย (PMC9016335); สปสช. ผลักดัน HLA-B*15:02 ทั่วประเทศปี 2018
+- EGFR mutation 47% ใน metastatic NSCLC ที่โรงพยาบาลตติยภูมิไทย (PubMed 36895484) — แทนข้อความ "ต้องตรวจสอบความชุก"
+(ลบ bullet liquid biopsy ราคาลดลง จนกว่าจะมีแหล่ง)

 ### Pilot success criteria (6 เดือน, 1 คลินิก)
-- ≥ X% ของ recommendation ที่เภสัชกรยอมรับ
-- จำนวน actionable PGx finding ต่อ 100 คน
-- เวลาทบทวนยาต่อราย ลดลง Y%
-- Critical omission = 0
-(กำหนด X, Y ร่วมกับโรงพยาบาลก่อนเริ่ม)
+- Site: โรงพยาบาลเอกชน 1 แห่งที่มีบริการ PGx, คลินิก cardiometabolic; เดือน 0–2 retrospective shadow (n ≥ 300), เดือน 3–6 prospective (~150–200 reviews)
+- Critical omission = 0 (gate) · Pharmacist acceptance ≥ 70% · Physician acceptance ≥ 50%
+- Alert ต่อ review ลด ≥ 50% · เวลา review ลด ≥ 30% · Citation precision ≥ 99%
+- รายงาน actionable drug-gene finding ต่อ 100 ผู้ป่วย (descriptive)
+- ไม่ claim การลด ADR จาก pilot 6 เดือน
+- Kill: omission จาก logic แก้ไม่ได้ใน 2 สัปดาห์ / acceptance < 50% / ผู้ป่วยที่มีผล PGx < 200 ราย
+(เป้าเป็นข้อเสนอ ตกลงกับโรงพยาบาลก่อนเริ่ม)

+### Partnership sequence (ใหม่)
+คณะเภสัช/มหาวิทยาลัย (gold standard, IRB) → โรงพยาบาลเอกชน 1 แห่ง (design partner) → lab PGx → HIS vendor → lab liquid biopsy → lab NMR (track วิจัย) → ประกัน/สปสช. (18 เดือน+)
```

**แก้ข้อ 13 Roadmap ให้สอดคล้อง** (เล็กน้อย): แถว "0–6 เดือน" เพิ่ม "สัมภาษณ์ 5 โรงพยาบาลเรื่องจำนวนผู้ป่วยที่มีผล PGx + เซ็น LOI design partner 1 ราย"; แถว "6–12 เดือน" เปลี่ยน "Prospective pilot 1 คลินิก" เป็น "pilot ตามเกณฑ์ใน §12 + ข้อเสนอราคาเชิงพาณิชย์เดือน 7"

---

## แหล่งอ้างอิง

- PGx alert gap + HLA-B test trends ในไทย: https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/
- Siriraj PGx landscape (4,662 ราย): https://pmc.ncbi.nlm.nih.gov/articles/PMC13432136/
- PREPARE results: https://pmc.ncbi.nlm.nih.gov/articles/PMC10213803 · Lancet correspondence: https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(23)00855-3/fulltext
- DDI override meta-analysis: https://journals.sagepub.com/doi/10.1177/14604582241263242 · https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7400042/
- HLA-B*15:02 national policy: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9294359/ · CEA: https://pubmed.ncbi.nlm.nih.gov/23895569/
- HLA-B*58:01 NHSO (🟡): https://acrjournals.onlinelibrary.wiley.com/doi/10.1002/acr2.70093
- EGFR ในไทย: https://pubmed.ncbi.nlm.nih.gov/36895484/ · Thai NSCLC biomarker recommendations: https://tlcr.amegroups.org/article/view/103441/html
- Genomic medicine ในไทย: https://pmc.ncbi.nlm.nih.gov/articles/PMC10875286/
- โรงพยาบาลเอกชน PGx: https://www.bumrungrad.com/en/centers/preventive-genomics-integrative-medicine · https://www.bangkokhospital.com/en/content/pharmacogenomics · https://www.samitivejhospitals.com/center/detail/Samitivej-Genomic-and-Life-Style-Wellness-Center
- Ramathibodi PGx lab: https://www.rama.mahidol.ac.th/postgrad/clinicalpatho/Lab/Pharmacogenomics · PGx card: https://www.tandfonline.com/doi/full/10.2217/pgs-2015-0009 · TPGxD-1: https://ascpt.onlinelibrary.wiley.com/doi/10.1111/cts.13830
- HOSxP/BMS: https://news.microsoft.com/source/asia/features/bangkok-medical-software-utilizes-presscribeai-by-looloo-health-to-enhance-healthcare-services-across-35-hospitals-in-thailand/
- Epic Genomics PGx CDS: https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2024.1458095/full · GenXys: https://www.genxys.com/clinical-decision-support-system/
- Translational Software 510(k): https://www.precisionmedicineonline.com/business-news/pgx-labs-searching-new-result-reporting-options-after-translational-softwares-failed
- KKU Phenome Lab: https://kkuipl.wordpress.com/about-us/
- Pharmacist PGx knowledge (🟡 abstract): https://pubmed.ncbi.nlm.nih.gov/32187156/
- ctDNA screening packages (ไม่ใช่ตลาด Module B): https://www.phyathai.com/en/pyt2/package/ctdna-program-pt2 · https://www.samitivejhospitals.com/package/detail/Circulating-Tumor-DNA
