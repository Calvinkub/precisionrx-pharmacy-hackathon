"""The consumer site shows numbers precomputed from the engines; they must never drift or be hand-edited."""

import json

from scripts.build_consumer_data import OUT, build


def test_computed_json_matches_engines():
    assert json.loads(OUT.read_text(encoding="utf-8")) == json.loads(json.dumps(build(), ensure_ascii=False))


def test_consumer_risks_come_from_validated_scores():
    d = build()
    assert d["risks"]["cvd"]["method"].startswith("Thai CV Risk Score")
    assert d["risks"]["diabetes"]["display"] == "12/17"
    assert d["risks"]["mets"]["met"] == 4
    assert d["insulin_resistance_pattern"] is True
    assert set(d["facts"]) >= {"TCVRS-2021", "TDRS-2006", "CFDNA-FRAGMENTOMICS-SEQ"}


def test_traces_add_up_to_the_result():
    import math
    d = build()
    t = d["traces"]
    assert sum(i["effect"] for i in t["diabetes"]["inputs"]) == d["risks"]["diabetes"]["value"]
    # FLI: reference logit + each input's logit term = the patient's logit
    logit = lambda f: math.log(f / (100 - f))
    base = logit(float(t["liver"]["base"].split()[1]))
    total = base + sum(i["effect"] for i in t["liver"]["inputs"])
    assert abs(100 / (1 + math.exp(-total)) - d["risks"]["liver"]["fli"]) < 1.5  # base shown rounded
    assert t["mets"]["result"] == f"{sum(i['met'] for i in t['mets']['inputs'])}/5"
    assert all(1 <= i["src"] <= 5 for k in ("diabetes", "cvd", "liver", "fib4", "mets", "insulin_resistance") for i in t[k]["inputs"])
    assert d["cfdna_run"]["qc_status"] == "pass" and len(d["cfdna_run"]["replicates"]) == 3


def test_whatif_reruns_the_same_formulas_with_targets():
    w = build()["whatif"]
    assert w["diabetes"] == {**w["diabetes"], "now": 12, "after": 7}  # BMI 26.8→<23 (−3), waist 92→<90 (−2)
    assert w["cvd"]["after"] < w["cvd"]["now"]
