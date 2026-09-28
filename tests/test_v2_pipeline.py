import math
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.agents import graph, rag, tools
from app.engines import calculators as C
from app.engines.cfdna_qc import analyse
from app.engines.careplan import export_fhir
from app.engines.panel import facts
from app.ingest import parsers as P
from app.ingest.normalize import build_record
from app.ingest.units import to_canonical
from app.main import app

client = TestClient(app)
P001 = Path("data/synthetic/patients/P001")


# ---------------- Tier 1
def test_unit_conversions():
    assert to_canonical("glucose", 108, "mg/dL")[0] == pytest.approx(5.99, abs=0.01)
    assert to_canonical("creatinine", 88.42, "umol/L")[0] == pytest.approx(1.0)
    assert to_canonical("albumin", 4.2, "g/dL")[0] == pytest.approx(42)
    assert to_canonical("hba1c", 48, "mmol/mol")[0] == pytest.approx(6.54, abs=0.02)
    assert to_canonical("glucose", 5, "furlongs") is None  # unknown unit is never guessed


def test_hl7_parser_reads_obx_and_pid():
    msg = "MSH|^~\\&|LIS\rPID|1||X9^^^H^MR||A^B||19800101|M\rOBR|1||L1|x|||202601020800\rOBX|1|NM|2160-0^Creatinine^LN||1.2|mg/dL|0.7-1.2||||F\r"
    r = P.parse_hl7_oru(msg, "t.hl7")
    assert r["demographics"]["sex"] == "male" and r["labs"][0][0] == "creatinine" and r["labs"][0][4] == date(2026, 1, 2)


def test_pdf_parser_extracts_text_layer_with_line_provenance():
    r = P.parse_lab_pdf((P001 / "lab_report_2026-06-12.pdf").read_bytes(), "x.pdf")
    got = {k: v for k, _, v, *_ in r["labs"]}
    assert got["alt"] == 48 and got["platelets"] == 250
    assert "Ferritin" in r["unmatched"]
    assert r["labs"][0][5].locator.startswith("page 1 line")


def test_record_merges_sources_and_reports_issues():
    rec, raw = build_record(P001, date(2026, 6, 12))
    assert {"fhir", "hl7v2", "pdf"} <= {o.provenance.source for o in rec.observations} | {"fhir"}
    assert rec.demographics.age == 52 and rec.demographics.waist_cm == 88 and rec.demographics.family_history_dm
    assert raw["n_metabolites"] > 200 and raw["n_interpreted_metabolites"] >= 28
    assert any(i.kind == "unmapped" for i in rec.issues)
    assert rec.obs("glucose").flags == ["converted"] and rec.obs("glucose").coding.code == "1558-6"


# ---------------- calculators + exact explanations
def test_published_worked_examples():
    assert C.egfr_ckd_epi_2021(1.0, 50, True) == pytest.approx(91.7, abs=0.1)
    assert C.egfr_ckd_epi_2021(0.8, 60, False) == pytest.approx(84.3, abs=0.1)
    assert C.fli(150, 27, 40, 95) == pytest.approx(61.5, abs=0.1)
    assert C.fib4(55, 40, 45, 200) == pytest.approx(1.64, abs=0.01)


def test_cvd_contributions_are_exact():
    r = C.thai_cv_risk(60, True, 150, True, 240, True, cv_tc=5.3)
    lp_gap = sum(c.contribution for c in r.contributions)
    s0 = C.S0
    # baseline LP + contributions reproduces the patient's risk exactly
    base_lp = math.log(math.log(1 - r.baseline / 100) / math.log(s0))
    assert (1 - s0 ** math.exp(base_lp + lp_gap)) * 100 == pytest.approx(r.value, abs=0.01)
    assert r.interval[0] <= r.value <= r.interval[1]


def test_tdrs_points_sum_to_score():
    r = C.thai_diabetes_score(52, False, 27.9, 88, False, True, False)
    assert sum(c.contribution for c in r.contributions) == r.value == 13


def test_mets_counts_criteria_and_treatment():
    r = C.metabolic_syndrome(True, 95, 1.2, 1.1, 120, 70, 5.0, on_bp_drug=True)
    assert r.value == 2 and r.category == "at_risk"


def test_ckd_needs_three_months_and_heat_map():
    r = C.ckd(1.4, 61, True, 45)
    assert r.display.startswith("57") and "G3a/A2" in r.display and r.category == "high"
    assert any("3 เดือน" in n for n in r.notes)


def test_fib4_older_cutoff_applies_above_65_only():
    # FIB-4 ≈1.8: at 65 the 1.3 cut-off applies (needs work-up); above 65 the 2.0 cut-off applies (low)
    assert C.liver(1.0, 22, 20, 80, 65, 30, 30, 200).category == "high"
    assert C.liver(1.0, 22, 20, 80, 66, 30, 30, 200).category == "low"


