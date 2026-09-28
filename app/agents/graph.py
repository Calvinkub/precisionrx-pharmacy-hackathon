"""Tier 2 — multi-agent harness on LangGraph with a shared PatientState (memory bus).

  orchestrator (LLM planner, validated) -> data_extraction -> risk_scoring -> clinical_reasoning
  -> [cfdna_qc] -> guideline_lookup -> care_plan -> summarizer (LLM, fact-ID constrained) -> verifier

Only the planner and the summarizer use an LLM; both are validated and have deterministic
fallbacks. Scores, flags and evidence come from code, so the same input gives the same result.
"""

from datetime import date, datetime
from statistics import mean

from langgraph.graph import END, START, StateGraph

from app.agents import llm, tools
from app.engines import calculators as C
from app.engines import careplan
from app.engines.cfdna_qc import analyse as cfdna_analyse
from app.engines.drug_effects import moved_by
from app.engines.meds import STATINS
from app.engines.nmr_factors import nmr_factors
from app.engines.nmr_summary import summarize as nmr_summarize
from app.engines.panel import catalog, facts
from app.ingest.normalize import build_record
from app.ingest.schemas import AgentMessage, PatientState, ToolCall

ORDER = ["data_extraction", "risk_scoring", "clinical_reasoning", "cfdna_qc", "guideline_lookup", "care_plan", "summarizer"]
CVI = {"total_c": 5.3, "creatinine": 4.4, "tg": 19.8}  # EFLM within-person CV% (EFLM-CVI)


def _msg(state: PatientState, agent: str, content: str) -> list[AgentMessage]:
    return [*state.agent_messages, AgentMessage(agent=agent, content=content)]


def _status(state: PatientState, node: str, s: str) -> dict:
    return {**state.execution_status, node: s}


def _tool(state: PatientState, agent: str, name: str, args: dict, output) -> list[ToolCall]:
    return [*state.tool_outputs, ToolCall(tool=name, args=args, output=output, agent=agent)]


# ------------------------------------------------------------------ nodes
def orchestrator(state: PatientState) -> dict:
    folder = tools.patient_folder(state.patient_id)
    files = sorted(p.name for p in folder.iterdir())
    available = {
        "ehr_fhir": any(f.endswith(".fhir.json") for f in files), "hl7_labs": any(f.endswith(".hl7") for f in files),
        "lab_pdf": any(f.endswith(".pdf") for f in files), "nmr": any(f.startswith("nmr") for f in files),
        "cfdna_electropherogram": any(f.startswith("cfdna") for f in files), "wearable": any(f.startswith("wearable") for f in files),
        "claims": any(f.startswith("claims") for f in files),
    }
    default = [s for s in ORDER if s != "cfdna_qc" or available["cfdna_electropherogram"]]
    planned, status = llm.plan(available)
    steps, source = default, "deterministic"
    if planned:
        s = [x for x in planned["steps"] if x in ORDER]
        valid = (s and s[0] == "data_extraction" and s[-1] == "summarizer"
                 and all(s.index(a) < s.index(b) for a, b in [("risk_scoring", "clinical_reasoning")] if a in s and b in s)
                 and ("cfdna_qc" not in s or available["cfdna_electropherogram"]))
        if valid and set(default) - {"cfdna_qc"} <= set(s):
            steps, source = sorted(set(s), key=ORDER.index), "llm"
    rationale = planned["rationale"] if (planned and source == "llm") else "ลำดับมาตรฐาน: ดึงข้อมูล → คำนวณความเสี่ยง → วิเคราะห์ข้าม modality → หาหลักฐาน → แผนดูแล → สรุป"
    return {"raw_data": {"files": files, "available": available}, "intermediate_features": {"plan": steps, "plan_source": source, "llm_status": status},
            "agent_messages": _msg(state, "orchestrator", f"แผน ({source}): {' → '.join(steps)} · {rationale}"),
            "execution_status": {**{s: ("pending" if s in steps else "skipped") for s in ORDER}, "orchestrator": "done"}}


