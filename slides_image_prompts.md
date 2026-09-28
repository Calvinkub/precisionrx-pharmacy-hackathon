# PrecisionRx — Image-Generation Prompts for the Hackathon Submission Deck

> Source of content: `idea.md` (v3), `market_research.md`, `business_strategy.md`, `business_case.md`, `idea_validation.md`.
> Structure: case-competition-slides skill (answer-first, action titles, pyramid, appendix for Q&A) + pitch-deck-strategist agent (rubric mapping, hook, demo peak, Q&A backup).
> Deck type: dense, detail-rich **submission deck** (read by judges without a presenter), 24 main slides + 6 appendix slides.

---

## How to use this file

1. Paste the **Global Style Block** (§1) at the top of **every** prompt, then paste the slide's own prompt. Consistency comes from repeating the same style block every time.
2. Use a model that renders text well (for example GPT-Image, Gemini image / "Nano Banana Pro", Ideogram, or FLUX with text support). Set aspect ratio **16:9**, and the highest resolution available (target 1920×1080 or 2560×1440).
3. All slide text is in **English**, because image models misspell Thai script often. If the event needs Thai, generate the layout first, then overlay the Thai text in Keynote/PowerPoint/Canva.
4. **Always proofread every number on the image** against this file. Image models change digits. If a number is wrong, regenerate or fix it with an editor.
5. Dense slides with many numbers often come out better as a real slide. The same content can be rendered as an editable HTML/PPTX deck with the case-competition-slides skill.
6. Placeholders in `[BRACKETS]` must be filled before generation (team name, event name, date).
7. Every number on a slide has a source footnote. Numbers marked "(assumption)" are team estimates. Keep that word on the slide.

### Titles test (read titles only, top to bottom)

1. PrecisionRx — gene results that act at the moment of prescribing
2. PrecisionRx turns existing PGx results into prescribing-time alerts and adds an oncology module that unifies cfDNA, germline PGx and drug interactions
3. Thai patients already pay for gene tests, but no Thai EHR warns the prescriber — and a patient has died from it
4. Adding more alerts is not the answer: doctors already override about 90% of interaction alerts
5. Three forces make 2026 the right moment: aging, expanding PGx coverage and a national PGx data layer
6. Two modules, one principle: rules decide, AI only explains, clinicians sign
7. The system changes ten specific prescribing decisions, each anchored to a guideline or drug label
8. A deterministic rule engine does the clinical work; the LLM only writes text from verified facts
9. The prescriber sees one stop card; the pharmacist sees only what needs action
10. In cancer care, cfDNA, germline PGx and TKI interactions produce a decision none of them gives alone
11. Every finding carries its evidence tier, and every sentence traces to a real source
12. Four demo cases show the full path from gene result to signed decision
13. We will prove it with pharmacist-graded cases before any claim of clinical benefit
14. Module A is a ฿20–60M serviceable market today; Module B is a differentiator, not the revenue engine
15. Competitors own pieces; nobody delivers Thai-mapped PGx alerts inside Thai hospital systems
16. Hospitals pay per active PGx patient; cancer centres pay a module licence; labs share revenue
17. Unit economics work at LTV:CAC ≈ 3.4, but hospital ROI depends on billable pharmacist review
18. Base case reaches ฿9.6M revenue in year 3 and monthly break-even around month 45–50
19. We start with private hospitals that already sell PGx, then enter public hospitals through the HIS vendor
20. Technically feasible now: every data input and building block already exists
21. Regulatory feasibility: we stay on the low-risk side by consuming only accredited lab results
22. A 6-month pilot with numeric targets and kill criteria decides go or no-go
23. Five risks could stop us; each has a mitigation and an early warning signal
24. We ask for one pilot hospital, one data partnership and mentor access
25. Appendix

---

## 1. Global Style Block (paste before every slide prompt)

```
STYLE: Professional consulting-grade presentation slide, 16:9, 1920x1080, flat vector design, clean Swiss grid layout, high information density but perfectly organized, generous but consistent margins (80 px), crisp sharp readable typography, no photorealism, no 3D, no stock-photo people, no gradients except very subtle ones, no clutter, no decorative emojis, no AI-looking glow.
BRAND: Product name "PrecisionRx". Palette: deep navy #0B2545 (primary, titles, header bar), teal #13A89E (accent, highlights, key numbers), soft white background #F7F9FB, mid-grey #5B6770 (body text), light grey #E3E8EE (panels, table rows), alert red #D64545 (only for STOP / risk), amber #E8A33D (only for warnings). 
TYPOGRAPHY: Modern geometric sans-serif (like Inter or IBM Plex Sans). Title at top-left, bold, navy, 40 px, one sentence. Body 18–22 px. Footnotes 12 px grey at bottom-left. All text must be spelled exactly as given in quotes, in English, no invented words, no lorem ipsum.
LAYOUT CONVENTIONS: Thin teal line under the title. Small slide number bottom-right in grey. Small "PrecisionRx | [TEAM NAME] | [EVENT NAME]" footer bottom-right. Icons are simple line icons, 2 px stroke, navy or teal. Tables have light grey alternating rows and navy header row with white text. Charts are flat, labeled directly, no 3D, no shadows.
```

**Negative prompt (if the model supports it):**
`blurry text, misspelled words, gibberish text, extra digits, distorted numbers, cartoon style, 3D render, photo of doctor, stock photo, neon, purple gradient, busy background, watermark, cropped text, overlapping text`

---

## 2. Slide prompts — Main deck

### Slide 1 — Title

**Action title:** PrecisionRx — gene results that act at the moment of prescribing

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Title slide. Left 60%: large bold navy headline "PrecisionRx". Below it, a teal subtitle "Gene results that act at the moment of prescribing". Below that, grey text on two lines: "Pharmacogenomic clinical decision support for Thai hospitals" and "+ Oncology pharmacy module: cfDNA · germline PGx · TKI interactions". At the bottom-left: "[TEAM NAME]  ·  [EVENT NAME]  ·  [DATE]".
Right 40%: a clean flat vector illustration: a stylised DNA double helix in teal that turns into a line of a prescription order form, ending in a small shield icon with a check mark. Navy and teal only, lots of white space.
No slide number on this slide.
```

---

### Slide 2 — Executive summary (the answer)

**Action title:** PrecisionRx turns existing PGx results into prescribing-time alerts and adds an oncology module that unifies cfDNA, germline PGx and drug interactions

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Executive summary slide. Title at top: "PrecisionRx turns existing PGx results into prescribing-time alerts, plus an oncology module that unifies cfDNA, germline PGx and drug interactions".
Top band (full width, light teal panel): bold text "Recommendation: Deploy PrecisionRx as a PGx alert layer inside the hospital system (HIS), starting with private hospitals that already sell PGx tests, and run a 6-month pilot with numeric go/no-go gates."
Below, three equal columns, each with a navy number circle, a bold heading and 3 bullet lines:
Column 1 — "1  The problem is real and fatal"
 • "No PGx alert system is connected to any Thai EHR (2022)"
 • "A HLA-B*15:02-positive patient received carbamazepine and died"
 • "96% of 4,662 Thai adults carry at least one actionable PGx result"
Column 2 — "2  The solution fits the workflow"
 • "Alerts appear inside the prescribing screen (CDS Hooks)"
 • "Only actionable findings are shown; the rest are collapsed"
 • "Rules decide; AI only explains; every sentence cites a source"
Column 3 — "3  The model is viable and testable"
 • "฿300–480 per active PGx patient per year (assumption)"
 • "LTV:CAC ≈ 3.4, payback ≈ 13 months (assumption)"
 • "Pilot gate: zero critical omissions, ≥70% pharmacist acceptance"
Bottom strip with three big teal numbers side by side, each with a small grey label: "96%" label "Thai adults with ≥1 actionable PGx result"; "~90%" label "interaction alerts overridden by doctors"; "฿9.6M" label "year-3 revenue, base case (assumption)".
Footnote: "Sources: PMC9016335; PLoS One 2026 (n=4,662); Felisberto et al., Health Informatics J 2024; team business case (assumptions)."
```

