from fastapi.testclient import TestClient

from app.engines.oncology import annotate_variants, assess_oncology
from app.main import app

client = TestClient(app)


def ids(result):
    return {f["id"] for f in result["findings"]}


def case(variants=(), meds=(), pgx=None):
    return {"ctdna": {"variants": list(variants)}, "meds": list(meds), "pgx": pgx or {}}


def test_chip_and_germline_flags():
    vs = annotate_variants({"variants": [
        {"gene": "DNMT3A", "variant": "R882H", "vaf": 1.2},
        {"gene": "BRCA2", "variant": "x", "vaf": 49.5},
        {"gene": "BRCA2", "variant": "y", "vaf": 8.0},
        {"gene": "EGFR", "variant": "L858R", "vaf": 20}]})
    flags = [[f["id"] for f in v.flags] for v in vs]
    assert flags == [["chip"], ["germline"], [], []]


def test_negative_ctdna_is_not_reassuring():
    assert "ctdna-negative" in ids(assess_oncology(case()))


def test_t790m_on_erlotinib_and_ppi_interaction():
    r = assess_oncology(case([{"gene": "EGFR", "variant": "T790M", "vaf": 3}],
                             [{"drug": "erlotinib", "status": "current"}, {"drug": "omeprazole", "status": "current"}]))
    assert {"t790m-osimertinib", "ddi-erlotinib-ppi"} <= ids(r)


def test_no_t790m_suggestion_when_already_on_osimertinib():
    r = assess_oncology(case([{"gene": "EGFR", "variant": "T790M", "vaf": 3}], [{"drug": "osimertinib", "status": "current"}]))
    assert "t790m-osimertinib" not in ids(r)


def test_dpyd_rules():
    fu = [{"drug": "capecitabine", "status": "planned"}]
    assert "dpyd-untested" in ids(assess_oncology(case([{"gene": "KRAS", "variant": "G12D", "vaf": 10}], fu)))
    r = assess_oncology(case([{"gene": "KRAS", "variant": "G12D", "vaf": 10}], fu, {"DPYD": "0"}))
    assert r["findings"][0]["id"] == "dpyd-poor" and r["findings"][0]["severity"] == "stop"
    r = assess_oncology(case([{"gene": "KRAS", "variant": "G12D", "vaf": 10}], fu, {"DPYD": "1.5 (HapB3)"}))
    assert "25–50%" in next(f for f in r["findings"] if f["id"] == "dpyd-im")["detail"]


def test_ugt1a1_poor_with_irinotecan():
    r = assess_oncology(case([{"gene": "KRAS", "variant": "G12D", "vaf": 10}], [{"drug": "irinotecan", "status": "planned"}], {"UGT1A1": "*28/*28"}))
    assert "ugt1a1-irinotecan" in ids(r)


def test_api_cases_cite_only_existing_facts():
    for c in client.get("/api/oncology/cases").json():
        r = client.get(f"/api/oncology/cases/{c['id']}").json()
        assert r["missing_facts"] == []
        assert r["findings"]


def test_case_o1_story():
    r = client.get("/api/oncology/cases/o1").json()
    got = {f["id"] for f in r["findings"]}
    assert {"t790m-osimertinib", "ddi-erlotinib-ppi", "flag-chip-DNMT3A", "flag-germline-BRCA2"} <= got
