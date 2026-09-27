# PrecisionRx — Market Research (ตรวจสอบแหล่งจริง)

> จัดทำ 27 ก.ย. 2026 (2569) · ใช้คู่กับ `idea.md` (v2) และ `critique_PrecisionRx.md` §7
>
> **ข้อควรรู้ก่อนอ่าน:** ทีมยังไม่มีบริษัท ไม่มีโรงพยาบาลหรือ lab ที่เป็นพาร์ทเนอร์ ไม่มี LOI ไม่มีข้อมูลคนไข้จริง และไม่มีรายได้ ตัวเลข TAM/SAM/SOM ในไฟล์นี้**เป็นการประมาณการของทีมเองทั้งหมด** โดยแยกไว้ชัดว่าส่วนไหนมีแหล่งอ้างอิง ส่วนไหนเป็นสมมติฐาน
>
> สัญลักษณ์: ✅ ยืนยันจากแหล่งปฐมภูมิ/ทางการ · 🟡 แหล่งทุติยภูมิ (ข่าว, เว็บคลินิก, บทความ review) · 📊 สมมติฐานหรือการวิเคราะห์ของเรา · ❓ **ยังยืนยันไม่ได้**

---

## 1. สรุป 10 บรรทัด

1. ✅ ไทยมีผู้สูงอายุ 60+ อยู่ **14.14 ล้านคน = 21.82%** ของประชากรตามทะเบียนราษฎร์ปี 2568 จึงเป็นสังคมสูงวัยโดยสมบูรณ์แล้ว ส่วน polypharmacy ในผู้สูงอายุไทยพบ **15%** ในหน่วยปฐมภูมิ และ **59.5%** ใน รพ.ทุติยภูมิเขต 8 (ความชุกขึ้นกับ setting มาก)
2. ✅ ข้อมูล SNP-array ของคนไทย 4,662 คนพบว่า **96% มี PGx genotype ที่ actionable ตาม CPIC อย่างน้อย 1 ยีน** ในกลุ่มคนที่ได้ statin มี SLCO1B1 actionable ~22–23% และในกลุ่มที่ได้ omeprazole มี CYP2C19 actionable 55% ตัวเลขนี้คือหลักฐานตลาดที่แข็งที่สุดของ Module A
3. ✅ สปสช. ครอบคลุมการตรวจ **HLA-B\*15:02** (ประสานกับกรมวิทย์ฯ 1,000 บาท/ราย ตรวจฟรีทุกสิทธิ) และ **HLA-B\*58:01** (ชดเชย 1,000 บาท สิทธิบัตรทอง) แล้ว ข้อ 6 ใน idea.md จึงควรเขียนว่า "ทำงานต่อยอดสิทธิที่มีอยู่" ไม่ใช่ "ต้องตรวจสอบ"
4. ✅ ราคา PGx panel ในไทยที่ตรวจเจอ: N Health "Drug-Gene Profile" **฿14,751** และ ATGenes (HLA 20+ ยา) **฿39,600** ส่วนการตรวจยีนเดี่ยว เช่น HLA สำหรับ carbamazepine ราคา **฿1,485** แปลว่าผู้ป่วยเอกชนจ่ายหลักหมื่น ต่อครั้งเดียวในชีวิต
5. ❓ **หาไม่เจอบริการ NMR lipoprotein/metabolomics ทางคลินิกในไทย** Nightingale มีข้อตกลงกับ Innoquest ที่ครอบคลุมไทยตั้งแต่ปี 2023 แต่ยังยืนยันไม่ได้ว่าให้บริการในไทยแล้ว ส่วน Bruker B.I.-LISA ขายในสถานะ "For research only" นี่คือความเสี่ยงใหญ่สุดของ Module A เพราะ input ที่ระบบต้องใช้อาจยังไม่มีในตลาดไทย
6. ✅ มะเร็งปอดไทย **23,871 รายใหม่/ปี** (GLOBOCAN 2024) และ EGFR mutation พบ **54–68%** ของ NSCLC ไทย (ตามคำแนะนำผู้เชี่ยวชาญ TLCR 2025) ส่วน liquid biopsy ระดับพรีเมียมราคา Guardant360 CDx cash **$8,455** (มิ.ย. 2026) และ FoundationOne Liquid list **$5,800** ยังไม่เจอราคาในไทย
7. 📊 TAM แบบ bottom-up ของ **Module A (SaaS ต่อโรงพยาบาล)** อยู่ที่ราว **฿0.4–0.8 พันล้าน/ปี** SAM (รพ.ที่มีบริการ PGx/preventive อยู่แล้ว) ราว **฿20–60 ล้าน/ปี** และ SOM ปีที่ 3 ราว **฿2–6 ล้าน/ปี** ทั้งหมดขึ้นกับราคาที่ยังไม่มีลูกค้าคนไหนยืนยัน
8. 📊 **Module B (คิดค่าอ่านผล cfDNA ต่อรายงาน) เป็นตลาดเล็กมากในไทย**: TAM ราว **฿10–25 ล้าน/ปี** และ SOM ต่ำกว่า ฿1 ล้าน Module B จึงเหมาะเป็นจุดต่างและเป็น demo มากกว่าเป็นแหล่งรายได้ ถ้าจะเก็บเงินควรขายเป็น license ต่อศูนย์มะเร็ง
9. คู่แข่งระดับโลกทำแค่ส่วนใดส่วนหนึ่ง: DDI (Lexidrug/Micromedex), PGx test+report (GeneSight $330, Genomind $599), PGx CDS (RxGenomix, Translational Software), oncology interpretation (OncoKB, navify, Tempus) ส่วนในไทยมี Rama PGx ID card, PGxCard (กินอยู่ดี × ม.บูรพา) และ Arincare (ร้านยา 6,000+ แห่ง) **ยังไม่เจอใครรวม PGx + DDI + response monitoring + adherence ไว้ในหน้าจอเภสัชกรเดียว** แต่คู่แข่งจริงคือ "CDS ใน HIS + เภสัชกรทำเองด้วย Excel"
10. ผลตรวจ claim: PREPARE, CPIC ×2, clopidogrel–omeprazole, TKI–PPI และ PDPA ม.26 **ถูก** (มีรายละเอียดต้องเติม) ส่วน ESC/EAS ApoB **ถูกบางส่วน** (ApoB เป็น secondary target ไม่ใช่เป้าหลัก) ที่**ต้องแก้**คือ "FDA CDS guidance 2022" ซึ่งถูกแทนด้วยฉบับ 6 ม.ค. 2026 แล้ว และ "liquid biopsy ราคาลดลง" ซึ่งยืนยันไม่ได้ และราคา cash ของ Guardant ปี 2026 ยังขึ้นด้วย

---

## 2. ข้อเท็จจริงตลาดไทย

### 2.1 ประชากรและ polypharmacy

| ข้อมูล | ตัวเลข | สถานะ | แหล่ง |
|---|---|---|---|
| ประชากรไทยตามทะเบียน ปี 2568 | 65,809,011 คน | ✅ (กรมการปกครอง ผ่าน TheCoverage) | [S1] |
| ผู้สูงอายุ 60+ ปี 2568 | 14,144,098 คน = **21.82%** | ✅ | [S1] |
| GISTDA ปี 2025: 60+ = 13.6 ล้าน, เด็ก <15 = 9.5 ล้าน | ต่างจาก [S1] เพราะใช้วิธีวิเคราะห์ต่างกัน | 🟡 | [S2] |
| Polypharmacy (≥5 ยา) ผู้สูงอายุในหน่วยปฐมภูมิ 8 แห่ง 4 ภาค (n=4,848, ข้อมูลปี 2017) | **15.0%** และ PIM ในใบสั่งยา 65.9% | ✅ | [S3] |
| Polypharmacy (≥5 API ต่อเนื่อง ≥90 วัน) ผู้สูงอายุ OPD รพ.ทุติยภูมิ 46 แห่ง เขต 8 (n=587,905) | **59.5%**, multimorbidity 48.6%, PIM 32.1% | ✅ | [S4] |
| ช่วงความชุก polypharmacy ในไทยจากงาน review | 29–75% | 🟡 (review ปี 2018) | [S5] |

