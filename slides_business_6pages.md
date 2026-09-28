# PrecisionRx — Business Deck, 6 Dense Pages (Image-Generation Prompts)

> Scope: business pages only — market size, customers and competition, business model, financials, feasibility, go-to-market.
> Density: about 3× the detail of `slides_image_prompts.md`, packed into compact multi-panel layouts.
> Sources: `market_research.md`, `business_strategy.md`, `business_case.md`, `idea_validation.md`, `idea.md` (v3), live prototype.
> Numbers marked "(assumption)" are team estimates. Keep that word on the slide.

---

## How to use

1. Paste the **Compact Style Block** (§1) before every page prompt.
2. Use the strongest text-rendering image model you have (GPT-Image, Gemini image / Nano Banana Pro, Ideogram). Set **16:9** and the **highest resolution (2560×1440 or 4K)**. Dense pages need high resolution or the small text breaks.
3. If a page comes out cluttered or with broken text, generate it in two halves (left and right panels) and join them, or build that page in Canva/PowerPoint using the same text.
4. **Proofread every number** against this file after generation. Image models change digits.
5. Fill `[TEAM NAME]` and `[EVENT NAME]` first.

### Titles test (read titles only)

1. A ฿20–60M serviceable market exists today because Thai PGx results are growing fast but are not used at prescribing
2. Private hospitals that already sell PGx pay first; competitors own pieces, nobody owns the Thai prescribing moment
3. Three revenue streams, one lab-agnostic interpretation layer: hospitals, cancer centres and labs
4. Unit economics work (LTV:CAC ≈ 3.4); break-even is around month 45–50 and depends on one billing assumption
5. Feasible now: the data, the standards and a working prototype exist; the remaining risks are regulatory and commercial
6. A 3-month gate and a 6-month pilot decide go or stop before large spending

---

## 1. Compact Style Block (paste before every page)

```
STYLE: Consulting-grade dense one-pager slide, 16:9, 2560x1440, flat vector, Swiss 12-column grid, compact dashboard layout with 6–10 bordered panels, tight but even gutters (24 px), outer margin 48 px, crisp readable small typography, strong visual hierarchy so the page is still scannable: big teal numbers first, then bold panel headings, then small body text.
BRAND: Product "PrecisionRx". Palette: deep navy #0B2545 (title, panel headers), teal #13A89E (key numbers, highlights), background #F7F9FB, panel fill white with 1 px light grey #E3E8EE border and 8 px radius, body text grey #3E4A52, alert red #D64545 (risks only), amber #E8A33D (warnings/assumptions only), green #2E9E5B (ready/verified only).
TYPOGRAPHY: Geometric sans-serif like Inter or IBM Plex Sans. Page title top-left, bold navy, 34 px, one sentence. Panel headings 17 px bold navy uppercase-small-caps. Body 13–15 px. Big stat numbers 36–48 px teal bold. Footnote line 11 px grey at bottom. All text spelled exactly as given in quotes, English only, no invented words, no lorem ipsum, no extra numbers.
CONVENTIONS: Thin teal rule under title. Tiny tag "(assumption)" in amber after any estimated number. Page number "n / 6" bottom-right, footer "PrecisionRx | [TEAM NAME] | [EVENT NAME]" bottom-right in grey. Line icons 2 px stroke. Tables: navy header row white text, zebra rows light grey. Charts flat, directly labeled, no 3D, no shadows, no gradients.
```

**Negative prompt:** `blurry text, misspelled words, gibberish, distorted digits, overlapping text, cramped unreadable text, cartoon, 3D, photo, stock people, neon, purple gradient, watermark, cropped panels`

---

## 2. Page prompts

### Page 1 / 6 — Market opportunity and size

**Title:** A ฿20–60M serviceable market exists today because Thai PGx results are growing fast but are not used at prescribing

