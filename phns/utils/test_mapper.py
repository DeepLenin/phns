from phns.utils import remap, single_char_encode


def test_remap():
    orig = ["aa", "el", "bcl", "zh", "sh"]
    mapped = remap(orig)
    assert mapped == ["aa", "l", "sil", "sh", "sh"]


def test_single_char_encode():
    orig = ["aa", "l", "sil", "sh", "sh"]
    mapped = single_char_encode(orig)
    assert mapped == 'al_SS'