📊 **ข้อสังเกต:** ความชุก polypharmacy ต่างกันมากตาม setting (15% ถึง 59.5%) ห้ามใช้ตัวเลขเดียวแทนทั้งประเทศ ถ้าพิตช์ ให้พูดว่า "ในผู้สูงอายุที่มารับบริการ OPD โรงพยาบาลทุติยภูมิ พบ polypharmacy ราว 6 ใน 10"

### 2.2 โรงพยาบาลและเภสัชกร

| ข้อมูล | ตัวเลข | สถานะ | แหล่ง |
|---|---|---|---|
| รพ.รัฐ ตติยภูมิ / ทุติยภูมิ / หน่วยปฐมภูมิ | **324 / 682 / 9,770** | ✅ WHO Pharmaceutical Country Profile 2025 | [S6] |
| รพ.สังกัดสำนักงานปลัด สธ. (มี.ค. 2022) | 901 แห่ง (ศูนย์ 34, ทั่วไป 92, ชุมชน 775) | 🟡 Wikipedia (บทความขอ citation เพิ่ม) | [S7] |
| รพ.เอกชน | 370 แห่ง (กทม. 116, ต่างจังหวัด 254), ~36,000 เตียง | 🟡 Krungsri Research Outlook 2020–22 (**ข้อมูลเก่า**) | [S8] |
| ร้านยา (retail pharmacies) | **19,126** แห่ง | ✅ | [S6] |
| ความหนาแน่นเภสัชกร (2023) | **6.16 ต่อประชากร 10,000** (แพทย์ 9.28) | ✅ WHO | [S6] |
| จำนวนเภสัชกรโดยประมาณ | ~40,500–44,100 คน | 📊 คำนวณจาก 6.16/10,000 × ประชากร 65.8M [S1] หรือ 71.67M (ประชากร UN ที่ WHO/GLOBOCAN ใช้ [S9]) — ❓ ยังไม่มีตัวเลขจากสภาเภสัชกรรมโดยตรง | [S6][S1][S9] |
| Arincare (แพลตฟอร์มร้านยา) | ร้านยาลงทะเบียน 6,000+ แห่ง, เภสัชกร 12,000+ คน (มิ.ย. 2026) | 🟡 | [S10] |

⚠️ การค้นเว็บครั้งแรกให้ตัวเลข "เภสัชกร 9.28/10,000" มา แต่เมื่อเปิดเอกสาร WHO พบว่า **9.28 คือแพทย์** ส่วนเภสัชกรคือ 6.16 ถ้าเคยใส่ตัวเลขนี้ในสไลด์ให้แก้

### 2.3 กลุ่มรพ.เอกชนที่มี preventive / lipid / PGx

| กลุ่ม/รพ. | สิ่งที่ยืนยันได้ | แหล่ง |
|---|---|---|
| **BDMS** | ✅ 60 รพ. 9,360 เตียง (Bangkok Hospital 32, Samitivej 7, Phyathai 8, Paolo 7, BNH 1, Royal 2, Local 3) ข้อมูล ส.ค. 2026 | [S11] |
| Bangkok Heart Hospital / Bangkok Hospital HQ | ✅ มี "Preventive Heart and Lipid Clinic" | [S12] |
| Bangkok Hospital | ✅ บริการ PGx ด้วย NGS ครอบคลุม "500+ ยา" (ไม่เปิดราคา) | [S13] |
| BNH (M BRACE) | ✅ PGx ครอบคลุม 126 ยา รวมค่าแพทย์แปลผล (ไม่เปิดราคา) | [S14] |
| Samitivej Sukhumvit | ✅ Genomics & Lifestyle Wellness Center เป็นศูนย์ส่งต่อด้าน genetics ของเครือ BDMS | [S15] |
| Bumrungrad | 🟡 โปรแกรม "Common Pharmacogenomics" 13 ยีน 147 ยา (มาจาก snippet ของผลค้นหา หน้าเว็บไม่แสดงรายละเอียด) | [S16] |
| N Health (เครือ BDMS) | ✅ "Pharmacogenetics Profile (Guideline-Based)" ขายบน HDmall | [S17] |

📊 **Beachhead:** BDMS เป็นเครือเดียวที่มีครบทั้ง lipid clinic, PGx lab (N Health, Bangkok Hospital) และศูนย์ genetics (Samitivej) ถ้าได้พาร์ทเนอร์ในเครือนี้ 1 แห่ง จะขยายต่อในเครือได้

### 2.4 มะเร็งปอดและ EGFR

| ข้อมูล | ตัวเลข | สถานะ | แหล่ง |
|---|---|---|---|
| มะเร็งปอดรายใหม่ในไทย (GLOBOCAN 2024, เผยแพร่ ก.ค. 2026) | **23,871** ราย (อันดับ 2 รองจากตับ), เสียชีวิต 21,811, 5-yr prevalence 32,153 | ✅ | [S9] |
| มะเร็งทุกชนิดรายใหม่ | 176,951 ราย | ✅ | [S9] |
| NSCLC ต่อมะเร็งปอดทั้งหมด | ~85% | 🟡 expert recommendation | [S18] |
| EGFR mutation ใน NSCLC ไทย | **54–68%** | 🟡 expert recommendation (TLCR 2025) | [S18] |
| รามาธิบดี 2012–2017: advanced NSCLC ที่รู้สถานะ EGFR (n=750) | **56.3%** EGFR+ | ✅ | [S19] |
| รพ.พุทธโสธร 2017–2022 (n=232 NSCLC) | 46.55% (adenocarcinoma aOR 14.39) | ✅ | [S20] |
| PIONEER: adenocarcinoma ระยะ IIIB/IV ในเอเชีย 7 ประเทศ รวมไทย (n=1,450) | **51.4%** | ✅ | [S21] |
| ตัวเลข PIONEER เฉพาะคนไทย | ❓ **ยังยืนยันไม่ได้** (ตารางรายประเทศอ่านจากหน้าเว็บไม่ได้) | — | [S21] |
| สิทธิการรักษา | ✅ ตรวจ EGFR ด้วย qPCR ได้รับการเบิกจ่ายในทุกสิทธิ; กรมบัญชีกลาง (OCPA) เปิดให้ใช้ erlotinib เป็น first-line (gefitinib เป็นทางเลือก) ตั้งแต่ 1 ธ.ค. 2568; osimertinib เบิกได้เป็นหลักใน CSMBS | [S22][S23][S18] |

### 2.5 Statin / GLP-1 RA