---

### Slide 3 — Problem 1

**Action title:** Thai patients already pay for gene tests, but no Thai EHR warns the prescriber — and a patient has died from it

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Problem slide. Title: "Thai patients already pay for gene tests, but no Thai EHR warns the prescriber — and a patient has died from it".
Left half: a horizontal flow diagram of 4 boxes connected by arrows, left to right: box 1 "Gene test done" (icon: test tube), box 2 "Result on paper card or PDF" (icon: document), box 3 "Doctor prescribes carbamazepine — no warning" (icon: prescription pad, amber outline), box 4 "SJS/TEN → death" (icon: warning triangle, red outline). Under the flow, a grey quote box in italics: "\"There is currently no PGx alert system connected with the electronic health records (EHR) in Thailand.\" — Ramathibodi PGx study, 2022".
Right half: a simple vertical bar chart titled "HLA-B tests at Ramathibodi". Two bars only: 2011 = "94", 2020 = "2,880" (teal, labeled on top). Caption under chart: "≈30× growth in 10 years". Below the chart, three stat tiles in a row: "96%" label "Thai adults with ≥1 CPIC-actionable genotype (n=4,662)"; "55%" label "omeprazole users with actionable CYP2C19"; "22–23%" label "statin users with actionable SLCO1B1".
Footnote: "Sources: PMC9016335 (Ramathibodi 2011–2020, 13,985 tests); PLoS One Aug 2026, Thai SNP-array cohort n=4,662."
```

---

### Slide 4 — Problem 2

**Action title:** Adding more alerts is not the answer: doctors already override about 90% of interaction alerts

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Problem slide. Title: "Adding more alerts is not the answer: doctors already override about 90% of interaction alerts".
Left third: a large donut chart, 90% segment grey labeled "Overridden ~90%", 10% segment teal labeled "Acted on". Center of donut: "~90%". Caption: "Physician override of drug-interaction alerts, meta-analysis of 16 studies (95% CI 85–95%)".
Middle third: heading "Even PGx alerts are ignored when they are noisy". Three horizontal bars: "Average PGx alert acceptance" = 63%; "CYP2C19–clopidogrel (lowest of 6 pairs)" = as low as 22%; "Accepted alert → real change in therapy" = 47%. Bars teal, values labeled at bar ends.
Right third: heading "Nobody sees the treatment trajectory". One big stat: "24.4%" label "ACS patients with a repeat LDL-C test within 120 days". Below: small line icon of a chart with a question mark, and text "Doctors see one value, not whether the drug works".
Bottom teal banner: "Design rule for PrecisionRx: remove noise first. Show only findings with a clear action."
Footnote: "Sources: Felisberto et al., Health Informatics J 2024; PMC10726431; Thai tertiary hospital ACS cohort (market_research.md S24)."
```

---

### Slide 5 — Why now

**Action title:** Three forces make 2026 the right moment: aging, expanding PGx coverage and a national PGx data layer

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Why-now slide. Title: "Three forces make 2026 the right moment: aging, expanding PGx coverage and a national PGx data layer".
Three tall vertical cards side by side, each with a line icon at top, a big teal number, a bold heading and 3 bullets:
Card 1 icon elderly person — big number "21.82%" — heading "Complete aged society" — bullets: "14.14 million Thais aged 60+ (2025)"; "Polypharmacy 59.5% in elderly OPD, secondary hospitals, Region 8"; "More drugs per patient = more gene–drug conflicts".
Card 2 icon shield with plus — big number "3 genes" — heading "Public coverage is expanding" — bullets: "NHSO covers HLA-B*15:02 and HLA-B*58:01 testing"; "Gold Card via Ramathibodi genomics centre: HLA-B*15:02, CYP2C19, CYP2C9"; "Volume of PGx results will rise fast".
Card 3 icon database with link — big number "11 hospitals" — heading "A national PGx data layer exists" — bullets: "Pook-Phan app (Dept. of Medical Sciences + Mahidol) stores lifetime drug-allergy genes"; "ThaiD identity + patient consent"; "Missing piece: the alert at the moment of prescribing".
Bottom strip, grey: "Evidence base: PREPARE trial (Lancet 2023) — preemptive 12-gene panel, clinically relevant ADR 21.0% vs 27.7%, OR 0.70 (95% CI 0.54–0.91). European population; no Thai outcome data yet."
Footnote: "Sources: Dept. of Provincial Administration 2025; Region 8 OPD study (n=587,905); NHSO; Hfocus Jul 2026; Thai PBS; Swen et al., Lancet 2023."
```

---

### Slide 6 — Solution overview

**Action title:** Two modules, one principle: rules decide, AI only explains, clinicians sign

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Solution overview slide. Title: "Two modules, one principle: rules decide, AI only explains, clinicians sign".
Top center: one-line teal statement in a rounded box: "Gene results patients already paid for must be used every time a new drug is prescribed."
Middle: two large side-by-side panels.
Left panel (navy header "MODULE A — PGx at prescribing (core)"): three rows with icons: "Input: germline PGx results (Pook-Phan, PGx labs) + medication orders from HIS"; "Action: hard stop or guidance card in the doctor's ordering screen; pharmacist review queue"; "Drugs first: carbamazepine, allopurinol, PPIs, statins, clopidogrel". Small sub-box at bottom: "Phase 2: Response module — ApoB + Reference Change Value + adherence (PDC)".
Right panel (teal header "MODULE B — Oncology pharmacy"): three rows: "Input: cfDNA/ctDNA variant report + germline DPYD/UGT1A1 + TKI medication list"; "Action: one report for oncology pharmacist and oncologist"; "Checks: targetable variant tier, TKI–PPI interaction, chemo toxicity genes, CHIP and germline flags".
Bottom: a horizontal 3-step band with icons: "RULES DECIDE (deterministic, unit-tested code)" → "AI EXPLAINS (LLM writes only from verified fact IDs)" → "CLINICIANS SIGN (pharmacist reviews, doctor decides)".
Small grey disclaimer under band: "Not a diagnosis tool. Not a prescribing tool. Clinical decision support only."
```

