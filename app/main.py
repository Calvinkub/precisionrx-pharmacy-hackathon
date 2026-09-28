"""PrecisionRx prototype API. Run: uv run uvicorn app.main:app --reload"""

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, WebSocket
from pydantic import BaseModel

from app.agents import tools as agent_tools
from app.agents.graph import GRAPH
from app.agents.graph import run as run_graph
from app.assess import AssessIn, assess
from app.engines.careplan import export_fhir as careplan_export
from app.ingest.normalize import build_record
from app.ingest.schemas import PatientState
from app.cds_hooks import router as cds_router
from app.engines.dispensing import regular_meds
from app.engines.drug_effects import effects_for
from app.engines.oncology import assess_oncology
from app.engines.panel import catalog, facts, parse_csv

ROOT = Path(__file__).resolve().parent
CASES = ROOT.parent / "data" / "synthetic"

app = FastAPI(title="PrecisionRx prototype (synthetic data only)")
WEB = ROOT.parent / "web" / "dist"  # Astro build output (cd web && pnpm build)
EVAL = ROOT.parent / "eval" / "results.json"
app.include_router(cds_router)


@app.get("/api/eval")
def eval_summary():
    if not EVAL.is_file():
        raise HTTPException(404, "run: uv run python -m eval.run_eval")
    return {"summary": json.loads(EVAL.read_text(encoding="utf-8"))["summary"]}


@app.get("/api/his/patients")
def his_patients():
    return json.loads((CASES / "his_patients.json").read_text(encoding="utf-8"))


@app.get("/api/catalog")
def get_catalog():
    return {"snapshot": facts()["snapshot"], "analytes": list(catalog().values())}


