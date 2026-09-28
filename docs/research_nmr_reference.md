> Research notes collected 2026-09-28 by a Claude research agent for the prototype. Verify before pitching.

# NMR metabolomics dashboard: sourced reference data (synthetic demo, not for clinical use)

I used only primary pages, PDFs, databases and abstracts that I opened. If I say "not found", I searched and found nothing reliable. Numbers marked *computed* are my own arithmetic on the sourced inputs.

**Four things to know before building:**
1. **The platforms measure on different scales.** Nightingale GlycA has a UK Biobank median of 0.81 mmol/L (810 µmol/L). The Labcorp GlycA cutoff is 400 µmol/L. Particle counts differ between platforms in the same way. Never apply a Labcorp cutpoint to a Nightingale value.
2. **UK Biobank samples are 5–10% diluted and were not fasting.** See the Nightingale data guide: https://research.nightingalehealth.com/uploads/documents/Venous-blood-analysis-Blood-biomarker-data-analysis-guide-Nightingale-Health.pdf
3. **UK Biobank glucose and lactate don't match clinical plasma values.** The glucose median is 3.6 mmol/L and the lactate median is 3.9 mmol/L. Low glucose with high lactate fits sugar being used up in the tube before processing. That explanation is my inference, not a sourced statement. Don't use these as clinical references.
4. **None of these reference distributions come from Thai people.** The one Thai population dataset I found is routine lipids only (section 1c).

---

## 1. Analyte panel and reference distributions

### 1a. Nightingale analytes: UK Biobank population distribution
- **Population:** UK Biobank, about 488,000 adults aged 40–69, recruited 2006–2010. It includes people on medication and is not a "healthy" reference interval.
- **Where the numbers come from:** the UK Biobank Showcase page for each field, `https://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=<Field>`.
- **Columns:** D1 is the 10th centile and D9 the 90th centile.
- **CVa** is Nightingale's technical CV from blind duplicate samples across the whole UK Biobank run: https://nightingalehealth.com/uploads/documents/Nightingale-Health-CoreMetabolomics-Blood-CVs-PubChemIDs.pdf

| Analyte | Abbrev | Unit | Field | D1 | Median | D9 | CVa % |
|---|---|---|---|---|---|---|---|
| Total cholesterol | Total-C | mmol/L | 23400 | 3.50 | 4.67 | 5.92 | 3.6 |
| Non-HDL cholesterol | non-HDL-C | mmol/L | 23401 | 2.30 | 3.30 | 4.47 | 3.9 |
| Remnant cholesterol | Remnant-C | mmol/L | 23402 | 1.06 | 1.55 | 2.13 | 3.7 |
| Clinical LDL cholesterol | LDL-C | mmol/L | 23404 | 1.68 | 2.56 | 3.55 | 4.8 |
| HDL cholesterol | HDL-C | mmol/L | 23406 | 0.95 | 1.29 | 1.80 | 3.4 |
| Total triglycerides | TG | mmol/L | 23407 | 0.69 | 1.22 | 2.17 | 3.6 |
| Apolipoprotein B | ApoB | g/L | 23439 | 0.61 | 0.84 | 1.13 | 3.0 |
| Apolipoprotein A1 | ApoA1 | g/L | 23440 | 1.18 | 1.45 | 1.81 | 2.9 |
| Total lipoprotein particles | Total-P | µmol/L* | 23427 | 14.0 | 17.0 | 20.5 | 3.5 |
| VLDL particles | VLDL-P | nmol/L* | 23428 | 92.9 | 142 | 208 | 3.5 |
| LDL particles | LDL-P | nmol/L* | 23429 | 866 | 1194 | 1596 | 3.1 |
| Large LDL-P | L-LDL-P | nmol/L* | 23530 | 529 | 733 | 987 | 3.2 |
| Medium LDL-P | M-LDL-P | nmol/L* | 23537 | 203 | 291 | 398 | 4.8 |
| Small LDL-P | S-LDL-P | nmol/L* | 23544 | 125 | 168 | 222 | 3.2 |
| HDL particles | HDL-P | µmol/L* | 23430 | 12.5 | 15.3 | 18.7 | 3.6 |
| Mean LDL diameter | LDL size | nm | 23432 | 23.81 | 23.94 | 24.04 | 0.1 |
| Glycoprotein acetyls | GlycA | mmol/L | 23480 | 0.67 | 0.81 | 0.98 | 3.4 |
| Glucose | Glc | mmol/L | 23470 | 2.74 | 3.62 | 4.71 | 4.4 |
| Lactate | Lac | mmol/L | 23471 | 2.62 | 3.87 | 5.49 | 5.2 |
| Citrate | Cit | mmol/L | 23473 | 0.051 | 0.066 | 0.085 | 6.8 |
| Leucine | Leu | µmol/L* | 23466 | 73.9 | 101.9 | 142.7 | 5.9 |
| Isoleucine | Ile | µmol/L* | 23465 | 33.0 | 49.1 | 75.7 | 9.4 |
| Valine | Val | µmol/L* | 23467 | 162.5 | 208.2 | 270.1 | 4.5 |
| Total BCAA | BCAA | µmol/L* | 23464 | 273.6 | 359.2 | 484.3 | 4.9 |
| Phenylalanine | Phe | µmol/L* | 23468 | 35.5 | 47.0 | 61.9 | 10.1 |
| Creatinine | Crea | µmol/L* | 23478 | 52.5 | 67.0 | 85.6 | 5.4 |
| Albumin | Alb | g/L | 23479 | 35.6 | 39.7 | 43.8 | 3.2 |
| Omega-3 % of total fatty acids | Omega-3 % | % | 23451 | 2.69 | 4.17 | 6.29 | 4.3 |
| Docosahexaenoic acid | DHA | mmol/L | 23450 | 0.147 | 0.228 | 0.346 | 7.3 |
| DHA % of total fatty acids | DHA % | % | 23457 | 1.23 | 1.92 | 2.83 | 6.3 |
| PUFA/MUFA ratio | PUFA/MUFA | ratio | 23458 | 1.35 | 1.81 | 2.23 | 2.1 |
| 3-Hydroxybutyrate | bOHB | µmol/L* | 23474 | 21.2 | 44.6 | 121.9 | 12.5 |
| Acetone | — | µmol/L* | 23477 | 9.9 | 13.0 | 19.9 | 12.6 |