---

### Slide 7 — Decisions changed

**Action title:** The system changes ten specific prescribing decisions, each anchored to a guideline or drug label

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Dense table slide. Title: "The system changes ten specific prescribing decisions, each anchored to a guideline or drug label".
A full-width table with navy header row and 5 columns: "#", "Situation", "Data used", "What the system does", "Evidence". 10 rows, alternating light grey:
1 | "Carbamazepine in HLA-B*15:02 positive" | "Germline PGx" | "HARD STOP at order entry" | "CPIC + NHSO coverage"
2 | "Allopurinol in HLA-B*58:01 positive" | "Germline PGx" | "HARD STOP at order entry" | "CPIC + NHSO coverage"
3 | "PPI in CYP2C19 ultrarapid / poor metabolizer" | "Germline PGx" | "CPIC PPI dose guidance" | "CPIC"
4 | "Simvastatin 40 mg in SLCO1B1 decreased function" | "Germline PGx" | "Alternative statin or limit to <20 mg/day" | "CPIC 2022, Strong"
5 | "Clopidogrel in CYP2C19 poor metabolizer (ACS/PCI)" | "Germline PGx" | "Avoid if possible; prasugrel or ticagrelor if no contraindication" | "CPIC 2022, Strong"
6 | "Clopidogrel + omeprazole/esomeprazole" | "Medication list" | "Avoid combination; suggest pantoprazole" | "Plavix label"
7 | "LDL-C at goal but ApoB above secondary goal" | "Lab (ApoB)" | "Show discordance + real change vs baseline (RCV)" | "ESC/EAS"
8 | "NSCLC progressing on EGFR TKI" | "cfDNA" | "Variant tier + labeled therapy → oncologist" | "Companion Dx / guideline"
9 | "Gefitinib/erlotinib + PPI" | "Medication list" | "Avoid PPI or separate dosing (erlotinib AUC −46% with omeprazole)" | "IRESSA / TARCEVA labels"
10 | "Before capecitabine/5-FU or irinotecan" | "Germline PGx" | "Flag DPYD / UGT1A1 → dose review" | "CPIC / DPWG"
Rows 1, 2 have a small red "STOP" tag. Rows 8, 9, 10 have a small teal "ONCOLOGY" tag. Rows 1, 3, 4, 8–10 have a small navy star meaning "in demo".
Legend under table: "★ = shown in demo   STOP = hard stop   ONCOLOGY = Module B".
Footnote: "CPIC wording quoted from CPIC 2022 statin and clopidogrel guidelines; PPI wording to be checked against current CPIC guideline before submission."
```

---

### Slide 8 — Architecture

**Action title:** A deterministic rule engine does the clinical work; the LLM only writes text from verified facts

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Technical architecture diagram slide. Title: "A deterministic rule engine does the clinical work; the LLM only writes text from verified facts".
Diagram flows top to bottom in 6 horizontal layers, each a rounded rectangle with a label on the left in navy bold:
Layer 0 "DATA SOURCES": three small boxes "Pook-Phan / PGx labs", "Liquid biopsy lab", "Hospital HIS (e.g. HOSxP)". Arrows go down labeled "HL7 FHIR: Patient · MedicationRequest · Observation · DiagnosticReport · Genomics Reporting IG".
Layer 1 "DETERMINISTIC ENGINES (unit-tested code)": six small boxes in a row: "PGx: PharmCAT → CPIC/DPWG + Thai drug codes (TMT)", "DDI rules (licensed database)", "Alert filter: actionable only", "Oncology: AMP/ASCO/CAP tier + CHIP + germline flags", "Response: RCV change test (phase 2)", "Adherence: PDC from refills".
Layer 2 "EVIDENCE STORE": one wide box "Versioned snapshot · every fact has ID + source + evidence tier · CPIC · PharmGKB · drug labels · ClinVar · OncoKB (licensed)".
Layer 3 "DELIVERY": two boxes: "CDS Hooks card in ordering screen (hard stop / guidance)" and "Pharmacist review queue (accept / modify / reject)".
Layer 4 "LLM LAYER (2 agents only)": two boxes: "Summarizer — writes brief from fact IDs only" and "Q&A agent — answers clinician questions, must cite fact IDs".
Layer 5 "VERIFIER + AUDIT": one wide box "Every sentence ↔ existing fact ID; unsupported sentences removed · audit log · sign-off · fixed model/prompt/evidence versions · temperature 0".
Right margin: a vertical teal bracket around layers 1–2 labeled "Same input → same output"; a vertical grey bracket around layer 4 labeled "Language only, no new facts".
Bottom-right small box, amber outline: "Privacy: genome data stays in Thailand; on-prem or Thai-hosted LLM; de-identified facts only; prompt-injection filter on free text".
Footnote: "LLM cost ≈ ฿35 per report (assumption); main cost is evidence curation and support."
```

---

### Slide 9 — User interface