| ข้อมูล | ตัวเลข | สถานะ | แหล่ง |
|---|---|---|---|
| ผู้ป่วย ACS ได้ high-intensity statin ตอนจำหน่าย (รพ.ตติยภูมิ 1 แห่ง) | เพิ่มจาก 10% (2013) เป็น 88% (2017) | ✅ | [S24] |
| ผู้ป่วยกลุ่มเดียวกันที่ได้ตรวจ LDL-C ซ้ำภายใน 120 วัน / ถึงเป้า | **24.4%** / 43.3% | ✅ ใช้รองรับปัญหาข้อ 2 ใน idea.md ("ไม่เห็น trajectory") ได้ดี | [S24] |
| การสั่ง simvastatin ร่วมกับยาที่ห้ามใช้ร่วม (26 รพ.ตติยภูมิ) | ลดจาก 3.6%/3.1% (2013) เหลือ 2.6%/2.0% (2015) | ✅ | [S25] |
| "Statin 54.7 → 68.3 DDD/1000/วัน" | ⚠️ **เป็นตัวเลขระดับโลก ไม่ใช่ของไทย** ห้ามใช้เป็นข้อมูลไทย | ✅ (Guadamuz, BMJ Open 2022) | [S26] |
| Wegovy (semaglutide) ในไทย | อย.อนุมัติ 2023, เปิดตัว เม.ย. 2025 (ตลาดแรกใน SEA), เริ่มที่ รพ.เอกชน | 🟡 | [S27] |
| ราคา Wegovy ในไทย | เว็บคลินิกแห่งหนึ่งระบุปากกา 2.4 mg ฿19,000 | 🟡 (ราคาคลินิกเดียว) | [S28] |
| แนวโน้มปริมาณการใช้ GLP-1 RA ในไทย (ปริมาณ/มูลค่า) | ❓ **ยังยืนยันไม่ได้** (รายงาน Grand View ตอบ 403 และไม่มีข้อมูล IQVIA ไทยสาธารณะ) | — | — |

### 2.6 PGx ในไทย (บริการที่มีอยู่)

| ข้อมูล | สถานะ | แหล่ง |
|---|---|---|
| สปสช. เริ่มนโยบายคัดกรอง HLA-B\*15:02 ทั่วประเทศปี 2018; ส่งตรวจที่สถาบันชีววิทยาศาสตร์ทางการแพทย์ + ศูนย์วิทย์ฯ 14 ศูนย์; "ค่าใช้จ่าย 1,000 บาท/ราย", "บริการตรวจฟรีทุกคนในสิทธิต่างๆ" | ✅ | [S29][S30] |
| สปสช. ชดเชยตรวจ HLA-B\*58:01 ราคา 1,000 บาท ในสิทธิ UCS (ประกาศ 2024 ตามที่อ้างในงานวิจัยปี 2025); เพิ่มเป็นสิทธิประโยชน์บัตรทองตั้งแต่ปลายปี 2020 | ✅ / 🟡 | [S31][S32] |
| Rama PPM เป็น reference lab ด้าน PGx แห่งแรกของไทย; HLA-B testing เพิ่มจาก 94 ครั้ง (2011) เป็น 2,880 ครั้ง (2020) | ✅ | [S30][S33] |
| Rama ออก **pharmacogenetic ID card** (HLA-B, CYP2D6, CYP2C19) พร้อม counselling | ✅ | [S34] |
| PGxCard / "กินอยู่ดี แพลตฟอร์ม" × คณะเภสัชฯ ม.บูรพา, ทุน สวรส., ทำงานร่วมกับศูนย์จีโนมรามาฯ, บัตรแพ้ยาอิเล็กทรอนิกส์ | ✅ | [S35] |
| คนไทย 4,662 คน: 95.99% มี CPIC-actionable ≥1; ผู้ใช้ statin มี SLCO1B1 actionable 21.95–23.05%; ผู้ใช้ omeprazole มี CYP2C19 actionable 55.02%; ผู้ใช้ rosuvastatin มี ABCG2 actionable 35.90% (PLoS One ส.ค. 2026) | ✅ | [S36] |
| Genomics Thailand มี pharmacogenomics เป็นหนึ่งในกลุ่มโรคเป้าหมาย | ✅ | [S23] |

---

## 3. ราคาการตรวจ

> ราคาในไทยที่ยืนยันได้มีน้อยมาก ส่วนใหญ่ต้องใช้ราคาต่างประเทศเป็นตัวเทียบ ถ้าแปลงเป็นบาท 📊 ใช้สมมติฐาน **~33 บาท/USD** และ **~36 บาท/EUR** (สมมติฐาน ไม่ใช่อัตราอ้างอิง)

### 3.1 PGx

| การตรวจ | ราคา | สถานะ | แหล่ง |
|---|---|---|---|
| N Health "Pharmacogenetics Profile (Guideline-Based)" | **฿14,751** (HDmall, ราคาใช้ได้ถึง 4 ต.ค. 2026; ราคาในรายการแนะนำ ฿15,320) | ✅ | [S17] |
| ATGenes "ตรวจยีนแพ้ยา >20 ชนิด" (เจาะเลือด) | **฿39,600** | ✅ | [S37] |
| ATGenes ตรวจยีนแพ้ยา carbamazepine (รายยา) | ฿1,485 | ✅ | [S37] |
| สปสช. HLA-B\*15:02 / HLA-B\*58:01 | ฿1,000 ต่อการตรวจ (ราคาชดเชย) | ✅ | [S29][S31] |
| GeneusDNA: "ตรวจแพ้ยา" | ฿1,500–4,000 ต่อรายการ | 🟡 (บล็อกผู้ขาย) | [S38] |
| Bangkok Hospital / BNH / Bumrungrad PGx | ❓ ไม่เปิดราคาบนเว็บ | — | [S13][S14][S16] |
| GeneSight (US, psychiatric PGx) | self-pay **$330** | ✅ | [S39] |
| Genomind PGx (US, at-home) | self-pay **$599** | ✅ | [S40] |

### 3.2 NMR metabolomics / lipoprotein

| การตรวจ | ราคา | สถานะ | แหล่ง |
|---|---|---|---|
| Labcorp NMR LipoProfile (US; LDL-P, LDL size, LPIR) | ปกติ **$119** (โปรฯ $89.25) | ✅ | [S41] |
| Nightingale consumer blood test (ฟินแลนด์) | €79 | 🟡 (ข่าว; หน้า Health Check ปัจจุบันไม่เปิดราคา) | [S42][S43] |
| Nightingale ใน SEA | ข้อตกลงกับ Innoquest (15 พ.ย. 2023) ครอบคลุม SG, MY, VN, PH, **TH**, ID, AU; lab สิงคโปร์คาดรับตัวอย่าง Q1 2025 — **ไม่เปิดราคา** | ✅ (press release) | [S44][S45] |
| Bruker IVDr B.I.-LISA (114 lipoprotein parameters, 150 ตัวอย่าง/วัน) | ❓ ไม่เปิดราคาต่อตัวอย่าง; listing ระบุ **"For research only"** | ✅ สถานะ RUO / ❓ ราคา | [S46][S47] |
| บริการ NMR ทางคลินิกในไทย | ❓ **ยังยืนยันไม่ได้ว่ามี** มีแต่ lab วิจัย เช่น KKU International Phenome Lab (NMR + LC-MS สำหรับงานวิจัย) | 🟡 | [S48] |

⚠️ **ผลต่อ idea.md:** idea เขียนว่า "รับเฉพาะผลจาก lab ISO 15189" แต่ถ้าในไทยยังไม่มี lab NMR ทางคลินิก Module A จะใช้ NMR จริงได้เฉพาะในงานวิจัย ควรเขียนให้ตรงว่า "NMR = research-use input จนกว่าจะมี lab ที่ได้ accreditation" และควรมี **fallback เป็น ApoB immunoassay ตามมาตรฐาน** ซึ่งเป็นการตรวจ clinical chemistry ทั่วไป (❓ ราคา ApoB ในไทยยังไม่ได้ตรวจสอบ)

### 3.3 Liquid biopsy / cfDNA

