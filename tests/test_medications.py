from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.engines.dispensing import parse_fills, pdc, regular_meds
from app.engines.drug_effects import effects_for, moved_by
from app.engines.nmr_summary import summarize
from app.main import app

client = TestClient(app)


def fill(d, days=30, drug="simvastatin"):
    return {"date": d, "drug": drug, "dose_mg": 40, "days_supply": days}


def test_pdc_full_coverage():
    f = parse_fills([fill("2026-01-01"), fill("2026-01-31"), fill("2026-03-02")])
    assert pdc(f, date(2026, 1, 1), date(2026, 4, 1)) == 100.0


def test_pdc_with_gap():
    # 60 days supplied over a 90-day window
    f = parse_fills([fill("2026-01-01"), fill("2026-03-02")])
    assert pdc(f, date(2026, 1, 1), date(2026, 4, 1)) == pytest.approx(66.7, abs=0.1)


def test_overlapping_supply_is_shifted_not_double_counted():
    # early refill on day 20: 60 days of drug, window 60 days -> 100%, not >100%
    f = parse_fills([fill("2026-01-01"), fill("2026-01-21")])
    assert pdc(f, date(2026, 1, 1), date(2026, 3, 2)) == 100.0


def test_status_new_regular_stopped():
    rows = [fill("2026-01-01", drug="a"), fill("2026-01-31", drug="a"),
            fill("2026-03-25", drug="b"),
            fill("2025-10-01", drug="c")]
    got = {m.drug: m.status for m in regular_meds(rows, date(2026, 4, 1))}
    assert got == {"a": "regular", "b": "new", "c": "stopped"}


def test_fills_after_as_of_are_ignored():
    assert regular_meds([fill("2026-05-01")], date(2026, 4, 1)) == []


def test_statin_moves_lipids_but_not_bcaa():
    m = moved_by(["simvastatin"])
    assert "apob" in m and "remnant_c" in m and "bcaa" not in m


def test_unknown_drug_says_no_evidence_instead_of_no_effect():
    e = effects_for("amlodipine")
    assert e["effects"] == [] and "ไม่พบหลักฐาน" in e["interpretation"]


def test_summary_flags_drug_lowered_domain():
    d = {x["id"]: x for x in summarize({"apob": 1.0}, None, diabetes=False, high_risk=False, drugs=["atorvastatin"])}
    assert d["atherogenic"]["drugs"] == ["atorvastatin"]
    assert "ความเสี่ยงก่อนรักษาสูงกว่านี้" in d["atherogenic"]["drug_note"]
    assert d["inflammation"]["drug_note"] is None


def test_medications_endpoint_case1_visit2():
    r = client.get("/api/cases/1/medications", params={"visit": 2}).json()
    meds = {m["drug"]: m for m in r["medications"]}
    assert set(meds) == {"simvastatin", "omeprazole"}
    assert meds["simvastatin"]["start_visit"] == 1 and meds["simvastatin"]["pdc_pct"] >= 80
    assert meds["simvastatin"]["class"] == "statin"
    assert meds["omeprazole"]["start_visit"] is None
    assert all(fid in r["facts"] for m in r["medications"] for fid in m["fact_ids"])


def test_medications_endpoint_as_of_first_visit_excludes_later_drugs():
    r = client.get("/api/cases/1/medications", params={"visit": 1}).json()
    assert [m["drug"] for m in r["medications"]] == ["omeprazole"]


def test_medications_endpoint_low_adherence_case2():
    r = client.get("/api/cases/2/medications", params={"visit": 2}).json()
    meds = {m["drug"]: m for m in r["medications"]}
    assert meds["atorvastatin"]["pdc_pct"] < 80 and meds["metformin"]["pdc_pct"] < 80
