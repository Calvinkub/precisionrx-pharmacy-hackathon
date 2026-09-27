from app.engines.lifestyle import lifestyle_advice
from app.engines.risk import Profile


def ids(advice):
    return {a.id for a in advice}


def test_healthy_active_person_gets_no_advice():
    p = Profile(age=40, sex="female", sbp=115, weight_kg=52, height_cm=160, waist_cm=70)
    assert lifestyle_advice(p, {"ldl_c": 2.5, "tg": 1.0, "glucose": 5.0}, activity_min_week=200) == []


def test_triggers():
    p = Profile(age=52, sex="female", sbp=138, smoker=True, weight_kg=67, height_cm=155, waist_cm=88)
    got = ids(lifestyle_advice(p, {"ldl_c": 4.4, "tg": 2.1, "glucose": 5.9}, alcohol_drinks_per_day=1))
    assert got == {"smoking", "weight", "prediabetes", "ldl_diet", "tg_diet", "sodium", "alcohol", "activity"}


def test_every_advice_has_fact():
    p = Profile(age=52, sex="male", sbp=150, smoker=True, weight_kg=90, height_cm=170, waist_cm=100)
    for a in lifestyle_advice(p, {"ldl_c": 5, "tg": 3, "glucose": 6}, alcohol_drinks_per_day=4):
        assert a.fact_ids