\*UK Biobank reports these in mmol/L. I converted them: mmol/L × 10⁶ = nmol/L, and mmol/L × 10³ = µmol/L. To convert ApoB from g/L to mg/dL, multiply by 100.

### 1b. Labcorp NMR LipoProfile cutpoints
Reference population: 5,362 people in MESA (Multi-Ethnic Study of Atherosclerosis, US) not on lipid medication (Mora et al., Atherosclerosis 2007). Sources: the Labcorp report guide at https://www.labcorp.com/tests/related-documents/L15035 and the GlycA test page at https://www.labcorp.com/tests/123850/glyca.

| Marker | Cutpoints / percentiles |
|---|---|
| LDL-P (nmol/L) | <1000 optimal; 1000–1299 near/above optimal; 1300–1599 borderline high; 1600–2000 high; >2000 very high. These edges are the 20th, 50th, 80th and 95th MESA centiles. |
| Small LDL-P (nmol/L) | 25th centile 117; 50th 527; 75th 839. Read from the sample-report graphic, which extracted poorly, so re-check against the PDF. |
| HDL-P (µmol/L) | 25th centile 26.7; 50th 30.5; 75th 34.9. Same caveat as small LDL-P. |
| GlycA (µmol/L) | Low <400; high ≥400 |
| LDL-P analytical reference interval | 457–2282 nmol/L; analytical CV 2.6–5.8% (Matyus 2014, Vantera analyser): https://pubmed.ncbi.nlm.nih.gov/25079243/ |

GlycA across US adults: mean ± SD was 403 ± 63, 374 ± 59 and 350 ± 56 µmol/L in MESA people with inadequate, average and optimal cardiovascular health scores (Benson 2018): https://pubmed.ncbi.nlm.nih.gov/30452775/

Not found: numeric cutpoints for Labcorp large VLDL-P and for the LP-IR insulin-resistance score. Bruker B.I.-LISA / IVDr reference intervals were also not found in a form I could open. For Bruker, I only found reproducibility data: across 11 spectrometers, the average relative SD for 105 lipoprotein parameters was 4.6% and 3.9% on two NIST reference samples (Jiménez 2018): https://pubmed.ncbi.nlm.nih.gov/30211542/

### 1c. Thai population lipids (routine lipids only)
Source: NHES-VI national survey, 17,018 Thai adults with no cardiovascular disease and no lipid-lowering drugs: https://pmc.ncbi.nlm.nih.gov/articles/PMC12801746/
- LDL-C median 126 mg/dL in men (95th centile 194) and 131 mg/dL in women (95th centile 198).
- The authors note that Thai LDL-C levels are high compared with other populations.

I found no Thai NMR, GlycA or lipoprotein-subclass reference data.

---

## 2. Biological variation

