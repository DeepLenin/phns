import numpy as np

from phns.compare import closest, to_emissions
from phns.graph import Graph


def assert_closest(canonical, closest):
    for k in ["target", "deletes", "inserts", "replaces"]:
        assert canonical.get(k) == closest.get(k), k


def test_to_emissions():
    graph = Graph()
    pronunciations = [list("wat"), list("what")]
    graph.attach(pronunciations)
    emissions = to_emissions(list("wot"), graph)
    canonical = [[1, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 1]]
    np.testing.assert_equal(canonical, emissions)


def test_closest_no_tail():
    phns = ["h", "o", "l"]
    graph = Graph()
    pronunciations = [list("helo"), list("halo")]
    graph.attach(pronunciations)
    meta = closest(phns, graph)
    result = {
        "deletes": [(3, "o")],
        "inserts": [],
        "replaces": [(1, "o")],
        "target": ["h", "e", "l", "o"],
    }
    assert_closest(result, meta)


def test_closest_no_longer_tail():
    phns = ["h", "o", "l"]
    graph = Graph()
    pronunciations = [list("helou"), list("halou")]
    graph.attach(pronunciations)
    meta = closest(phns, graph)
    result = {
        "deletes": [(3, "o"), (4, "u")],
        "inserts": [],
        "replaces": [(1, "o")],
        "target": ["h", "e", "l", "o", "u"],
    }
    assert_closest(result, meta)


def test_closest_no_root():
    phns = ["a", "t"]
    graph = Graph()
    pronunciations = [list("what"), list("wat")]
    graph.attach(pronunciations)
    meta = closest(phns, graph)
    result = {
        "deletes": [(0, "w")],
        "inserts": [],
        "replaces": [],
        "target": ["w", "a", "t"],
    }
    assert_closest(result, meta)


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
