from app.engines.nmr_summary import DOMAINS, summarize
from app.engines.panel import catalog


def by_id(domains):
    return {d["id"]: d for d in domains}


def test_every_domain_member_is_in_catalog_and_each_analyte_used_once():
    cat = catalog()
    seen = [m for d in DOMAINS for m in d["members"]]
    assert set(seen) <= set(cat)
    assert len(seen) == len(set(seen))
    assert set(seen) == set(cat)  # all 28 analytes are covered by some domain


def test_apob_above_target_but_within_band_is_warning():
    d = by_id(summarize({"apob": 1.04}, None, diabetes=False, high_risk=False))["atherogenic"]
    assert d["status"] == "warning" and "สูงกว่าเป้า ApoB 100" in d["headline"]
    assert d["key"]["target"] == 1.00


def test_apob_target_is_tighter_for_high_risk():
    d = by_id(summarize({"apob": 0.85}, None, diabetes=True, high_risk=True))["atherogenic"]
    assert d["key"]["target"] == 0.80 and d["status"] == "warning"


def test_glucose_bands():
    g = lambda v: by_id(summarize({"glucose": v}, None, diabetes=False, high_risk=False))["glucose"]["status"]
    assert (g(5.0), g(5.9), g(7.4)) == ("good", "warning", "serious")


def test_trend_is_in_headline():
    d = by_id(summarize({"apob": 1.04}, {"apob": 1.38}, diabetes=False, high_risk=False))["atherogenic"]
    assert d["key"]["verdict"] == "improved" and "ดีขึ้นจริง" in d["headline"]


def test_other_out_of_range_member_raises_good_to_warning():
    d = by_id(summarize({"glyca": 0.80, "hdl_c": 1.3, "apoa1": 1.0}, None, diabetes=False, high_risk=False))["protective"]
    assert d["status"] == "warning" and d["out_of_range"] == ["ApoA1"]


def test_low_value_is_not_a_concern_when_lower_is_better():
    d = by_id(summarize({"apob": 0.7, "remnant_c": 0.8}, None, diabetes=False, high_risk=False))["atherogenic"]
    assert d["out_of_range"] == [] and d["status"] == "good"


def test_missing_key_marker():
    d = by_id(summarize({}, None, diabetes=False, high_risk=False))["inflammation"]
    assert d["status"] == "none" and d["key"] is None