def data_extraction(state: PatientState) -> dict:
    folder = tools.patient_folder(state.patient_id)
    rec, raw = build_record(folder)
    blocking = [i for i in rec.issues if i.severity == "blocking"]
    msg = (f"รวม {len(rec.sources)} แหล่ง: lab {len(rec.observations)} ค่า, NMR {raw['n_metabolites']} สาร "
           f"(ตีความได้ {raw['n_interpreted_metabolites']}), ยา {len(rec.medications)}, โรค {len(rec.conditions)}, "
           f"wearable {len(rec.lifestyle)} วัน, เคลม {len(rec.claims)} · ปัญหาข้อมูล {len(rec.issues)} ({len(blocking)} ร้ายแรง)")
    return {"normalized_json": rec, "raw_data": {**state.raw_data, **raw},
            "agent_messages": _msg(state, "data_extraction", msg), "execution_status": _status(state, "data_extraction", "done")}


def _features(state: PatientState) -> dict:
    rec = state.normalized_json
    d = rec.demographics
    labs = {o.key: o for o in rec.observations if "implausible" not in o.flags}
    nmr = {m.key: m.value for m in rec.metabolomics if m.interpreted}
    bmi = d.weight_kg / (d.height_cm / 100) ** 2 if d.weight_kg and d.height_cm else None
    drugs = [m.drug for m in rec.medications if m.status == "active"]
    val = lambda k: labs[k].value if k in labs else nmr.get(k)
    src = {k: {"document": o.provenance.document, "locator": o.provenance.locator, "source": o.provenance.source} for k, o in labs.items()}
    act = [x.active_minutes for x in rec.lifestyle if x.active_minutes is not None]
    steps = [x.steps for x in rec.lifestyle if x.steps is not None]
    return {
        "age": d.age, "male": d.sex == "male", "bmi": bmi, "waist": d.waist_cm, "sbp": d.sbp, "dbp": d.dbp, "smoker": d.smoker,
        "diabetes": rec.has_condition("E11") or (val("hba1c") or 0) >= 6.5, "hypertension": rec.has_condition("I10"),
        "family_dm": d.family_history_dm, "drugs": drugs, "on_statin": any(x in STATINS for x in drugs),
        "on_glucose_drug": any(x in ("metformin", "semaglutide", "liraglutide") for x in drugs),
        "on_bp_drug": any(x in ("amlodipine", "losartan", "enalapril") for x in drugs),
        "labs": {k: val(k) for k in ("total_c", "ldl_c", "hdl_c", "tg", "glucose", "hba1c", "creatinine", "uacr", "alt", "ast", "ggt", "platelets")},
        "nmr": nmr, "sources": src,
        "active_minutes_week": mean(act) * 7 if act else None, "steps_day": mean(steps) if steps else None,
        "prediabetes": 5.7 <= (val("hba1c") or 0) < 6.5 or 5.6 <= (val("glucose") or 0) < 7.0,
    }


def risk_scoring(state: PatientState) -> dict:
    f = _features(state)
    L, src = f["labs"], f["sources"]
    common_src = {"sbp": {"document": "record.fhir.json", "locator": "Observation/bp"}, "waist_cm": {"document": "record.fhir.json", "locator": "Observation/8280-0"}}
    tc_mg = L["total_c"] * 38.67 if L["total_c"] else None
    scores = [
        C.thai_cv_risk(f["age"], f["male"], f["sbp"], f["diabetes"], tc_mg, f["smoker"], CVI["total_c"], {**common_src, **src}),
        C.thai_diabetes_score(f["age"], f["male"], f["bmi"], f["waist"], f["hypertension"], f["family_dm"], f["diabetes"], {**common_src, **src}),
        C.metabolic_syndrome(f["male"], f["waist"], L["tg"], L["hdl_c"], f["sbp"], f["dbp"], L["glucose"],
                             on_lipid_drug=False, on_bp_drug=f["on_bp_drug"], on_glucose_drug=f["on_glucose_drug"], sources={**common_src, **src}),
        C.ckd(L["creatinine"], f["age"], f["male"], L["uacr"], CVI["creatinine"], src),
        C.liver(L["tg"], f["bmi"], L["ggt"], f["waist"], f["age"], L["ast"], L["alt"], L["platelets"], CVI["tg"], {**common_src, **src}),
    ]
    vectors = [s.to_dict() for s in scores]
    if f["on_statin"]:
        for v in vectors:
            if v["id"] == "cvd":
                v["notes"].append("ใช้ statin อยู่ — total cholesterol ที่ใช้คำนวณถูกยาลดลงแล้ว ความเสี่ยงก่อนรักษาสูงกว่านี้")
    calls = state.tool_outputs
    for s in scores:
        calls = [*calls, ToolCall(tool="clinical_calculator", args={"calc_type": s.method}, output={"value": s.value, "category": s.category}, agent="risk_scoring")]
    summary = ", ".join(f"{s.disease} {s.display} ({s.category_label})" for s in scores)
    return {"intermediate_features": {**state.intermediate_features, "features": {k: v for k, v in f.items() if k not in ("sources",)}},
            "risk_vectors": vectors, "tool_outputs": calls,
            "agent_messages": _msg(state, "risk_scoring", summary), "execution_status": _status(state, "risk_scoring", "done")}


