"""PrecisionRx prototype API. Run: uv run uvicorn app.main:app --reload"""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile

from app.assess import AssessIn, assess
from app.cds_hooks import router as cds_router
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
