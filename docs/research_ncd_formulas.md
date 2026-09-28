> Primary-source check collected 2026-09-28 by a Claude research agent. Verify before pitching.

I checked all nine items. Most came from primary sources. Where a site blocked me (403 errors or Cloudflare), the report names the fallback source I used. Two things matter most for the prototype. First, WHO's actual preventability figure is "at least 80%" of heart disease, stroke and type 2 diabetes, not "80% of premature…", and I could not open WHO's own copy. Second, the ">400 metabolites" claim does not match any NMR panel I found (item 9).

# Evidence report: Thai NCD-screening CDS (synthetic demo)

## 1. CKD-EPI 2021 and KDIGO 2024
**Source:** NKF, https://www.kidney.org/ckd-epi-creatinine-equation-2021-0
> "eGFR = 142 * min(standardized Scr/K, 1)α * max(standardized Scr/K, 1)^-1.200 * 0.9938^Age * 1.012 [if female]" — κ 0.7 (F) / 0.9 (M); α −0.241 (F) / −0.302 (M); Scr in mg/dL, IDMS-standardized; eGFR in mL/min/1.73 m².

The same coefficients appear in Table 1 of Inker 2021, NEJM (https://pmc.ncbi.nlm.nih.gov/articles/PMC8822996/): "2021 CKD-EPI creatinine … 142 … F: −0.241; M: −0.302 … −1.200 … 0.9938 … 1.012".

**Worked examples (my calculation):**
- Man, 50 y, Scr 1.0 mg/dL: 142 × (1.111)^−1.2 × 0.9938^50 = 142 × 0.881 × 0.733 = **91.7 → G1**
- Woman, 60 y, Scr 0.8 mg/dL: **84.3 → G2**
- Man, 70 y, Scr 1.5 mg/dL: **49.8 → G3a** (extra check)

**Source:** KDIGO 2024, Kidney Int 105(4S), https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf (PDF text extracted)
> "CKD is defined as abnormalities of kidney structure or function, present for a minimum of 3 months, with implications for health."

- Table 2: G1 ≥90 "Normal or high"; G2 60–89 "Mildly decreased"; G3a 45–59; G3b 30–44; G4 15–29; G5 <15 "Kidney failure".
- Footnote: "In the absence of evidence of kidney damage, neither G1 nor G2 fulfils the criteria for CKD."
- Table 3 (ACR): A1 <30 mg/g (<3 mg/mmol); A2 30–300 (3–30); A3 >300 (>30).

**Fact text:** "CKD-EPI 2021 (race-free): 142×min(Scr/κ,1)^α×max(Scr/κ,1)^−1.200×0.9938^age×1.012[F]; κ 0.7/0.9, α −0.241/−0.302. KDIGO 2024: CKD = abnormality >3 months; G1–G5 ≥90/60–89/45–59/30–44/15–29/<15; A1–A3 ACR <30/30–300/>300 mg/g."

## 2. FIB-4 and MASLD
**Source:** EASL-EASD-EASO 2024 guideline, Obes Facts copy, https://pmc.ncbi.nlm.nih.gov/articles/PMC11299976/
> "FIB-4 (Fibrosis-4 index) = age x AST/(platelet count x √(ALT)) (age in years, ALT and AST in U/L, and platelet count in 10^9/L)"

> "If FIB-4 is below 1.3, these individuals can be assumed to be at low risk of advanced fibrosis and may be re-assessed every 1-3 years … If FIB-4 is >1.3 (or >2.0 in individuals aged >65), the risk for advanced fibrosis is increased." It also says "intermediate range (1.3-2.67)" and "in individuals older than 65 years, a different lower FIB-4 cut-off of 2.0 applies."

- I did not open the AASLD 2023 guidance. EASL states ">2.67" only as the top of the intermediate range.
- Worked example (my calculation): 55 y, AST 40, ALT 45, platelets 200 → **1.64, indeterminate**.

**Nomenclature (same source):**
> "MASLD replaces the old term non-alcoholic fatty liver disease (NAFLD)… The nomenclature of SLD and definition of MASLD were established in June 2023, following an international, multi-society guided Delphi process."
> "MASLD is defined as the presence of hepatic steatosis in conjunction with (at least) one cardiometabolic risk factor and no other discernible cause."

Table 3 criteria:
- BMI ≥25 (≥23 kg/m² in Asians), or waist ≥90/≥80 cm (South Asian/Chinese), ≥85/≥90 cm (Japanese)
- Prediabetes (HbA1c 5.7–6.4%), T2D or its treatment
- TG ≥1.7 mmol/L (150 mg/dL) or lipid-lowering treatment
- HDL ≤1.0 mmol/L (men) / ≤1.3 mmol/L (women) or lipid-lowering treatment
- BP ≥130/85 or antihypertensive treatment

**Fact text:** "FIB-4 = age×AST/(PLT[10^9/L]×√ALT); <1.3 low risk, 1.3–2.67 indeterminate, >2.67 high; age >65 uses 2.0 as the lower cutoff (EASL-EASD-EASO 2024). NAFLD was renamed MASLD in 2023: steatosis plus ≥1 of 5 cardiometabolic criteria."

## 3. Fatty Liver Index
**Source:** Bedogni 2006, BMC Gastroenterol 6:33, full text via Europe PMC XML of PMC1636651 (https://pmc.ncbi.nlm.nih.gov/articles/PMC1636651/)
> "FLI = (e^(0.953*loge(triglycerides) + 0.139*BMI + 0.718*loge(ggt) + 0.053*waist circumference − 15.745)) / (1 + e^(same)) * 100"

> "A FLI < 30 (negative likelihood ratio = 0.2) rules out and a FLI ≥ 60 (positive likelihood ratio = 4.3) rules in fatty liver."

- Units from Table 1: TG in mg·dL⁻¹, GGT in U·L⁻¹, waist in cm.
- The population was Italian (Dionysos study), and the authors state it needs external validation.
- Worked example (my calculation): TG 150, BMI 27, GGT 40, waist 95 → **FLI 61.5**.

**Fact text:** "FLI = e^y/(1+e^y)×100, y = 0.953·ln(TG mg/dL)+0.139·BMI+0.718·ln(GGT U/L)+0.053·waist(cm)−15.745; <30 rules out, ≥60 rules in."

## 4. Metabolic syndrome (Alberti 2009)
**Could not open the full text:** ahajournals.org returned 403 and the lipid.org copy returned 404.

**Source:** abstract via Europe PMC (PMID 19805654)
> "It was agreed that there should not be an obligatory component… Three abnormal findings out of 5 would qualify a person for the metabolic syndrome. A single set of cut points would be used for all components except waist circumference… national or regional cut points for waist circumference can be used."

**Thresholds (secondary sources, not the original Table 1):**
- PMC5045945 lists: TG ≥1.7 mmol/L (150 mg/dL); HDL <1.0 mmol/L (men) / <1.3 mmol/L (women); BP ≥130/≥85; fasting glucose ≥100 mg/dL. It marks TG, HDL and BP as met "or drug treatment as indicated".
- A search snippet (not opened) says the original Table 1 counts drug treatment as an alternate indicator for all four (TG, HDL, BP, glucose).
- PMC13448046 quotes the Asian cutoff as "≥90 cm in men and ≥80 cm in women".

**Fact text:** "Harmonized MetS (2009): ≥3 of 5 — waist (Asian ≥90 cm M / ≥80 cm F), TG ≥150 mg/dL or treatment, HDL <40 (M) / <50 (F) mg/dL or treatment, BP ≥130/85 or treatment, fasting glucose ≥100 mg/dL or treatment."

## 5. LOINC
loinc.org was blocked by Cloudflare. The names and units below come from NLM Clinical Tables (LOINC content), `clinicaltables.nlm.nih.gov/api/loinc_items`.

| Code | Long common name | UCUM |
|---|---|---|
| 13457-7 | Cholesterol in LDL [Mass/volume] in Serum or Plasma by calculation | mg/dL |
| 18262-6 | Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay | mg/dL |
| 2085-9 | Cholesterol in HDL [Mass/volume] in Serum or Plasma | mg/dL |
| 2571-8 | Triglyceride [Mass/volume] in Serum or Plasma | mg/dL |
| 2093-3 | Cholesterol [Mass/volume] in Serum or Plasma | mg/dL |
| 1884-6 | Apolipoprotein B [Mass/volume] in Serum or Plasma | mg/dL |
| 1558-6 | Fasting glucose [Mass/volume] in Serum or Plasma | mg/dL |
| 4548-4 | Hemoglobin A1c/Hemoglobin.total in Blood | % |
| 2160-0 | Creatinine [Mass/volume] in Serum or Plasma | mg/dL |
| 1742-6 | Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma | U/L |
| 1920-8 | Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma | U/L |
| 2324-2 | Gamma glutamyl transferase [Enzymatic activity/volume] in Serum or Plasma | U/L |
| 777-3 | Platelets [#/volume] in Blood by Automated count | 10*3/uL |
| 1751-7 | Albumin [Mass/volume] in Serum or Plasma | g/dL |
| 54434-6 | Lipoprotein.beta.subparticle [Moles/volume] in Serum or Plasma | nmol/L |
| 82730-3 | GlycA [Moles/volume] in Serum or Plasma | umol/L |
| 98979-8 | Glomerular filtration rate [Volume Rate/Area] in Serum, Plasma or Blood by Creatinine-based formula (CKD-EPI 2021)/1.73 sq M | mL/min/{1.73_m2} |

Notes on the table:
- **54434-6** is LDL particle number, but the code does not name a method. I found no "by NMR" code for it.
- **HbA1c:** I found no code labeled "NGSP". The generic 4548-4 in % is the one to use; 17856-6 is the HPLC variant.
- **Platelets:** 10*3/uL is the same number as 10^9/L, so FIB-4 can use the value directly.

## 6. ICD-10
WHO ICD-10 2019 was read from `icd.who.int/browse10/2019/en/GetConcept`. ICD-10-CM was read from NLM Clinical Tables (current FY).

| Condition | WHO ICD-10 (2019) | ICD-10-CM (US) |
|---|---|---|
| T2DM | E11 "Type 2 diabetes mellitus" (4th character .9 = without complications) | E11.9 |
| Prediabetes | R73.0 "Abnormal glucose tolerance test", Incl.: "Impaired glucose tolerance, Prediabetes"; R73.9 "Hyperglycaemia, unspecified" | R73.03 Prediabetes; R73.01 Impaired fasting glucose |
| Lipids | E78.0 pure hypercholesterolaemia, E78.1, E78.2 mixed, E78.5 unspecified | E78.00, E78.1, E78.2, E78.5 |
| Hypertension | I10 Essential (primary) hypertension | I10 |
| CKD | N18.1–N18.5, N18.9; WHO has no 3a/3b split (N18.3 = GFR 30–59) | N18.1, N18.2, N18.30/.31 (3a)/.32 (3b), N18.4, N18.5, N18.6 ESRD, N18.9 |
| Fatty liver | K76.0 "Fatty (change of) liver, NEC", Incl. NAFLD | K76.0; NASH K75.81 |
| Metabolic syndrome | **No specific code**; E88.8 "Other specified metabolic disorders" does not list it | **E88.810** Metabolic syndrome (older E88.81 is now subdivided) |
| Lung cancer | C34.x | C34.90 |
| Colon cancer | C18.x | C18.9 |

I did not check Thai ICD-10-TM, which is WHO-based.

## 7. cfDNA fragment size
- **(a)** Lo 2010, Sci Transl Med, abstract (Europe PMC):
  > "fragmentation pattern reminiscent of nuclease-cleaved nucleosomes… a 166-base pair (bp) peak relative to a 143-bp peak"

  Snyder 2016, Cell (https://pmc.ncbi.nlm.nih.gov/articles/PMC4715266/):
  > "dominant peak at ~167 bp (coincident with the length of DNA associated with a chromatosome), and ~10.4 bp periodicity"

  I found no verbatim "~330 bp" sentence. Mouliere 2018 refers to "multiples of 167 bp" and "mono-, and di-nucleosomal" lengths.
- **(b)** Agilent PDFs were 403. From a search snippet only: the Cell-free DNA ScreenTape "%cfDNA" region is **50–700 bp**, separating mono- and multimers from "HMW DNA larger than 700 bp". Pisareva/Thierry 2021 (https://pmc.ncbi.nlm.nih.gov/articles/PMC8525023/):
  > "the accumulation of leukocyte DNA is a risk in EDTA tubes when blood is stored for more than 4 h"; "the lysed cells release their DNA in blood and increase the background DNA."

  I did not open CEN/TS 16835-3.
- **(c)** Mouliere 2018 (https://pmc.ncbi.nlm.nih.gov/articles/PMC6483061/):
  > "We detected enrichment of ctDNA in fragment sizes between 90–150 bp" (also 250–320 bp); used low-pass WGS (0.4×)
- **(d)** Cristiano 2019 (https://pmc.ncbi.nlm.nih.gov/articles/PMC6774252/):
  > "The method is based on low coverage WGS of isolated cfDNA… We performed WGS at 1–2x coverage"

  The Bioanalyzer was used only for QC.
- **(e)** I found one capillary-electrophoresis-only study, relevant because it is Thai: "CEliver", Communications Medicine 2026 (https://pmc.ncbi.nlm.nih.gov/articles/PMC13022191/), Chiang Mai.
  - Uses machine learning on 332 electropherogram features plus AFP, for HCC surveillance in HBV/HCV/cirrhosis patients.
  - External validation n=69 (27 HCC): 85% sensitivity, 100% specificity, AUC 0.93.
  - Authors list the small sample and viral-etiology bias as limitations.
  - It is single-centre, uses AFP alongside the CE features, is for HCC surveillance only, and has no regulatory clearance. I found no validated CE-only method for multi-cancer, lung or colon screening.

## 8. WHO preventability
- I could not open WHO's own copy: the iris.who.int PDFs returned 403 and the old chp page returned 404.
- The wording widely attributed to WHO's 2005 report *Preventing chronic diseases: a vital investment* (from search snippets):
  > "If the major risk factors for chronic disease were eliminated, at least 80% of heart disease, stroke and type 2 diabetes would be prevented; and 40% of cancer would be prevented."
- The current WHO NCD and CVD fact sheets give no percentage. The CVD sheet says only "Most cardiovascular diseases can be prevented by addressing behavioural and environmental risk factors."
- Recommendation: cite as "WHO 2005, *Preventing chronic diseases: a vital investment*". Do not write "80% of premature…".

## 9. NMR panel sizes
- **Nightingale:** "250+ metabolic measures" (research.nightingalehealth.com/products/metabolomics). The UK Biobank companion document says: "A total of 249 metabolic measures, of which 168 absolute levels and 81 ratio measures."
- **Bruker B.I.LISA:** "112 lipoprotein composition parameters" (https://pmc.ncbi.nlm.nih.gov/articles/PMC12888004/). The Bruker product page does not give a total.
- **Bruker B.I.QUANT-PS:** "B.I.QUANT-PS 2.0 offers the quantification from 26 metabolites up to 41 metabolites" (bruker.com B.I.QUANT-PS page).

**Fact text:** "Clinical-grade NMR panels measure about 250 measures (Nightingale) or 112 lipoprotein parameters plus about 41 small molecules (Bruker IVDr). A '>400 metabolites' claim is not supported. Most of these measures are lipoprotein-derived, not distinct metabolites."

Downloaded source files are in `/tmp/claude-1000/-home-eggchad-eakject-comp-med-precisionrx-pharmacy-hackathon/980092ed-9201-43a7-bb21-bbee68321c33/scratchpad/`.