**Action title:** The prescriber sees one stop card; the pharmacist sees only what needs action

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Product UI mockup slide. Title: "The prescriber sees one stop card; the pharmacist sees only what needs action".
Two flat UI mockups side by side inside simple browser/window frames (flat vector, not photographic).
Left mockup, label above it "Doctor — ordering screen (CDS Hooks card)": a grey hospital ordering form in the background, and on top a card with a red left border: red header "STOP — Carbamazepine"; text lines "HLA-B*15:02 POSITIVE (source: Pook-Phan, 2024-03-12)"; "CPIC: do not use — risk of SJS/TEN"; small navy tag "Guideline". Three buttons: "Why?", "Choose another drug", "Override + reason → notify pharmacist".
Right mockup, label above it "Pharmacist — review queue": section header "ACTION NEEDED (2)" with two amber-bordered cards: card 1 "Simvastatin 40 mg — SLCO1B1 decreased function", sub-text "CPIC 2022: alternative statin, or limit to <20 mg/day", tag "Guideline", buttons "Why? · Accept · Modify · Reject"; card 2 "Omeprazole — CYP2C19 ultrarapid metabolizer", sub-text "CPIC: consider dose increase", tag "Guideline", same buttons. Section header "MONITOR" with one grey line "ApoB −6% vs baseline — within normal variation (RCV)". Section header "NO ACTION" with one collapsed line "7 other checks passed".
Bottom callouts with thin teal lines pointing to UI parts: "Hard stop only for life-threatening gene–drug pairs"; "'Why?' opens the real rule trace, not an AI story"; "Non-actionable checks collapsed to fight alert fatigue".
```

---

### Slide 10 — Oncology cfDNA module

**Action title:** In cancer care, cfDNA, germline PGx and TKI interactions produce a decision none of them gives alone

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Oncology module slide. Title: "In cancer care, cfDNA, germline PGx and TKI interactions produce a decision none of them gives alone".
Left 45%: a three-circle Venn diagram. Circle 1 teal "Tumour DNA (cfDNA/ctDNA)" with small text "Which target? Why resistant? No repeat biopsy". Circle 2 navy "Patient DNA (germline PGx)" with small text "DPYD · UGT1A1 · CYP2C19: which chemo is tolerated?". Circle 3 grey "Medication list" with small text "TKI–PPI and CYP3A4 interactions". Center overlap label bold: "Oncology pharmacist decision".
Right 55%: two stacked panels.
Panel top, heading "Thai relevance": three stat tiles: "23,871" label "new lung cancers per year in Thailand (GLOBOCAN 2024)"; "47–56%" label "EGFR mutation in Thai NSCLC studies"; "erlotinib" label "first-line EGFR TKI reimbursed by CSMBS from 1 Dec 2025".
Panel bottom, heading "Safety flags the system always shows" as a 5-row checklist with small icons:
 "ctDNA not detected ≠ no mutation → consider tissue biopsy";
 "DNMT3A / TET2 / ASXL1 variants → possible clonal hematopoiesis (CHIP)";
 "VAF ~50% or ~100% in BRCA1/2 → possible germline → genetic counselling";
 "ctDNA dynamics for response → tagged 'Emerging'";
 "Separate blood tube for cfDNA (stabilizing tube or time-limited processing)".
Bottom teal strip: "Business role: licence per cancer centre (all cancer patients), not a per-cfDNA-report business. Thai TAM for cfDNA reports alone ≈ ฿11–27M/year (assumption)."
Footnote: "Sources: GLOBOCAN 2024 Thailand; Ramathibodi EGFR cohort 56.3%; Thai tertiary hospital NSCLC 47%; OCPA 2025 notice; IRESSA/TARCEVA labels."
```

---

### Slide 11 — Safety and honesty

**Action title:** Every finding carries its evidence tier, and every sentence traces to a real source

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Safety slide. Title: "Every finding carries its evidence tier, and every sentence traces to a real source".
Left 40%: three stacked horizontal tags, each a coloured pill with explanation:
 navy pill "GUIDELINE" — "CPIC level A/B, drug label, companion diagnostic";
 amber pill "EMERGING" — "published research, not yet in guidelines (ctDNA dynamics, pharmacometabolomics)";
 grey pill "UNKNOWN" — "variant of uncertain significance, no data → never used for action".
Right 60%: a vertical "Why?" trace diagram, 5 boxes connected by down arrows: "Conclusion: avoid simvastatin 40 mg" → "Engine: PGx engine v1.3" → "Rule: CPIC 2022 SLCO1B1 decreased function → alternative statin or <20 mg/day (fact ID CPIC-STAT-014)" → "Patient data: SLCO1B1 *1/*5, simvastatin 40 mg daily" → "Source: CPIC statin guideline 2022, Strong". Side label: "Real reasoning path, not a generated narrative".
Bottom band, three items with shield icons: "Verifier removes any sentence without a valid fact ID"; "No claim of accuracy or outcome from synthetic data"; "Audit log of every input, output, override and sign-off".
Footnote: "Fact ID and version shown are illustrative examples for the demo."
```

---

### Slide 12 — Demo cases

**Action title:** Four demo cases show the full path from gene result to signed decision

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Demo overview slide. Title: "Four demo cases show the full path from gene result to signed decision".
Four equal cards in a 2×2 grid. Each card: a letter badge, a patient line, a scenario, and "What it shows".
Card A (red badge "A — OPENING"): "Male, 34, epilepsy"; "Doctor orders carbamazepine; HLA-B*15:02 positive stored in Pook-Phan"; "Shows: hard stop in the ordering screen".
Card B (navy badge "B"): "Female, 52"; "Simvastatin 40 mg + omeprazole; SLCO1B1 decreased + CYP2C19 ultrarapid"; "Shows: two PGx findings in one card, 'Why?' trace, pharmacist accepts".
Card C (grey badge "C — PHASE 2"): "Same patient, 3 months later"; "LDL-C at goal, ApoB above secondary goal, adherence PDC 92%"; "Shows: response module, RCV, adherence check".
Card D (teal badge "D — cfDNA"): "Male, 64, EGFR+ NSCLC"; "On erlotinib + omeprazole, progressing; ctDNA shows resistance mutation + DNMT3A variant; capecitabine planned"; "Shows: variant tier → oncologist, TKI–PPI flag, CHIP flag, DPYD check".
Under the grid, a horizontal 5-step path with icons: "Gene result arrives" → "Rule engine fires" → "Card / queue item" → "Pharmacist accept/modify/reject" → "Signed report to doctor".
Grey badge top-right of slide: "All demo patients are synthetic".
```

---

### Slide 13 — Evaluation plan

**Action title:** We will prove it with pharmacist-graded cases before any claim of clinical benefit

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Evaluation slide. Title: "We will prove it with pharmacist-graded cases before any claim of clinical benefit".
Left half, heading "Hackathon evaluation": text "Gold-standard set: 30–50 synthetic cases covering all 10 decisions, answer key by 2–3 pharmacists". Below, a metrics table with columns "Metric" and "Target":
 "Critical-omission rate" | "0"
 "Citation precision" | "≥ 99%"
 "Concordance with CPIC (PharmCAT + mapping)" | "100%"
 "False-flag rate" | "report"
 "Alerts per case vs standard DDI checker" | "≥ 50% fewer"
 "Inter-rater agreement between pharmacists" | "ceiling of system"
Small note: "Regression tests run on every prompt, model or evidence change".
Right half, heading "Pilot evaluation (6 months, 1 hospital)": a horizontal timeline with two segments: "Months 0–2: retrospective replay, n ≥ 300, no effect on care" and "Months 3–6: live use, ~150–200 reviews". Below, target tiles: "0 critical omissions (go/no-go)", "≥70% pharmacist acceptance", "≥50% physician acceptance", "≥30% less review time". Below, expected yield: "Expected actionable findings per 100 patients: ~55 in omeprazole users, ~22 in statin users".
Bottom red-outlined strip: "We do not claim ADR reduction from the pilot. We do not claim accuracy from synthetic data."
Footnote: "Expected yield from PLoS One 2026 Thai cohort; targets from business_strategy.md."
```

---

### Slide 14 — Market sizing

**Action title:** Module A is a ฿20–60M serviceable market today; Module B is a differentiator, not the revenue engine

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Market sizing slide. Title: "Module A is a ฿20–60M serviceable market today; Module B is a differentiator, not the revenue engine".
Left 55%: three nested concentric circles (TAM > SAM > SOM) for Module A, teal shades from light to dark. Labels:
 Outer "TAM ฿0.41–0.83 billion/yr — 1,376 hospitals (324 tertiary + 682 secondary public + 370 private) × ฿300k–600k";
 Middle "SAM ฿18–60M/yr — 60–100 hospitals with PGx or preventive/lipid clinics";
 Inner "SOM year 3 ฿2–6M/yr — 5–10 hospitals".
Right 45%: a smaller identical set of circles in grey for Module B with labels: "TAM ≈ ฿11–27M/yr — ≈7,400–8,900 cfDNA reports × ฿1,500–3,000"; "SAM ≈ ฿2–8M/yr"; "SOM year 3 ≈ ฿0.3–1.2M/yr".
Under Module B: a small funnel with steps "23,871 lung cancers → 85% NSCLC → ~70% advanced (assumption) → cfDNA at diagnosis 20–30% + at resistance".
Bottom, two teal insight boxes: "Cross-check: ฿400 per patient per year vs ฿14,751 PGx panel → software is ~37× cheaper than the test it makes useful"; "Bottom-up denominators are sourced; all prices are assumptions not yet confirmed by any customer".
Footnote: "Sources: WHO Pharmaceutical Country Profile 2025; Krungsri Research (private hospitals, older data); BDMS 2026; GLOBOCAN 2024; N Health price on HDmall. Prices = team assumptions."
```

