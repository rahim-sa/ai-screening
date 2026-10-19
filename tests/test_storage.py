import time

from ai_screening.library import load_use_cases
from ai_screening.storage import build_assessment, load_assessment, save_assessment


def make_assessment():
    rows = load_use_cases()
    results = [(rows[0], "DO", "Passed all six gates"), (rows[1], "LATER", "Yearly cost unknown")]
    return build_assessment("Acme Ltd", "Education", "cut time 10%", "Anna", results)


def test_do_result_keeps_prescription_and_others_do_not():
    use_cases = make_assessment()["use_cases"]
    assert "Form to prescribe" in use_cases[0]["prescription"]
    assert "prescription" not in use_cases[1]


def test_save_and_load_gives_the_same_data(tmp_path):
    assessment = make_assessment()
    path = save_assessment(assessment, tmp_path)
    assert path.suffix == ".json"
    assert "acme-ltd" in path.name
    assert load_assessment(path) == assessment


def test_saving_twice_makes_two_files(tmp_path):
    save_assessment(make_assessment(), tmp_path)
    time.sleep(1.1)
    save_assessment(make_assessment(), tmp_path)
    assert len(list(tmp_path.glob("*.json"))) == 2