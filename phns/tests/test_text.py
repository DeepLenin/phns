from phns import from_text


def test_from_text_single_word():
    res = from_text("hello")
    assert len(res) == 2
    assert res[0] == (["hh", "ah", "l", "ow"], )


def test_from_text_multiple_words():
    res = from_text("hello world abzug")
    print(res)
    assert len(res) == 4
    assert res == [
        (["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]),
        (["hh", "ah", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"]),
        (["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "ah", "g"]),
        (["hh", "eh", "l", "ow"], ["w", "er", "l", "d"], ["ae", "b", "z", "uh", "g"])
    ]
