from phns import from_text
from phns.utils import deep_str


def test_from_text_single_word():
    res = from_text("hello", apply_heuristics=False).to_list()
    assert len(res) == 2
    assert deep_str(res[0]) == ["hh", "ah", "l", "ow"]


def test_from_text_multiple_words():
    res = from_text("hello world abzug", apply_heuristics=False).to_list()
    assert len(res) == 4
    assert deep_str(res) == [
        ["hh", "ah", "l", "ow", "w", "er", "l", "d", "ae", "b", "z", "ah", "g"],
        ["hh", "ah", "l", "ow", "w", "er", "l", "d", "ae", "b", "z", "uh", "g"],
        ["hh", "eh", "l", "ow", "w", "er", "l", "d", "ae", "b", "z", "ah", "g"],
        ["hh", "eh", "l", "ow", "w", "er", "l", "d", "ae", "b", "z", "uh", "g"],
    ]


def test_from_text_multiple_words_with_heuristics():
    res = from_text("fat boy texts good girl", apply_heuristics=True).to_list()
    assert len(res) == 16

    # fmt: off
    assert sorted(deep_str(res)) == sorted([
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'ih', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'ih', 'g', 'er', 'l'],
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'uh', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'uh', 'g', 'er', 'l'],
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'ih', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'ih', 'g', 'er', 'l'],
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'uh', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 'p', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'uh', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'ih', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'ih', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'uh', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 'g', 'uh', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'ih', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'ih', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'uh', 'd', 'g', 'er', 'l'],
        ['f', 'ae', 't', 'b', 'oy', 't', 'eh', 'k', 's', 't', 's', 'g', 'uh', 'g', 'er', 'l'],
    ])
    # fmt: on


def test_from_text_missing_handler():
    res = from_text("foobar42", lambda _: [["p"]]).to_list()
    assert deep_str(res) == [["p"]]


def test_from_text_missing_handler_skip():
    res = from_text("foobar42", lambda _: False)
    assert res is None
