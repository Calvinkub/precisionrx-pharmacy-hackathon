> Research notes collected 2026-09-28 by a Claude research agent for the prototype. Verify before pitching.

I found the exact Thai CV Risk equations, the Thai diabetes score table and nearly all the guideline items, each with a source URL. Two things to know first. The official calculator and the MOPH/HDC reporting spec use different baseline survival values, so the same person gets a different risk. And the metformin HbA1c figure comes from a meta-analysis, not from an ADA guideline.

# Research report for the PrecisionRx prototype (synthetic demo)

## 1. Thai CV Risk Score (Rama-EGAT)

**Main source:** the JavaScript behind the official Ramathibodi calculator, "Thai CV risk score 2.5, Copyright 2021": https://www.rama.mahidol.ac.th/cardio_vascular_risk/thai_cv_risk_score/scripts/formular.js (page: https://www.rama.mahidol.ac.th/cardio_vascular_risk/thai_cv_risk_score/tcvrs_en.html)

**Variable coding (from the file header):**
- age: 30–70 years
- smoke: 0/1
- dm: 0/1
- sbp: 70–220 mmHg
- sex: 1 = male, 0 = female
- lipids: mg/dL
- waist and height: cm

The web form takes waist in inches and converts it with `wc_cm = parseInt(inches × 2.5)`. WHR in the code means waist ÷ height. The LDL/HDL inputs are commented out ("Cancle 2021-04-23"), so **no LDL/HDL version exists in the current calculator**. Since 2021 it has three equations.

**Baseline survival:** `S0 = 0.964588`. Risk = `1 − S0^exp(FullScore − C)`.

| Version | FullScore | C |
|---|---|---|
| A. Total cholesterol (TC) | 0.08183·age + 0.39499·sex + 0.02084·SBP + 0.69974·DM + 0.00212·TC + 0.41916·smoke | 7.04423 |
| B. Non-lab, waist/height | 0.079·age + 0.128·sex + 0.019350987·SBP + 0.58454·DM + 3.512566·(waist/height) + 0.459·smoke | 7.712325 |
| C. Non-lab, waist only (cm) | 0.08372·age + 0.05988·sex + 0.02034·SBP + 0.59953·DM + 0.01283·waist + 0.459·smoke | 7.31047 |

Which equation runs: A if TC > 0, otherwise B if waist/height > 0, otherwise C.

**The two sources disagree on S0.** The Ministry of Public Health's 2018 reporting spec (HDC, "43 files") uses the same coefficients but `S0 = 0.978296`, with C = 7.04423 for TC and 7.720484 for waist/height: http://info2.muaklekhospital.com/wp-content/uploads/2018/08/cvd2561_d.pdf. Pick one version and label it; I suggest the official calculator's 0.964588.

**Comparison value in the calculator.** It also computes a "same age/sex person" risk for a "N times higher/lower" message. The reference person has SBP 120 (men over 60: 132; women 60 or under: 115; women over 60: 130), TC 200, no diabetes, non-smoker, waist/height 0.52667 for women and 0.58125 for men, and waist 79 cm for women and 93 cm for men.

**Risk categories and advice in the calculator (English text verbatim):**
- **Under 10%, "low risk":** "It is reasonable to prevent atherosclerotic cardiovascular disease in the future by regular execise, high fiber dietary [+add-ons] and annual health checkup."
- **10% to under 20%, "medium risk":** "You should have regular execise, high fiber dietary [+add-ons] and annual health checkup."
- **20–30%, "high risk":** "You must visit the physician for health checkup and recieve properly therapy. You must have regular execise, high fiber dietary [+add-ons] now."
- **Over 30%, "very high risk":** same text as high risk. The number is displayed only as "is over 30".

The spelling errors ("execise", "recieve") are in the original.

Add-on phrases:
- smoker → "quit smoking"
- DM = 1 → "keep blood sugar level within normal range"
- SBP ≥ 140 → "achieve goal of blood pressure controlling"
- TC ≥ 220 → "intensify cholesterol-lowering therapy"
- large waist → "body weight lowering"

Thai versions: เลิกสูบบุหรี่ / รักษาระดับน้ำตาลในเลือดให้อยู่ในเกณฑ์ปกติ / ควบคุมระดับความดันโลหิตให้ดี / เข้ารับการรักษาเพื่อลดโคเรสเตอรอลในเลือด / ลดน้ำหนักให้อยู่ในเกณฑ์ปกติ.

The code also has an LDL ≥ 190 check, but it can never fire because LDL is always 0. The waist rule compares the converted **cm** value against 38 (men) and 32 (women), which looks like a unit bug. Use 90/80 cm instead (section 5).

The MOPH spec uses five levels instead: under 10% low; 10 to under 20% moderate; 20 to under 30% high; 30 to under 40% very high; 40% or more "dangerously high" (same PDF).

