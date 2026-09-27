"""Regression gate: the gold-standard eval set must stay clean."""

from eval.run_eval import run


def test_eval_set_has_no_omissions_or_false_flags():
    s, results = run()
    failing = {r["id"]: r["problems"] for r in results if not r["pass"]}
    assert failing == {}
    assert s["omissions"] == 0 and s["false_flags"] == 0 and s["citations_missing"] == 0


def test_eval_set_size():
    s, _ = run()
    assert s["cases"] >= 30