| การตรวจ | ราคา | สถานะ | แหล่ง |
|---|---|---|---|
| Guardant360 CDx / Guardant360 Liquid CDx (US) | cash **$8,455** (มีผล 8 มิ.ย. 2026) | ✅ | [S49] |
| Guardant360 (Medicare เดิม) | $5,000 (ADLT คาดว่าจะเป็น $8,455) | 🟡 | [S50] |
| FoundationOne Liquid (US) | list **$5,800** (ตอนเปิดตัวปี 2018) | 🟡 (ข่าวปี 2018 อาจล้าสมัย) | [S51] |
| Tempus xF | ไม่มี rate card; ADLT ของ xT CDx $4,500 | 🟡 | [S52] |
| LucenceINSIGHT (สิงคโปร์) | "upwards of SGD 1000" | 🟡 | [S53] |
| cobas EGFR plasma / liquid biopsy ในไทย | ❓ **ยังยืนยันไม่ได้** (ไม่พบราคาเผยแพร่) | — | — |
| Guardant360 CDx ได้รับอนุมัติ HSA สิงคโปร์ 2023 | 🟡 | [S53] |

📊 **"Liquid biopsy ราคาลดลง" ใน idea.md §12 Why-now:** ไม่พบหลักฐาน และราคา cash ของ Guardant ในสหรัฐฯ ปี 2026 ยัง**สูงขึ้น** (จาก Medicare $5,000 เป็น $8,455) ควรตัดข้อนี้ออก หรือเปลี่ยนเป็น "ตรวจ EGFR plasma แบบ PCR เข้าถึงได้มากขึ้น" ซึ่งต้องหาหลักฐานมาใส่ก่อน

---

## 4. คู่แข่ง

| ผู้เล่น | ทำอะไร | Pricing model (ถ้าเปิด) | Gap เทียบ PrecisionRx | แหล่ง |
|---|---|---|---|---|
| **UpToDate Lexidrug** (Lexicomp เดิม, Wolters Kluwer) | ฐานข้อมูลยา + DDI + มีฐานข้อมูล PGx | Subscription สถาบัน; ❓ ไม่เปิดราคา | ไม่ผูก genotype ของคนไข้รายคน ไม่มี longitudinal response หรือ adherence | [S54][S55] |
| **Micromedex** (Merative) | Drug/DDI/tox reference ใช้ใน 80+ ประเทศ | Subscription; ❓ ไม่เปิดราคา | เหมือน Lexidrug; เป็น reference ไม่ใช่ workflow รายคนไข้ | [S56] |
| **GeneSight** (Myriad) | PGx test + report ด้าน psychiatry | Test-based; self-pay $330 | ขายผลตรวจของตัวเอง, เน้นจิตเวช, ไม่ lab-agnostic | [S39] |
| **Genomind** | PGx test (at-home) + report | Self-pay $599 | เหมือน GeneSight; รายงานครั้งเดียว | [S40] |
| **RxGenomix** (ExactMeds) | PGx program สำหรับเภสัชกร/นายจ้าง: testing, practice integration, population analytics | ❓ ไม่เปิดราคา | **ใกล้ที่สุดในเชิง pharmacist workflow** แต่ไม่มี NMR/cfDNA และไม่มีในไทย | [S57] |
| **Translational Software** | PGx CDS/portal ให้ lab และ EHR, FHIR PGx API (2016), ทำงานร่วม DrFirst, FDB | B2B ผ่าน lab/EHR; ❓ ราคา; ❓ สถานะความเป็นเจ้าของปัจจุบัน | Engine PGx ที่โตแล้ว → **ถ้าเข้าไทยจะเป็นคู่แข่งตรง** แต่ไม่มี TMT mapping, สิทธิการรักษาไทย หรือ NMR | [S58][S59] |
| **OncoKB** (MSK) | Precision oncology knowledge base; มี FDA decision summary | ฟรีสำหรับงานวิจัยในสถาบันการศึกษา; **รพ.และบริษัทต้องจ่าย annual license** | เป็น KB ไม่ใช่ workflow; PrecisionRx ต้องจ่ายค่า license ถ้าใช้เชิงพาณิชย์ | [S60][S61] |
| **navify Mutation Profiler / Therapy Matcher / Tumor Board** (Roche) | อ่านผล NGS (CE-IVD) + จับคู่ยา + tumor board | Enterprise; ❓ | ไม่มี germline PGx หรือ DDI สำหรับเภสัชกร | [S62] |
| **Tempus** | Test (xT/xF) + data platform + CDS | Enterprise pricing, รายได้หลักจากการเบิกค่าตรวจ | ผูกกับ assay ของตัวเอง, ตลาดหลักคือสหรัฐฯ | [S52] |
| **Guardant / Foundation Medicine** | Liquid biopsy + report | Test-based ($8,455 / $5,800) | รายงานของ assay ตัวเอง ไม่มี germline PGx + DDI | [S49][S51] |
| **Nightingale Health** | NMR blood test + health report; lab สิงคโปร์ ISO 13485, ได้ HSA approval | Consumer €79 (FI); B2B ผ่าน Innoquest | รายงาน risk ของ assay ตัวเอง ไม่มีมุมมองเรื่องยา; **มีช่องทางเข้าไทยแล้ว** (Innoquest) ห้ามพูดว่า "ไม่มีในเอเชีย" | [S44][S45] |
| **Labcorp NMR LipoProfile** | LDL-P ด้วย NMR (US) | $119 | เฉพาะสหรัฐฯ | [S41] |
| **Rama PPM + PGx ID card** (ไทย) | Reference lab + บัตร PGx + counselling | บริการของรพ. | เป็นบัตร/รายงาน ยังไม่เป็น CDS ที่ทำงานอัตโนมัติทุกครั้งที่สั่งยา → **พาร์ทเนอร์ได้ ไม่ใช่คู่แข่ง** | [S34] |
| **PGxCard / กินอยู่ดี × ม.บูรพา** (ไทย) | แพลตฟอร์มดิจิทัล PGx + บัตรแพ้ยาอิเล็กทรอนิกส์ (ทุน สวรส.) | ❓ | **คู่แข่งไทยที่ใกล้ที่สุดฝั่ง PGx** ต้องไปดูระบบจริงก่อนพิตช์ | [S35] |
| **N Health / Bangkok Hospital / ATGenes** (ไทย) | ขาย PGx panel + รายงาน | ฿14,751 / ไม่เปิด / ฿39,600 | รายงานครั้งเดียว ไม่ใช้ซ้ำตอนสั่งยาใหม่ → **เป็น lab partner** | [S17][S13][S37] |
| **Arincare** (ไทย) | SaaS ร้านยา + telepharmacy + e-Rx; ร้านยา 6,000+ แห่ง | SaaS | ยังไม่พบฟีเจอร์ PGx แต่เป็น **ช่องทางกระจาย (channel)** หรือคู่แข่งถ้าเพิ่ม CDS | [S10] |
| **CDS ใน HIS (HOSxP ฯลฯ)** + เภสัชกรทำเอง | Rule DDI/แพ้ยา | รวมอยู่ใน HIS | คู่แข่งตัวจริงคือ "ของที่มีอยู่แล้วฟรี" ❓ ยังไม่ได้ตรวจความสามารถ PGx rule ใน HOSxP | — |

📊 **ข้อสรุปเชิงกลยุทธ์**
- จุดที่ยังไม่มีใครครอง: **ใช้ PGx ซ้ำทุกครั้งที่สั่งยา + DDI + adherence (PDC) ในหน้าจอเดียวของเภสัชกร พร้อม mapping ไทย (TMT, สิทธิ สปสช./CSMBS, allele frequency ไทย)** ข้อนี้พอป้องกันได้ แต่เป็นความได้เปรียบด้าน **เวลาและการโฟกัส** ไม่ใช่สิ่งที่คนอื่นลอกไม่ได้ เพราะ Translational Software หรือ RxGenomix ทำ localisation ได้ถ้าเห็นว่าตลาดไทยคุ้ม
- NMR และ cfDNA เป็นจุดต่างบนเวที แต่ในตลาดจริงยังเป็นจุดอ่อน: NMR ยังไม่มี clinical lab ในไทย ส่วน cfDNA มีปริมาณน้อย
- Lab ไทยที่ขาย PGx (N Health, Bangkok Hospital, ATGenes, Rama) ควรวางเป็น **ช่องทาง/พาร์ทเนอร์** เพราะลูกค้าของเขาจะได้ประโยชน์จากผลตรวจมากขึ้นถ้าใช้ซ้ำได้

