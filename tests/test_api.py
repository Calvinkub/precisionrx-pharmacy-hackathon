from fastapi.testclient import TestClient

from app.engines.panel import catalog, facts
from app.main import app

client = TestClient(app)


def load(case_id, upto=None):
    c = client.get(f"/api/cases/{case_id}").json()
    body = {k: c[k] for k in ("profile", "meds", "pgx")}
    body["alcohol_drinks_per_day"] = c["profile"].get("alcohol_drinks_per_day", 0)
    body["activity_min_week"] = c["profile"].get("activity_min_week")
    body["visits"] = c["visits"][: upto or len(c["visits"])]
    return client.post("/api/assess", json=body).json()


def ids(items):
    return {x["id"] for x in items}


def test_every_cited_fact_exists():
    for case in ("1", "2", "3"):
        r = load(case)
        assert r["missing_facts"] == []


def test_every_synthetic_value_is_in_catalog():
    cat = catalog()
    for case in ("1", "2", "3"):
        for v in client.get(f"/api/cases/{case}").json()["visits"]:
            assert set(v["values"]) <= set(cat)


def test_case1_story():
    r = load("1")
    f = ids(r["findings"])
    assert {"pgx-slco1b1-simva", "pgx-cyp2c19-omeprazole", "resp-simvastatin"} <= f
    assert "apob_discordance" in ids(r["nmr_factors"])
    verdict = {t["id"]: t["verdict"] for t in r["trend"]}
    assert verdict["apob"] == "improved"  # -25% > RCV ~19%
    assert verdict["tg"] == "within_variation"  # -17% < RCV ~56%
    assert verdict["ldl_p"] == "not_assessable"  # no CVi


def test_case1_first_visit_has_no_trend_or_response():
    r = load("1", upto=1)
    assert r["trend"] == []
    assert "resp-simvastatin" not in ids(r["findings"])


def test_case2_adherence_before_non_response():
    r = load("2")
    f = ids(r["findings"])
    assert "adh-atorvastatin" in f and "resp-atorvastatin" not in f
    assert "target-atorvastatin" in f
    assert "adh-metformin" in f  # generic PDC rule covers non-statins too
    assert r["risks"][0]["category"] == "very_high"


def test_case3_hard_stop_first():
    r = load("3")
    assert r["findings"][0]["severity"] == "stop"


def test_csv_parse():
    csv = "analyte,value\ndate,2026-09-20\nApoB,0.9\nLDL-C,2.3\nfoo,1\n"
    r = client.post("/api/panel/parse", files={"file": ("x.csv", csv, "text/csv")}).json()
    assert r["values"] == {"apob": 0.9, "ldl_c": 2.3}
    assert r["unknown"] == ["foo"] and r["date"] == "2026-09-20"


def test_every_fact_has_source_url_and_verification_flag():
    for fid, f in facts()["facts"].items():
        assert f["source"] and f["url"].startswith("http"), fid
        assert isinstance(f["verified"], bool), fid