- **CVi (within-person variation):** EFLM Biological Variation Database meta-analysis medians. I pulled them from the database's API at https://biologicalvariation.eu/api/meta_calculations on 2026-09-28.
- **CVa (analytical variation):** the Nightingale NMR technical CVs from the table in section 1a.
- **RCV (reference change value)** = 2.77 × √(CVa² + CVi²). This is a two-sided, 95% cut-off for a "real" change between two tests. It is *computed* by me, not published.

| Analyte | CVi % (EFLM, 95% CI) | CVg % (between-person) | CVa % (NMR) | RCV % (computed) |
|---|---|---|---|---|
| ApoB | 6.2 (3.3–13.5) | 20.4 | 3.0 | 19.1 |
| ApoA1 | 4.7 (3.6–4.8) | 8.0 | 2.9 | 15.3 |
| LDL-C | 7.4 (7.0–8.5) | 24.3 | 4.8 | 24.4 |
| HDL-C | 5.7 (5.3–8.2) | 22.8 | 3.4 | 18.4 |
| Total cholesterol | 5.3 (4.8–6.2) | 15.5 | 3.6 | 17.7 |
| Triglycerides | 19.8 (17.5–21.4) | 35.3 | 3.6 | 55.7 |
| Glucose | 4.7 (3.0–5.4) | 8.0 | 4.4 | 17.8 |
| Creatinine | 4.4 (2.3–4.9) | 15.8 | 5.4 | 19.3 |
| Albumin | 2.5 (1.3–3.0) | 4.3 | 3.2 | 11.2 |
| HbA1c (IFCC) | 1.6 (1.3–2.5) | 7.3 | n/a | n/a |
| Lactate | No EFLM meta-analysis. Older Ricos 2014 database: CVi 27.2%, from 1 paper only: https://www.westgard.com/clia-and-quality-regulation-requirements/quality-requirements/biodatabase1.html | 16.7 (Ricos) | 5.2 | 76.7 |
| GlycA | 4.3%: weekly samples for 5 weeks in 23 healthy volunteers. Same study: hsCRP 29.2%, cholesterol 5.7%, TG 18.0%. Assay CVs 1.9% within a run and 2.6% between runs (Otvos 2015): https://pubmed.ncbi.nlm.nih.gov/25779987/ | — | 3.4 | 15.2 |
| LDL-P, BCAA, small/large particle subclasses | **Within-person CVi not found** | — | 3.1–9.4 | — |

Related findings:
- GlycA levels stay stable within the same person for up to about 10 years (Ritchie 2015): https://pubmed.ncbi.nlm.nih.gov/27136058/
- For comparison, EFLM lists CRP with a CVi of 34.7%.

---

## 3. Guideline targets

### ESC/EAS 2019 targets, kept unchanged by the 2025 focused update
Sources:
- 2019 guideline full text: https://academic.oup.com/eurheartj/article/41/1/111/5556353 (I read it from a PDF mirror: https://www.sahta.com/documentos/d_WtT7X0uJYM0RCsirFeKUXK3lv0Hu8CfuRioESCfLc.pdf)
- 2025 focused update: https://academic.oup.com/eurheartj/article/46/42/4359/8234482 (doi 10.1093/eurheartj/ehaf190). The ESC summary says LDL-C goals "have not changed": https://www.escardio.org/communities/councils/cardiology-practice/education/cardiopractice/what-is-new-in-the-2025-focused-update-of-the-2019-esc-eas-guidelines-for-the-m/

| Risk category | LDL-C | Non-HDL-C (secondary target) | ApoB (secondary target) |
|---|---|---|---|
| Very high | <1.4 mmol/L (<55 mg/dL) and ≥50% reduction | <2.2 mmol/L (<85 mg/dL) | <65 mg/dL |
| High | <1.8 mmol/L (<70 mg/dL) and ≥50% reduction | <2.6 mmol/L (<100 mg/dL) | <80 mg/dL |
| Moderate | <2.6 mmol/L (<100 mg/dL) | <3.4 mmol/L (<130 mg/dL) | <100 mg/dL |
| Low | <3.0 mmol/L (<116 mg/dL) | — | — |
| Recurrent event within 2 years | <1.0 mmol/L (<40 mg/dL) may be considered | <1.8 mmol/L (<70 mg/dL) may be considered (diabetes section) | <55 mg/dL may be considered (diabetes section) |