---

## 5. TAM / SAM / SOM (bottom-up)

> ⚠️ **ทุกราคาในหัวข้อนี้เป็นสมมติฐาน (📊) ยังไม่มีโรงพยาบาลไหนยืนยันว่าจะจ่ายราคานี้** ส่วน denominator มีแหล่งอ้างอิง ถ้าถูกถามว่า "ใครเคยจ่ายราคานี้" ให้ตอบตรงๆ ว่ายังไม่มี และอธิบายว่าจะ validate อย่างไร

### 5.1 Module A — Cardiometabolic, pharmacist-led (SaaS ต่อโรงพยาบาล)

**สูตร:** จำนวน รพ. × สัดส่วนที่เข้าถึงได้ × ค่า SaaS ต่อปี

| ชั้น | Denominator | สถานะ | Penetration / filter | ราคา/ปี (📊) | มูลค่า/ปี |
|---|---|---|---|---|---|
| **TAM** | รพ.รัฐตติยภูมิ 324 + ทุติยภูมิ 682 [S6] + เอกชน 370 [S8] = **1,376 แห่ง** | ✅/🟡 (ตัวเลขเอกชนเก่า) | 100% | ฿300,000–600,000 | **฿0.41–0.83 พันล้าน** |
| **SAM** | รพ.ที่มีบริการ PGx หรือ preventive/lipid clinic อยู่แล้ว (ตัวอย่างที่ยืนยันได้: เครือ BDMS 60 แห่ง [S11], Rama, Chula [S63]) → สมมติ **60–100 แห่ง** | 📊 (❓ ไม่มีรายชื่อครบ) | — | ฿300,000–600,000 | **฿18–60 ล้าน** |
| **SOM (ปีที่ 3)** | **5–10 แห่ง** (1 pilot site ปีแรก แล้วขยายในเครือเดียวกัน) | 📊 | ~8–10% ของ SAM | ฿400,000 | **฿2–4 ล้าน** (ถึง ~฿6 ล้าน ถ้าได้ ฿600k/แห่ง) |

**Cross-check มุมคนไข้ (📊):** สมมติ 1 รพ.ทบทวนยา 1,000 ราย/ปี ด้วย SaaS ฿400,000 ต้นทุนจะตก ~฿400/ราย ถูกกว่า PGx panel ฿14,751 [S17] ราว 37 เท่า จึงพอขายเป็น "ต้นทุนเล็กที่ทำให้ผลตรวจราคาแพงถูกใช้ซ้ำได้" แต่ถ้าบวกค่า NMR ทุก 3–6 เดือน (❓ ยังไม่มีราคาไทย; เทียบ US $89–119 [S41]) ต้นทุนต่อคนจะขึ้นตามจำนวน visit เหมือนที่กรรมการธุรกิจเตือนใน critique §7

**Capacity check (📊):** SOM 10 รพ. × 1,000 ราย = 10,000 reviews/ปี ฝั่งซอฟต์แวร์รับได้ แต่ถ้าทุกคนต้องมี NMR จะต้องมี lab ที่รันได้ ~20,000 ตัวอย่าง/ปี (2 ครั้ง/คน) ปัจจุบันยังไม่มี clinical NMR lab ในไทย ดังนั้น **SOM ที่ทำได้จริงคือ PGx + DDI + adherence + lipid ปกติ/ApoB ส่วน NMR เป็น add-on สำหรับงานวิจัย**

**ข้อมูลรองรับ value story (✅):** ใน 100 คนที่ได้ statin จะมี ~22–23 คนที่มี SLCO1B1 actionable และใน 100 คนที่ได้ omeprazole จะมี ~55 คนที่มี CYP2C19 actionable [S36] ตัวเลขนี้ใช้เป็นตัวเลขคาดการณ์ "actionable PGx finding ต่อ 100 คน" ใน pilot success criteria ได้เลย

### 5.2 Module B — Oncology cfDNA interpretation (ค่าอ่านผลต่อรายงาน)

**สูตร:** มะเร็งปอดรายใหม่ × NSCLC × ระยะลุกลาม × โอกาสที่ต้องตรวจ cfDNA × ค่าบริการต่อรายงาน

| ขั้น | ค่า | สถานะ | แหล่ง |
|---|---|---|---|
| มะเร็งปอดรายใหม่/ปี | 23,871 | ✅ | [S9] |
| × NSCLC 85% | ≈ 20,290 | 🟡 | [S18] |
| × ระยะลุกลามตอนวินิจฉัย **70%** | ≈ 14,200 | 📊 ❓ (ไม่พบตัวเลขไทยที่ยืนยันได้) | — |
| (ก) ตรวจ cfDNA ตอนวินิจฉัย เพราะชิ้นเนื้อไม่พอ **20–30%** | ≈ 2,840–4,260 | 📊 | — |
| (ข) EGFR+ 54% × ถึงระยะดื้อยาและตรวจซ้ำ **60%** | ≈ 4,600 | 🟡 [S18] / 📊 | — |
| **รวมรายงาน cfDNA ที่อาจเกิดขึ้น/ปี** | **≈ 7,400–8,900** | 📊 | — |
| ค่าอ่านผลต่อรายงาน | ฿1,500–3,000 | 📊 | — |
| **TAM** | **≈ ฿11–27 ล้าน/ปี** | 📊 | — |
| **SAM**: เฉพาะคนที่เข้าถึงการตรวจจริง (CSMBS ครอบคลุม ~10% ของประชากร, UCS 71%, SSS 19% [S6] + จ่ายเอง/ประกันเอกชน) → สมมติ uptake 20–30% | ≈ 1,500–2,700 รายงาน → **≈ ฿2–8 ล้าน/ปี** | 📊 | [S6] |
| **SOM (ปีที่ 3)**: 1–2 ศูนย์มะเร็ง ≈ 200–400 รายงาน | **≈ ฿0.3–1.2 ล้าน/ปี** | 📊 | — |

📊 **ข้อสรุป:** Module B **ไม่ควรเป็นแหล่งรายได้หลัก** ในไทย เพราะปริมาณรายงานน้อยและคนส่วนใหญ่อยู่ในสิทธิ UCS ที่ไม่เบิก liquid biopsy มี 2 ทางเลือกที่สมเหตุสมผลกว่า
1. ขายเป็น **license "oncology pharmacy module" ต่อศูนย์มะเร็ง** ครอบคลุมทุกคนไข้มะเร็ง (DPYD/UGT1A1 + DDI ของยา TKI/เคมีบำบัด) ไม่เก็บเฉพาะรายงาน cfDNA
2. ใช้ Module B เป็น **หลักฐานว่าสถาปัตยกรรมขยายได้** (lab-agnostic, AMP/ASCO/CAP tier) บนเวที แต่ตอนพิตช์ธุรกิจให้นำด้วย Module A

