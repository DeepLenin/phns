from phns.utils import timit_to_cmu, single_char_encode


def test_timit_to_cmu():
    orig = ["aa", "el", "bcl", "zh", "sh"]
    mapped = timit_to_cmu(orig)
    assert mapped == ["aa", "l", "sil", "zh", "sh"]


def test_single_char_encode():
    orig = ["aa", "l", "sil", "sh", "sh"]
    mapped = single_char_encode(orig)
    assert mapped == 'al_SS'
