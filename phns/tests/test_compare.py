from phns import compare, closest


def test_compare_add():
    phns1 = ["a", "b", "c"]
    phns2 = ["a", "b", "c", "d"]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_compare_del():
    phns1 = ["a", "b", "c"]
    phns2 = ["a", "b"]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_compare_rep():
    phns1 = ["a", "b", "c"]
    phns2 = ["a", "x", "c"]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_compare_sublist_del():
    phns1 = ["a", "b", "c"]
    phns2 = [["a", "b"], ["c", "d"]]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_closest():
    phns = ["a", "b", "c"]
    variants = [["a", "b", "c", "d", "e"], ["a", "b"]]
    res = closest(phns, variants)
    assert res["cer"] == 1 / len(phns)
    assert res["distance"] == 1
    assert res["phns"] == ["a", "b"]


def test_closest_equal():
    phns = ["a", "b", "c"]
    variants = [["a", "b", "c", "d"], ["a", "b"]]
    res = closest(phns, variants)
    assert res["cer"] == 1 / len(phns)
    assert res["distance"] == 1
    assert res["phns"] == ["a", "b", "c", "d"]