def _phenotype(nmr: dict) -> list[dict]:
    cat = catalog()
    rows = []
    for k in ("leucine", "isoleucine", "valine", "bcaa", "phenylalanine", "glyca", "apob", "tg", "glucose", "omega3_pct"):
        if k in nmr and k in cat and cat[k]["ref_low"] is not None:
            lo, hi = cat[k]["ref_low"], cat[k]["ref_high"]
            rows.append({"id": k, "abbr": cat[k]["abbr"], "value": nmr[k], "unit": cat[k]["unit"], "low": lo, "high": hi,
                         "position": round((nmr[k] - lo) / (hi - lo), 2)})  # 0 = P10, 1 = P90
    return rows


def clinical_reasoning(state: PatientState) -> dict:
    f = state.intermediate_features["features"]
    rec = state.normalized_json
    nmr, L = f["nmr"], f["labs"]
    risks = {v["id"]: v for v in state.risk_vectors}
    flags = []
    # cross-modal: molecular signal ahead of the clinical glucose threshold
    bcaa_hi = nmr.get("bcaa") is not None and nmr["bcaa"] > catalog()["bcaa"]["ref_high"]
    if bcaa_hi and not f["diabetes"]:
        flags.append({"id": "bcaa-prediabetes", "severity": "monitor", "kind": "cross-modal",
                      "title": "BCAA สูงร่วมกับ HbA1c/FPG ในช่วงก่อนเบาหวาน" if f["prediabetes"] else "BCAA สูงแม้น้ำตาลยังปกติ",
                      "detail": f"BCAA {nmr['bcaa']:.0f} µmol/L > P90 · HbA1c {L['hba1c'] or '–'}% — สัญญาณทาง metabolic สัมพันธ์กับเบาหวานในอนาคต (หลักฐานเบื้องต้น ไม่ใช่การวินิจฉัย)",
                      "fact_ids": ["BCAA-T2D", "ADA-2026-DX"]})
    for x in nmr_factors(nmr, risks.get("cvd", {}).get("value"), f["diabetes"]):
        flags.append({"id": x.id, "severity": x.severity, "kind": "nmr", "title": x.title, "detail": x.detail, "fact_ids": x.fact_ids})
    moved = moved_by(f["drugs"])
    for a, effs in moved.items():
        if a == "apob" and a in nmr:
            flags.append({"id": "drug-lowered-apob", "severity": "info", "kind": "medication", "title": "ค่าไขมันถูกยาลดลง",
                          "detail": f"{', '.join(e['drug'] for e in effs)} ลด ApoB/LDL — ความเสี่ยงหัวใจก่อนรักษาสูงกว่าที่เห็น",
                          "fact_ids": effs[0]["fact_ids"]})
    # comorbidity: conditions in claims/EHR the scores should know about
    coded = sorted({c.coding.code for c in rec.conditions} | {c.coding.code for c in rec.claims})
    if f["diabetes"] and risks.get("ckd", {}).get("category") in ("moderate", "high", "very_high"):
        flags.append({"id": "dm-ckd", "severity": "action", "kind": "comorbidity", "title": "เบาหวานร่วมกับไตเสื่อมตามเกณฑ์ KDIGO",
                      "detail": f"eGFR/UACR {risks['ckd']['display']} ในผู้ป่วยเบาหวาน — ยืนยันซ้ำใน 3 เดือน และทบทวนยาที่ขับทางไต", "fact_ids": ["KDIGO-2024"]})
    # lifestyle from wearable
    if f["active_minutes_week"] is not None and f["active_minutes_week"] < 150:
        flags.append({"id": "low-activity", "severity": "monitor", "kind": "lifestyle", "title": "กิจกรรมทางกายต่ำกว่าเกณฑ์",
                      "detail": f"smartwatch เฉลี่ย {f['active_minutes_week']:.0f} นาที/สัปดาห์ ({f['steps_day']:.0f} ก้าว/วัน) — เกณฑ์ WHO 150–300 นาที", "fact_ids": ["WHO-PA-2020"]})
    # data quality flags
    for i in rec.issues:
        if i.severity in ("warning", "blocking") and i.kind in ("missing", "implausible", "unit_unknown"):
            flags.append({"id": f"data-{i.field}", "severity": "monitor", "kind": "data", "title": f"ข้อมูล: {i.field}", "detail": i.detail, "fact_ids": []})
    features = {**state.intermediate_features, "phenotype": _phenotype(nmr), "flags": flags, "coded_conditions": coded,
                "nmr_domains": nmr_summarize(nmr, None, diabetes=f["diabetes"], high_risk=f["diabetes"] or (risks.get("cvd", {}).get("value") or 0) >= 20, drugs=f["drugs"])}
    return {"intermediate_features": features, "agent_messages": _msg(state, "clinical_reasoning", f"สัญญาณเตือน {len(flags)} รายการ: " + ", ".join(x["title"] for x in flags[:5])),
            "execution_status": _status(state, "clinical_reasoning", "done")}