```
[COMPACT STYLE BLOCK]
Dense one-pager. Title: "A ฿20–60M serviceable market exists today because Thai PGx results are growing fast but are not used at prescribing".
GRID: top row = 5 small stat tiles across full width; middle row = 3 panels (left 40%, centre 35%, right 25%); bottom row = 2 panels (left 60%, right 40%); footnote line.

TOP ROW — 5 stat tiles, each big teal number + small grey label:
 "96%" — "Thai adults with ≥1 CPIC-actionable PGx result (n=4,662)"
 "94 → 2,880" — "HLA-B tests per year at Ramathibodi, 2011 → 2020"
 "~90%" — "drug-interaction alerts overridden by doctors (meta-analysis)"
 "21.82%" — "Thais aged 60+ (2025): complete aged society"
 "23,871" — "new lung cancers per year in Thailand (GLOBOCAN 2024)"

MIDDLE LEFT panel "MODULE A — PGx AT PRESCRIBING (CORE)": three nested concentric circles in teal shades with labels on leader lines:
 outer "TAM ฿0.41–0.83B / yr" + small "1,376 hospitals: 324 tertiary + 682 secondary public + 370 private × ฿300k–600k (assumption)"
 middle "SAM ฿18–60M / yr" + small "60–100 hospitals with PGx or preventive/lipid clinics (assumption)"
 inner "SOM yr-3 ฿2–6M / yr" + small "5–10 hospitals"
MIDDLE CENTRE panel "MODULE B — ONCOLOGY cfDNA": a vertical funnel with 5 steps and values:
 "23,871 lung cancers" → "× 85% NSCLC ≈ 20,290" → "× ~70% advanced ≈ 14,200 (assumption)" → "cfDNA at diagnosis 20–30% + at TKI resistance ≈ 7,400–8,900 reports/yr" → "× ฿1,500–3,000 per report".
 Under funnel three small lines: "TAM ≈ ฿11–27M / yr", "SAM ≈ ฿2–8M / yr", "SOM yr-3 ≈ ฿0.3–1.2M / yr". Small amber note: "Differentiator, not the revenue engine".
MIDDLE RIGHT panel "DEMAND SIGNALS": 5 compact bullet rows with small icons:
 "55% of omeprazole users carry actionable CYP2C19"
 "22–23% of statin users carry actionable SLCO1B1"
 "NHSO pays ฿1,000 per HLA-B*15:02 / *58:01 test"
 "Gold Card via Ramathibodi covers HLA-B*15:02, CYP2C19, CYP2C9 (2026)"
 "EGFR mutation in 47–56% of Thai NSCLC"

BOTTOM LEFT panel "WHY NOW — 4 FORCES": a 4-column mini table with headers "Force", "Evidence", "Effect on us":
 "Aging + polypharmacy" | "Polypharmacy 59.5% in elderly OPD (Region 8, n=587,905)" | "More gene–drug conflicts per patient"
 "Public PGx coverage" | "NHSO HLA-B since 2018; Gold Card expansion 2026" | "More PGx results to act on"
 "National PGx data layer" | "Pook-Phan app: lifetime drug-allergy genes, ThaiD, 11 hospitals" | "Data source ready; alert missing"
 "Evidence base" | "PREPARE (Lancet 2023): ADR 21.0% vs 27.7%, OR 0.70" | "Rationale; European data only"
BOTTOM RIGHT panel "UNIT-OF-VALUE CROSS-CHECK": two horizontal bars compared: "PGx panel price ฿14,751 (N Health)" long grey bar vs "PrecisionRx ≈ ฿400 per patient-year (assumption)" short teal bar; caption "Software ≈ 37× cheaper than the test it makes useful". Below: "Status quo competitor = results left on paper cards and PDFs".

FOOTNOTE: "Sources: PLoS One 2026 Thai cohort; PMC9016335; Felisberto 2024; DOPA 2025; GLOBOCAN 2024; WHO Pharmaceutical Country Profile 2025; Krungsri Research; NHSO; Hfocus Jul 2026; Thai PBS; Swen et al., Lancet 2023; HDmall. Prices and penetration are assumptions."
```