@app.get("/api/cases")
def list_cases():
    out = []
    for f in sorted(CASES.glob("case_*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        out.append({"id": c["id"], "label": c["label"], "story": c.get("story", "")})
    return out


@app.get("/api/cases/{case_id}")
def get_case(case_id: str):
    f = CASES / f"case_{case_id}.json"
    if not f.is_file() or f.parent != CASES:
        raise HTTPException(404, "case not found")
    return json.loads(f.read_text(encoding="utf-8"))


def _case(case_id: str) -> dict:
    f = CASES / f"case_{case_id}.json"
    if not f.is_file() or f.parent != CASES:
        raise HTTPException(404, "case not found")
    return json.loads(f.read_text(encoding="utf-8"))


@app.get("/api/cases/{case_id}/medications")
def case_medications(case_id: str, visit: int = 1):
    """Regular medications as of a visit, pulled from the (synthetic) dispensing record."""
    c = _case(case_id)
    visits = c["visits"]
    idx = min(max(visit, 1), len(visits)) - 1
    as_of = date.fromisoformat(visits[idx]["date"])
    store = facts()["facts"]
    out, used = [], {"DISPENSING-PDC", "PQA-PDC80"}
    for m in regular_meds(c.get("dispensing", []), as_of):
        # index of the first visit taken ON this drug (None = already on it at visit 1)
        start_visit = next((i for i, v in enumerate(visits) if date.fromisoformat(v["date"]) >= m.first_fill), None)
        eff = effects_for(m.drug)
        used.update(eff["fact_ids"])
        out.append({**asdict(m), "first_fill": m.first_fill.isoformat(), "last_fill": m.last_fill.isoformat(),
                    "start_visit": None if start_visit in (None, 0) else start_visit, **eff})
    return {"as_of": as_of.isoformat(), "source": "ประวัติการรับยาจากห้องยา (ข้อมูลจำลอง)", "medications": out,
            "facts": {k: store[k] for k in sorted(used) if k in store}}


ONCO = CASES / "oncology"


# ---------------------------------------------------------------- v2: NCD multi-omics pipeline (doctor + pharmacist)
@app.get("/api/v2/patients")
def v2_patients():
    out = []
    for d in sorted(agent_tools.PATIENTS.iterdir()):
        if d.is_dir():
            rec, raw = build_record(d)
            out.append({"id": d.name, "sex": rec.demographics.sex, "age": rec.demographics.age, "sources": rec.sources,
                        "conditions": [c.coding.code for c in rec.conditions]})
    return out


@app.post("/api/v2/patients/{patient_id}/run")
def v2_run(patient_id: str):
    try:
        state = run_graph(patient_id)
    except KeyError:
        raise HTTPException(404, "patient not found")
    store = facts()["facts"]
    return {**state.model_dump(mode="json"), "facts": store}


@app.websocket("/ws/v2/patients/{patient_id}/run")
async def v2_run_ws(ws: WebSocket, patient_id: str):
    """Streams one event per finished agent node (local/dev; serverless hosts should use the REST route)."""
    await ws.accept()
    try:
        for update in GRAPH.stream(PatientState(patient_id=patient_id), stream_mode="updates"):
            for node, delta in update.items():
                msgs = delta.get("agent_messages") or []
                await ws.send_json({"node": node, "message": msgs[-1].content if msgs else "", "status": "done"})
        await ws.send_json({"node": "__end__", "status": "done"})
    except KeyError:
        await ws.send_json({"error": "patient not found"})
    await ws.close()


@app.get("/api/v2/tools")
def v2_tools():
    return agent_tools.TOOL_SCHEMAS


@app.post("/api/v2/tools/{name}")
def v2_tool(name: str, args: dict):
    fn = agent_tools.TOOLS.get(name)
    if not fn:
        raise HTTPException(404, "unknown tool")
    try:
        return {"tool": name, "output": fn(**args)}
    except (KeyError, TypeError, ValueError) as e:
        raise HTTPException(422, f"{type(e).__name__}: {e}")


class CarePlanIn(BaseModel):
    patient_id: str
    items: list[dict]
    approver: str
    note: str = ""


@app.post("/api/v2/careplan/export")
def v2_careplan(body: CarePlanIn):
    if not body.approver.strip():
        raise HTTPException(422, "approver required")
    if not any(i.get("selected") for i in body.items):
        raise HTTPException(422, "select at least one item")
    return careplan_export(body.patient_id, body.items, body.approver.strip(), body.note)


@app.get("/api/oncology/cases")
def onco_cases():
    return [{"id": c["id"], "label": c["label"]} for c in
            (json.loads(f.read_text(encoding="utf-8")) for f in sorted(ONCO.glob("*.json")))]


@app.get("/api/oncology/cases/{case_id}")
def onco_case(case_id: str):
    f = ONCO / f"{case_id}.json"
    if not f.is_file() or f.parent != ONCO:
        raise HTTPException(404, "case not found")
    c = json.loads(f.read_text(encoding="utf-8"))
    result = assess_oncology(c)
    store = facts()["facts"]
    used = {fid for x in result["findings"] for fid in x["fact_ids"]} | {fid for v in result["variants"] for fl in v["flags"] for fid in fl["fact_ids"]}
    return {**c, **result, "facts": {k: store[k] for k in sorted(used) if k in store},
            "missing_facts": sorted(k for k in used if k not in store)}


@app.post("/api/panel/parse")
async def parse_panel(file: UploadFile):
    text = (await file.read()).decode("utf-8", errors="replace")
    values, unknown, date = parse_csv(text)
    if not values:
        raise HTTPException(422, "ไม่พบค่าสารที่รู้จักในไฟล์ (ต้องมีคอลัมน์ analyte,value)")
    return {"values": values, "unknown": unknown, "date": date}


@app.post("/api/assess")
def post_assess(req: AssessIn):
    if not req.visits:
        raise HTTPException(422, "ต้องมีผลตรวจอย่างน้อย 1 ครั้ง")
    return assess(req)


# Astro build as low-priority frontend routes: API routes always win. On Vercel these files are
# promoted to the CDN at build time. Falls back to a hint when the site is not built yet.
if WEB.is_dir():
    app.frontend("/", directory=WEB)
else:
    @app.get("/")
    def not_built():
        return {"error": "UI not built", "fix": "cd web && pnpm install && pnpm build"}