def cfdna_qc(state: PatientState) -> dict:
    rec = state.normalized_json
    if not rec.cfdna:
        return {"execution_status": _status(state, "cfdna_qc", "skipped")}
    qc = cfdna_analyse(rec.cfdna.sizes_bp, rec.cfdna.intensity, rec.cfdna.concentration_ng_ul)
    qc["trace"] = {"sizes_bp": rec.cfdna.sizes_bp, "rfu": rec.cfdna.intensity, "instrument": rec.cfdna.instrument}
    flags = [*state.intermediate_features.get("flags", []), *[{**x, "kind": "cfdna"} for x in qc["findings"] if x["severity"] != "info"]]
    return {"intermediate_features": {**state.intermediate_features, "cfdna": qc, "flags": flags},
            "agent_messages": _msg(state, "cfdna_qc", f"cfDNA: peak {qc['main_peak_bp']:.0f} bp, HMW {qc['hmw_fraction']:.0%} → {qc['status']}"),
            "execution_status": _status(state, "cfdna_qc", "done")}


QUERIES = {"cvd": ("ความเสี่ยงโรคหัวใจ Thai CV risk LDL ApoB target", "cardiovascular"),
           "dm": ("diabetes risk prediabetes FPG HbA1c lifestyle", "diabetes"),
           "mets": ("metabolic syndrome waist triglyceride HDL blood pressure glucose", "metabolic"),
           "ckd": ("eGFR CKD-EPI albuminuria KDIGO", "kidney"),
           "masld": ("fatty liver FIB-4 fibrosis FLI", "liver")}


def guideline_lookup(state: PatientState) -> dict:
    evidence, calls = [], state.tool_outputs
    for rid, (q, dom) in QUERIES.items():
        hits = tools.vector_db_search(q, dom, 3)
        calls = [*calls, ToolCall(tool="vector_db_search", args={"query": q, "domain": dom}, output=[h["fact_id"] for h in hits], agent="guideline_lookup")]
        evidence += [{**h, "for": rid} for h in hits]
    cited = {fid for v in state.risk_vectors for fid in v["fact_ids"]} | {fid for x in state.intermediate_features.get("flags", []) for fid in x["fact_ids"]}
    store = facts()["facts"]
    for fid in sorted(cited - {e["fact_id"] for e in evidence}):
        if fid in store:
            evidence.append({"fact_id": fid, "score": None, "text": store[fid]["text"], "source": store[fid]["source"],
                             "url": store[fid]["url"], "level": store[fid]["level"], "for": "cited"})
    return {"retrieved_evidence": evidence, "tool_outputs": calls,
            "agent_messages": _msg(state, "guideline_lookup", f"หลักฐาน {len(evidence)} ชิ้น (ค้นด้วย vector search {len(QUERIES)} ครั้ง)"),
            "execution_status": _status(state, "guideline_lookup", "done")}


