import pytest

from phns.utils.contractions import decode, encode


def assert_each_encoded_position(sentence, expected):
    sentence = sentence.split()
    results = []
    for idx in range(len(sentence)):
        result = encode(idx, sentence)
        if "^" in result[0]:
            results.append(result)
        else:
            assert result[1] == 0
    assert results == expected


def assert_decoded(examples, expected):
    results = []
    for example in examples:
        results.append(decode(example))
    assert results == expected


def test_encode_simple():
    text = "I am living because my soul is not dying do not presume"
    assert_each_encoded_position(
        text,
        [("i^am", 1), ("soul^is^not", 2), ("is^not", 1), ("do^not", 1)],
    )


def test_encode_with_aliases():
    text = "let us be it is who it was not of course right man"
    assert_each_encoded_position(
        text,
        [
            ("let^us", 1),
            ("it^is", 1),
            ("it^was^not", 2),
            ("was^not", 1),
            ("of^course", 1),
        ],
    )


def test_encode_big_stuff():
    text = (
        "alex would not have vscode for now, but I hope it would have changed his heart"
    )
    assert_each_encoded_position(
        text,
        [
            ("alex^would^not^have", 3),
            ("would^not^have", 2),
            ("it^would^have", 2),
            ("would^have", 1),
        ],
    )


def test_decode_simple():
    assert_decoded(
        [
            "that^is",
            "i^am",
            "soul^is^not",
            "is^not",
            "dying^do^not",
            "do^not",
            "i^am^not",
        ],
        [
            [["that", "is"], ["that's"]],
            [["i", "am"], ["i'm"]],
            [
                ["soul", "is", "not"],
                ["soul", "ain't"],
                ["soul", "isn't"],
                ["soul's", "not"],
            ],
            [["is", "not"], ["isn't"], ["ain't"]],
            [["dying", "do", "not"], ["dying", "don't"]],
            [["do", "not"], ["don't"]],
            [["i", "am", "not"], ["i", "ain't"], ["i'm", "not"]],
        ],
    )


def test_decode_alias():
    assert_decoded(
        ["let^us", "it^is^not", "it^was"],
        [
            [["let", "us"], ["let's"]],
            [
                ["it", "is", "not"],
                ["'tis", "not"],
                ["it", "ain't"],
                ["it", "isn't"],
                ["it's", "not"],
            ],
            [["it", "was"], ["'twas"], ["it's"]],
        ],
    )


def test_decode_incorrect():
    for example in ["let^uo", "you^am", "writers^do", "you^will^not^have"]:
        with pytest.raises(ValueError):
            decode(example)


def test_decode_complex():
    assert_decoded(
        ["alex^would^not^have"],
        [
            [
                ["alex", "would", "not", "have"],
                ["alex'd", "not", "have"],
                ["alex", "wouldn't", "have"],
                ["alex", "wouldn't've"],
            ]
        ],
    )