**Worked examples.** No source gives any, so I computed these with S0 = 0.964588. Values with the MOPH S0 = 0.978296 are in brackets.
1. **Version A, man aged 60, smoker, no DM, SBP 140, TC 220:** terms 4.9098 + 0.39499 + 2.9176 + 0 + 0.4664 + 0.41916 = 9.10795. Minus 7.04423 = 2.06372; exp = 7.87521; 1 − 0.964588^7.87521 = **24.72%**, high [15.87%].
2. **Version A, woman aged 45, non-smoker, no DM, SBP 120, TC 200:** 3.68235 + 0 + 2.5008 + 0.424 = 6.60715; minus 7.04423 = −0.43708; exp = 0.64592 → **2.30%**, low [1.41%].
3. **Version B, woman aged 50, DM, SBP 130, waist 85 cm, height 155 cm, non-smoker:** 3.95 + 0 + 2.51563 + 0.58454 + 3.512566 × 0.548387 (= 1.92625) = 8.97641; minus 7.712325 = 1.26409; exp = 3.53987 → **11.98%**, moderate [7.42% with C = 7.720484].

## 2. Diabetes risk

**Thai diabetes risk score** (Aekplakorn et al., Diabetes Care 2006;29:1872). The cohort was aged 35–55 and followed for 12 years. The best cutoff was **6 or more out of 17**: sensitivity 77%, specificity 60%, AUC 0.74 (https://pubmed.ncbi.nlm.nih.gov/16873795/). The paper itself returned 403, so the points below come from the Diabetes Association of Thailand's online form code (https://www.dmthai.org/new/index.php/sara-khwam-ru/sahrab-bukhkhl-thawpi/evaluation-form):

| Factor | Points |
|---|---|
| Age 34–39 / 40–44 / 45–49 / 50 or older | 0 / 0 / 1 / 2 |
| Sex: female / male | 0 / 2 |
| BMI under 23 / 23 to under 27.5 / 27.5 or more | 0 / 3 / 5 |
| Waist: men 90 cm or more, women 80 cm or more | 2 (else 0) |
| Hypertension | 2 |
| Parent or sibling with diabetes | 4 |

Result bands on the same page (12-year risk):

| Score | Risk | Chance of diabetes | Re-assess |
|---|---|---|---|
| 0–2 | under 5%, "low" (1 in 20) | | every 3 years |
| 3–5 | 5–10%, "moderate" (1 in 12) | | every 1–3 years |
| 6–8 | 11–20%, "high" (1 in 7) | add blood glucose test | every 1–3 years |
| over 8 | over 20%, "very high" (1 in 3 to 1 in 4) | add blood glucose test | every year |

The advice text in all bands also covers exercise, weight control and blood pressure checks.

**ADA cutpoints** (Standards of Care 2026, Section 2: https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926/2-Diagnosis-and-Classification-of-Diabetes):
- **Prediabetes:** FPG 100–125 mg/dL (5.6–6.9 mmol/L), or A1C 5.7–6.4% (39–47 mmol/mol), or impaired glucose tolerance.
- **Diabetes:** FPG 126 mg/dL or higher, or A1C 6.5% or higher.
- **Not verified this session:** 2-hour OGTT 200 mg/dL or higher, IGT 140–199, and random glucose 200 or higher with symptoms. The page returned 403.

## 3. Lifestyle rules

| Trigger | Recommendation (source wording) | Source |
|---|---|---|
| All patients with high BP; BP 130–139/80–89 | Sodium "no >2 g of sodium per day" (about 1 tsp salt or 3 tsp fish sauce/soy sauce); stricter "no >1.5 g/d may further aid" | 2024 Thai HT guideline, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12919385/ |
| Any adult | WHO: under 2000 mg/day sodium (under 5 g salt) | https://www.who.int/news-room/fact-sheets/detail/salt-reduction |
| Inactive | WHO 2020: 150–300 min/week moderate or 75–150 min/week vigorous aerobic activity; muscle strengthening on 2 or more days/week | https://pubmed.ncbi.nlm.nih.gov/33239350/ |
| High BP | Moderate exercise (50–70% of max HR) averaging 150 min/week, or vigorous 75 min/week; "no >2 consecutive days of rest" | Thai HT 2024 (above) |
| High LDL-C | Saturated fat "<7% of total daily caloric intake"; replace with unsaturated oils; avoid trans fat; more fibre; plant stanols 2 g/d | RCPT 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11650434/ |
| High TG | "abstain from consuming alcoholic beverages"; cut carbohydrates; sugar under 10% of energy. TG over 500 mg/dL → fibrate. TG 150–499 on a statin in high-risk patients → pure EPA 4 g/d | RCPT 2024 |
| Dyslipidemia | Aerobic exercise 150–300 min/week "to help reduce LDL-C and TG, and increase HDL-C" | RCPT 2024 |
| Smoker | "quit smoking or refer patients to a smoking cessation clinic" | RCPT 2024; Thai HT 2024 (cigarettes, vaping, waterpipe) |
| Drinks alcohol | Women at most 1, men at most 2 standard drinks/day (1 drink ≈ 10 g), with alcohol-free days; non-drinkers should not start | Thai HT 2024 |
| Drinks alcohol | ESC 2021: under 100 g/week (Class I, level B) | https://academic.oup.com/eurheartj/article/42/34/3227/6358713 (via https://www.jacc.org/doi/10.1016/j.jacc.2022.02.001) |
| Prediabetes | "weight reduction of at least 5–7% of initial body weight … and ≥150 min/week of moderate-intensity physical activity" (rec. 3.3) | ADA 2026 Section 3, https://pmc.ncbi.nlm.nih.gov/articles/PMC12690170/ |
| Prediabetes, high risk | Consider metformin "especially those aged 25–59 years with BMI ≥35 kg/m2, higher fasting plasma glucose (e.g., ≥110 mg/dL), and higher A1C (e.g., ≥6.0%)" (rec. 3.7) | same |
| Overweight | Weight loss with cognitive-behavioural therapy; Thai normal BMI 18.5–22.9; waist under 90 cm (men) / under 80 cm (women), or waist/height under 0.5 | Thai HT 2024 |
| Age 35 or older, LDL under 190, Thai CV risk over 10% | Target LDL-C under 100 mg/dL and at least 30% reduction; low-to-moderate intensity statin | RCPT 2024 |
| Thai CV risk under 10%, LDL under 190 | "consistently implement lifestyle modifications" | RCPT 2024 |
| LDL-C over 190 (age 21 or older) | Target under 100 and at least 50% reduction; moderate-intensity statin, switch to high intensity if not at target in 4–12 weeks | RCPT 2024 |

- **Weight loss 5–10% for high BP:** the specific percentage was not found in the Thai HT 2024 text I read.
- **Expected mmHg drop from each lifestyle change:** not found in the Thai guideline.

## 4. Medication response and adherence

**Statin intensity (ACC/AHA 2018):** high intensity lowers LDL-C by 50% or more, moderate by 30–49%, low by under 30%. Repeat lipids "4 to 12 weeks after statin initiation or dose adjustment", then every 3–12 months (https://www.ahajournals.org/doi/10.1161/CIR.0000000000000625; summary https://www.aafp.org/pubs/afp/issues/2019/0501/p589.html).

**RCPT 2024 Table A1.1 (Thai drug list):**
- **High intensity (over 50%):** atorvastatin 40–80 mg; rosuvastatin 20 mg.
- **Moderate (about 30–50%):** atorvastatin 10–20 mg; fluvastatin 80 mg; pitavastatin 1–4 mg; pravastatin 40 mg; rosuvastatin 5–10 mg; simvastatin 20–40 mg.
- **Low (under 30%):** fluvastatin 20–40 mg; pravastatin 10–20 mg; simvastatin 10 mg.

RCPT also says a "follow-up blood test is recommended within 4–12 weeks after starting the medication to evaluate its effectiveness and assess patient adherence", then every 3–12 months (https://pmc.ncbi.nlm.nih.gov/articles/PMC11650434/).

**Adherence:** the Pharmacy Quality Alliance uses a PDC threshold of 80% for statins, RAS antagonists and diabetes drugs, and 90% for antiretrovirals (https://www.pqaalliance.org/adherence-measures; https://www.pqaalliance.org/assets/docs/PQA_PDC-CMP-PH_Rationale.pdf).

**Metformin:** monotherapy lowered HbA1c by **1.12%** (95% CI 0.92–1.32) versus placebo (Hirst et al., Diabetes Care 2012;35:446, https://pubmed.ncbi.nlm.nih.gov/22275444/). This is a meta-analysis, not a guideline figure.

## 5. BMI and waist cutoffs for Asians

- **WHO expert consultation (Lancet 2004;363:157):** Asians face substantial risk below 25 kg/m². Proposed public-health action points are **23.0, 27.5, 32.5 and 37.5** kg/m² (https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(03)15268-3/abstract).
- **Thai normal BMI:** 18.5–22.9 (Thai HT 2024).
- **Thai "obese" definition:** BMI **25 or more** and/or waist **90 cm or more in men, 80 cm or more in women**, or waist more than height ÷ 2 (DMThai page above).
- **Overweight band 23–24.9:** implied by these sources, not stated in them.

**Not found or not verified:**
- The Thai CV Risk development paper with its coefficients (the official calculator code is the source instead).
- A Thai CV Risk version with LDL/HDL. It was removed from the calculator in 2021.
- The ADA OGTT and random-glucose cutpoints.
- Expected mmHg reductions from lifestyle changes in the Thai guideline.