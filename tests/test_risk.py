import pytest

from app.engines.risk import Profile, thai_cv_risk, thai_diabetes_risk


# Worked examples computed from the official calculator equations (docs/research_risk_lifestyle.md §1)
def test_tcvrs_tc_version_high():
    r = thai_cv_risk(Profile(age=60, sex="male", sbp=140, smoker=True, total_chol_mg_dl=220))
    assert r.value == pytest.approx(24.72, abs=0.05)
    assert r.category == "high"


def test_tcvrs_tc_version_low():
    r = thai_cv_risk(Profile(age=45, sex="female", sbp=120, total_chol_mg_dl=200))
    assert r.value == pytest.approx(2.30, abs=0.05)
    assert r.category == "low"


def test_tcvrs_waist_height_version():
    r = thai_cv_risk(Profile(age=50, sex="female", sbp=130, diabetes=True, waist_cm=85, height_cm=155))
    assert r.value == pytest.approx(11.98, abs=0.05)
    assert r.category == "moderate"


def test_tcvrs_needs_sbp():
    assert thai_cv_risk(Profile(age=50, sex="male", total_chol_mg_dl=200)).category == "not_assessable"


def test_tdrs_scoring():
    # 52 F (2) + BMI 27.9 (5) + waist 88 (2) + no HT + family hx (4) = 13
    p = Profile(age=52, sex="female", weight_kg=67, height_cm=155, waist_cm=88, family_history_dm=True)
    r = thai_diabetes_risk(p)
    assert r.value == 13
    assert r.category == "very_high"


def test_tdrs_low():
    p = Profile(age=36, sex="female", weight_kg=50, height_cm=160, waist_cm=70)
    assert thai_diabetes_risk(p).value == 0


def test_tdrs_skipped_when_diabetic():
    p = Profile(age=52, sex="male", diabetes=True, weight_kg=70, height_cm=170, waist_cm=90)
    assert thai_diabetes_risk(p).category == "not_assessable"
