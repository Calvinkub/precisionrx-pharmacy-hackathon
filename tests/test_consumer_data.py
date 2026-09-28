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