---

### Page 2 / 6 — Customers, payers and competition

**Title:** Private hospitals that already sell PGx pay first; competitors own pieces, nobody owns the Thai prescribing moment

```
[COMPACT STYLE BLOCK]
Dense one-pager. Title: "Private hospitals that already sell PGx pay first; competitors own pieces, nobody owns the Thai prescribing moment".
GRID: left column 42% = 2 stacked panels; right column 58% = 1 large matrix panel on top + 2 small panels side by side below; footnote.

LEFT TOP panel "WHO USES · WHO BUYS · WHO BENEFITS": table with columns "", "Module A — PGx at prescribing", "Module B — Oncology pharmacy":
 "User" | "Doctor (alert card in HIS) + pharmacist (review queue)" | "Oncology pharmacist + oncologist"
 "Buyer" | "Hospital executive" | "Cancer centre director"
 "Approvers" | "Pharmacy & Therapeutics Committee, IT, DPO" | "Tumour board, IT, DPO"
 "Budget line" | "Pharmacy/clinical IT software" | "Oncology service"
 "Beneficiary" | "Patient (fewer ADRs); hospital (sold PGx tests now used)" | "Patient; cancer centre"
LEFT BOTTOM panel "BEACHHEAD — PRIVATE HOSPITALS THAT SELL PGx": list with small hospital icons:
 "Bangkok Hospital — PGx NGS, 500+ drugs"
 "BNH — PGx 126 drugs incl. doctor interpretation"
 "Samitivej — Genomics & Lifestyle Wellness Center"
 "Bumrungrad — 13-gene, 147-drug PGx program"
 "N Health — PGx profile ฿14,751"
 Teal highlight line: "BDMS group = 60 hospitals: win 1, expand inside the group".
 Red small line: "Pipeline today: 0 contacted".
 Grey line: "Next segment: public hospitals via HIS vendor for Gold-Card genes".

RIGHT TOP panel "COMPETITIVE MATRIX": rows = players, columns = capabilities; cells filled teal circle = yes, half circle = partial, empty circle = no.
 Columns: "Stores PGx", "CPIC logic", "Alert at prescribing", "Thai drug codes + NHSO rules", "Pharmacist workflow", "Oncology cfDNA + germline + DDI".
 Rows:
 "Status quo (PDF / card)": full, empty, empty, empty, empty, empty
 "Pook-Phan (Thai govt)": full, empty, empty, half, empty, empty
 "PGxCard / Burapha": full, half, empty, half, empty, empty
 "PharmCAT (open source)": empty, full, empty, empty, empty, empty
 "Lexidrug / Micromedex": empty, half, half, empty, half, empty
 "Epic genomics": full, full, full, empty, half, empty
 "Nalagenetics (SEA, CE mark)": full, full, half, empty, half, empty
 "Tabula Rasa MedWise (US)": half, half, half, empty, full, empty
 "QIAGEN QCI / Roche navify / OncoKB": empty, empty, empty, empty, empty, half
 "HOSxP (HIS)": empty, empty, half, full, half, empty
 "PrecisionRx": all full — row highlighted with light teal background and bold text.
RIGHT BOTTOM-LEFT panel "HOW WE TREAT EACH": 4 short lines: "Pook-Phan, PGx labs → data sources", "PharmCAT → our engine, not our moat", "HOSxP → channel, not rival", "Nalagenetics → most direct regional threat".
RIGHT BOTTOM-RIGHT panel "WHY WON'T THE HIS VENDOR BUILD IT?": short paragraph: "They can — Epic did. The real cost is keeping CPIC evidence current, Thai drug mapping, liability and Thai FDA burden. A US PGx CDS company stopped the service after failing FDA 510(k). HOSxP's recent AI work is documentation, not PGx. We sell fewer alerts and plug in as their module." Small amber tag: "Moat = time + focus + Thai data, not impossibility".

FOOTNOTE: "Sources: hospital websites; BDMS 2026; Thai PBS; PharmCAT GitHub; Nalagenetics CE-mark release; MobiHealthNews; Microsoft Source Asia May 2025; market_research.md §4; idea_validation.md."
```