- **Triglycerides:** there is no treatment goal. A TG below 1.7 mmol/L (<150 mg/dL) indicates lower risk.
- **2025 changes to risk categories:** they now use SCORE2 / SCORE2-OP 10-year risk: very high ≥20%, high 10–<20%, moderate 2–<10%, low <2%.
- **Lp(a):** measure at least once in every adult's lifetime; above 50 mg/dL (>105 nmol/L) counts as a risk modifier.
- **Newer:** a 2026 ACC/AHA dyslipidemia guideline exists, but its page returned an error (403), so I have no numbers from it.

### ADA Standards of Care 2025
Source: https://diabetesjournals.org/care/article/48/Supplement_1/S27/157566

| | Diabetes | Prediabetes |
|---|---|---|
| Fasting plasma glucose | ≥7.0 mmol/L (126 mg/dL) | 5.6–6.9 mmol/L (100–125 mg/dL) |
| HbA1c | ≥6.5% (48 mmol/mol) | 5.7–6.4% |
| 2-hour glucose (75 g OGTT) | ≥11.1 mmol/L (200 mg/dL) | — |

### Thai guideline: RCPT 2024 dyslipidemia guideline
This updates the 2016 version. Thai version approved April 2024; English version October 2024. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC11650434/

| Group | LDL-C target |
|---|---|
| Acute coronary syndrome | <55 mg/dL and ≥50% reduction |
| Chronic coronary syndrome | <70 mg/dL and ≥50% reduction; <55 mg/dL recommended if feasible |
| Non-cardioembolic stroke/TIA with >50% carotid or intracranial stenosis | <70 mg/dL |
| Familial hypercholesterolaemia | <70 mg/dL and ≥50% reduction |
| Primary prevention, LDL-C >190 mg/dL | <100 mg/dL and ≥50% reduction |
| Primary prevention, Thai CV Risk Score >10% | <100 mg/dL and ≥30% reduction |
| Type 2 diabetes with target-organ damage, ASCVD risk factors, CKD or albuminuria | <70 mg/dL and ≥50% reduction |
| CKD stage 3a–5, not on dialysis | <100 mg/dL or ≥30% reduction |

Other RCPT points:
- Fibrate when fasting TG >500 mg/dL.
- Pure EPA 4 g/day if TG stays at 150–499 mg/dL on a statin in high-risk patients.
- Calculate non-HDL-C when TG is high or the patient has diabetes or obesity.
- RCPT sets **no numeric ApoB or non-HDL-C target**.

---

## 4. Evidence linking NMR biomarkers to disease risk