### 5.3 สิ่งที่ต้องทำเพื่อเปลี่ยนสมมติฐานให้เป็นข้อเท็จจริง
- สัมภาษณ์หัวหน้าเภสัชกร รพ.เอกชน 3–5 แห่ง (เริ่มจากเครือ BDMS) ถามงบซอฟต์แวร์ CDS ปัจจุบันและจำนวน medication review ต่อปี → ใช้ validate ราคา SaaS
- ขอตัวเลขจาก lab PGx (N Health, Rama PPM) ว่าตรวจกี่รายต่อปี → ใช้เป็น denominator ของ SAM ที่ดีกว่าจำนวน รพ.
- ถาม Innoquest Thailand ว่าเปิดบริการ Nightingale ในไทยแล้วหรือยัง และราคาเท่าไร
- ขอข้อมูลระยะโรคตอนวินิจฉัยจาก Thai Cancer Registry หรือจากศูนย์มะเร็งพาร์ทเนอร์ เพื่อแทนสมมติฐาน 70%

---

## 6. ผลตรวจ claim ใน idea.md

| # | Claim ใน idea.md | ผล | รายละเอียด / สิ่งที่ควรแก้ | แหล่ง |
|---|---|---|---|---|
| 1 | PREPARE (Swen et al., Lancet 2023) preemptive 12-gene panel ลด clinically relevant ADR ~30% | ✅ **ถูก มีรายละเอียดต้องเติม** | Lancet 2023;401:347–356 (4 ก.พ. 2023), n=6,944, 7 ประเทศยุโรป ในกลุ่มที่มี actionable result ADR เกิด 21.0% vs 27.7%, **OR 0.70 (95% CI 0.54–0.91)** ทั้งประชากรได้ OR 0.70 (0.61–0.79) · สิ่งที่ต้องรู้: open-label cluster-randomised crossover, ผู้ร่วมวิจัย **97.7% เป็นคนยุโรป/เมดิเตอร์เรเนียน/ตะวันออกกลาง**, ใช้แนวทาง **DPWG ไม่ใช่ CPIC**, follow-up 12 สัปดาห์ และมีจดหมายใน Lancet ที่แย้งว่า "benefits are unclear" · **ควรเขียนว่า** "odds ของ ADR ลดลง 30% (OR 0.70) ในการศึกษาที่ยุโรป ยังไม่มีข้อมูลในคนไทย" | [S64][S65][S66] |
| 2 | ESC/EAS 2019 ยอมรับ ApoB เป็นเป้าหมายได้ | 🟡 **ถูกบางส่วน** | 2019 ESC/EAS แนะนำ apoB สำหรับประเมินความเสี่ยง และใช้**แทน LDL-C** ได้ในคนที่ TG สูง เบาหวาน อ้วน หรือ LDL-C ต่ำมาก (Class I, Level C) กำหนด **secondary goal** apoB <65 / <80 / <100 mg/dL ตามระดับความเสี่ยง · **LDL-C ยังเป็นเป้าหลัก** และมี 2025 Focused Update แล้ว ควรเขียนว่า "ApoB เป็น secondary target" และอ้าง guideline ฉบับล่าสุด | [S67][S68] |
| 3 | FDA CDS guidance 2022 criteria (non-device CDS) | ❌ **ล้าสมัย ต้องแก้** | FDA ออก CDS guidance ฉบับปรับปรุง **6 ม.ค. 2026 ที่ supersede ฉบับ 2022** ประเด็นสำคัญ: อนุโลมให้ output เป็นคำแนะนำเดียวได้ถ้าทางคลินิกมีคำตอบที่เหมาะสมเพียงข้อเดียว, ย้ายเรื่อง time-critical ไปอยู่ใน criterion 4 และ**ไม่พูดถึง AI เลย** ส่วน criterion 1 ยังเหมือนเดิม คือซอฟต์แวร์ที่ "acquire/process/analyze signal จาก IVD" เป็น device ทางออกของ idea (รับเฉพาะผลที่ lab ประมวลแล้ว) จึงยังสอดคล้อง · ⚠️ ส่วน LLM summarizer อยู่ในพื้นที่ที่ guidance ไม่ได้ตอบ และ guidance ของสหรัฐฯ **ไม่มีผลทางกฎหมายในไทย** ใช้ได้แค่เป็นกรอบเทียบ | [S69][S70] |
| 4 | PDPA มาตรา 26 ครอบคลุมข้อมูลพันธุกรรม/สุขภาพ | ✅ **ถูก** | ม.26 ระบุชัดทั้ง health, genetic, biometric ว่าเป็นข้อมูลอ่อนไหว ต้องได้ explicit consent เว้นแต่เข้าข้อยกเว้น (เช่น vital interest, เวชศาสตร์ป้องกัน/การวินิจฉัยทางการแพทย์ตามเงื่อนไข) ❓ ถ้อยคำภาษาไทยของ ม.26(5) ยังไม่ได้เทียบกับราชกิจจาฯ ต้องให้ `thai-healthtech-legal` ตรวจก่อนอ้างข้อยกเว้น | [S71][S72] |
| 5 | Gefitinib/erlotinib + PPI ลดการดูดซึม | ✅ **ถูก** | **IRESSA label:** "Avoid concomitant use… with proton pump inhibitors, if possible. If… required, take IRESSA 12 hours after the last dose or 12 hours before the next dose of the PPI" · **TARCEVA label:** avoid PPI, "separation of doses may not eliminate the interaction"; omeprazole ลด AUC 46%, Cmax 61% · รายละเอียดที่ควรเติม: ในไทย erlotinib เป็น first-line ที่เบิกได้ [S22] เคส D จึงสมจริง แต่หลังพบ T790M ยาต่อไปคือ osimertinib ❓ ยังไม่ได้ตรวจ label ของ osimertinib เรื่อง PPI | [S73][S74][S75] |
| 6 | Clopidogrel + omeprazole/esomeprazole (CYP2C19 inhibition) | ✅ **ถูก** | Plavix label (2022) W&P 5.1: "Avoid concomitant use of Plavix with omeprazole or esomeprazole"; dexlansoprazole, lansoprazole, pantoprazole มีผลน้อยกว่า → เสนอ pantoprazole ได้ · ผลต่อ clinical outcome ยังถกเถียง ควรติดป้ายเป็น [Label] ไม่ใช่ [Outcome] | [S76][S77] |
| 7 | CPIC SLCO1B1–simvastatin | ✅ **ถูก** | CPIC 2022 (SLCO1B1/ABCG2/CYP2C9): **decreased function** → "Prescribe an alternative statin… If simvastatin therapy is warranted, limit dose to <20 mg/day" (Strong); **poor function** → alternative statin (Strong) · เคส B (simvastatin 40 mg + decreased function) จึงเกินเพดานที่ CPIC แนะนำชัดเจน | [S78][S79] |
| 8 | CPIC CYP2C19–clopidogrel | ✅ **ถูก แต่ควรแก้ถ้อยคำใน UI** | CPIC 2022 update (ACS/PCI): **PM** → "Avoid clopidogrel if possible. Use prasugrel or ticagrelor at standard dose if no contraindication" (Strong); **IM** → "Avoid standard dose (75 mg) clopidogrel if possible…" (Strong) · สำหรับ neurovascular ใช้คำว่า "consider an alternative P2Y12" (Moderate) · UI ใน idea §7 เขียน "consider alternative antiplatelet" ซึ่ง**อ่อนกว่าที่ CPIC เขียนสำหรับ PM ในบริบทหัวใจ** ควรใช้ถ้อยคำตรงตามต้นฉบับ | [S80] |
| 9 | สปสช. HLA-B\*15:02 / \*58:01 ("ต้องตรวจสอบสิทธิ") | ✅ ตรวจแล้ว | ครอบคลุมทั้งคู่ (ดู §2.6) เปลี่ยนเป็น "ต่อยอดสิทธิประโยชน์ สปสช. ที่มีอยู่" ได้เลย | [S29][S31] |
| 10 | EGFR พบบ่อยใน adenocarcinoma คนไทย ("ต้องตรวจสอบตัวเลข") | ✅ | ใช้ "54–68% ของ NSCLC ไทย" [S18] หรือ "56% ใน advanced NSCLC ที่รามาฯ" [S19] ❓ ตัวเลข PIONEER เฉพาะคนไทยยังยืนยันไม่ได้ | [S18][S19] |
| 11 | "Liquid biopsy ราคาลดลงและแพร่หลายขึ้น" | ❓ **ยืนยันไม่ได้ ควรตัด** | ไม่พบหลักฐานว่าราคาในไทยลดลง และราคา cash ของ Guardant ในสหรัฐฯ ปี 2026 สูงขึ้น | [S49][S50] |
| 12 | "ไทยเป็นสังคมสูงวัย → polypharmacy เพิ่ม" | ✅ | 60+ = 21.82% (2568); polypharmacy 15–59.5% ตาม setting | [S1][S3][S4] |
| 13 | NMR จาก "Bruker IVDr หรือ Nightingale" + "รับจาก lab ISO 15189 เท่านั้น" | ⚠️ **ขัดกันเองในบริบทไทย** | Bruker B.I.-LISA อยู่ในสถานะ RUO และยังยืนยันไม่ได้ว่ามี clinical NMR lab ในไทย ควรเขียนใหม่ว่า NMR เป็น research input จนกว่าจะมี lab ที่ได้ accreditation | [S46][S44] |
| 14 | OncoKB "ต้องเช็ก license" | ✅ ตรวจแล้ว | ฟรีเฉพาะงานวิจัยในสถาบันการศึกษา ถ้าเป็นรพ.หรือเชิงพาณิชย์ต้องจ่าย annual license (ใส่ใน cost ของ Module B) | [S60] |
| 15 | "ระบบ DDI เดิมถูก override เป็นส่วนใหญ่" (alert fatigue) | ❓ **ยังยืนยันไม่ได้** (อยู่นอกขอบเขตรอบนี้) | ต้องหาแหล่งอ้างอิงก่อนพูดบนเวที | — |