# ---------------- cfDNA QC
def test_cfdna_never_calls_cancer_and_flags_contamination():
    good = P.parse_cfdna_electropherogram((P001 / "cfdna_2026-06-12.csv").read_text(), "a.csv")
    bad = P.parse_cfdna_electropherogram(Path("data/synthetic/patients/P002/cfdna_2026-05-06.csv").read_text(), "b.csv")
    g, b = analyse(good.sizes_bp, good.intensity, 0.4), analyse(bad.sizes_bp, bad.intensity, 0.4)
    assert g["status"] == "pass" and 160 <= g["main_peak_bp"] <= 172
    assert b["status"] == "fail" and any(f["id"] == "cfdna-hmw" for f in b["findings"])
    text = " ".join(f["title"] + f["detail"] for f in g["findings"] + b["findings"])
    assert "RUO" in text and "ไม่ใช่การคัดกรองมะเร็ง" in text


# ---------------- Tier 2/3
def test_graph_runs_every_node_and_cites_only_known_facts():
    s = graph.run("P002")
    assert set(s.execution_status.values()) == {"done"}
    store = facts()["facts"]
    cited = {f for v in s.risk_vectors for f in v["fact_ids"]} | {f for x in s.intermediate_features["flags"] for f in x["fact_ids"]}
    assert cited <= set(store)
    assert s.summary["sentences"] and all(set(x["fact_ids"]) <= set(store) for x in s.summary["sentences"])
    ids = {v["id"] for v in s.risk_vectors}
    assert ids == {"cvd", "dm", "mets", "ckd", "masld"}


def test_verifier_drops_unsupported_sentences(monkeypatch):
    monkeypatch.setattr(graph.llm, "summarize", lambda payload: ({"sentences": [
        {"text": "ok", "fact_ids": ["KDIGO-2024"]}, {"text": "made up", "fact_ids": ["FAKE-1"]}]}, "ok (test)"))
    s = graph.run("P002")
    assert [x["text"] for x in s.summary["sentences"]] == ["ok"] and s.summary["dropped_unsupported"] == 1


def test_invalid_llm_plan_falls_back(monkeypatch):
    monkeypatch.setattr(graph.llm, "plan", lambda a: ({"steps": ["summarizer"], "rationale": "x"}, "ok (test)"))
    s = graph.run("P001")
    assert s.intermediate_features["plan_source"] == "deterministic" and s.execution_status["risk_scoring"] == "done"


def test_rag_returns_citable_chunks_for_thai_query():
    hits = rag.search("ไตเสื่อม albuminuria", "kidney", 3)
    assert hits and all(h["fact_id"] in facts()["facts"] for h in hits)


def test_tools_reject_path_traversal():
    with pytest.raises(KeyError):
        tools.patient_folder("../../app")


# ---------------- API + care plan
def test_api_run_tools_ws_and_export():
    r = client.post("/api/v2/patients/P001/run").json()
    assert r["execution_status"]["summarizer"] == "done" and r["normalized_json"]["demographics"]["patient_id"] == "P001"
    assert client.post("/api/v2/tools/terminology_code_resolver", json={"term": "HbA1c", "target_standard": "loinc"}).json()["output"]["code"] == "4548-4"
    assert client.post("/api/v2/tools/nope", json={}).status_code == 404
    with client.websocket_connect("/ws/v2/patients/P001/run") as ws:
        nodes = []
        while True:
            e = ws.receive_json()
            nodes.append(e["node"])
            if e["node"] == "__end__":
                break
    assert nodes[0] == "orchestrator" and "summarizer" in nodes
    items = r["intermediate_features"]["care_plan"]
    assert client.post("/api/v2/careplan/export", json={"patient_id": "P001", "items": items, "approver": " "}).status_code == 422


def test_fhir_careplan_export_only_selected_items():
    items = [{"id": "a", "category": "lab", "title": "A", "detail": "", "interval_weeks": 4, "rationale": "", "fact_ids": ["KDIGO-2024"], "selected": True},
             {"id": "b", "category": "lab", "title": "B", "detail": "", "interval_weeks": 4, "rationale": "", "fact_ids": [], "selected": False}]
    b = export_fhir("P9", items, "Dr X")
    kinds = [e["resource"]["resourceType"] for e in b["entry"]]
    assert kinds == ["CarePlan", "ServiceRequest"]
    assert b["entry"][0]["resource"]["activity"][0]["reference"]["reference"] == b["entry"][1]["fullUrl"]


def test_cfdna_run_summary_matches_slide_conventions():
    r = client.get("/api/cfdna/runs/E10146").json()
    bct, roche = r["tubes"]
    assert bct["average_size_bp"] == 158.3 and bct["total_ng"] == 27.54
    assert roche["average_size_bp"] == 157 and roche["total_ng"] == 28.79
    # the 3000 bp alignment marker must not count as high-molecular-weight DNA
    assert all(x["hmw_fraction"] < 0.1 for x in bct["replicates"])
    assert roche["replicates"][1]["qc_status"] == "fail"
    assert bct["external_score"]["ruo"] is True
