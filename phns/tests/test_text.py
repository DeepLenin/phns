from phns import from_text
from phns.utils import deep_str


def test_from_text_single_word():
    res = from_text("hello")
    assert len(res) == 2
    assert deep_str(res[0]) == [["hh", "ah", "l", "ow"]]


def test_from_text_multiple_words():
    res = from_text("hello world abzug", apply_heuristics=False)
    assert len(res) == 4
    assert deep_str(res) == [
        [["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]],
        [["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"]],
        [["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]],
        [["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"]]
    ]


def test_from_text_multiple_words_with_heuristics():
    res = from_text("fat boy texts good girl", apply_heuristics=True)
    assert len(res) == 4
    assert deep_str(res) == [
        [["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]],
        [["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"]],
        [["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]],
        [["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"]]
    ]


def test_from_text_missing_handler():
    res = from_text("foobar42", lambda _: ['p'])
    assert res == [[['p']]]


def test_from_text_missing_handler_skip():
    res = from_text("foobar42", lambda _: False)
    assert res is None