---

### Slide 15 — Competitive landscape

**Action title:** Competitors own pieces; nobody delivers Thai-mapped PGx alerts inside Thai hospital systems

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Competitive landscape slide. Title: "Competitors own pieces; nobody delivers Thai-mapped PGx alerts inside Thai hospital systems".
Top 60%: a feature comparison matrix. Rows (players): "Status quo (PDF / card)", "Pook-Phan (Thai govt)", "PharmCAT (open source)", "Lexidrug / Micromedex", "Epic genomics", "Nalagenetics (SEA)", "Tabula Rasa MedWise (US)", "QIAGEN QCI / Roche navify / OncoKB", "HOSxP (HIS)", "PrecisionRx". Columns: "Stores PGx result", "CPIC logic", "Alert at prescribing", "Thai drug codes + NHSO rules", "Pharmacist workflow", "Oncology cfDNA + germline + DDI". Cells use filled teal circle (yes), half circle (partial), empty circle (no). PrecisionRx row highlighted with teal background and all columns filled. Pook-Phan row: stores = full, others mostly empty. PharmCAT: CPIC logic = full. Lexidrug: CPIC logic = half. Epic: CPIC logic = full, alert = full, Thai = empty. Nalagenetics: CPIC = full, alert = half, Thai = empty. MedWise: pharmacist workflow = full, CPIC = half. Oncology tools: oncology column = half. HOSxP: alert at prescribing = half (general drug-allergy only).
Bottom 40%, two columns:
Left, heading "How we treat them": "Pook-Phan, PGx labs = data sources"; "PharmCAT = our engine (not our moat)"; "HOSxP = channel, not rival"; "Nalagenetics = most direct regional threat".
Right, heading "Why won't the HIS vendor just build it?": "They can — Epic did. The real cost is keeping evidence current, Thai drug mapping, liability and Thai FDA burden. A US PGx CDS company stopped the service after failing FDA 510(k). We sell fewer alerts, and plug into the HIS instead of competing with it."
Footnote: "Sources: Thai PBS; PharmCAT GitHub; Nalagenetics CE-mark release; MobiHealthNews; HOSxP site; market_research.md §4. Moat = time and focus, not impossibility."
```

---

### Slide 16 — Business model

**Action title:** Hospitals pay per active PGx patient; cancer centres pay a module licence; labs share revenue

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Business model slide. Title: "Hospitals pay per active PGx patient; cancer centres pay a module licence; labs share revenue".
Top 45%: a money-flow diagram. Center box navy "PrecisionRx (interpretation layer, lab-agnostic)". Three payer boxes around it with teal arrows pointing into the center:
 left "Private hospital (Module A)" arrow label "Setup ฿250,000 + ฿300–480 per active PGx patient/yr (min. 1,000 patients)";
 right "Cancer centre (Module B)" arrow label "Module licence or ฿3,000 per oncology report";
 bottom "PGx / liquid biopsy lab" arrow label "฿500 revenue share per result".
Grey arrows out of the center to "Doctor (alert)", "Pharmacist (queue)", "Patient (fewer ADRs)" labeled "value".
Bottom 55%: a 3-column table titled "Who uses, who buys, who benefits" with rows:
 "User" | "Doctor + pharmacist" | "Oncology pharmacist + oncologist"
 "Buyer" | "Hospital executive; approved by Pharmacy & Therapeutics Committee, IT, DPO" | "Cancer centre"
 "Beneficiary" | "Patient; hospital (PGx tests it sold now used)" | "Patient; cancer centre"
Column headers: "", "Module A — PGx at prescribing", "Module B — Oncology pharmacy".
Side note box: "We do not sell lab tests. Insurers never see individual genetic data, only aggregate outcomes."
Footnote: "All prices are assumptions to validate with customers. ฿3,000 per report is <5% of one month of osimertinib (≈ USD 1,963/month, PubMed 41455170)."
```

---

### Slide 17 — Unit economics and customer ROI

**Action title:** Unit economics work at LTV:CAC ≈ 3.4, but hospital ROI depends on billable pharmacist review

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Financial slide. Title: "Unit economics work at LTV:CAC ≈ 3.4, but hospital ROI depends on billable pharmacist review".
Left 50%, heading "Our unit economics (Module A, per hospital)": a row of 5 KPI tiles: "67%" label "contribution margin"; "฿400k" label "CAC"; "฿1.36M" label "LTV"; "3.4×" label "LTV:CAC"; "13 mo" label "payback". Under it a small grey line: "Including year-3 curation cost: LTV:CAC ≈ 2.0, payback ≈ 23 months". Below, a sensitivity table titled "Price sensitivity": columns "Price per patient/yr" and "LTV:CAC": "฿480" = "3.4"; "฿360" = "2.2"; "฿300" = "1.6".
Right 50%, heading "Hospital ROI (per year)": a horizontal waterfall-style bar chart:
 bar "Pharmacist time saved" +฿133k;
 bar "ADRs avoided (฿7,215 per admission)" +฿75k;
 marker "ROI without billing ≈ 0.37× — does not pay";
 bar "Billable pharmacist PGx review (~฿700 × ≥510/yr)" large teal bar;
 marker "ROI with billing ≈ 2.2×".
