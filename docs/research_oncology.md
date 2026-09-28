> Primary-source check collected 2026-09-28 by a Claude research agent. Verify before pitching.

# Primary-source check: oncology pharmacy CDS evidence (read 2026-09-28)

Summary: 8 of the 9 items were checked against primary text. One source could not be opened: the IASLC 2021 full text for item 9, so a primary FDA device label is used there instead. Two corrections to your wording:
- **Erlotinib H2RA timing:** the separation rule applies to H2-receptor antagonists only. It is not a PPI rule.
- **Osimertinib and PPIs:** the label does not use the phrase "no clinically meaningful effect". It says osimertinib exposure "was not affected".

---

### 1. Osimertinib (TAGRISSO): current DailyMed SPL, Revised 09/2026
URL: https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/5e81b4a7-b971-45e1-9c31-29cea8c87ce7.xml

- §1.5: "TAGRISSO is indicated for the treatment of adult patients with metastatic EGFR T790M mutation-positive NSCLC, as detected by an FDA-approved test, whose disease has progressed on or after EGFR TKI therapy."
- §2.2 Table 1: T790M, monotherapy, "Source for Testing: Plasma or tumor".
- §12.3: "Gastric Acid Reducing Agents: The exposure of osimertinib was not affected by concurrent administration of a single 80 mg TAGRISSO tablet following 40 mg omeprazole administration for 5 days."
- There is no PPI or acid-reducer entry in §7 Drug Interactions.

**Fact:** Osimertinib is FDA-indicated for metastatic EGFR T790M+ NSCLC that progressed on or after EGFR TKI therapy. Omeprazole did not affect osimertinib exposure, and the label has no PPI restriction.

### 2. Erlotinib (TARCEVA): FDA label, Revised 10/2016
URL: https://www.accessdata.fda.gov/drugsatfda_docs/label/2016/021743s025lbl.pdf (the PDF itself carries the note "may not be the latest")

- §7: "Co-administration of TARCEVA with proton pump inhibitors (e.g., omeprazole) and H-2 receptor antagonists (e.g., ranitidine) decreased erlotinib exposure… For proton pump inhibitors, avoid concomitant use if possible. For H-2 receptor antagonists and antacids, modify the dosing schedule… Increasing the dose of TARCEVA when co-administered with gastric PH elevating agents is not likely to compensate for the loss of exposure."
- §2.4 on PPIs: "Separation of doses may not eliminate the interaction since proton pump inhibitors affect the pH of the upper GI tract for an extended period. Avoid concomitant use if possible."
- §2.4 on H2RAs: "TARCEVA must be taken 10 hours after the H2-receptor antagonist dosing and at least 2 hours before the next dose of the H2-receptor antagonist."
- §2.4 on antacids: "separated by several hours".
- §12.3: "When a proton pump inhibitor (omeprazole) was co-administered with TARCEVA the erlotinib exposure [AUC] was decreased by 46% and the erlotinib maximum concentration [Cmax] was decreased by 61%."

**Fact:** Omeprazole lowered erlotinib AUC by 46% and Cmax by 61%. Avoid PPIs if possible, because separating doses does not remove the interaction. With an H2RA, take erlotinib 10 h after it and at least 2 h before the next dose.

### 3. Gefitinib (IRESSA): DailyMed SPL, published Aug 18, 2025
URL: https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/827d60e8-7e07-41b7-c28b-49ef1c4a5a41.xml

- §7.1: "Avoid concomitant use of IRESSA with proton pump inhibitors, if possible. If treatment with a proton-pump inhibitor is required, take IRESSA 12 hours after the last dose or 12 hours before the next dose of the proton-pump inhibitor. Take IRESSA 6 hours after or 6 hours before an H2-receptor antagonist or an antacid."
- §12.3: "high doses of ranitidine with sodium bicarbonate… decreased mean gefitinib AUC by 47%".

**Fact:** Your wording is confirmed. Avoid PPIs if possible. If one is needed, give gefitinib 12 h after or 12 h before the PPI, and 6 h after or before an H2RA or antacid.

### 4. CPIC DPYD and fluoropyrimidines (Amstutz 2018, "2017 Update")
URL: https://files.cpicpgx.org/data/guideline/publication/fluoropyrimidines/2017/29152729.pdf

Table 2:

| Phenotype | Activity score | Recommendation | Strength |
|---|---|---|---|
| Intermediate metabolizer | 1 | "Reduce starting dose based on activity score followed by titration of dose based on toxicity or therapeutic drug monitoring (if available)." "Reduce dose by 50%" | Strong |
| Intermediate metabolizer | 1.5 | "Reduce dose by 25% to 50%" | Moderate |
| Poor metabolizer | 0.5 | "Avoid use of 5-fluorouracil or 5-fluorouracil prodrug-based regimens. In the event… alternative agents are not considered a suitable therapeutic option, 5-fluorouracil should be administered at a strongly reduced dosed with early therapeutic drug monitoring." | Strong |
| Poor metabolizer | 0 | "Avoid use of 5-fluorouracil or 5-fluorouracil prodrug-based regimens." | Strong |

- Footnote (d) on the table: "In the absence of phenotyping data, a dose of <25% of the normal starting dose is estimated."

Pending update: ClinPGx blog, 09 Jul 2026 (https://blog.clinpgx.org/cpic-comment-on-pending-dpyd-guideline-update/, read through WebFetch).
- The HapB3 variant c.1129-5923C>G "will be assigned an allele value of 0.75… activity score of 1.75… initiate treatment at 75% of the intended dose in cycle 1."
- The full guideline is "expected to be finalized in fall 2026". Current entries stay at 0.5 until then.
- I found no published 2024 CPIC DPYD update. The cpicpgx.org page redirects to a ClinPGx page that needs JavaScript, and the NCBI table behind reCAPTCHA could not be opened.

**Fact:** Under CPIC 2017, cut the starting dose 50% for activity score 1 (strong) and 25–50% for score 1.5 (moderate), then titrate. Avoid 5-FU and capecitabine at scores 0 and 0.5 (strong).

### 5. Pre-treatment DPD / DPYD testing
EMA, 30 Apr 2020. URL: https://www.ema.europa.eu/en/news/ema-recommendations-dpd-testing-prior-treatment-fluorouracil-capecitabine-tegafur-flucytosine (read through WebFetch)
- "Patients should be tested for the lack of the enzyme dihydropyrimidine dehydrogenase (DPD) before starting cancer treatment with fluorouracil given by injection or infusion (drip) or with the related medicines, capecitabine and tegafur."

US capecitabine label (XELODA, H2-Pharma SPL, Revised 10/2025). URL: https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/e702d84d-7162-4751-bf37-d724cc7e45a5.xml
- §2.1: "Prior to initiating XELODA, test patients for genetic variants of the DPYD gene unless immediate treatment is necessary. An FDA-authorized test for the detection of the DPYD gene… is not currently available… Avoid use… in patients known to have certain homozygous or compound heterozygous DPYD variants that result in complete DPD deficiency. No XELODA dose has been proven safe for patients with complete DPD deficiency. For patients with partial DPD deficiency, individualize the dosage…"

Fluorouracil injection (Alembic SPL, Revised 01/2026). URL: https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/6b34cbf2-66f9-48a4-b41f-deb84ba8e8c4.xml
- This label now has a **Boxed Warning**: "WARNING: SERIOUS ADVERSE REACTIONS OR DEATH IN PATIENTS WITH COMPLETE DPD DEFICIENCY… Test patients for genetic variants of DPYD prior to initiating fluorouracil unless immediate treatment is necessary."
- In the XELODA SPL I pulled, I did not find the "WARNING:" boxed header, only the §2.1/§5.1 text.

**Fact:** The EMA (2020) and current US labels both say to test for DPYD variants or DPD deficiency before starting fluorouracil or capecitabine, unless treatment is urgent. Avoid the drug in complete DPD deficiency.

### 6. Irinotecan and UGT1A1: CAMPTOSAR SPL, published May 13, 2026
URL: https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/e518dfc6-7e93-4fee-a66c-51e1ab71c056.xml

- "consider a reduction in the CAMPTOSAR starting dose by at least one level for patients known to be homozygous or compound heterozygous for the UGT1A1*28 and/or *6 alleles (*28/*28, *6/*6, *6/*28). Closely monitor… for neutropenia… The precise dosage reduction in this patient population is not known."
- §5.3: "These individuals are UGT1A1 poor metabolizers and experience increased systemic exposure to SN-38."
- I did not check for a CPIC UGT1A1–irinotecan guideline or the DPWG.

**Fact:** For UGT1A1 poor metabolizers (*28/*28, *6/*6, *6/*28), the FDA label says to consider lowering the irinotecan starting dose by at least one level and to watch closely for neutropenia. Note the label says "consider", not "reduce".

### 7. Clonal hematopoiesis (CHIP) in cfDNA
Razavi et al., Nat Med 2019. URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7061455/fullTextXML
- Abstract: "The vast majority of cfDNA mutations (81.6% in controls and 53.2% in patients with cancer) had features consistent with clonal hematopoiesis… emphasizing the importance of matched cfDNA-white blood cell sequencing."
- Results: "the vast majority of the WBC-matched somatic mutations detected in cfDNA… involved canonical CH genes, such as DNMT3A, TET2, PPM1D and TP53."
- Methods: "The 15 canonical genes known to be associated with CH were DNMT3A, TET2, ASXL1, PPM1D, TP53, JAK2, RUNX1, SF3B1, SRSF2, IDH1, IDH2, U2AF1, CBL, ATM and CHEK2."

Hu et al., Clin Cancer Res 2018. Abstract only, from the Europe PMC API (PMID 29567812); full text could not be opened.
- "most JAK2 mutations, some TP53 mutations, and rare KRAS mutations detected in cfDNA are derived from CH not tumor."

Guardant360 CDx FDA labeling, P200010S008C. URL: https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200010S008C.pdf
- "Genomic findings from cfDNA may originate from circulating tumor DNA (ctDNA) fragments, germline alterations, or non-tumor somatic alterations, such as clonal hematopoiesis of indeterminate potential (CHIP)."

**Fact:** Many cfDNA variants, especially in DNMT3A, TET2, PPM1D, ASXL1, JAK2 and TP53, come from clonal hematopoiesis rather than the tumor. Matched white-blood-cell sequencing helps tell them apart.

### 8. Incidental germline findings
Mandelker et al., Ann Oncol 2019 (ESMO Precision Medicine Working Group). URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6683854/fullTextXML
- "A heterozygous germline pathogenic variant in a CSG would be anticipated to be present in 50% of alleles across body tissues, including a tumour."
- Box 1: "Germline-focussed tumour analysis can be restricted to variants of VAF >30% (SNVs) or >20% (small insertions/deletions)."
- BRCA1, BRCA2, PALB2, MLH1, MSH2, MSH6, PMS2 and others are listed under "germline sample laboratory confirmation", "Any tumour type".
- Caveat: this paper covers tumour-only tissue sequencing, not ctDNA. I found no "~100% VAF" wording in it.

Guardant360 CDx label (same URL as item 7):
- "The assay filters germline variants from reporting except for pathogenic BRCA1, BRCA2, ATM, and CDK12 alterations. However, if a reported alteration is suspected to be germline, confirmatory testing should be considered… The test is not intended to replace germline testing."

**Fact:** A pathogenic variant in a cancer-predisposition gene such as BRCA1/2 at about 50% VAF on tumor or plasma sequencing may be germline. It needs confirmatory germline testing, since tumor and ctDNA assays do not replace germline testing.

### 9. A "not detected" ctDNA result
- **Could not open** the IASLC 2021 consensus (Rolfo et al., JTO, PMID 34246791). jto.org returned 403 and the paper is not in PMC. The abstract has no negative-result wording.
- NCCN was not checked.

Guardant360 CDx FDA labeling instead. URL: https://www.accessdata.fda.gov/cdrh_docs/pdf20/P200010S008C.pdf
- "A negative result from a plasma specimen does not assure that the patient's tumor is negative for genomic findings. NSCLC patients who are negative for the biomarkers listed in Table 1 should be reflexed to tissue biopsy testing… using an FDA-approved tumor tissue test, if feasible."
- "A negative result for any given variant does not preclude the presence of this variant in tumor tissue."
- It also notes that TAGRISSO efficacy "has not been established in the EGFR T790M plasma-positive, tissue-negative or unknown population".
- The current TAGRISSO label no longer contains the older "if not detected in plasma, test tumor tissue" sentence.

**Fact:** A negative plasma ctDNA result does not rule out a driver mutation. Where feasible, follow it with tissue testing using an FDA-approved tissue test.