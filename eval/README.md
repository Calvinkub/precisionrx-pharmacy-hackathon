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

## Limits (say these on stage)
- Synthetic cases test that rules behave as specified. They do **not** measure clinical accuracy.
- Labels are one author's reading of the guidelines until pharmacists review them; inter-rater agreement is not yet measured.
- 4 cited fact ids are still `verified: false` (wording from memory / secondary source) — see report.