---

## 7. แหล่งอ้างอิง

**ประชากร / ระบบสุขภาพ**
- [S1] TheCoverage.info (อ้างกรมการปกครอง) — https://www.thecoverage.info/news/content/10963
- [S2] Nation Thailand, GISTDA 2025 — https://www.nationthailand.com/news/general/40054741
- [S3] Vatcharavongvan et al., Can Geriatr J 2021 (PMID 34912488) — https://cgjonline.ca/index.php/cgj/article/view/516
- [S4] Kedthongma et al., Aging Clin Exp Res 2026 (PMID 42334761) — https://pubmed.ncbi.nlm.nih.gov/42334761/
- [S5] Polypharmacy in the Elderly, Rama Med J 2018 — https://he02.tci-thaijo.org/index.php/ramajournal/article/view/100635
- [S6] WHO SEARO, Thailand Pharmaceutical Country Profile 2025 — https://cdn.who.int/media/docs/default-source/searo/hsd/edm/thailand-medical-products-profile-2025.pdf?sfvrsn=dbe76c34_3
- [S7] Wikipedia, Hospitals in Thailand — https://en.wikipedia.org/wiki/Hospitals_in_Thailand
- [S8] Krungsri Research, Private Hospital Outlook 2020–2022 — https://www.krungsri.com/en/research/industry/industry-outlook/services/private-hospitals/io/io-private-hospitals
- [S9] GLOBOCAN 2024 Thailand fact sheet (IARC) — https://gco.iarc.who.int/media/globocan/factsheets/populations/764-thailand-fact-sheet.pdf
- [S10] The Story Thailand, Arincare Series B+ (3 มิ.ย. 2026) — https://www.thestorythailand.com/en/arincare-secures-series-b/
- [S11] BDMS Investor Relations, BDMS Network — https://investor.bdms.co.th/en/general/bdms-network
- [S12] Bangkok Heart Hospital, Preventive Heart and Lipid Clinic — https://www.bangkokhospital.com/en/bangkok-heart/center-clinic/bht-special-cardiac-center/preventive-heart-and-lipid-clinic/overview
- [S13] Bangkok Hospital, Pharmacogenomic — https://www.bangkokhospital.com/en/content/pharmacogenomics
- [S14] BNH M BRACE — https://mbrace.bnhhospital.com/why_pharmacogenomics/
- [S15] Samitivej Genomic and Lifestyle Wellness Center — https://www.samitivejhospitals.com/center/detail/Samitivej-Genomic-and-Life-Style-Wellness-Center
- [S16] Bumrungrad, โปรแกรมตรวจยีนแพ้ยาและปรับยา — https://www.bumrungrad.com/th/packages/drug-genes-common-pharmacogenomics
- [S17] HDmall, N Health Pharmacogenetics Profile (Guideline-Based) — https://hdmall.co.th/health-checkup/test-gene-allergy-drug-pharmacogenetics-profile-guideline-based-n-health

**มะเร็งปอด / EGFR / สิทธิ**
- [S18] Shuangshoti et al., Expert recommendations for biomarker evaluation of advanced NSCLC in Thailand, Transl Lung Cancer Res 2025 — https://tlcr.amegroups.org/article/view/103441/html
- [S19] Khiewngam et al., Front Oncol 2023 (PMID 36895484) — https://pubmed.ncbi.nlm.nih.gov/36895484/
- [S20] EGFR in Thai NSCLC, Buddhasothorn Hospital — https://he01.tci-thaijo.org/index.php/CMMJ-MedCMJ/article/view/269836
- [S21] Shi et al., PIONEER, J Thorac Oncol 2014 (PMID 24419411) — https://pmc.ncbi.nlm.nih.gov/articles/PMC4132036/
- [S22] กรมประชาสัมพันธ์: กรมบัญชีกลางปรับเกณฑ์ Erlotinib–Gefitinib 1 ธ.ค. 2568 — https://www.prd.go.th/th/content/category/detail/id/39/iid/442147
- [S23] Genomic medicine and cancer clinical trial in Thailand (PMC) — https://pmc.ncbi.nlm.nih.gov/articles/PMC10875286/

**Statin / GLP-1**
- [S24] Wongsalap & Jedsadayanmata, J Cardiol 2020 (PMID 31519405) — https://pubmed.ncbi.nlm.nih.gov/31519405/
- [S25] Rattanachotphanit et al., Ther Adv Drug Saf 2019 — https://pmc.ncbi.nlm.nih.gov/articles/PMC6354302/
- [S26] Guadamuz et al., BMJ Open 2022 (PMID 36691204) — https://pubmed.ncbi.nlm.nih.gov/36691204/
- [S27] College of Contemporary Health, Wegovy launch in Thailand — https://www.contemporaryhealth.co.uk/glp-1s-medications/novo-nordisk-introduces-wegovy-to-thailand-marking-first-launch-in-southeast-asia/
- [S28] TRT Bangkok (คลินิก), Wegovy Thailand — https://www.trtbangkok.com/wegovy-thailand/

