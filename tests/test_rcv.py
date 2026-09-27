import pytest

from app.engines.rcv import compare, rcv_percent


def test_rcv_formula():
    # sqrt(2) * 1.96 * sqrt(3^2 + 4^2) = 2.772 * 5 = 13.86
    assert rcv_percent(3, 4) == pytest.approx(13.86, abs=0.01)


def test_small_change_is_within_variation():
    c = compare(100, 94, cva=3, cvi=4, better="lower")
    assert c.verdict == "within_variation"
    assert c.pct_change == pytest.approx(-6)


def test_large_drop_is_improvement_when_lower_is_better():
    assert compare(100, 70, cva=3, cvi=4, better="lower").verdict == "improved"


def test_large_rise_is_worsening_when_lower_is_better():
    assert compare(100, 130, cva=3, cvi=4, better="lower").verdict == "worsened"


def test_higher_is_better():
    assert compare(100, 130, cva=3, cvi=4, better="higher").verdict == "improved"


def test_no_direction():
    assert compare(100, 130, cva=3, cvi=4).verdict == "changed"


def test_missing_cvi_refuses_to_judge():
    c = compare(100, 50, cva=3, cvi=None, better="lower")
    assert c.verdict == "not_assessable"
    assert c.rcv_pct is None
