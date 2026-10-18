from ai_screening.gates import PASSED, QUESTIONS, STOPS, check_gate, is_ready


def test_six_gates_in_order():
    keys = [key for key, _, _ in QUESTIONS]
    assert keys == ["fix", "data", "cost", "check", "blocker", "owner"]


def test_simple_fix_means_no_ai():
    assert check_gate("fix", "y")[0] == "NO_AI"


def test_data_not_ready_or_unknown_means_later():
    assert check_gate("data", "n")[0] == "LATER"
    assert check_gate("data", "u")[0] == "LATER"


def test_cost_unknown_is_later_and_small_is_park():
    assert check_gate("cost", "u")[0] == "LATER"
    assert check_gate("cost", "s")[0] == "PARK"


def test_unaffordable_errors_mean_no_ai():
    assert check_gate("check", "n")[0] == "NO_AI"


def test_legal_blocker_means_no_ai():
    assert check_gate("blocker", "y")[0] == "NO_AI"


def test_no_owner_means_later():
    assert check_gate("owner", "n")[0] == "LATER"


def test_good_answers_do_not_stop():
    assert check_gate("fix", "n") is None
    assert check_gate("data", "y") is None
    assert check_gate("cost", "y") is None
    assert check_gate("check", "y") is None
    assert check_gate("blocker", "n") is None
    assert check_gate("owner", "y") is None


def test_passing_everything_means_do():
    assert PASSED[0] == "DO"


def test_every_stop_uses_an_allowed_answer():
    allowed = {key: options for key, _, options in QUESTIONS}
    for key, answer in STOPS:
        assert answer in allowed[key]

def test_ready_needs_target_and_owner():
    assert is_ready("cut time 10%", "Anna") is True
    assert is_ready("", "Anna") is False
    assert is_ready("cut time 10%", "  ") is False

def test_unknown_answer_always_means_later():
    for key, _, options in QUESTIONS:
        if "u" in options:
            assert check_gate(key, "u")[0] == "LATER"