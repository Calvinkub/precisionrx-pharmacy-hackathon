# PrecisionRx — Pharmacy Hackathon

PGx-at-prescribing clinical decision support for Thai hospitals, plus an oncology pharmacy module (cfDNA + germline PGx + TKI interactions).

Status: hackathon concept. No company, partners, patient data or revenue yet.

## Prototype (branch `dev/prototype`)

NMR Response Dashboard: NMR panel (left) + patient history and medications (right) → disease risk from validated Thai scores, NMR add-on factors, medication findings for the pharmacist queue, lifestyle advice, and visit-to-visit change judged by Reference Change Value. **Synthetic data only.**

```bash
uv sync
(cd web && pnpm install && pnpm build)      # Astro UI → web/dist (served by FastAPI)
uv run uvicorn app.main:app --port 8765     # http://localhost:8765
uv run pytest                               # engine + API + CDS Hooks tests + eval gate
uv run python -m eval.run_eval --sheet      # eval report → eval/report.md
```

Pages (consumer app, one sample person `web/src/data/mockPatient.json`): `/` Multi-omics landing (decorative art, no data) · `/identification/` Identification data (BMI, waist, BP, smoking — only the fields provided) · `/metabolomics/` Metabolites Profile (NMR spectrum, insight ↔ raw) · `/molecular/` cfDNA Pattern (CE electropherogram + QC; methylation/origin are **labelled mock values**) · `/action-plan/` Advices (next steps, checklist, PDF brief, .ics). Theme: dark neon by default, light via the toggle.
Risk numbers are computed by the Python engines: after changing the profile run `uv run python -m scripts.build_consumer_data` (writes `web/src/data/computed.json`; a test fails if it drifts). The doctor/pharmacist APIs (`/api/v2/*`, `/api/cfdna/*`, `/api/oncology/*`, CDS Hooks) remain; their old pages were removed.
UI dev with hot reload: run the Python server, then `cd web && pnpm dev` → http://localhost:4321 (proxies `/api` and `/cds-services` to port 8765). Type/a11y check: `pnpm check`.

| Path | Content |
|---|---|
| `app/engines/` | Deterministic engines: `risk.py` (Thai CV Risk, Thai diabetes score), `rcv.py`, `panel.py`, `nmr_factors.py`, `meds.py` (PGx, DDI, statin response, adherence), `lifestyle.py` |
| `app/cds_hooks.py` | CDS Hooks service (API only; the mock HIS page was removed) |
| `app/engines/dispensing.py`, `drug_effects.py` | Regular meds + PDC from refill history; which NMR markers each drug moves (`evidence/drug_effects.yaml`) |
| `app/engines/oncology.py` | cfDNA module: CHIP / possible-germline flags, ctDNA-negative caveat, T790M → osimertinib, TKI + PPI, DPYD / UGT1A1 |
| `app/evidence/` | `facts.yaml` (every output cites a fact id + source), `analytes.yaml` (NMR catalog: reference band, CVa, CVi) |
| `web/` | Astro 7 + Tailwind v4 + lucide (`src/pages`, `src/components`, `src/layouts/MainLayout.astro`, `src/styles/app.css` tokens). `public/sample_panel.csv` = upload example |
| `data/synthetic/` | 3 cardiometabolic cases (with dispensing history) + `oncology/` 3 cfDNA cases |
| `eval/` | 45-case gold-standard eval set, runner, report, pharmacist review sheet |
| `docs/` | Research notes behind the numbers (verify before pitching) |
| [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) | Plan and status |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | 5-tier NCD multi-omics architecture: what is where, and the honest substitutions |
| [DEPLOY.md](DEPLOY.md) | Deploy to Vercel (`vercel.json`) or any Docker host (`Dockerfile`) |

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