**PGx ไทย**
- [S29] กรมวิทยาศาสตร์การแพทย์, การตรวจยีน HLA-B\*1502 — https://www.dmsc.moph.go.th/th/detailAll/1095/nw/25
- [S30] Implementation of HLA-B\*15:02 genotyping as standard-of-care in Thailand, Front Pharmacol 2022 — https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2022.867490/full
- [S31] Dilokthornsakul et al., Updated economic evaluation of HLA-B\*58:01 testing, ACR Open Rheumatol 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12364558/
- [S32] Hfocus, บัตรทองเพิ่มสิทธิประโยชน์ใหม่ 6 รายการ (ธ.ค. 2020) — https://www.hfocus.org/content/2020/12/20582
- [S33] Evolution of HLA-B pharmacogenomics… 10-year retrospective study in Thailand — https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/
- [S34] (ผลค้นหาอ้างถึง Rama pharmacogenetic ID card ใน [S33]) และ "A success story in pharmacogenomics: Genetic ID card for SJS/TEN", Pharmacogenomics 2016 — https://www.tandfonline.com/doi/full/10.2217/pgs-2015-0009
- [S35] PGxCard — กินอยู่ดี แพลตฟอร์ม — https://www.kydse.com/pgxcard-2/
- [S36] Pharmacogenomic landscape in Thailand: array-based profiling and EMR-linked medication exposure, PLoS One 2026 — https://pmc.ncbi.nlm.nih.gov/articles/PMC13432136/
- [S37] HDmall, ATGenes ตรวจยีนแพ้ยา >20 ชนิด — https://hdmall.co.th/health-checkup/7-dna-test-drug-allergy-related-at-genes
- [S38] GeneusDNA, ราคาตรวจ DNA 2569 — https://www.geneusdna.com/th/blog/dna-test-kit-price-thailand-2025

**ราคาต่างประเทศ / คู่แข่ง**
- [S39] GeneSight cost — https://genesight.com/cost/
- [S40] Genomind cost and coverage — https://genomind.com/cost-and-coverage/
- [S41] Labcorp OnDemand, NMR LipoProfile — https://www.ondemand.labcorp.com/lab-tests/nmr-lipoprofile-test
- [S42] MobiHealthNews, Nightingale consumer service — https://www.mobihealthnews.com/news/emea/helsinki-headquartered-nightingale-health-introduces-consumer-blood-testing-service
- [S43] Nightingale Health Check — https://nightingalehealth.com/health-check
- [S44] Nightingale × Innoquest (15 พ.ย. 2023) — https://nightingalehealth.com/news/inside-information-nightingale-health-and-innoquest-diagnostics-enter-into-collaboration-agreement-to-make-nightingale-healths-technology-accessible-in-the-southeast-asia-region/
- [S45] Nightingale Singapore laboratory — https://nightingalehealth.com/news/nightingale-health-announces-opening-of-its-singapore-laboratory/
- [S46] SelectScience, B.I.-LISA IVDr (For research only) — https://www.selectscience.net/products/bi-lisa-ivdr-lipoprotein-subclass-analysis-(for-research-only)/?prodID=220875
- [S47] Bruker B.I.-LISA — https://www.bruker.com/en/products-and-solutions/mr/nmr-clinical-research-solutions/b-i-lisa.html
- [S48] KKU Phenome Centre — https://kkuipl.wordpress.com/
- [S49] Guardant Health, cash pay price — https://guardanthealth.com/products/tests-for-patients-with-early-and-advanced-stage-cancer/
- [S50] Guardant Health Q2 earnings call highlights (Yahoo Finance) — https://finance.yahoo.com/healthcare/articles/guardant-health-q2-earnings-call-000301628.html
- [S51] MedCity News, FoundationOne Liquid launch (2018) — https://medcitynews.com/2018/09/foundation-medicine-launches-liquid-biopsy-test/
- [S52] UsagePricing, Tempus AI pricing blueprint — https://www.usagepricing.com/blueprint/tempus
- [S53] Biotech Connection Singapore, Liquid biopsy in Asia — https://www.biotechconnection-sg.org/liquid-biopsy-in-asia/
- [S54] Wolters Kluwer, UpToDate Lexidrug — https://www.wolterskluwer.com/en/solutions/uptodate/about/mobile-apps/lexidrug
- [S55] Purdue Libraries, Drug databases guide (Lexicomp PGx database) — https://guides.lib.purdue.edu/c.php?g=352750&p=2377853
- [S56] Merative Micromedex — https://www.merative.com/clinical-decision-support/micromedex
- [S57] RxGenomix Solutions — https://rxgenomix.com/solutions/
- [S58] Business Wire, Translational Software FHIR PGx API (2016) — https://www.businesswire.com/news/home/20160815005310/en/Translational-Software-Launches-FHIR-Based-Pharmacogenomics-API-Allowing
- [S59] DrFirst × Translational Software — https://drfirst.com/press-releases/translational-software-inc-drfirst-team-provide-pharmacogenomics-based-e-prescribing-medication-management
- [S60] OncoKB Licensing FAQ — https://faq.oncokb.org/licensing
- [S61] FDA, OncoKB Decision Summary — https://www.fda.gov/media/152847/download
- [S62] Roche navify Mutation Profiler — https://navify.roche.com/marketplace/products/navify-mutation-profiler
- [S63] Chulalongkorn Hospital, Excellence Center for Genomics and Precision Medicine — https://kcmh.chulalongkornhospital.go.th/en/ec/excellence-center-for-genomics-and-precision-medicine-en/

**ตรวจ claim**
- [S64] Swen et al., Lancet 2023;401:347–356 (PMID 36739136) — https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(22)01841-4/abstract
- [S65] Summary: Use of a multi-gene pharmacogenetic panel reduces adverse drug effects, Cell Rep Med 2023 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10213803
- [S66] Lancet correspondence: "The PREPARE study: benefits of pharmacogenetic testing are unclear" — https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(23)00855-3/fulltext
- [S67] Apolipoprotein B: bridging the gap between evidence and clinical practice, Circulation 2024 (สรุปคำแนะนำ ESC/EAS 2019 เรื่อง apoB) — https://pmc.ncbi.nlm.nih.gov/articles/PMC11219008/
- [S68] ESC, 2025 Focused Update of the 2019 ESC/EAS dyslipidaemia guidelines — https://www.escardio.org/guidelines/clinical-practice-guidelines/all-esc-practice-guidelines/dyslipidaemias/
- [S69] Covington, 5 key takeaways from FDA's revised CDS guidance (ม.ค. 2026) — https://www.cov.com/en/news-and-insights/insights/2026/01/5-key-takeaways-from-fdas-revised-clinical-decision-support-cds-software-guidance
- [S70] FDA CDS Software FAQs — https://www.fda.gov/medical-devices/software-medical-device-samd/clinical-decision-support-software-frequently-asked-questions-faqs
- [S71] DLA Piper, Data protection laws of the world – Thailand — https://www.dlapiperdataprotection.com/index.html?t=law&c=TH
- [S72] PDPA Thailand, Section 26 (อังกฤษ) — https://pdpathailand.com/pdpa/content_eng/article26_eng.php
- [S73] IRESSA prescribing information (DailyMed) — https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=827d60e8-7e07-41b7-c28b-49ef1c4a5a41
- [S74] TARCEVA label (FDA 2016) — https://www.accessdata.fda.gov/drugsatfda_docs/label/2016/021743s025lbl.pdf
- [S75] Drugs.com, Tarceva prescribing information — https://www.drugs.com/pro/tarceva.html
- [S76] PLAVIX label (FDA 2022) — https://www.accessdata.fda.gov/drugsatfda_docs/label/2022/020839s078lbl.pdf
- [S77] TCTMD, FDA label change fails to stem uncertainty over PPI use with clopidogrel — https://www.tctmd.com/news/fda-label-change-fails-stem-uncertainty-over-ppi-use-clopidogrel-0
- [S78] Cooper-DeHoff et al., CPIC SLCO1B1/ABCG2/CYP2C9 statin guideline, CPT 2022 — https://pmc.ncbi.nlm.nih.gov/articles/PMC9035072
- [S79] CPIC statin guideline PDF — https://files.cpicpgx.org/data/guideline/publication/statins/2022/publication.pdf
- [S80] Lee et al., CPIC CYP2C19–clopidogrel 2022 update — https://files.cpicpgx.org/data/guideline/publication/clopidogrel/2022/35034351.pdf