| Study | Key finding | Citation |
|---|---|---|
| Buergel 2022, Nat Med | A neural network on 168 NMR markers (117,981 UK Biobank people, checked in 4 other cohorts) was linked to event rates in 23 of 24 conditions (not breast cancer). Age + sex + metabolomic state matched or beat established predictors for 15 endpoints. It added information beyond clinical variables for 8 diseases, including T2D, dementia and heart failure. | https://pubmed.ncbi.nlm.nih.gov/36138150/ |
| Julkunen 2023, Nat Commun | Atlas of 249 NMR measures in 118,461 UK Biobank people against more than 700 diseases, beyond cardiometabolic disease (infection, cancers, joint and mental health). | https://pubmed.ncbi.nlm.nih.gov/36737450/ ; https://research.nightingalehealth.com/atlas |
| Otvos 2011, J Clin Lipidol (MESA, n=6,814) | When LDL-C and LDL-P disagree, only LDL-P predicted CVD: HR 1.45 (1.19–1.78) per SD, versus LDL-C HR 1.07 (0.88–1.30). | https://pubmed.ncbi.nlm.nih.gov/21392724/ |
| Akinkuolie 2014, JAHA (Women's Health Study, n=27,491) | Top vs bottom quarter of GlycA: CVD HR 1.64 (1.39–1.93). This fell to 1.03 after adjusting for hsCRP, so GlycA is not independent of CRP. | https://pubmed.ncbi.nlm.nih.gov/25249300/ |
| Ritchie 2015, Cell Syst | High GlycA reflects chronic inflammation and neutrophil activity, and predicts severe infection (sepsis, pneumonia). | https://pubmed.ncbi.nlm.nih.gov/27136058/ |
| Würtz 2015, Circulation | After adjusting for routine lipids, CVD HRs per SD: phenylalanine 1.18, MUFA 1.17, omega-6 0.89, DHA 0.90. | https://pubmed.ncbi.nlm.nih.gov/25573147/ |
| Wang 2011, Nat Med | Isoleucine, leucine, valine, tyrosine and phenylalanine predicted diabetes; top quarter of a 3-amino-acid score had more than 5-fold risk. **Measured by LC-MS, not NMR.** | https://pubmed.ncbi.nlm.nih.gov/21423183/ |
| Ahola-Olli 2019, Diabetologia (NMR, n=11,896 young Finns) | Branched-chain and aromatic amino acids predicted T2D (OR 1.31–1.33 per SD), as did VLDL triglycerides (OR 1.33–1.50), after adjusting for BMI and fasting glucose. | https://pubmed.ncbi.nlm.nih.gov/31584131/ |
| Fischer 2014, PLoS Med (n=17,345) | GlycA-related α1-acid glycoprotein (HR 1.67), albumin (0.70), VLDL size (0.69) and citrate (1.33) predicted all-cause mortality. | https://pubmed.ncbi.nlm.nih.gov/24586121/ |

**Limitations to show in the pitch:**
- The data are mostly white European (UK Biobank, Finnish cohorts), plus US MESA.
- These are associations, not proof of cause. ApoB/LDL is the exception, where the ESC 2025 update treats ApoB-containing lipoproteins as a direct cause of ASCVD.
- Nothing has been validated in Thai people.
- UK Biobank samples were diluted and not fasting.
- Buergel's model only added value over clinical variables for 8 diseases, not all 24.

---

## 5. Drug effects on NMR biomarkers (pharmacometabolomics)

| Drug | Effect | Citation |
|---|---|---|
| Statins | NMR data on 716 people starting a statin versus 4,874 non-users. Relative to the LDL-C drop, remnant-C fell 80% as much, TG 25% and omega-6 68%. No robust change in amino acids, ketones or glycolysis metabolites. The pattern matched the HMGCR gene variant rs12916 (R²=0.94). | Würtz 2016 JACC: https://pubmed.ncbi.nlm.nih.gov/26965542/ |
| Metformin | CAMERA trial (18 months, NMR): tyrosine fell 6.1 µmol/L and alanine rose 42 µmol/L. Phenylalanine fell and histidine rose (weaker evidence). **No change in BCAAs** or lactate. | Preiss 2016: https://pubmed.ncbi.nlm.nih.gov/26887663/ |
| Metformin | GIPS-III trial (after heart attack, 4 months): LDL-C, large LDL-P and LDL size fell slightly; ApoB did not change. | Eppinga 2016: https://pubmed.ncbi.nlm.nih.gov/26808474/ |
| GLP-1 RA (liraglutide 1.2 mg) | After diet-induced weight loss, ApoB stayed low over 1 year on liraglutide. With the diet alone, ApoB went back up by 0.06 mmol/L. | Engelbrechtsen 2017: https://pubmed.ncbi.nlm.nih.gov/29259801/ |
| GLP-1 RA (semaglutide) | NMR trial data: **not found**. The semaglutide study I found used gel electrophoresis, not NMR. | — |
| Fenofibrate (on a statin, T2D) | Versus placebo: TG −23%, VLDL-TG −51%, ApoB −16%; large, medium and small VLDL particles −45%, −66% and −67%. | Chan 2010: https://pubmed.ncbi.nlm.nih.gov/20649626/ |
| Pemafibrate (PROMINENT trial) | Did not reduce major cardiac events and **increased ApoB and LDL-C**. Good teaching case that a TG drop can come with an ApoB rise. | ESC/EAS 2025 update (doi 10.1093/eurheartj/ehaf190) |
| Icosapent ethyl 4 g (ANCHOR) | Versus placebo: total VLDL-P −12.2%, large VLDL-P −46.4%, LDL-P −7.7%, small LDL-P −13.5%. | Ballantyne 2015: https://pubmed.ncbi.nlm.nih.gov/26073397/ |
| Icosapent ethyl 4 g (MARINE, TG ≥500 mg/dL) | Large VLDL-P −27.9%, LDL-P −16.3%, small LDL-P −25.6%. | Bays 2012: https://pubmed.ncbi.nlm.nih.gov/23312052/ |
| Omega-3 EPA+DHA 1.6 g/day | TG response varies a lot between people: 8 of 35 were responders (median −37%), 16 were non-responders (median 0%). | Rundblad 2019: https://pubmed.ncbi.nlm.nih.gov/31057673/ |
| Omega-3 supplement vs Nightingale omega-3 % / DHA % in a trial | **Not found** | — |

**Suggestions for the dashboard:**
- Use the RCV column to decide whether a change is real. For example, ApoB has to move about 19% before it counts as a change beyond normal variation. TG needs about 56%.
- Amino acids are a useful "should not move" check for statins (Würtz 2016).
- The lowest-noise markers to track progress are ApoB, LDL-P and GlycA (CVa about 3%, CVi about 4–6%).