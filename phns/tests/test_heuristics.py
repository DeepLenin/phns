from phns.heuristics import apply
from phns.utils import deep_phn


def test_assimilate_without_changes():
    canonical = deep_phn([["dh", "ah1"], ["b", "oy"]])  # the boy
    assert apply([canonical]) == [canonical]


def test_assimilate_with_one_change():
    canonical = deep_phn([["f", "ae", "t"], ["b", "oy"]])  # fat boy
    changed = deep_phn([["f", "ae", "p"], ["b", "oy"]])
    assert apply([canonical]) == sorted([canonical, changed])


def test_assimilate_with_two_changes():
    canonical = deep_phn([["f", "ae", "t"], ["b", "oy"], ["g", "uh", "d"], ["b", "oy"]])  # fat boy good boy
    changed1 = deep_phn([["f", "ae", "t"], ["b", "oy"], ["g", "uh", "b"], ["b", "oy"]])
    changed2 = deep_phn([["f", "ae", "p"], ["b", "oy"], ["g", "uh", "d"], ["b", "oy"]])
    changed3 = deep_phn([["f", "ae", "p"], ["b", "oy"], ["g", "uh", "b"], ["b", "oy"]])

    assert apply([canonical]) == sorted([canonical, changed1, changed2, changed3])


def test_assimilate_coalescence():
    canonical = deep_phn([["g", "uh", "d"], ["y", "ih", "r"]])
    changed   = deep_phn([["g", "uh"], ["jh", "ih", "r"]])
    assert apply([canonical]) == sorted([canonical, changed])


def test_consonant_cluster():
    canonical = deep_phn([["f", "ae", "k", "t", "s"], ["t", "r", "uh"]])
    changed1 = deep_phn([["f", "ae", "k", "s"], ["t", "r", "uh"]])
    changed2 = deep_phn([["f", "ae", "k", "t", "s"], ["r", "uh"]])
    changed3 = deep_phn([["f", "ae", "k", "s"], ["r", "uh"]])
    assert apply([canonical]) == sorted([canonical, changed1, changed2, changed3])


def test_seq_order():
    canonical = deep_phn([["f", "ae", "k", "t"], ["b", "ae", "d"]])
    changed1 = deep_phn([["f", "ae", "k", "p"], ["b", "ae", "d"]])
    changed2 = deep_phn([["f", "ae", "k"], ["b", "ae", "d"]])
    assert apply([canonical]) == sorted([canonical, changed1, changed2])


def test_seq_order_2():
    canonical = deep_phn([["f", "ae", "k", "t", "ch", "ae", "t"], ["b", "ae", "d"]])
    changed1 = deep_phn([["f", "ae", "k", "ch", "ae", "t"], ["b", "ae", "d"]])
    changed2 = deep_phn([["f", "ae", "k", "t", "ch", "ae", "p"], ["b", "ae", "d"]])
    changed3 = deep_phn([["f", "ae", "k", "ch", "ae", "p"], ["b", "ae", "d"]])
    assert apply([canonical]) == sorted([canonical, changed1, changed2, changed3])


def test_consonant_cluster_doubles():
    canonical = deep_phn([["t", "eh", "k", "s", "t", "s"]])
    changed = deep_phn([["t", "eh", "k", "s"]])
    assert apply([canonical]) == sorted([canonical, changed])

def test_unstressed_ah():
    canonical = deep_phn([["p", "ah0", "l", "iy1", "s"]])
    changed = deep_phn([["p", "l", "iy1", "s"]])
    assert apply([canonical]) == sorted([canonical, changed])
