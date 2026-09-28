# Architecture — mapping to the NCD multi-omics directive

Status 2026-09-29. Synthetic data only. Every number the system shows comes from a published formula or a cited study in `app/evidence/facts.yaml`; LLMs never produce facts.

| Directive tier | Where | What it does | Honest substitution (why) |
|---|---|---|---|
| **1 Ingestion & normalization** | `app/ingest/` | FHIR R4 Bundle, HL7 v2 ORU^R01, lab PDF (text layer), NMR panel CSV of any size, cfDNA electropherogram CSV, wearable JSON, claims CSV → one `PatientRecord` (Pydantic) with provenance per value | No imputation for scores: missing inputs are reported per score (`DataIssue`), because imputed labs would silently change a risk. Unknown units are rejected, never guessed. |
| Terminology / units | `app/evidence/terminology.yaml`, `app/ingest/units.py` | LOINC + ICD-10 (checked on NLM Clinical Tables / WHO browser), UCUM canonical units with explicit conversion factors | Metabolic syndrome has no WHO ICD-10 code → ICD-10-CM E88.810. |
| NMR ">400 metabolites" | parser keeps every row | 215 synthetic rows kept; 29 interpreted | Real clinical panels report ~250 measures (Nightingale) or 112 + 41 (Bruker) — `NMR-PANEL-SIZE`. Unknown analytes are stored, not interpreted. |
| **2 Multi-agent harness** | `app/agents/graph.py` (LangGraph `StateGraph`, shared `PatientState`) | orchestrator → data_extraction → risk_scoring → clinical_reasoning → cfdna_qc → guideline_lookup → care_plan → summarizer/verifier | Only the planner and the summarizer call Claude (`claude-opus-5`, server-side fallbacks on). Both outputs are schema-validated; an invalid plan falls back to the standard order; every summary sentence must cite a retrieved fact id or it is dropped. Without credentials the same graph runs on deterministic templates. |
| **3 Tools** | `app/agents/tools.py`, REST `/api/v2/tools/{name}` | `vector_db_search`, `ehr_db_query`, `lab_reference_lookup`, `terminology_code_resolver`, `clinical_calculator` (eGFR CKD-EPI 2021, FIB-4, FLI, BMI, Thai CV Risk) + Claude tool JSON schemas | "ASCVD risk" uses Thai CV Risk Score (validated in Thais) instead of US Pooled Cohort Equations. |
| RAG | `app/agents/rag.py` | char-3-gram TF-IDF vectors + cosine over the verified evidence store (works for Thai text) | Corpus is our verified facts, not full guideline PDFs (licensing + every chunk must be citable). No external embedding service → deterministic. |
| **4 Risk analytics & XAI** | `app/engines/calculators.py` | 5 diseases: CVD (Thai CV Risk), T2D (Thai Diabetes Score), MetS (harmonized 2009, Asian waist), CKD (CKD-EPI 2021 + KDIGO 2024 heat map), MASLD (FLI + FIB-4) | **No XGBoost/SHAP**: there is no outcome data to train or calibrate on, so a trained model would be fabricated. Instead the explanations are *exact*: log-hazard terms vs the calculator's reference person (= Shapley values of a linear predictor against a fixed baseline), points, criteria, logit terms. Uncertainty = Monte Carlo over within-person variation (EFLM CVi) of lab inputs. |
| Audit trail | `Contribution.source`, `ToolCall`, `retrieved_evidence` | each contribution points to document + locator (e.g. `lab_2026-05-06.hl7 · line 9 OBX|4`); each tool call and evidence hit is logged in state | |
| **5 Doctor UI** | API only (`/api/v2/*`; the `/ncd/` page was replaced by the consumer app, 28 Sep 2026) | risk vector, exact waterfall, metabolic radar, cfDNA electropherogram + QC, agent trace, care-plan editor → approve → FHIR `CarePlan` + `ServiceRequest` bundle (`/api/v2/careplan/export`) | cfDNA shows **sample QC** + a research-only short-fragment number. It does **not** raise a cancer alert: CE fragment-size profiles are not a validated cancer screen (validated fragmentomics uses sequencing — `CFDNA-FRAGMENTOMICS-SEQ`). |
| API | `app/main.py` | REST `/api/v2/patients`, `/run`, `/tools`, `/careplan/export`; WebSocket `/ws/v2/patients/{id}/run` streams one event per agent node | WebSocket is for local/dev; serverless hosts (Vercel) use the REST route — the UI falls back automatically. |

The web UI is now a 5-page consumer app (`/` hero + risk traces, `/identification/`, `/metabolomics/`, `/molecular/`, `/action-plan/`) whose risk numbers come from these same engines via `scripts/build_consumer_data.py`; cfDNA values there are a labelled mock.

## Run
```bash
uv run python -m scripts.make_synthetic_patients   # regenerate P001/P002 multi-source folders
uv run uvicorn app.main:app --port 8765             # http://localhost:8765/  (agent run: POST /api/v2/patients/P002/run)
ANTHROPIC_API_KEY=... uv run uvicorn app.main:app --port 8765   # enables Claude planner + summarizer
```

## Known limits
- Scores are validated in their own cohorts (Thai CV Risk, Thai diabetes score in Thais; FLI in Italians; CKD-EPI in US cohorts). NMR reference bands are UK Biobank P10–P90.
- `METS-HARMONIZED-2009` and `WHO-2005-PREVENTABLE` wording is from abstract/secondary copies (`verified: false`, shown with a dashed marker).
- CKD needs abnormality for > 3 months; a single visit can only flag "confirm".