---

### Page 3 / 6 — Business model and pricing

**Title:** Three revenue streams, one lab-agnostic interpretation layer: hospitals, cancer centres and labs

```
[COMPACT STYLE BLOCK]
Dense one-pager. Title: "Three revenue streams, one lab-agnostic interpretation layer: hospitals, cancer centres and labs".
GRID: top 45% = money-flow diagram full width; bottom 55% = 3 panels (pricing table 45%, business model canvas 35%, rules 20%); footnote.

TOP panel "MONEY AND VALUE FLOW": centre navy rounded box "PrecisionRx — interpretation layer (lab-agnostic, no lab tests sold)". Left: three input boxes with grey arrows into centre labeled "data": "Pook-Phan / PGx labs", "Liquid biopsy labs", "Hospital HIS (FHIR)". Right: three payer boxes with thick teal arrows into centre labeled with price:
 "Private hospital — Module A": "Setup ฿250,000 + ฿300–480 per active PGx patient / yr, minimum 1,000 patients (assumption)"
 "Cancer centre — Module B": "Module licence, or ฿3,000 per oncology report (assumption)"
 "PGx / liquid biopsy lab": "฿500 revenue share per result (assumption)"
 Bottom: three grey arrows out to "Doctor — fewer, sharper alerts", "Pharmacist — one review queue", "Patient — avoided ADRs". Small amber note on the side: "Insurers (phase 3) see only aggregate outcomes, never individual genetic data".

BOTTOM LEFT panel "PRICING AND RATIONALE": table columns "Stream", "Price", "Why this price", "Phase":
 "Module A setup" | "฿250,000 once" | "Integration + Thai drug mapping + training" | "1"
 "Module A per active patient" | "฿300–480 / yr" | "≈ 2–3% of a ฿14,751 PGx panel; re-uses a result already paid for" | "1"
 "Module B" | "Licence or ฿3,000 / report" | "< 5% of one month of osimertinib (≈ USD 1,963)" | "2"
 "Lab revenue share" | "฿500 / result" | "Lab's test becomes more valuable" | "1–2"
 "HIS vendor resale" | "Revenue share (TBD)" | "Reach public hospitals" | "2"
 "Insurer program" | "Per member (TBD after pilot data)" | "No price until evidence exists" | "3"
BOTTOM CENTRE panel "BUSINESS MODEL CANVAS (COMPACT)": 9 tiny boxes in canvas layout with 1–2 lines each:
 "Key partners: pharmacy faculty, PGx labs, HIS vendor, liquid biopsy labs"
 "Key activities: evidence curation, Thai mapping, integration, support"
 "Key resources: versioned evidence store, rule engines, eval set"
 "Value proposition: gene results used at every prescription, fewer alerts"
 "Relationships: pilot → annual contract, pharmacist training"
 "Channels: direct to private groups, then HIS vendor"
 "Segments: private hospitals with PGx; cancer centres"
 "Cost structure: curation + support (fixed), LLM ≈ ฿35 / report"
 "Revenue: setup + per-patient + licence + lab share"
BOTTOM RIGHT panel "RULES WE KEEP": 4 short lines with check icons: "We do not sell lab tests", "Pricing validated with 3–5 chief pharmacists before pilot", "Genetic data never leaves Thailand", "No insurer price before pilot evidence".

FOOTNOTE: "All prices are assumptions to validate with customers. Osimertinib cost: PubMed 41455170. PGx panel price: N Health on HDmall. Sources: business_strategy.md, business_case.md."
```