Amber callout box: "Key assumption to validate first: the hospital can bill patients for pharmacist PGx review, or include it in the PGx package price."
Footnote: "Sources: Thai ADR admission cost (Pharmacy Practice); Mayo Clinic PGx consult time 24 min (PubMed 37478473); all other values are assumptions in business_case.md."
```

---

### Slide 18 — 3-year projection

**Action title:** Base case reaches ฿9.6M revenue in year 3 and monthly break-even around month 45–50

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Financial projection slide. Title: "Base case reaches ฿9.6M revenue in year 3 and monthly break-even around month 45–50".
Left 60%: grouped bar chart titled "Revenue, base case (฿ million)". Three bars: "Year 1" = "0.5", "Year 2" = "3.4", "Year 3" = "9.6", teal, values on top. Under each bar small grey text: Year 1 "1 pilot hospital", Year 2 "~5 hospitals + 1 cancer centre", Year 3 "12 hospitals + 3 cancer centres". A thin dotted line annotation beyond year 3: "Monthly break-even ≈ month 45–50 (run-rate ≈ ฿19–21M/yr)".
Right 40%: a scenario table with columns "Scenario", "Year-3 outcome", "Cash need":
 "Base" | "Break-even month 45–50" | "≈ ฿25M trough, ≈ ฿30M with buffer"
 "Upside" | "Break-even in year 3" | "lower"
 "Downside" | "Loses ≈ ฿27M, no break-even" | "stop at kill gate"
Below the table: "Team: 5 → 11 people. Year-1 cash need ≈ ฿7M."
Bottom teal strip: "Kill/pivot rules at month 12 and month 24 (see Feasibility plan)."
Footnote: "All figures are team assumptions from business_case.md; Year-2 customer count is illustrative. Not a forecast of certainty."
```

---

### Slide 19 — Go-to-market and partnerships

**Action title:** We start with private hospitals that already sell PGx, then enter public hospitals through the HIS vendor

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Go-to-market slide. Title: "We start with private hospitals that already sell PGx, then enter public hospitals through the HIS vendor".
Top 50%: a staircase diagram with 3 steps rising left to right:
 Step 1 (teal) "Beachhead: private hospitals that already sell PGx" with sub-lines "Bangkok Hospital (PGx NGS 500+ drugs) · BNH (126 drugs) · Samitivej Genomics Center · Bumrungrad · N Health"; "BDMS group: 60 hospitals — win 1, expand inside the group"; "Pitch: 'the gene results your patients paid for, used at every new prescription'".
 Step 2 (navy) "Cancer centres: Module B licence".
 Step 3 (grey) "Public hospitals: PGx connector via the HIS vendor for Gold-Card genes".
Small red note under step 1: "No hospital contacted yet — pipeline is zero today".
Bottom 50%: a horizontal numbered partnership sequence with 7 circles and arrows: "1 Pharmacy faculty (validation)" → "2 One private hospital (pilot)" → "3 PGx lab" → "4 HIS vendor (FHIR sandbox)" → "5 Liquid biopsy lab / cancer centre" → "6 NMR lab (research only)" → "7 Insurers / NHSO (18+ months)". Under each circle a tiny time tag: "M0", "M0–3", "M3", "M6–12", "M9–18", "M18+", "M18+".
Footnote: "Sources: hospital websites (Bangkok Hospital, BNH, Samitivej, Bumrungrad, N Health); BDMS 2026 annual data."
```

---

### Slide 20 — Feasibility plan 1: technical

**Action title:** Technically feasible now: every data input and building block already exists

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Feasibility slide (technical). Title: "Technically feasible now: every data input and building block already exists".
Left 55%: a table with columns "Component", "Exists today?", "How we use it", "Readiness":
 "Germline PGx results" | "Yes — Pook-Phan, Rama PPM, private PGx labs" | "FHIR / file import" | green dot
 "CPIC logic" | "Yes — PharmCAT open source" | "Engine core" | green dot
 "Order-time alert standard" | "Yes — HL7 CDS Hooks, FHIR" | "Card in ordering screen" | green dot
 "Thai drug codes" | "Yes — TMT" | "Map CPIC drugs to TMT" | amber dot
 "DDI knowledge" | "Yes — licensed databases, drug labels" | "Rule engine" | amber dot (licence)
 "cfDNA variant reports" | "Yes — liquid biopsy labs" | "Structured import + tiering" | amber dot
 "Oncology knowledge base" | "Yes — OncoKB (commercial licence)" | "Evidence store" | amber dot
 "Clinical NMR lab in Thailand" | "Not confirmed" | "Phase 2–3, research only" | red dot
 "HOSxP PGx field / API" | "Not confirmed" | "Integration partner needed" | red dot
Right 45%, heading "What we build in the hackathon": checklist with teal ticks: "PGx engine on PharmCAT + TMT mapping for demo drugs"; "CDS Hooks mock of the ordering screen"; "Pharmacist review queue UI"; "Oncology module on synthetic cfDNA reports"; "Evidence store + verifier + 'Why?' trace"; "30–50 case evaluation harness".
Below: small stack row "Stack: Python rule engines · FHIR JSON · CDS Hooks · PostgreSQL evidence store · Thai-hosted or on-prem LLM · web UI".
Bottom strip: "Legend: green = available now · amber = available, needs licence or mapping · red = unconfirmed, not needed for Module A launch".
```

---

### Slide 21 — Feasibility plan 2: regulatory and legal

**Action title:** Regulatory feasibility: we stay on the low-risk side by consuming only accredited lab results

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Feasibility slide (regulatory). Title: "Regulatory feasibility: we stay on the low-risk side by consuming only accredited lab results".
Top: a wide quote box, navy border, heading "Intended use (draft)": "PrecisionRx applies published pharmacogenomic guidelines and drug-label rules to existing accredited laboratory results (germline pharmacogenomic genotypes and, for oncology, cfDNA variant reports) and current medications, and presents evidence-linked alerts and summaries to support prescribing and pharmacist medication review. It does not diagnose disease or select treatment; all recommendations require clinician review."
Middle: a 2×3 grid of cards with icons:
 "Medical device (SaMD)": "Likely a medical device under the Thai Medical Device Act → consult Thai FDA on class. Regional peer Nalagenetics needed CE mark."
 "Design choice": "No raw spectrum, no variant calling → we never process IVD signals (US FDA CDS guidance, Jan 2026: signal processing = device)."
 "PDPA": "Section 26: health and genetic data are sensitive → explicit, separate consent for PGx and cfDNA; no transfer abroad; DPO."
 "Lab quality": "Accept results only from ISO 15189 labs; research-only results labelled RUO."
 "Professional roles": "Pharmacist recommends, doctor prescribes; every override needs a reason; sign-off logged."
 "Licences and ethics": "OncoKB and DDI database licences; IRB/EC approval before any real patient data."
