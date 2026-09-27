# PrecisionRx — Eval report (SYNTHETIC)

> Gold labels written by hand from guideline/label text, **pending pharmacist review**.
> Synthetic cases only — these numbers show the rules behave as specified, not clinical accuracy.

| Metric | Value |
|---|---|
| Cases passed | 45/45 |
| Omissions of expected findings (target 0) | 0 of 21 (0.0%) |
| False flags (stop/action + NMR factors) | 0 |
| Risk category agreement | 7/7 |
| RCV trend verdict agreement | 3/3 |
| Citations checked / missing fact ids | 134 / 0 |
| Unverified fact ids still cited | ACR-2020-HLAB5801, CPIC-CYP2C19-CLOP-IM-2022, CPIC-CYP2C19-PPI-2020, LABEL-CBZ-HLA |
| Alerts per case: naive baseline → PrecisionRx | 1.78 → 0.53 (−70.0%) |

Naive baseline = alert on every drug with an available PGx result, every clopidogrel+PPI pair, and every analyte outside its reference band.

## Per case

| Case | Scenario | Result | Alerts (naive → ours) |
|---|---|---|---|
| E01 | HLA-B*15:02 positive + carbamazepine | ✅ | 2 → 1 |
| E02 | HLA-B*15:02 positive + oxcarbazepine | ✅ | 2 → 1 |
| E03 | HLA-B*15:02 negative + carbamazepine (no alert) | ✅ | 2 → 0 |
| E04 | Carbamazepine, HLA-B*15:02 never tested (label — screen before starting) | ✅ | 1 → 1 |
| E05 | HLA-B*58:01 positive + allopurinol | ✅ | 2 → 1 |
| E06 | HLA-B*58:01 negative + allopurinol (no alert) | ✅ | 2 → 0 |
| E07 | Allopurinol, HLA-B*58:01 never tested (Thai/SE Asian ancestry — test first) | ✅ | 1 → 1 |
| E08 | SLCO1B1 decreased function + simvastatin 40 | ✅ | 2 → 1 |
| E09 | SLCO1B1 poor function + simvastatin 20 | ✅ | 2 → 1 |
| E10 | SLCO1B1 normal function + simvastatin 40 (no alert) | ✅ | 2 → 0 |
| E11 | SLCO1B1 decreased function on rosuvastatin 10 — within CPIC ≤20 mg starting dose, no alert | ✅ | 2 → 0 |
| E12 | CYP2C19 poor metabolizer + clopidogrel | ✅ | 2 → 1 |
| E13 | CYP2C19 intermediate metabolizer + clopidogrel (CPIC 2022 — avoid standard dose in ACS/PCI) | ✅ | 2 → 1 |
| E14 | CYP2C19 normal metabolizer + clopidogrel (no alert) | ✅ | 2 → 0 |
| E15 | Clopidogrel + omeprazole (label DDI) | ✅ | 2 → 1 |
| E16 | Clopidogrel + esomeprazole (label DDI) | ✅ | 2 → 1 |
| E17 | Clopidogrel + pantoprazole (preferred PPI — no alert) | ✅ | 2 → 0 |
| E18 | CYP2C19 PM + clopidogrel + omeprazole — PGx + DDI both shown | ✅ | 4 → 2 |
| E19 | CYP2C19 ultrarapid + omeprazole | ✅ | 2 → 1 |
| E45 | CYP2C19 ultrarapid + esomeprazole — CPIC PPI guideline gives no recommendation for esomeprazole | ✅ | 2 → 0 |
| E20 | CYP2C19 rapid + pantoprazole | ✅ | 2 → 1 |
| E21 | CYP2C19 normal + omeprazole (no alert) | ✅ | 2 → 0 |
| E22 | Simvastatin 40 (moderate), LDL-C −41%, PDC 92 — responding as expected | ✅ | 1 → 0 |
| E23 | Atorvastatin 40 (high), LDL-C −20%, PDC 95 — true non-response | ✅ | 1 → 1 |
| E24 | Atorvastatin 40, LDL-C −10%, PDC 50 — adherence first, not "drug failure" | ✅ | 2 → 1 |
| E25 | Rosuvastatin 20 (high), LDL-C −45% (expected ≥50%), PDC 90 — below expected | ✅ | 1 → 1 |
| E26 | Metformin PDC 60% — adherence | ✅ | 2 → 1 |
| E27 | Amlodipine PDC exactly 80% — at threshold, no alert | ✅ | 1 → 0 |
| E28 | 60M smoker DM SBP150 on atorvastatin, LDL-C 3.2 — Thai CV risk >10%, LDL above RCPT target | ✅ | 1 → 1 |
| E29 | 45F low risk on atorvastatin 10, LDL-C 3.0 — risk <10%, no target alert | ✅ | 1 → 0 |
| E30 | Thai CV risk worked example — 60M smoker SBP140 TC 220 mg/dL → 24.7% high | ✅ | 1 → 0 |
| E31 | Thai CV risk worked example — 45F SBP120 TC 200 mg/dL → 2.3% low | ✅ | 1 → 0 |
| E32 | Thai diabetes score — 52F BMI 27.9 waist 88 family history → 13/17 very high | ✅ | 1 → 0 |
| E33 | Already diabetic — diabetes screening score not applicable | ✅ | 1 → 0 |
| E34 | LDL-C 2.4 at target, ApoB 105 mg/dL — ApoB discordance | ✅ | 1 → 1 |
| E35 | LDL-C 2.4, ApoB 85 mg/dL, low risk — no discordance | ✅ | 1 → 0 |
| E36 | Diabetic, LDL-C 1.7, ApoB 85 mg/dL — above high-risk ApoB target 80 | ✅ | 2 → 1 |
| E37 | GlycA 1.10 mmol/L (> P90) | ✅ | 2 → 1 |
| E38 | BCAA 520 µmol/L, not diabetic | ✅ | 2 → 1 |
| E39 | BCAA 520 µmol/L in known diabetic — diabetes-risk flag must not fire | ✅ | 3 → 0 |
| E40 | Trend: ApoB −25% (improved), TG −40% (within RCV 56%), LDL-P −30% (no CVi) | ✅ | 1 → 0 |
| E41 | Trend: TG +70% (worsened), glucose +20% (worsened), HDL-C +25% (improved) | ✅ | 2 → 0 |
| E42 | Trend: ApoB −10% — within variation, must not claim improvement | ✅ | 1 → 0 |
| E43 | Healthy 40F, no drugs, normal panel, active — nothing to flag | ✅ | 1 → 0 |
| E44 | Polypharmacy (8 drugs), full PGx panel all normal — zero alerts | ✅ | 6 → 0 |