---

### Page 4 / 6 — Unit economics, customer ROI and 3-year financials

**Title:** Unit economics work (LTV:CAC ≈ 3.4); break-even is around month 45–50 and depends on one billing assumption

```
[COMPACT STYLE BLOCK]
Dense one-pager. Title: "Unit economics work (LTV:CAC ≈ 3.4); break-even is around month 45–50 and depends on one billing assumption".
GRID: top row = 6 KPI tiles; middle row = 2 panels (revenue chart 55%, hospital ROI waterfall 45%); bottom row = 3 panels (scenarios 40%, sensitivity 35%, key assumptions 25%); footnote.

TOP ROW — 6 KPI tiles (teal number + grey label, each with tiny amber "(assumption)"):
 "67%" — "contribution margin per hospital"
 "฿400k" — "customer acquisition cost"
 "฿1.36M" — "lifetime value"
 "3.4×" — "LTV:CAC (2.0× incl. yr-3 curation)"
 "13 mo" — "CAC payback (23 mo incl. curation)"
 "฿35" — "LLM cost per report"

MIDDLE LEFT panel "REVENUE, BASE CASE (฿ MILLION)": vertical bar chart, 3 teal bars with values on top: "Year 1: 0.5", "Year 2: 3.4", "Year 3: 9.6". Under bars small labels: "1 pilot hospital", "~5 hospitals + 1 cancer centre", "12 hospitals + 3 cancer centres". A dashed extension arrow to the right labeled "Monthly break-even ≈ month 45–50 at run-rate ≈ ฿19–21M/yr (≈25 hospitals + 6 cancer centres)". Small line under chart: "Team 5 → 11 people · gross margin ≈ 24% in yr 3 → ≈ 62% at 40 hospitals".
MIDDLE RIGHT panel "HOSPITAL ROI PER YEAR": horizontal waterfall bars:
 "Pharmacist time saved" +฿133k
 "ADRs avoided (฿7,215 per admission)" +฿75k
 marker line "ROI without billing ≈ 0.37× — does not pay" (red text)
 "Billable pharmacist PGx review ≈ ฿700 × ≥510 / yr" large teal bar
 marker line "ROI with billing ≈ 2.2×" (teal bold)
 Amber callout: "Key assumption #1: hospital can bill the review or bundle it into the PGx package".

BOTTOM LEFT panel "SCENARIOS": table columns "Scenario", "Year-3 revenue", "Break-even", "Cash need":
 "Upside" | "above base" | "within year 3" | "lower than base"
 "Base" | "฿9.6M" | "≈ month 45–50" | "≈ ฿25M trough, ≈ ฿30M with buffer; yr-1 ≈ ฿7M"
 "Downside" | "below base" | "none" | "loss ≈ ฿27M → stop at kill gate"
BOTTOM CENTRE panel "PRICE SENSITIVITY": small table "Price / active patient / yr" vs "LTV:CAC": "฿480 → 3.4", "฿360 → 2.2", "฿300 → 1.6". Plus line: "Half as many hospitals → cash need ≈ ฿26M".
BOTTOM RIGHT panel "3 ASSUMPTIONS THAT MOVE EVERYTHING": numbered: "1 Billable pharmacist review", "2 Sales speed: 12 hospitals by yr 3, 9–12 month cycle", "3 ~1,000 active PGx patients per hospital".

FOOTNOTE: "All figures are team estimates from business_case.md (Python model, formulas in §5.1). Sourced inputs: Thai ADR admission cost (Pharmacy Practice); Mayo Clinic PGx consult 24 min (PubMed 37478473). Year-2 customer count is illustrative."
```

---

### Page 5 / 6 — Feasibility (technical, regulatory, operational)

**Title:** Feasible now: the data, the standards and a working prototype exist; the remaining risks are regulatory and commercial

