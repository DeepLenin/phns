from phns import from_text


def test_from_text_single_word():
    res = from_text("hello")
    assert len(res) == 2
    assert res[0] == (["hh", "ah", "l", "ow"], )


def test_from_text_multiple_words():
    res = from_text("hello world abzug")
    assert len(res) == 4
    assert res == [
        (["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]),
        (["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"]),
        (["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]),
        (["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"])
    ]


def test_from_text_missing_handler():
    res = from_text("foobar42", lambda _: [666])
    assert res == [(666,)]


def test_from_text_missing_handler_skip():
    res = from_text("foobar42", lambda _: False)
    assert res is None

