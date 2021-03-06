from phns.utils import CMU_DICTIONARY, single_char_encode, timit_to_cmu


def test_cmu_sorted():
    assert list(CMU_DICTIONARY.phn_to_id.items())[:3] == [
        ("BLANK", 0),
        ("aa", 1),
        ("ae", 2),
    ]


def test_timit_to_cmu():
    orig = ["aa", "el", "bcl", "zh", "sh"]
    mapped = timit_to_cmu(orig)
    assert mapped == ["aa", "l", "sil", "zh", "sh"]


def test_single_char_encode():
    orig = ["aa", "l", "sil", "sh", "sh"]
    mapped = single_char_encode(orig)
    assert mapped == "al_SS"
