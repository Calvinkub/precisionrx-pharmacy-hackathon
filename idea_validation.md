# PrecisionRx — Idea Validation (ล่าจุดตาย + คู่แข่งที่ซ่อนอยู่)

> ผู้ประเมิน: project-idea-validator (YC-style, anti-sycophancy) + วิธี teardown ของ competitive-analyst
> ประเมิน `idea.md` v2 และ `critique_PrecisionRx.md` · วันที่ 27 ก.ย. 2026
> หลักการ: ตั้งสมมติฐานว่าไอเดียมีจุดตายจนกว่าหลักฐานจะบอกว่าไม่มี · ทุก claim เรื่องคู่แข่ง/ตลาดมี URL · ข้อที่หาไม่เจอเขียนว่า "ไม่พบในการค้น" ไม่ใช่ "ไม่มี"
> ไฟล์นี้ไม่ซ้ำกับ market_research.md / business_strategy.md / business_case.md — ที่นี่เน้น **อะไรจะฆ่าไอเดียนี้**

---

## 0. สรุป 30 วินาที

**คำตัดสิน**
- **Hackathon: PIVOT (แล้ว GO)** — v2 แก้ปัญหาวิทยาศาสตร์ที่กรรมการชุดแรกติไว้ได้ดีจริง แต่ยังขาย "3 omics" ซึ่งกรรมการเภสัชที่รู้จักระบบไทยจะถามว่า "คนไข้ไทยคนไหนมีผลครบ 3 อย่าง" และ "ต่างจาก ผูกพันธุ์ ของกรมวิทย์ฯ ยังไง" ถ้าไม่เตรียมคำตอบ คะแนนนวัตกรรมและธุรกิจจะร่วง
- **Venture จริง: NO-GO ในรูปแบบปัจจุบัน** — ส่วนที่มีหลักฐานแข็ง (PGx CDS) เป็นของที่คนอื่นทำอยู่แล้ว หรือทำได้ฟรี ส่วนที่แปลกใหม่ (NMR response tracking) ไม่มี lab คลินิกในไทยรองรับให้เห็น และถูกแทนได้ด้วย ApoB ราคาถูก ส่วน cfDNA เป็นตลาดคนละกลุ่มที่มีเจ้าตลาดอยู่แล้ว **มีทางรอดแบบมีเงื่อนไข** ถ้าย่อเหลือ PGx-at-prescribing ที่ต่อกับโครงสร้างพื้นฐานของรัฐ (ดูข้อ 8)

**จุดตาย 3 ข้อแรก**
1. **กลุ่มคนไข้ที่มีข้อมูลครบแทบไม่มีอยู่จริง** — ในไทยการตรวจ PGx ส่วนใหญ่เป็นแบบ reactive ยีนเดียว (HLA-B) ไม่ใช่ panel ค้นหาไม่พบ lab คลินิกที่ให้บริการ NMR lipoprotein แบบซ้ำหลายครั้ง และคนไข้มะเร็งที่มี ctDNA ก็แทบไม่มี PGx panel ล่วงหน้า
2. **จุดส่งมอบผิดที่** — PGx มีคุณค่าตอนสั่งยาหรือจ่ายยาใน HIS แต่ PrecisionRx เป็นหน้าจอเภสัชกรแยกต่างหาก ขณะที่รัฐกำลังสร้างชั้นกลางนี้เอง (ผูกพันธุ์ เชื่อม 11 รพ.) และเครื่องยนต์ CPIC มีของฟรีอยู่แล้ว (PharmCAT)
3. **ดีมานด์ฝั่งผู้ใช้ยังต่ำมาก** — เภสัชกรโรงพยาบาลไทยเพียง 7% เคยแนะนำหรือแปลผล PGx ในรอบปี และ alert CYP2C19–clopidogrel ในโรงพยาบาลที่มีระบบครบแล้วมีอัตรายอมรับต่ำสุด (บางงานต่ำถึง 22%)

**การเปลี่ยนที่คมที่สุดเพียงข้อเดียว**: ตัดเหลือ **omics เดียว (germline PGx)** และย้ายจุดส่งมอบจาก "หน้าจอเภสัชกรแยก" ไปเป็น **CDS ตอนสั่งยาหรือจ่ายยาใน HIS** (HOSxP ผ่าน FHIR/CDS Hooks) โดยรับผล PGx จากแพลตฟอร์ม ผูกพันธุ์ หรือจาก lab ส่วน NMR ถอยไปเป็น "ApoB discordance + RCV จาก lab ปกติ" และย้าย cfDNA ไปไว้ใน roadmap

---

## 1. ทวนไอเดีย (ตามที่ทีมเสนอ)

| ด้าน | สิ่งที่ idea.md v2 อ้าง |
|---|---|
| ปัญหา | ยาไม่เหมาะกับพันธุกรรม, ไม่รู้ว่ายาได้ผลจริงไหม, แยก non-adherence ไม่ได้, alert fatigue, ผล molecular มะเร็งกระจัดกระจาย |
| ผู้ใช้ | เภสัชกรคลินิก cardiometabolic + เภสัชกรมะเร็ง |
| ผู้จ่าย | รพ.เอกชนที่มี preventive/lipid clinic, ศูนย์มะเร็ง / lab liquid biopsy |
| ความได้เปรียบที่อ้าง | รวม 3 omics + RCV + adherence + evidence store ที่ version ได้ + บริบทไทย (TMT, allele frequency) |
| รายได้ | SaaS ต่อโรงพยาบาล (Module A) + ค่าบริการต่อรายงาน แบ่งรายได้กับ lab (Module B) |

