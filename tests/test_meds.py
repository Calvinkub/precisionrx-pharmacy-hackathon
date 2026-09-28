from app.engines.meds import (
    Medication, ddi_findings, pgx_findings, statin_intensity, statin_response,
)


def test_hla_b1502_carbamazepine_is_hard_stop():
    f = pgx_findings([Medication("Carbamazepine", 200)], {"HLA-B*15:02": "positive"})
    assert [x.severity for x in f] == ["stop"]


def test_hla_negative_no_alert():
    assert pgx_findings([Medication("carbamazepine", 200)], {"HLA-B*15:02": "negative"}) == []


def test_simvastatin_slco1b1():
    f = pgx_findings([Medication("simvastatin", 40)], {"SLCO1B1": "Decreased function"})
    assert f[0].fact_ids == ["CPIC-SLCO1B1-2022"]


def test_omeprazole_cyp2c19_ultrarapid():
    f = pgx_findings([Medication("omeprazole", 20)], {"CYP2C19": "ultrarapid metabolizer"})
    assert f[0].id == "pgx-cyp2c19-omeprazole"


def test_clopidogrel_omeprazole_ddi_but_not_pantoprazole():
    assert len(ddi_findings([Medication("clopidogrel"), Medication("omeprazole")])) == 1
    assert ddi_findings([Medication("clopidogrel"), Medication("pantoprazole")]) == []


def test_statin_intensity_table():
    assert statin_intensity(Medication("atorvastatin", 40)) == "high"
    assert statin_intensity(Medication("simvastatin", 40)) == "moderate"
    assert statin_intensity(Medication("simvastatin", 10)) == "low"


def test_low_adherence_checked_before_non_response():
    f = statin_response(Medication("atorvastatin", 40, pdc_pct=55), 4.0, 3.6)
    assert f[0].category == "adherence"


def test_non_response_with_good_adherence():
    f = statin_response(Medication("atorvastatin", 40, pdc_pct=95), 4.0, 3.2)  # -20%, expected >=50%
    assert f[0].category == "response" and f[0].severity == "action"


def test_expected_response():
    f = statin_response(Medication("simvastatin", 40, pdc_pct=92), 4.4, 2.6)  # -41%, expected >=30%
    assert f[0].severity == "info"