def care_plan(state: PatientState) -> dict:
    risks = {v["id"]: v for v in state.risk_vectors}
    items = careplan.propose(risks, state.intermediate_features["features"], state.intermediate_features.get("flags", []))
    return {"intermediate_features": {**state.intermediate_features, "care_plan": items},
            "agent_messages": _msg(state, "care_plan", f"เสนอ {len(items)} รายการให้แพทย์เลือก/แก้ไข/อนุมัติ"),
            "execution_status": _status(state, "care_plan", "done")}


def _template_summary(state: PatientState) -> list[dict]:
    out = []
    for v in state.risk_vectors:
        if v["category"] not in ("not_assessable", "not_applicable"):
            out.append({"text": f"{v['disease']}: {v['display']} — {v['category_label']} ({v['method']})", "fact_ids": v["fact_ids"][:2]})
    for x in state.intermediate_features.get("flags", [])[:3]:
        if x["fact_ids"]:
            out.append({"text": f"{x['title']}", "fact_ids": x["fact_ids"][:2]})
    return out


def summarizer(state: PatientState) -> dict:
    allowed = sorted({e["fact_id"] for e in state.retrieved_evidence})
    payload = {"risks": [{k: v[k] for k in ("disease", "display", "category_label", "method", "fact_ids", "notes")} for v in state.risk_vectors],
               "flags": [{k: x[k] for k in ("title", "detail", "fact_ids")} for x in state.intermediate_features.get("flags", [])],
               "allowed_fact_ids": allowed}
    out, status = llm.summarize(payload)
    sentences, mode = (out["sentences"], "llm") if out else (_template_summary(state), "template")
    # verifier: drop any sentence without a known fact id; strip unknown ids
    kept, dropped = [], 0
    for s in sentences:
        ids = [i for i in s.get("fact_ids", []) if i in allowed]
        if ids:
            kept.append({"text": s["text"], "fact_ids": ids})
        else:
            dropped += 1
    return {"summary": {"mode": mode, "llm_status": status, "sentences": kept, "dropped_unsupported": dropped,
                        "generated_at": datetime.now().isoformat(timespec="seconds")},
            "agent_messages": _msg(state, "summarizer", f"สรุป {len(kept)} ประโยค ({mode}; ตัดประโยคที่ไม่มีหลักฐาน {dropped}) · {status}"),
            "execution_status": _status(state, "summarizer", "done")}


def _route(after: str):
    def pick(state: PatientState) -> str:
        plan = state.intermediate_features.get("plan", ORDER)
        rest = [s for s in ORDER[ORDER.index(after) + 1:] if s in plan] if after in ORDER else [s for s in ORDER if s in plan]
        return rest[0] if rest else END
    return pick


def build_graph():
    g = StateGraph(PatientState)
    g.add_node("orchestrator", orchestrator)
    for name, fn in [("data_extraction", data_extraction), ("risk_scoring", risk_scoring), ("clinical_reasoning", clinical_reasoning),
                     ("cfdna_qc", cfdna_qc), ("guideline_lookup", guideline_lookup), ("care_plan", care_plan), ("summarizer", summarizer)]:
        g.add_node(name, fn)
    g.add_edge(START, "orchestrator")
    targets = {n: n for n in ORDER} | {END: END}
    g.add_conditional_edges("orchestrator", _route("orchestrator"), targets)
    for n in ORDER:
        g.add_conditional_edges(n, _route(n), targets)
    return g.compile()


GRAPH = build_graph()


def run(patient_id: str) -> PatientState:
    out = GRAPH.invoke(PatientState(patient_id=patient_id))
    return out if isinstance(out, PatientState) else PatientState(**out)
