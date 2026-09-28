"""PrecisionRx prototype API. Run: uv run uvicorn app.main:app --reload"""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.assess import AssessIn, assess
from app.cds_hooks import router as cds_router
from app.engines.panel import catalog, facts, parse_csv

ROOT = Path(__file__).resolve().parent
CASES = ROOT.parent / "data" / "synthetic"

app = FastAPI(title="PrecisionRx prototype (synthetic data only)")
app.include_router(cds_router)
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/his")
def his():
    return FileResponse(ROOT / "static" / "his.html")


@app.get("/queue")
def queue_page():
    return FileResponse(ROOT / "static" / "queue.html")


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
