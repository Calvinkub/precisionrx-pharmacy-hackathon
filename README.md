# PrecisionRx — Pharmacy Hackathon

PGx-at-prescribing clinical decision support for Thai hospitals, plus an oncology pharmacy module (cfDNA + germline PGx + TKI interactions).

Status: hackathon concept. No company, partners, patient data or revenue yet.

## Prototype (branch `dev/prototype`)

NMR Response Dashboard: NMR panel (left) + patient history and medications (right) → disease risk from validated Thai scores, NMR add-on factors, medication findings for the pharmacist queue, lifestyle advice, and visit-to-visit change judged by Reference Change Value. **Synthetic data only.**

```bash
uv sync
uv run uvicorn app.main:app --port 8765   # http://localhost:8765 (NMR dashboard, ?case=1&visit=2)
                                           # http://localhost:8765/his (mock HIS ordering, ?hn=HN-0003&drug=clopidogrel&dose=75)
                                           # http://localhost:8765/queue (pharmacist queue)
uv run pytest                              # engine + API tests + eval gate
uv run python -m eval.run_eval --sheet     # eval report → eval/report.md
```

| Path | Content |
|---|---|
| `app/engines/` | Deterministic engines: `risk.py` (Thai CV Risk, Thai diabetes score), `rcv.py`, `panel.py`, `nmr_factors.py`, `meds.py` (PGx, DDI, statin response, adherence), `lifestyle.py` |
| `app/cds_hooks.py` | CDS Hooks service: discovery, `order-select`, `order-sign`, feedback → pharmacist queue |
| `app/evidence/` | `facts.yaml` (every output cites a fact id + source), `analytes.yaml` (NMR catalog: reference band, CVa, CVi) |
| `app/static/` | Single-page UI; `sample_panel.csv` = upload example (visit 3 of case 1) |
| `data/synthetic/` | 3 demo cases |
| `eval/` | 45-case gold-standard eval set, runner, report, pharmacist review sheet |
| `docs/` | Research notes behind the numbers (verify before pitching) |
| [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) | Plan and status |

## Files

| File | Content |
|---|---|
| [idea.md](idea.md) | Current idea (v3) |
| [idea_v2.md](idea_v2.md), [idea_v1_original.md](idea_v1_original.md) | Earlier versions |
| [critique_PrecisionRx.md](critique_PrecisionRx.md) | Simulated 6-judge panel critique of v2 |
| [market_research.md](market_research.md) | Thai market facts, test prices, competitors, TAM/SAM/SOM, claim check |
| [business_strategy.md](business_strategy.md) | Payer map, beachhead, pilot design, partnerships, pitch narrative |
| [business_case.md](business_case.md) | Unit economics, customer ROI, 3-year projection |
| [idea_validation.md](idea_validation.md) | Fatal-flaw analysis and hidden competitors |
| [.claude/skills/](.claude/skills/) | Claude Code judge skills (pharmacy, physician, biology/omics, AI/tech, regulatory, business, panel chair) |

Numbers marked 📊 are assumptions. Items marked ❓ are not yet verified. Check sources before using them in a pitch.