**ให้เครดิตตามจริงก่อน** (สิ่งที่ผ่านการตรวจแล้ว):
- ใช้ deterministic engine + LLM แค่สรุป + verifier เป็นสถาปัตยกรรมที่ถูกต้องและพิสูจน์ได้ ดีกว่าทีม hackathon ส่วนใหญ่
- RCV และการแยก adherence (PDC) ก่อนสรุปว่ายาไม่ได้ผล เป็นความรู้ lab medicine และเภสัชกรรมจริง กรรมการจะให้คะแนน
- ช่องว่างที่อ้างไว้มีอยู่จริง (อย่างน้อยในปี 2022): งานของรามาธิบดีเขียนตรง ๆ ว่า *"there is currently no PGx alert system connected with the electronic health records (EHR) in Thailand"* และยกเคสผู้ป่วยเสียชีวิตเพราะข้อมูลไม่เชื่อมกัน — [Frontiers/PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/)
- Why-now มีจริง: สิทธิบัตรทองผ่านศูนย์จีโนมรามาฯ ครอบคลุม "การตรวจเลือกยา เช่น HLA-B\*15:02, CYP2C19, CYP2C9" — [Hfocus ก.ค. 2026](https://www.hfocus.org/content/2026/07/38689)

---

## 2. สมมติฐานจุดตาย (เรียงจากร้ายแรงที่สุด)

### FF1 — "Empty intersection": คนไข้ที่มีข้อมูลครบทั้ง 3 ชนิดแทบไม่มีในไทย ⚠️ ร้ายแรงสูงสุด

**สมมติฐาน**: คุณค่าที่ขายคือ "รวม 3 แหล่งเป็นหน้าเดียว" แต่ถ้าแทบไม่มีคนไข้ที่มีข้อมูลเกิน 1 แหล่ง ผลิตภัณฑ์จริงในวันแรกก็คือ PGx CDS ธรรมดา ซึ่งเป็นตลาดที่มีคนทำอยู่แล้ว

**หลักฐาน**
- PGx ในไทยส่วนใหญ่เป็นยีนเดียวแบบ reactive: ที่รามาธิบดี HLA-B คิดเป็น **63% ของงาน PGx ทั้งหมด** มีการตรวจ HLA-B 13,985 รายในช่วง 2011–2020 โดยใช้กับ allopurinol 38%, carbamazepine 33% และ abacavir 26% — [PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/) คนไข้เหล่านี้ไม่มี CYP2C19/SLCO1B1 panel ซึ่งเป็นแกนของ Demo A และ B
- **NMR**: ค้นหาทั้งภาษาไทยและอังกฤษแล้ว **ไม่พบ lab คลินิกในไทยที่ให้บริการ NMR lipoprotein (LDL-P) เป็นบริการตรวจรักษา** ผลลัพธ์ที่เจอเป็นของสหรัฐฯ ทั้งหมด เช่น Labcorp และ Mayo งาน NMR ที่พบในไทยเป็นงานวิจัย เช่น [PMC11940625](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11940625/) และแพลตฟอร์ม Bruker B.I.LISA ยังถูกขายเป็น "(For research only)" ในบางช่องทาง — [SelectScience](https://www.selectscience.net/products/bi-lisa-ivdr-lipoprotein-subclass-analysis-(for-research-only)/?prodID=220875) **นี่ขัดกับหลักของ idea.md เองที่ว่า "รับเฉพาะผลจาก lab ISO 15189"** (ต้องยืนยันด้วยการโทรถาม lab จริง แต่ถ้าไม่มี Module A ก็ไม่มี input)
- งานของศิริราช (n=4,662, 2026) พบว่า 96% มี genotype ที่ actionable แต่มีเพียง **32.6% ที่เคยได้รับยาในกลุ่มที่ศึกษาในรอบ 10 ปี** และผู้เขียนพูดถึง CDS เป็นงาน "near-term prioritization" ไม่ใช่ของที่ใช้อยู่ — [PLOS One / PMC13432136](https://pmc.ncbi.nlm.nih.gov/articles/PMC13432136/)
- **cfDNA**: คนไข้มะเร็งปอดที่ตรวจ ctDNA ได้ผลเป็นรายงานจาก lab (Guardant, Gene Solutions ฯลฯ) ค้นแล้ว **ไม่พบ** หลักฐานว่ามีการตรวจ PGx panel ล่วงหน้าในกลุ่มนี้ในไทย

**ผลต่อไอเดีย**: เคส B (PGx + NMR + RCV) และเคส D (ctDNA + DPYD + DDI) ที่ใช้เป็นเคสเด่นบนเวที เป็นเคสที่แทบไม่เกิดในโลกจริงของไทยตอนนี้

### FF2 — ส่งมอบผิดจุด และเจอคู่แข่งที่มองไม่เห็น (รัฐ + HIS + ของฟรี)

**สมมติฐาน**: คุณค่าของ PGx เกิดตอนที่ order ถูกสร้างใน HIS ถ้าผลิตภัณฑ์เป็นหน้าจอ review แยก เภสัชกรจะไม่เปิด และผู้เล่นที่คุม HIS หรือข้อมูลอยู่แล้วจะยึดชั้นนี้ไป

**หลักฐาน**
- **ผูกพันธุ์** (กรมวิทยาศาสตร์การแพทย์ + มหิดล): แอปที่เก็บผลยีนแพ้ยาตลอดชีวิต (HLA-B\*58:01, HLA-B\*15:02, HLA-B\*57:01, NAT2) ยืนยันตัวตนด้วย ThaiD เชื่อม 11 โรงพยาบาล ให้แพทย์และเภสัชกรเข้าดูได้เมื่อได้รับ consent และตั้งแผนจะเชื่อมกับ HIS — [Thai PBS](https://www.thaipbs.or.th/news/content/337301) · [Hfocus ก.พ. 2024](https://www.hfocus.org/content/2024/02/29811) **นี่คือ incumbent ของรัฐในชั้นข้อมูล PGx ที่ idea.md ไม่ได้พูดถึงเลย**
- เครื่องยนต์ genotype → phenotype → CPIC/DPWG มี **ของฟรี open-source** แล้ว คือ PharmCAT ของ PharmGKB/ClinPGx — [GitHub](https://github.com/pharmgkb/pharmcat) · [PharmCAT methods](https://pharmcat.clinpgx.org/methods/) ดังนั้น "PGx engine" ไม่ใช่ moat
- Epic Genomics Module มี Genomic Indicators ที่ลิงก์ไป CPIC และทำให้ CDS alert ยิงตาม genotype — [Frontiers 2024](https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2024.1458095/full) · [CPT tutorial 2025](https://ascpt.onlinelibrary.wiley.com/doi/abs/10.1002/cpt.3599) ระบบเดียวทำ 195 alerts ครอบคลุม 51 ยา — [JACCP 2024](https://accpjournals.onlinelibrary.wiley.com/doi/10.1002/jac5.1996) โรงพยาบาลเอกชนไทยที่ใช้ EHR ระดับนี้ได้ PGx CDS มาจาก vendor อยู่แล้ว
- Medi-Span ใส่ PGx ในการ screen contraindication และ Lexidrug มีฐานข้อมูล PGx มาตั้งแต่ 2003 — [Wolters Kluwer](https://www.wolterskluwer.com/en/solutions/uptodate/enterprise/lexidrug-content-sets-and-tools) · [Medi-Span](https://www.wolterskluwer.com/en/solutions/medi-span/medi-span) ดังนั้น "DDI checker ไม่มี PGx" ในตารางคู่แข่งของ idea.md **ไม่จริง**
- ไต้หวันพิสูจน์แล้วว่าคุณค่าอยู่ที่ CPOE: การเตือน HLA-B\*15:02 ในระบบสั่งยาเพิ่มอัตราการตรวจจาก 23.7% เป็น 55.6% — [PMC12386126](https://pmc.ncbi.nlm.nih.gov/articles/PMC12386126/)

### FF3 — ดีมานด์ฝั่งผู้ใช้ต่ำ และหมอไม่ทำตาม flag ที่เป็นเคสเด่น

**หลักฐาน**
- สำรวจเภสัชกรโรงพยาบาลไทย 21 แห่ง (n=123, response rate 20.5%): **มีเพียง 7% ที่เคยแนะนำหรือแปลผล PGx ในรอบปีที่ผ่านมา** 46.3% มีคะแนนความรู้ PGx ต่ำ และมีความกังวลเรื่องการเบิกจ่าย ความเป็นส่วนตัว และการเลือกปฏิบัติ — [PubMed 32187156](https://pubmed.ncbi.nlm.nih.gov/32187156/)
- แม้ในระบบที่มี PGx CDS ครบแล้ว อัตรายอมรับ alert เฉลี่ยประมาณ 63% และ **CYP2C19–clopidogrel ต่ำสุดใน 6 คู่ยีน-ยา** บางงานต่ำถึง 22% นอกจากนี้การกดยอมรับ alert กับการเปลี่ยนการรักษาจริงตรงกันเพียง 47% — [PMC10726431](https://pmc.ncbi.nlm.nih.gov/articles/PMC10726431/) **เคส A ที่ทีมใช้เป็นหน้าเปิด คือคู่ที่หมอ override มากที่สุด**
- มาเลเซียก็รายงานว่าอุปสรรคอันดับหนึ่งคือบุคลากรขาดความรู้ PGx — [PMC11551526](https://pmc.ncbi.nlm.nih.gov/articles/PMC11551526/)
- ข้อสังเกต (ต้องตรวจสอบกับ guideline): ในผู้ป่วย ACS แนวปฏิบัติปัจจุบันมักเลือก ticagrelor/prasugrel เป็นหลักอยู่แล้ว ทำให้ช่องที่ CYP2C19 จะเปลี่ยนการตัดสินใจแคบลงเหลือกลุ่มที่จำเป็นต้องใช้ clopidogrel

### FF4 — NMR response tracking ถูกแทนด้วยของถูกกว่า และไม่มี action ที่ guideline รองรับ

- ปัญหา "LDL-C ถึงเป้า แต่อนุภาคยังสูง" ตอบได้ด้วย **ApoB immunoassay** ซึ่งถูกกว่าและมีในแทบทุก lab ขณะที่ LDL-P จาก NMR ส่วนใหญ่มีจาก Labcorp รายเดียว — [สรุปเปรียบเทียบ](https://precisionhealthreports.com/ldl-p-vs-apob) (แหล่งรอง ต้องอ้าง NLA/ESC ต้นฉบับในสไลด์) · ApoB กับ NMR LDL-P สัมพันธ์กันแบบเส้นตรง แต่ผลไม่เทียบเท่ากันและยังไม่ standardize — [PubMed 30087138](https://pubmed.ncbi.nlm.nih.gov/30087138/) · [JAHA](https://www.ahajournals.org/doi/10.1161/JAHA.123.030405)
- Labcorp ขาย NMR LDL-P เพื่อ "adjudicate response to treatment" มาหลายปีแล้ว — [Labcorp LDL-P](https://www.labcorp.com/tests/123828/ldl-p) **ดังนั้น "NMR ติดตามการตอบสนองต่อ statin" ไม่ใช่ของใหม่** ที่ใหม่มีแค่ RCV กับ PGx ที่วางคู่กัน
- Nightingale ขยับเข้าพื้นที่ติดตาม metabolic health ระหว่างใช้ GLP-1 แล้ว (กับ Supernormal ในฟินแลนด์) — [Inderes](https://www.inderes.fi/en/releases/nightingale-health-and-supernormal-partner-to-bring-at-home-blood-testing-to-medical-weight-loss-in-finland) ซึ่งหักล้างเคส C บางส่วน
- RCV ต้องใช้ค่า CVi ต่อ analyte ผมคาดว่าค่า CVi ของ NMR subclass (LDL-P, small LDL-P, GlycA) มีข้อมูลใน EFLM น้อยหรือไม่มี (**ต้องตรวจสอบกับ EFLM BV database**) ถ้าไม่มี RCV ของ Module A ก็คำนวณได้แค่กับ ApoB/lipid ทั่วไป ซึ่งกลับไปสนับสนุนข้อสรุปว่าไม่ต้องใช้ NMR

### FF5 — Oncology/cfDNA เป็นตลาดคนละกลุ่มที่มีเจ้าตลาดแล้ว

- การแปลผลและจัด tier variant ทำโดยซอฟต์แวร์ของ lab หรือ vendor: QCI Interpret (รองรับ liquid biopsy และ AMP/ASCO/CAP) — [QIAGEN](https://digitalinsights.qiagen.com/products-overview/clinical-insights-portfolio/qiagen-clinical-insight__trashed/qci-interpret-one/) · navify Mutation Profiler + Tumor Board ของ Roche — [Roche](https://navify.roche.com/marketplace/products/navify-mutation-profiler)
- Gene Solutions (K-TRACK, SPOT-MAS) ทำงานกับโรงพยาบาลและคลินิกกว่า 4,500 แห่งใน SEA รวมถึงไทย และมีแพลตฟอร์มผู้ใช้ของตัวเองชื่อ K-CONNECT — [Gene Solutions](https://genesolutions.com/our-test/k-track) · [K-CONNECT](https://kconnect.genesolutions.com/experience-mrd/) · Guardant มี AMEA และ Guardant360 Response สำหรับติดตามผล — [Guardant AMEA](https://www.guardanthealthamea.com/products/tests-for-patients-with-early-and-advanced-stage-cancer/) · [Guardant360 Response](https://www.guardantcomplete.com/hcp/solutions/guardant360-response/)
- ข้อความ "TKI + PPI ลดการดูดซึม" มีอยู่ใน DDI checker ทุกตัว ไม่ได้สร้างความต่าง
- ผู้ซื้อ (ศูนย์มะเร็ง / lab), ผู้ใช้ (oncologist + เภสัชกรมะเร็ง), consent และหลอดเก็บตัวอย่าง **แยกจาก Module A ทั้งหมด** สุดท้ายคือสอง startup ในสไลด์เดียว

### FF6 — Regulatory และ liability (ร้ายแรงรอง ไม่ใช่ตัวฆ่าใน hackathon)

- ตัวอย่าง: Nalagenetics ต้องได้ **CE mark** สำหรับซอฟต์แวร์ PGx CDS ก่อนขาย และใช้เป็นใบเบิกทางขอ approval ใน SEA — [PR Newswire](https://en.prnasia.com/releases/apac/nalagenetics-obtains-ce-mark-for-its-pharmacogenomics-software-nala-clinical-decision-support-module-pgx-core-363414.shtml) แปลว่าคู่แข่งในภูมิภาคถือซอฟต์แวร์นี้เป็นเครื่องมือแพทย์ PrecisionRx ที่มี 3 engine ก็เท่ากับต้องขออนุญาตสามเท่า
- PDPA: consent แยกสามชุด (idea.md ข้อ 11 เขียนไว้เอง) ทำให้ onboarding ยากขึ้นสามเท่า

---

## 3. Competitor teardown

| # | ชื่อ | ทำอะไร | ภูมิภาค | ทับซ้อนกับ PrecisionRx | URL |
|---|---|---|---|---|---|
| 1 | **ผูกพันธุ์** (กรมวิทย์ฯ + มหิดล) | แอปเก็บผลยีนแพ้ยาตลอดชีวิต, ThaiD, เชื่อม 11 รพ., แพทย์/เภสัชเข้าดูได้เมื่อได้ consent | ไทย | **สูง** — ชั้นข้อมูล PGx ระดับชาติ ฟรี มีรัฐหนุน | [Thai PBS](https://www.thaipbs.or.th/news/content/337301) |
| 2 | PPM Ramathibodi / ศูนย์จีโนมรามาฯ | Lab PGx (HLA-B, CYP450), PGx card, สิทธิบัตรทองสำหรับ HLA-B/CYP2C19/CYP2C9 | ไทย | สูง — เป็นทั้งแหล่งข้อมูลและผู้ที่น่าจะสร้าง CDS เอง | [PPM RAMA](http://ppmrama.com/the-pharmaceutical-laboratory-of-genetics/cyp450-profile-genotyping/) · [Hfocus 2026](https://www.hfocus.org/content/2026/07/38689) |
| 3 | Bangkok Hospital (BDMS) Drug-Gene Profile | PGx แบบ NGS ครอบคลุมยาหลายกลุ่ม ขายเป็นแพ็กเกจ precision medicine | ไทย | กลาง — รพ.เอกชนที่เป็น beachhead ของทีมมีบริการของตัวเองแล้ว | [Bangkok Hospital](https://www.bangkokhospital.com/en/content/pharmacogenomics) |
| 4 | BMS-HOSxP | HIS ที่ใช้มากในโรงพยาบาลรัฐ มี alert แพ้ยาที่เภสัชกรต้องกดรับทราบ | ไทย | สูง (ในฐานะช่องทาง/ผู้คุมประตู) — ถ้า HOSxP เพิ่ม PGx field ก็จบ | [HOSxP ระบบเภสัชกรรม](https://hosxp.net/wordpress/?page_id=6631) |
| 5 | **Nalagenetics** | PGx CDS (CE-marked) + qPCR kit, 170 drug-gene reports, ใช้ใน Singapore IMPT | SG/ID/SEA | **สูง** — คู่แข่งตรงที่สุดในภูมิภาค บอกชัดว่าจะขยายใน SEA | [CE mark PR](https://en.prnasia.com/releases/apac/nalagenetics-obtains-ce-mark-for-its-pharmacogenomics-software-nala-clinical-decision-support-module-pgx-core-363414.shtml) · [IMPT study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11903297/) |
| 6 | Singapore PRECISE / NUHS PPGx | Pre-emptive PGx ในคลินิก วัด barrier ของ clinician (95% มี variant actionable; 21.2% ของผู้ใช้ยาได้คำแนะนำ) | สิงคโปร์ | กลาง — เป็นต้นแบบระดับรัฐที่ไทยน่าจะลอก | [NUHS PPGx](https://www.nuhs.edu.sg/research/research-facilities/centre-for-precision-health/pre-emptive-pharmacogenomics-ppgx) |
| 7 | Epic Genomics Module | Genomic Indicators + CDS alert ตาม CPIC ใน EHR | Global | สูงใน รพ.ที่ใช้ Epic | [Frontiers](https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2024.1458095/full) |
| 8 | Oracle Health (Cerner) | Genomics/Variant API บน FHIR Genetic Observation | Global | กลาง | [Oracle Genomics API](https://docs.healtheintent.com/api/v1/genomics) |
| 9 | Wolters Kluwer (Lexidrug, Medi-Span) | DDI + PGx content + PGx contraindication screening | Global (มีใช้ในไทย) | **สูง** — หักล้างข้อที่อ้างว่า "DDI checker ไม่มี PGx" | [Lexidrug](https://www.wolterskluwer.com/en/solutions/uptodate/enterprise/lexidrug-content-sets-and-tools) · [Medi-Span](https://www.wolterskluwer.com/en/solutions/medi-span/medi-span) |
| 10 | Translational Software PGxAPI | PGx knowledge base + API บน FHIR สำหรับ EHR/ระบบร้านยา | US | สูง (B2B engine) | [PGxAPI](https://www.translationalsoftware.com/pgxapi) |
| 11 | PharmCAT (PharmGKB/ClinPGx) | Open-source VCF → diplotype → CPIC/DPWG report | Global ฟรี | สูง — ทำให้ PGx engine กลายเป็นของฟรี | [GitHub](https://github.com/pharmgkb/pharmcat) |
| 12 | Tabula Rasa **MedWise** | Risk score ที่ดูยาทั้งหมดพร้อมกัน **รวม PGx + PK/PD + DDI** สำหรับเภสัชกร | US | **สูงในเชิงแนวคิด** — "PGx + DDI + pharmacist workflow" ถูกทำเป็นสินค้าแล้ว | [MobiHealthNews](https://www.mobihealthnews.com/news/tabula-rasa-healthcare-launches-medwise-prevent-adverse-drug-events) · [Pgx profile](https://www.tandfonline.com/doi/full/10.2217/pgs-2021-0085) |
| 13 | Genomind / GeneSight (Myriad) | รายงาน PGx รวม gene-drug, drug-drug, drug-drug-gene + consult | US | กลาง (เน้นจิตเวช) | [Genomind](https://genomind.com/solutions/pharmacogenetic-testing/) |
| 14 | Labcorp NMR LipoProfile | NMR LDL-P เพื่อ "adjudicate response to treatment" ใน statin-treated | US | กลาง — ทำ NMR response monitoring อยู่แล้ว | [Labcorp](https://www.labcorp.com/tests/123828/ldl-p) |
| 15 | Nightingale Health | NMR panel, ติดตาม metabolic health ระหว่างใช้ GLP-1 (Supernormal) | EU/US | กลาง | [Inderes](https://www.inderes.fi/en/releases/nightingale-health-and-supernormal-partner-to-bring-at-home-blood-testing-to-medical-weight-loss-in-finland) |
| 16 | QIAGEN QCI Interpret | Oncology variant interpretation รองรับ liquid biopsy, AMP/ASCO/CAP | Global | สูงต่อ Module B | [QIAGEN](https://digitalinsights.qiagen.com/products-overview/clinical-insights-portfolio/qiagen-clinical-insight__trashed/qci-interpret-one/) |
| 17 | Roche navify Mutation Profiler / Tumor Board | NGS reporting + tumor board + CDS apps | Global | สูงต่อ Module B | [Roche](https://navify.roche.com/marketplace/products/navify-mutation-profiler) |
| 18 | Gene Solutions (K-TRACK / K-CONNECT) | ctDNA profiling/MRD + portal ของตัวเอง, >4,500 รพ.ใน SEA รวมไทย | SEA | สูงต่อ Module B | [K-TRACK](https://genesolutions.com/our-test/k-track) |
| 19 | Guardant Health AMEA | Guardant360 CDx / Response พร้อมรายงาน therapy matching | Global/AMEA | สูงต่อ Module B | [Guardant AMEA](https://www.guardanthealthamea.com/products/tests-for-patients-with-early-and-advanced-stage-cancer/) |

**ช่องว่างที่เหลือจริงหลัง teardown** (ให้เครดิต):
- ค้นแล้ว **ไม่พบ** บริษัทที่รวม germline PGx + metabolomic response + RCV เป็นหน้าเดียวสำหรับเภสัชกร การค้นหา "pharmacometabolomics company" ได้แค่งานวิชาการ — [PMC4976774](https://pmc.ncbi.nlm.nih.gov/articles/PMC4976774/) แต่ **ช่องว่างนี้อาจว่างเพราะยังไม่มีดีมานด์หรือ input** (ดู FF1, FF4) ไม่ใช่เพราะไม่มีใครคิด
- ในไทย **ยังไม่พบ PGx CDS เชิงพาณิชย์ที่ต่อ HOSxP** (ผูกพันธุ์เป็นแอปดูผล ยังไม่ใช่ CDS ตอนสั่งยา) นี่คือช่องที่มีอยู่จริงที่สุด

---

## 4. หลักฐานดีมานด์

| สัญญาณ | ทิศทาง | แหล่ง |
|---|---|---|
| การตรวจ HLA-B ที่รามาฯ เพิ่มจาก 94 ครั้ง (2011) เป็น 2,880 ครั้ง (2020) หรือราว 30 เท่า โดยมีนโยบาย/การเบิกจ่ายเป็นตัวขับ (UCS จ่ายราว 28 USD/ราย) | บวก (แต่เป็นยีนเดียว reactive) | [PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/) |
| บัตรทองผ่านศูนย์จีโนมรามาฯ ครอบคลุม HLA-B\*15:02, CYP2C19, CYP2C9 | บวก — ปริมาณผล CYP2C19 กำลังจะเพิ่ม | [Hfocus 2026](https://www.hfocus.org/content/2026/07/38689) |
| ผูกพันธุ์: คนไทยราว 9.7 ล้านคนมียีนแพ้ยา, เชื่อม 11 รพ. | บวกต่อปัญหา / ลบต่อ PrecisionRx (รัฐทำเอง) | [Thai PBS](https://www.thaipbs.or.th/news/content/337301) |
| ศิริราช: 55% ของผู้ใช้ omeprazole และราว 22–23% ของผู้ใช้ statin มี phenotype ที่ actionable | บวก — CYP2C19–PPI และ SLCO1B1–statin คือ high-yield จริง | [PMC13432136](https://pmc.ncbi.nlm.nih.gov/articles/PMC13432136/) |
| เภสัชกรโรงพยาบาลเพียง 7% เคยแปลผล PGx ในรอบปี | **ลบ** — ผู้ใช้ปลายทางยังไม่มีพฤติกรรมนี้ | [PubMed 32187156](https://pubmed.ncbi.nlm.nih.gov/32187156/) |
| ไม่พบ lab คลินิก NMR lipoprotein ในไทย | **ลบ** ต่อ Module A (ต้องยืนยัน) | ค้นแล้วไม่พบ (ดู FF1) |
| สิทธิบัตรทอง 2569 ครอบคลุม gefitinib ที่ผลิตในไทย และตรวจ EGFR | กลาง — ใช้การตรวจชิ้นเนื้อเป็นหลัก ไม่พบว่าเบิก liquid biopsy ได้ | [Thai PBS Policy Watch](https://policywatch.thaipbs.or.th/article/life-337) |

**ข้อสรุปเรื่องดีมานด์**: ดีมานด์ที่มีหลักฐานเป็น **"PGx ยีนไม่กี่ตัวที่รัฐจ่ายเงินให้ ต้องไปโผล่ตอนสั่งยา"** ไม่ใช่ "multi-omics medication review" ยังไม่มีหลักฐานเชิงปริมาณเลย (search volume, LOI, หรือการสัมภาษณ์เภสัชกร) ที่แสดงว่าเภสัชกรไทยอยากได้หน้าจอ review แยกอีกหน้า **สิ่งที่ต้องทำก่อนพิตช์**: สัมภาษณ์เภสัชกรโรงพยาบาล 5–10 คน (ทั้งรัฐที่ใช้ HOSxP และเอกชน) แล้วถามว่า "ผล CYP2C19 ของคนไข้อยู่ที่ไหนตอนคุณจ่าย clopidogrel"

---

## 5. อุปสรรคการ adoption

| อุปสรรค | หลักฐาน | ผลต่อ PrecisionRx |
|---|---|---|
| **ต้นทุนและการเบิกจ่าย** | เภสัชกรกังวลเรื่อง reimbursement [PubMed 32187156](https://pubmed.ncbi.nlm.nih.gov/32187156/); การเบิกจ่ายครอบคลุมเฉพาะยีนที่กำหนด | panel ครบ + NMR ซ้ำ + ctDNA = ต้นทุนต่อคนสูงมาก ผู้ป่วยบัตรทองจ่ายไม่ได้ ตลาดจึงเหลือแค่เอกชน |
| **ความรู้และเวลาของเภสัชกร** | 46.3% ความรู้ต่ำ; 7% เคยทำ [PubMed 32187156](https://pubmed.ncbi.nlm.nih.gov/32187156/); มาเลเซียพบแบบเดียวกัน [PMC11551526](https://pmc.ncbi.nlm.nih.gov/articles/PMC11551526/) | หน้าจอที่รวม 3 omics เพิ่มภาระการเรียนรู้ ไม่ได้ลด |
| **การยอมรับของแพทย์** | acceptance เฉลี่ยราว 63%; clopidogrel ต่ำสุด; alert ≠ การกระทำจริง (47%) [PMC10726431](https://pmc.ncbi.nlm.nih.gov/articles/PMC10726431/) | เภสัชกร "เสนอ" แต่หมอไม่เปลี่ยน ทำให้ ROI ที่โรงพยาบาลเห็นต่ำ |
| **Integration** | Thai PGx ยังไม่ต่อ EHR (2022) [PMC9016335](https://pmc.ncbi.nlm.nih.gov/articles/PMC9016335/); CDS ต้องอยู่ใน workflow [PMC9291515](https://pmc.ncbi.nlm.nih.gov/articles/PMC9291515/) | ถ้าไม่ฝังใน HIS จะไม่ถูกใช้ ต้องได้ความร่วมมือจาก vendor HIS |
| **Privacy / discrimination** | กังวลเรื่องการเลือกปฏิบัติ [PubMed 32187156](https://pubmed.ncbi.nlm.nih.gov/32187156/) | consent 3 ชุด ข้อมูลอ่อนไหว 3 ชนิด |

### การรวม 3 omics เป็นจุดแข็งหรือจุดอ่อนด้าน distribution?

**จุดอ่อน ในทุกมิติที่ตรวจ ยกเว้นมิติเดียว**

| มิติ | 1 omics (PGx) | 3 omics |
|---|---|---|
| Lab partner | 1 (หรือรับจากผูกพันธุ์) | 3 ราย และ NMR อาจไม่มี lab คลินิกในไทย |
| Consent / หลอดเลือด | 1 / 1 | 3 / 2–3 หลอด (idea.md ข้อ 4.5 ยอมรับเอง) |
| ผู้ซื้อ | ฝ่ายเภสัชกรรม รพ. | ฝ่ายเภสัช + lipid clinic + ศูนย์มะเร็ง (3 budget holders) |
| ผู้ใช้ | เภสัชกรทุกคนที่จ่ายยา | เภสัชกร cardiometabolic + เภสัชกรมะเร็ง (สองกลุ่มที่ไม่ค่อยเจอกัน) |
| ภาระ อย. | 1 intended use | 3 engine และหลายรายการในระดับความเสี่ยงต่างกัน |
| ความถี่การใช้ | ทุกครั้งที่สั่งยาใหม่ (ตรวจครั้งเดียว ใช้ตลอดชีวิต) | NMR ทุก 3–6 เดือนในกลุ่มเล็ก, ctDNA เป็นช่วง ๆ |

**มิติเดียวที่การรวมมีเหตุผลจริง**: ภายใน oncology (germline DPYD/UGT1A1 + ctDNA + DDI ของ TKI) คนไข้คนเดียวกันต้องใช้ทั้งสองอย่างจริง แต่คู่ PGx + NMR ใน cardiometabolic เป็นการ **วางคู่กัน** ไม่ใช่การ **รวมที่ทำให้เกิด decision ใหม่** เพราะ SLCO1B1 บอกเรื่อง myopathy ส่วน ApoB บอกเรื่อง efficacy สองอย่างนี้ไม่ได้ขยายความหมายของกันและกัน

---

## 6. ความยากทางเทคนิค (สั้น ๆ)

| ส่วน | Hackathon | Production |
|---|---|---|
| PGx engine | ง่าย (PharmCAT/CPIC tables) | ง่าย — จึงไม่ใช่ moat |
| DDI engine | กลาง (ต้องมี license ฐานข้อมูล) | **แพง** — license Lexidrug/Medi-Span หรือสร้างเอง |
| RCV engine | ง่าย | ติดที่ CVi ของ NMR analyte (ต้องตรวจสอบ) |
| cfDNA tiering | กลาง | **ยากและแพง** — OncoKB มีเงื่อนไข license เชิงพาณิชย์ และต้องแข่งกับ QCI/navify |
| HIS integration | ข้าม (mock) | **ยากที่สุด และเป็นตัวตัดสินจริง** |
| LLM + verifier | กลาง | กลาง |

---

## 7. คำตัดสิน

### Hackathon — **PIVOT → GO**
- v2 ผ่านกรรมการวิทยาศาสตร์และ tech ได้แล้ว (RCV, deterministic engine, claim discipline)
- ความเสี่ยงบนเวที: (1) "ผูกพันธุ์ทำอยู่แล้วไหม" (2) "คนไข้คนไหนมี NMR คลินิกในไทย" (3) "clopidogrel alert หมอ override เยอะที่สุดนะ" (4) "ทำไมไม่ใช้ ApoB"
- **ทำได้ภายในเวลาที่มี**: ให้ PGx-at-prescribing เป็นพระเอก แล้ววาง "ต่อกับผูกพันธุ์/HOSxP ผ่าน FHIR" ไว้บนสไลด์สถาปัตยกรรม ให้ NMR/RCV เป็น "Response module (ApoB ก่อน, NMR เมื่อมี lab)" และย้าย cfDNA ไปไว้ในสไลด์ roadmap หรือ Q&A ไม่ต้องเป็น demo หลัก เปลี่ยนเคสเปิดจาก clopidogrel เป็น **CYP2C19–PPI** (high-yield ที่สุดตามข้อมูลศิริราช) หรือ **HLA-B ที่เป็น hard stop** ซึ่งมีการเบิกจ่ายและมีหลักฐานเรื่องการเสียชีวิต

### Venture จริง — **NO-GO ในรูปแบบปัจจุบัน / CONDITIONAL PIVOT**
- รูปแบบ 3 omics: no-go เพราะ FF1 + FF2 + FF5 รวมกันแปลว่าไม่มี input ไม่มีช่องทาง และมีเจ้าตลาดในทุกโมดูล
- ทางเลือกที่ยังมีชีวิต: **"PGx CDS connector สำหรับโรงพยาบาลรัฐที่ใช้ HOSxP"** ซึ่งรับผลจากผูกพันธุ์หรือ lab แล้วยิง alert ตอนสั่งหรือจ่ายยาสำหรับยีนที่บัตรทองจ่าย ผู้ซื้ออาจเป็น สปสช./กรมวิทย์ฯ (ในรูปทุนหรือ procurement) หรือ vendor HIS (license)
  - **ความเสี่ยงหลักของทางนี้**: รัฐหรือ vendor HIS สร้างเอง และ Nalagenetics เข้าตลาดไทย
  - **Kill criterion**: ถ้าภายใน 3 เดือนไม่ได้ LOI จาก รพ. 1 แห่ง + ความร่วมมือจาก BMS-HOSxP หรือทีมผูกพันธุ์ ให้หยุด

---

## 8. การเปลี่ยนที่คมที่สุดเพียงข้อเดียว

> **ตัดจาก "3-omics medication review หน้าจอแยก" ให้เหลือ "germline PGx ที่ไปโผล่ในจังหวะสั่งยาหรือจ่ายยาใน HIS ไทย" โดยต่อกับผูกพันธุ์และ HOSxP แทนการแข่งกับทั้งสอง**

เหตุผลที่ข้อนี้ขยับโอกาสได้มากที่สุด:
1. แก้ FF1 เพราะ input มีอยู่จริงและกำลังเพิ่มจากการเบิกจ่ายของบัตรทอง (HLA-B, CYP2C19, CYP2C9)
2. แก้ FF2 เพราะเปลี่ยนรัฐจากคู่แข่งเป็น data source หรือลูกค้า และไปอยู่ตรงจุดที่ไต้หวันพิสูจน์แล้วว่าได้ผล (CPOE ทำให้อัตราตรวจเพิ่มจาก 23.7% เป็น 55.6%)
3. แก้ปัญหา distribution เพราะเหลือ 1 lab, 1 consent และ 1 ผู้ซื้อ
4. **เก็บความได้เปรียบจริงของทีมไว้** คือ alert ที่ลด noise (แสดงเฉพาะที่ actionable), ปุ่ม "Why?" ที่เป็น trace จริง, การแยก adherence และ verifier ซึ่งทั้งหมดนี้ยังไม่พบในระบบ alert ของ HIS ไทย
5. NMR/RCV ยังอยู่ได้ในฐานะ "response module ขั้นที่ 2" โดยเริ่มจาก ApoB ที่ lab ทุกแห่งมี แล้วค่อยเพิ่ม NMR เมื่อมี lab คลินิก ส่วน cfDNA เก็บไว้เป็น spin-off สำหรับ oncology ในอนาคต

---

## 9. สิ่งที่ต้องตรวจสอบก่อนใช้ไฟล์นี้บนเวที

- [ ] โทรถาม lab/รพ. ไทย 2–3 แห่งว่ามี NMR lipoprotein (Bruker IVDr / Nightingale) เป็นบริการคลินิกหรือไม่ ถ้ามี FF1 ส่วน NMR จะอ่อนลง
- [ ] เช็กสถานะปัจจุบันของผูกพันธุ์ (จำนวน รพ. ปี 2026, มี API/FHIR ไหม, มี alert ตอนสั่งยาไหม)
- [ ] เช็ก EFLM BV database ว่ามี CVi ของ LDL-P, GlycA และ ApoB หรือไม่
- [ ] เช็กถ้อยคำ ESC/ACC ล่าสุดเรื่อง P2Y12 ใน ACS และ ApoB เป็น target (อ้างต้นฉบับ ไม่ใช้แหล่งรอง)
- [ ] ยืนยันว่า HOSxP มี PGx field หรือโมดูลแล้วหรือยัง (ค้นแล้วพบแค่ alert แพ้ยาทั่วไป)
- [ ] สัมภาษณ์เภสัชกร 5–10 คน เพื่อหาหลักฐานดีมานด์เชิงปริมาณ ซึ่งตอนนี้ยังไม่มีเลย