Bottom grey strip: "US FDA guidance is a reference framework only; it has no legal force in Thailand. Legal review required before claiming PDPA Section 26(5) exemptions."
Footnote: "Sources: Thai Medical Device Act B.E. 2551 (amended 2562); PDPA B.E. 2562 s.26; US FDA CDS guidance (6 Jan 2026); Nalagenetics CE-mark release."
```

---

### Slide 22 — Feasibility plan 3: roadmap and pilot

**Action title:** A 6-month pilot with numeric targets and kill criteria decides go or no-go

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Roadmap / Gantt slide. Title: "A 6-month pilot with numeric targets and kill criteria decides go or no-go".
Top 60%: a horizontal Gantt chart with a month axis "M0 … M24". Rows (bars):
 "Hackathon build + 30–50 case eval" bar at start, teal;
 "Interview 5–10 hospital pharmacists" bar M0–M1;
 "LOI from 1 hospital + talks with Pook-Phan team and HIS vendor" bar M0–M3, with a red diamond at M3 labeled "Gate 1";
 "IRB + Thai FDA consultation" bar M3–M6;
 "Pilot: retrospective replay (n ≥ 300)" bar M3–M5;
 "Pilot: live use (~150–200 reviews)" bar M5–M9, red diamond at M9 labeled "Gate 2";
 "Expand inside hospital group + Module B at 1 cancer centre" bar M9–M18;
 "Response module (ApoB + RCV)" bar M12–M18;
 "NMR research track + Thai reference values; public-hospital connector" bar M18–M24.
Bottom 40%: three gate cards side by side:
 "Gate 1 (M3)": "Go if: 1 hospital LOI + cooperation from Pook-Phan team or HIS vendor. Else: stop or pivot."
 "Gate 2 (M9, pilot end)": "Go if: 0 critical omissions, ≥70% pharmacist acceptance, ≥50% physician acceptance, ≥50% fewer alerts, ≥30% less review time."
 "Kill triggers": "Acceptance <50% · site has <200 patients with PGx results · hospital cannot bill pharmacist review."
Footnote: "Targets from business_strategy.md; timeline indicative."
```

---

### Slide 23 — Risks and mitigations

**Action title:** Five risks could stop us; each has a mitigation and an early warning signal

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Risk slide. Title: "Five risks could stop us; each has a mitigation and an early warning signal".
Left 40%: a 2×2 risk matrix (x-axis "Likelihood", y-axis "Impact") with 5 numbered dots: dot 1 high-high (red), dot 2 high-high (red), dot 3 medium-high (amber), dot 4 medium-medium (amber), dot 5 low-high (amber).
Right 60%: a table with columns "#", "Risk", "Mitigation", "Early signal":
 1 | "Low pharmacist demand (only 7% interpreted PGx last year; 46.3% low PGx knowledge)" | "Only actionable alerts; 'Why?' explanations; built-in training" | "Interview results; pilot acceptance"
 2 | "Hospital cannot bill for pharmacist review → ROI fails" | "Bundle into PGx package price; validate before pilot" | "Answer from hospital finance at LOI stage"
 3 | "Government or HIS vendor builds it" | "Partner as data source/channel; be the HIS module" | "HOSxP or Pook-Phan roadmap"
 4 | "Regional competitor enters (Nalagenetics)" | "Thai drug codes, NHSO rules, HOSxP integration first" | "SEA announcements"
 5 | "Thai FDA classifies as higher-risk device" | "Early consultation; no signal processing; clinician can review basis" | "Thai FDA feedback"
Footnote: "Sources: PubMed 32187156 (survey of Thai hospital pharmacists, from abstract); Nalagenetics release; team analysis."
```

---

### Slide 24 — Team and ask

**Action title:** We ask for one pilot hospital, one data partnership and mentor access

**Prompt:**
```
[GLOBAL STYLE BLOCK]
Closing slide. Title: "We ask for one pilot hospital, one data partnership and mentor access".
Left 50%, heading "Team": four placeholder profile cards with simple line-icon avatars (no photos), each with name and role lines: "[NAME] — Clinical pharmacy / PGx", "[NAME] — AI & software engineering", "[NAME] — Biology / genomics", "[NAME] — Business & regulatory". Under them: "Advisors wanted: oncology pharmacist, hospital IT (HIS), regulatory".
Right 50%, heading "Our ask": three large numbered teal items:
 "1  One pilot hospital that already sells PGx tests";
 "2  Data partnership: Pook-Phan team or a PGx lab + HIS sandbox access";
 "3  Mentors: hospital pharmacy leadership, Thai FDA SaMD process, oncology".
Bottom center, big navy closing line: "The gene results patients already paid for should protect them every time a doctor prescribes."
Small grey line under it: "Status: concept stage — no company, partners or revenue yet."
```

---

## 3. Appendix slides (backup for Q&A)

### Slide 25 — Appendix divider

```
[GLOBAL STYLE BLOCK]
Section divider slide. Solid navy background, large white text centered "Appendix", smaller teal text below "Backup for judge questions". Below, a white list of 6 items: "A1 Response module and RCV method"; "A2 PREPARE evidence in detail"; "A3 Claim verification table"; "A4 Clinical limitations"; "A5 Financial assumptions"; "A6 Market facts and sources".
```

### A1 — Response module and RCV method

**Action title:** A change counts as real only when it exceeds the patient's own normal variation

```
[GLOBAL STYLE BLOCK]
Method slide. Title: "A change counts as real only when it exceeds the patient's own normal variation".
Left 50%: formula box, large and clear: "RCV = √2 × Z × √(CVa² + CVi²)". Under it, a legend: "CVa = analytical variation of the assay (from the lab)"; "CVi = within-person biological variation (EFLM Biological Variation Database)"; "Z = 1.96 (two-sided, 95%) or 1.65 (one-sided)". Decision rule box: "|% change| > RCV → 'real change'  ·  otherwise → 'within normal variation'".
Right 50%: a simple line chart of one patient's ApoB over 3 visits with a shaded teal band around the baseline labeled "RCV band"; the second point inside the band labeled "within variation", third point below the band labeled "real change ↓". Below: bullets "Start with ApoB (standard lab test); add NMR LDL-P/TRL/GlycA only when a Thai clinical NMR lab exists"; "No arrow shown if CVi is unavailable for that analyte"; "Adherence (PDC from refills) checked before calling non-response"; "ApoB is a secondary target in ESC/EAS guidance; LDL-C remains primary".
Footnote: "Illustrative chart; values not from a real patient."
```

### A2 — PREPARE evidence in detail

**Action title:** PREPARE supports preemptive PGx, but it is European evidence and its size of benefit is debated

```
[GLOBAL STYLE BLOCK]
Evidence slide. Title: "PREPARE supports preemptive PGx, but it is European evidence and its size of benefit is debated".
Left: a two-bar chart "Clinically relevant ADR, patients with an actionable result": "Standard care 27.7%" (grey) vs "PGx-guided 21.0%" (teal). Under chart: "OR 0.70 (95% CI 0.54–0.91)".
Right: a fact table: "Journal" = "Lancet 2023;401:347–356"; "Design" = "Open-label, cluster-randomised crossover"; "n" = "6,944 in 7 European countries"; "Panel" = "12 genes, preemptive"; "Guideline used" = "DPWG (not CPIC)"; "Population" = "97.7% European / Mediterranean / Middle Eastern"; "Follow-up" = "12 weeks"; "Debate" = "Lancet letters argue benefits are unclear".
Bottom teal strip: "How we use it: as rationale, never as a promise of the same effect in Thai patients."
Footnote: "Swen et al., Lancet 2023; ACC journal scan 2023; Lancet correspondence 2023."
```

### A3 — Claim verification table

**Action title:** Every number in this deck was checked against a source; unverified items are flagged

```
[GLOBAL STYLE BLOCK]
Dense verification table. Title: "Every number in this deck was checked against a source; unverified items are flagged".
Table columns: "Claim", "Status", "Source". Status uses small coloured pills: green "Verified", amber "Partly / secondary", red "Unverified".
Rows:
 "No PGx alert connected to Thai EHR (2022)" | Verified | "PMC9016335"
 "96% Thai adults with ≥1 actionable PGx result" | Verified | "PLoS One 2026"
 "DDI alert override ~90%" | Verified | "Felisberto 2024"
 "PREPARE OR 0.70" | Verified | "Lancet 2023"
 "CPIC SLCO1B1 simvastatin <20 mg/day" | Verified | "CPIC 2022"
 "CPIC CYP2C19 clopidogrel avoid in PM" | Verified | "CPIC 2022"
 "Clopidogrel + omeprazole avoid" | Verified | "Plavix label"
 "Erlotinib AUC −46% with omeprazole" | Verified | "TARCEVA label"
 "NHSO covers HLA-B*15:02 and *58:01" | Verified | "NHSO / PMC"
 "Gold Card covers CYP2C19, CYP2C9" | Partly | "Hfocus Jul 2026 — confirm with NHSO notice"
 "ApoB as target" | Partly | "ESC/EAS: secondary target; check 2025 update"
 "Pharmacists 46.3% low PGx knowledge, 7% interpreted" | Partly | "PubMed 32187156 (abstract)"
 "Clinical NMR lab in Thailand" | Unverified | "None found"
 "HOSxP PGx field" | Unverified | "Not found"
 "CPIC PPI wording" | Unverified | "Check before submission"