```
[COMPACT STYLE BLOCK]
Dense one-pager. Title: "Feasible now: the data, the standards and a working prototype exist; the remaining risks are regulatory and commercial".
GRID: left 50% = technical readiness table (tall panel); right 50% = 3 stacked panels (prototype proof, regulatory, operations); footnote.

LEFT panel "TECHNICAL READINESS": table columns "Component", "Exists today", "Our use", "Status" with coloured status dots:
 "Germline PGx results" | "Pook-Phan, Rama PPM, private PGx labs" | "FHIR / file import" | green
 "CPIC logic" | "PharmCAT (open source)" | "Engine core" | green
 "Prescribing-time alert standard" | "HL7 CDS Hooks + FHIR" | "Card in ordering screen" | green
 "Thai drug codes" | "TMT" | "Map CPIC drugs to TMT" | amber
 "DDI knowledge" | "Licensed DDI databases, drug labels" | "Rule engine" | amber
 "cfDNA variant reports" | "Liquid biopsy labs" | "Import + AMP/ASCO/CAP tier" | amber
 "Oncology knowledge base" | "OncoKB (commercial licence)" | "Evidence store" | amber
 "HOSxP PGx field / API" | "Not confirmed" | "Needs HIS partner" | red
 "Clinical NMR lab in Thailand" | "Not confirmed (research only)" | "Phase 2–3, ApoB first" | red
 Legend under table: "green = ready · amber = needs licence or mapping · red = unconfirmed, not needed for Module A launch".

RIGHT TOP panel "PROTOTYPE PROOF (LIVE)": 4 stat tiles: "5 pages" — "live on Vercel: dashboard, medications, risk & self-care, cfDNA"; "45 cases" — "gold-standard eval set"; "−70.7%" — "alerts per case vs alert-everything (1.78 → 0.52)"; "43 / 43" — "automated tests passing". Small grey line: "Deterministic rule engines + evidence store; every output cites a fact ID; synthetic data only". URL line: "precisionrx-demo.vercel.app".
RIGHT MIDDLE panel "REGULATORY FEASIBILITY": 5 compact rows with icons:
 "SaMD: likely a medical device under Thai Medical Device Act → early Thai FDA consultation"
 "Design choice: no raw spectrum, no variant calling → never processes IVD signals"
 "PDPA s.26: explicit, separate consent for PGx and cfDNA; data stays in Thailand; DPO"
 "Labs: ISO 15189 results only; research-use results labelled RUO"
 "Ethics & licences: IRB/EC before real data; OncoKB + DDI licences budgeted"
RIGHT BOTTOM panel "OPERATIONAL FEASIBILITY": 4 rows: "Team 5 in yr 1: clinical pharmacist, 2 engineers, evidence curator, BD/regulatory"; "Evidence curation is the main fixed cost"; "Pharmacist knowledge gap: 46.3% low PGx knowledge → built-in 'Why?' + training"; "Physician acceptance ≈ 63% average in literature → show only actionable alerts".

FOOTNOTE: "Sources: PharmCAT GitHub; HL7 CDS Hooks; Thai Medical Device Act B.E. 2551 (amended 2562); PDPA B.E. 2562 s.26; US FDA CDS guidance (Jan 2026, reference only); PubMed 32187156 (abstract); PMC10726431; prototype eval/report.md. Team plan is an assumption."
```

---

### Page 6 / 6 — Go-to-market, pilot, risks and ask

**Title:** A 3-month gate and a 6-month pilot decide go or stop before large spending

