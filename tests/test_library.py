from ai_screening.library import (
    list_industries,
    load_use_cases,
    parse_numbers,
    use_cases_for,
)


def test_library_has_54_use_cases():
    assert len(load_use_cases()) == 54


def test_industries_do_not_include_cross_industry():
    industries = list_industries(load_use_cases())
    assert "Banking" in industries
    assert "Cross-industry" not in industries


def test_filter_includes_cross_industry():
    rows = use_cases_for(load_use_cases(), "Banking")
    assert {row["Industry"] for row in rows} == {"Banking", "Cross-industry"}


def test_parse_numbers():
    assert parse_numbers("1, 4,7", 10) == [0, 3, 6]
    assert parse_numbers("0", 10) is None
    assert parse_numbers("11", 10) is None
    assert parse_numbers("a", 10) is None
    assert parse_numbers("", 10) is None
    assert parse_numbers("2,2", 10) is None