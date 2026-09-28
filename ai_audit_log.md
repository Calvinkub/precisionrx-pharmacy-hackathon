# AI Audit Log — PrecisionRx prototype

File: [ai_audit_log.csv](ai_audit_log.csv) (UTF-8, 35 rows). Generator: [scripts/make_ai_audit_log.py](scripts/make_ai_audit_log.py).

## What is real and what is simulated

| Column | Source |
|---|---|
| `ai_decision`, `risk_level`, `reason`, `confidence` | **Real engine output** from branch `dev/prototype` on the synthetic demo data (CDS Hooks, `/api/assess`, oncology report) |
| `timestamp`, `user_id`, `outcome` | **Simulated** for the demo. Every outcome starts with `simulated:` |

All patients are synthetic. No real patient data.

## Columns

| Column | Meaning |
|---|---|
| `timestamp` | Time of the event (ISO 8601, +07:00) |
| `user_id` | Who triggered the event: `MD-demo-01` doctor at order entry, `RPh-demo-01` pharmacist review, `RPh-onc-demo-01` oncology pharmacist |
| `action` | What the user did: `order-select <HN>: <drug> <dose>`, `assess case <n> visit <v>`, `oncology report <id>` |
| `ai_decision` | Decision type + finding title: `hard_stop`, `flag_for_review`, `monitor`, `inform`, `no_alert` |
| `confidence` | **Evidence confidence**, not a model probability. The rules are deterministic. `high` = all cited facts are guideline / label / validated score and verified · `medium` = at least one emerging fact · `low` = assumption, unverified or missing fact |
| `risk_level` | From finding severity: stop → `critical`, action → `high`, monitor → `medium`, info → `low` |
| `reason` | Fact IDs the decision cites, with source (from `app/evidence/facts.yaml`) |
| `outcome` | Clinician response (simulated): blocked, accepted, overridden with reason → pharmacist queue, modified, acknowledged, signed |

## Summary of this log

- 35 events: 6 prescribing-time events (doctor, 5 orders), 21 pharmacist review events on 3 NMR cases, 8 oncology report events on 3 cfDNA cases
- Risk: 2 critical (HLA-B hard stops), 19 high, 2 medium, 12 low
- Confidence: 33 high, 2 medium (emerging evidence, e.g. CHIP flag)
- 1 `no_alert` row: amlodipine for HN-0002 causes no new finding (shows the alert-fatigue rule)

## Regenerate

```bash
git switch dev/prototype
uv run python scripts/make_ai_audit_log.py ai_audit_log.csv
```

In production, the same columns would be written by the server at each CDS Hooks call, assessment and feedback event, with real user IDs and real outcomes, and stored append-only.
