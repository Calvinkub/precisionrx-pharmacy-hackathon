# Eval set

45 synthetic cases (`cases.yaml`), gold labels written by hand from guideline and label text **before** running the engine. Labels are drafts until 2–3 pharmacists review them (`review_sheet.csv`, open in Excel/Sheets).

```bash
uv run python -m eval.run_eval --sheet   # → report.md, results.json, review_sheet.csv
uv run pytest tests/test_eval.py         # regression gate: 0 omissions, 0 false flags
```

Coverage: HLA-B hard stops and untested patients · SLCO1B1–simvastatin · CYP2C19–clopidogrel / PPI · clopidogrel+PPI DDI · statin response, LDL target and adherence (PDC) · Thai CV Risk and Thai diabetes score · NMR add-on factors · RCV trend verdicts · negative controls (healthy person, 8-drug polypharmacy with normal PGx).

## What the first run found (2026-09-28)

First run: 40/45. The eval caught real engine gaps, which were then fixed:

| Case | Problem | Fix |
|---|---|---|
| E04, E07 | Carbamazepine / allopurinol with **no HLA-B result** → no alert | New rule: "order HLA-B test before starting" |
| E13 | CYP2C19 **intermediate** metabolizer + clopidogrel → no alert | Added CPIC 2022 IM rule |
| E45 | Esomeprazole flagged for CYP2C19 UM although CPIC gives no esomeprazole recommendation | PPI rule restricted to CPIC PPIs |
| E44 | Label error: the "no alert" control had LDL-C 100.5 mg/dL, above the patient's target — the engine was right | Label fixed (documented in `cases.yaml`) |

Second run: 45/45, 0 omissions, 0 false flags, alerts per case 1.78 (naive) → 0.53 (−70%).

### Primary-source wording check (same day)
All cited facts were checked against CPIC PDFs, the 2026 Tegretol FDA label and the ACR 2020 gout guideline. One more label and rule were wrong:

| Case | Problem | Fix |
|---|---|---|
| E20 | CYP2C19 **rapid** metabolizer + PPI was labelled as an alert, but CPIC 2020 gives the same recommendation as for normal metabolizers | Label → no alert; rule removed for RM |
| — | Ultrarapid wording was "consider increasing dose"; CPIC says "Increase starting daily dose by 100%" (Optional) | Wording fixed; new case E46 |
| — | Poor metabolizer + PPI had no rule (CPIC: consider 50% reduction for chronic therapy) | Added as monitor-level item |

Current: 46/46, 0 omissions, 0 false flags, 0 unverified facts cited, alerts per case 1.78 → 0.52 (−71%).

## Limits (say these on stage)
- Synthetic cases test that rules behave as specified. They do **not** measure clinical accuracy.
- Labels are one author's reading of the guidelines until pharmacists review them; inter-rater agreement is not yet measured.
- Clopidogrel CPIC rules depend on the indication (ACS/PCI vs stroke vs PAD); the engine does not yet read the indication, so the card text lists each.