```
[COMPACT STYLE BLOCK]
Dense one-pager. Title: "A 3-month gate and a 6-month pilot decide go or stop before large spending".
GRID: top 38% = Gantt timeline full width; middle 34% = 3 panels (pilot targets 40%, partnership sequence 35%, kill criteria 25%); bottom 28% = 2 panels (risk table 70%, ask 30%); footnote.

TOP panel "ROADMAP M0 → M24": horizontal Gantt with month axis "M0, M3, M6, M9, M12, M18, M24" and bars:
 "Interview 5–10 hospital pharmacists" M0–M1
 "LOI from 1 hospital + talks with Pook-Phan team and HIS vendor" M0–M3 → red diamond "Gate 1 (M3)"
 "IRB + Thai FDA consultation" M3–M6
 "Pilot A: retrospective replay, n ≥ 300, no effect on care" M3–M5
 "Pilot B: live use, ~150–200 reviews" M5–M9 → red diamond "Gate 2 (M9)"
 "Expand inside hospital group" M9–M18
 "Module B at 1 cancer centre" M9–M18
 "Response module: ApoB + RCV" M12–M18
 "Public-hospital connector via HIS vendor; NMR research track" M18–M24

MIDDLE LEFT panel "PILOT SUCCESS TARGETS (SET BEFORE START)": 6 small tiles: "0 critical omissions (go/no-go)"; "≥ 70% pharmacist acceptance"; "≥ 50% physician acceptance"; "≥ 50% fewer alerts per review"; "≥ 30% less review time"; "≥ 99% citation precision". Grey line: "Expected yield: ~55 actionable findings / 100 omeprazole users; ~22 / 100 statin users". Red line: "No ADR-reduction claim from the pilot".
MIDDLE CENTRE panel "PARTNERSHIP SEQUENCE": numbered vertical list with time tags: "1 Pharmacy faculty — validation — M0"; "2 One private hospital — pilot — M0–3"; "3 PGx lab — data + revenue share — M3"; "4 HIS vendor — FHIR sandbox — M6–12"; "5 Liquid biopsy lab / cancer centre — M9–18"; "6 NMR lab — research only — M18+"; "7 Insurers / NHSO — M18+".
MIDDLE RIGHT panel "KILL / PIVOT TRIGGERS" (red border): "No LOI + no HIS or Pook-Phan cooperation by M3"; "Acceptance < 50% at M9"; "Site has < 200 patients with PGx results"; "Hospital cannot bill pharmacist review"; "Review again at M12 and M24 against financial plan".

BOTTOM LEFT panel "TOP RISKS": table columns "Risk", "Likelihood / impact", "Mitigation", "Early signal":
 "Low pharmacist demand (7% interpreted PGx last year)" | "High / high" | "Actionable-only alerts, 'Why?' trace, training" | "Interviews, pilot acceptance"
 "Hospital cannot bill review → ROI fails" | "High / high" | "Bundle into PGx package; confirm before LOI" | "Hospital finance answer"
 "Government or HIS vendor builds it" | "Medium / high" | "Partner as data source and module" | "HOSxP / Pook-Phan roadmap"
 "Regional competitor (Nalagenetics) enters" | "Medium / medium" | "Thai codes, NHSO rules, HOSxP first" | "SEA announcements"
 "Thai FDA higher-risk class" | "Low / high" | "Early consultation; no signal processing" | "Thai FDA feedback"
BOTTOM RIGHT panel "OUR ASK" (teal border): "1 One pilot hospital that already sells PGx"; "2 Data partnership: Pook-Phan team or a PGx lab + HIS sandbox"; "3 Mentors: hospital pharmacy leadership, Thai FDA SaMD, oncology"; "Year-1 budget ≈ ฿7M (assumption)".

FOOTNOTE: "Targets and gates from business_strategy.md; risks from idea_validation.md; PubMed 32187156; timeline indicative. Status: concept stage — no company, partners or revenue yet."
```

---

## 3. Before generating — checklist

- [ ] Fill `[TEAM NAME]`, `[EVENT NAME]`
- [ ] Generate at 2560×1440 or higher; split a page into halves if text breaks
- [ ] Proofread every number against this file
- [ ] Keep "(assumption)" on every estimated number
- [ ] Re-check the prototype stats (5 pages, 45 cases, −70.7%, 43 tests) against the live site before submission
