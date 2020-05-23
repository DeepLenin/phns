import numpy as np

from phns.compare import closest, to_emissions
from phns.graph import Graph


def assert_closest(canonical, closest):
    for k in ["target", "deletes", "inserts", "replaces"]:
        assert canonical.get(k) == closest.get(k), k


def check_closest(phns, pronunciations, expected_meta):
    graph = Graph()
    graph.attach(pronunciations)
    meta = closest(phns, graph)
    assert_closest(expected_meta, meta)


def test_to_emissions():
    graph = Graph()
    pronunciations = {tuple("wat"): 1, tuple("what"): 2}
    graph.attach(pronunciations)
    emissions = to_emissions(list("wot"), graph)
    canonical = [[1, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 1]]
    np.testing.assert_equal(canonical, emissions)


def test_closest_no_tail():
    phns = ["h", "o", "l"]
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    check_closest(
        phns,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o"],
        },
    )


def test_closest_no_longer_tail():
    phns = ["h", "o", "l"]
    pronunciations = {tuple("helou"): 1, tuple("halou"): 2}
    check_closest(
        phns,
        pronunciations,
        {
            "deletes": {3: "o", 4: "u"},
            "inserts": {},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o", "u"],
        },
    )


def test_closest_no_root():
    phns = ["a", "t"]
    pronunciations = {tuple("what"): 1, tuple("wat"): 2}
    check_closest(
        phns,
        pronunciations,
        {
            "deletes": {0: "w"},
            "inserts": {},
            "replaces": {},
            "target": ["w", "a", "t"],
        },
    )


def test_closest_with_gap_in_middle():
    phns = list("hu")
    pronunciations = {tuple("helou"): 1, tuple("halou"): 2}
    check_closest(
        phns,
        pronunciations,
        {
            "deletes": {1: "e", 2: "l", 3: "o"},
            "inserts": {},
            "replaces": {},
            "target": ["h", "e", "l", "o", "u"],
        },
    )


# TODO: Adapt with new API
"""
def test_compare_add():
    return
    phns1 = ["a", "b", "c"]
    phns2 = ["a", "b", "c", "d"]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_compare_del():
    return
    phns1 = ["a", "b", "c"]
    phns2 = ["a", "b"]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_compare_rep():
    return
    phns1 = ["a", "b", "c"]
    phns2 = ["a", "x", "c"]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_compare_sublist_del():
    return
    phns1 = ["a", "b", "c"]
    phns2 = [["a", "b"], ["c", "d"]]
    res = compare(phns1, phns2)
    assert res["cer"] == 1 / len(phns1)
    assert res["distance"] == 1


def test_closest():
    return
    phns = ["a", "b", "c"]
    variants = [["a", "b", "c", "d", "e"], ["a", "b"]]
    res = closest(phns, variants)
    assert res["cer"] == 1 / len(phns)
    assert res["distance"] == 1
    assert res["phns"] == ["a", "b"]


def test_closest_equal():
    return
    phns = ["a", "b", "c"]
    variants = [["a", "b", "c", "d"], ["a", "b"]]
    res = closest(phns, variants)
    assert res["cer"] == 1 / len(phns)
    assert res["distance"] == 1
    assert res["phns"] == ["a", "b", "c", "d"]
"""