Footnote: "Full source list in market_research.md §7."
```

### A4 — Clinical limitations

**Action title:** We state the limits openly so judges and clinicians can trust the rest

```
[GLOBAL STYLE BLOCK]
Limitations slide. Title: "We state the limits openly so judges and clinicians can trust the rest".
Two columns of bullet cards with small warning icons.
Left column "PGx and prescribing":
 "Does not diagnose; does not choose drugs — clinicians decide";
 "PGx covers only the genes tested; a negative result does not mean every drug is safe";
 "PGx alert acceptance ~63%; accepted alerts change therapy only 47% of the time";
 "No Thai outcome data for PGx-guided prescribing yet".
Right column "Omics and oncology":
 "No confirmed clinical NMR lab in Thailand; NMR reference ranges mostly European";
 "Negative ctDNA does not exclude a mutation";
 "Some variants may be CHIP or germline";
 "ctDNA dynamics for response are emerging evidence";
 "VUS and incidental germline findings go to genetic counselling".
Footnote: "PMC10726431; market_research.md; idea.md §10."
```

### A5 — Financial assumptions

**Action title:** The financials rest on three assumptions we will test first

```
[GLOBAL STYLE BLOCK]
Assumptions slide. Title: "The financials rest on three assumptions we will test first".
Three large horizontal rows, each with number badge, assumption, value, sensitivity and how to test:
 "1  Hospital can bill pharmacist PGx review" | "~฿700 × ≥510 reviews/yr" | "Without it, hospital ROI falls from ≈2.2× to ≈0.37×" | "Ask hospital finance before LOI"
 "2  Sales speed and CAC" | "12 hospitals by year 3; CAC ≈ ฿400k; 9–12 month sales cycle" | "Half the hospitals → cash need ≈ ฿26M" | "Track first 3 sales cycles"
 "3  Price and volume" | "฿480 per active patient/yr; ~1,000 active PGx patients per hospital" | "฿360 → LTV:CAC 2.2; ฿300 → 1.6" | "Ask PGx labs for annual test counts"
Side panel: "Other inputs: LLM ≈ ฿35/report; ADR admission ฿7,215; pharmacist PGx consult 24 min; GLP-1 ฿7,500–19,000/month; osimertinib ≈ USD 1,963/month."
Footnote: "All values from business_case.md; assumptions unless a source is named."
```

### A6 — Market facts and sources

**Action title:** Thai market facts behind the sizing

```
[GLOBAL STYLE BLOCK]
Fact sheet slide. Title: "Thai market facts behind the sizing".
A 3-column grid of 12 small fact tiles, each with a teal number and a grey label:
 "65.8M" "Thai registered population (2025)";
 "21.82%" "aged 60+";
 "324 / 682" "public tertiary / secondary hospitals";
 "370" "private hospitals (older data)";
 "19,126" "retail pharmacies";
 "6.16 per 10,000" "pharmacist density (2023)";
 "60" "BDMS hospitals";
 "฿14,751" "N Health PGx profile price";
 "฿1,000" "NHSO payment per HLA-B test";
 "23,871" "new lung cancers/yr (GLOBOCAN 2024)";
 "$8,455" "Guardant360 CDx US cash price (2026)";
 "$119" "Labcorp NMR LipoProfile US price".
Footnote: "Sources: DOPA 2025; WHO Pharmaceutical Country Profile 2025; Krungsri Research; BDMS 2026; HDmall; NHSO; GLOBOCAN 2024; Guardant; Labcorp — see market_research.md §7."
```

---

## 4. Rubric mapping (from pitch-deck-strategist)

Default rubric from `.claude/skills/judge-panel/SKILL.md`. Replace with the event rubric if available.

| Criterion (weight) | Slides that score it |
|---|---|
| Problem significance (20%) | 3, 4, 5 |
| Innovation / differentiation (20%) | 6, 9, 10, 15 |
| Scientific and clinical validity (20%) | 7, 11, 13, A1, A2, A3, A4 |
| Technical feasibility and demo (15%) | 8, 12, 20 |
| Safety, ethics, regulation (10%) | 11, 21, A4 |
| Business model and impact (15%) | 14, 16, 17, 18, 19, 22, A5 |

## 5. Top judge questions → backup slide

| Question | Answer slide |
|---|---|
| "How is this different from Pook-Phan?" | 15 |
| "Why won't HOSxP just build it?" | 15, 23 |
| "Which Thai lab does clinical NMR?" | 20, A1, A4 |
| "Why cfDNA?" | 10 |
| "Who pays and is it worth it for the hospital?" | 16, 17, A5 |
| "Is PREPARE applicable to Thais?" | A2 |
| "Is this a medical device?" | 21 |
| "How do you stop hallucination?" | 8, 11 |
| "What if doctors ignore the alerts?" | 4, 9, 13 |
| "What happens if the pilot fails?" | 22 |

## 6. Before generating — checklist

- [ ] Fill `[TEAM NAME]`, `[EVENT NAME]`, `[DATE]`, team member names
- [ ] Replace the default rubric with the event rubric if one exists
- [ ] Verify the 3 unverified items (clinical NMR lab, HOSxP PGx field, CPIC PPI wording) or keep them flagged
- [ ] After generation, proofread every number against this file
- [ ] Keep the word "assumption" on every financial number that has no source
