from phns.heuristics import apply


def test_assimilate_without_changes():
    canonical = [["dh", "ah"], ["b", "oy"]]  # the boy
    assert apply([canonical]) == [canonical]


def test_assimilate_with_one_change():
    canonical = [["f", "ae", "t"], ["b", "oy"]]  # fat boy
    changed = [["f", "ae", "p"], ["b", "oy"]]
    assert apply([canonical]) == sorted([canonical, changed])


def test_assimilate_with_two_changes():
    canonical = [["f", "ae", "t"], ["b", "oy"], ["g", "uh", "d"], ["b", "oy"]]  # fat boy good boy
    changed1 = [["f", "ae", "t"], ["b", "oy"], ["g", "uh", "b"], ["b", "oy"]]
    changed2 = [["f", "ae", "p"], ["b", "oy"], ["g", "uh", "d"], ["b", "oy"]]
    changed3 = [["f", "ae", "p"], ["b", "oy"], ["g", "uh", "b"], ["b", "oy"]]

    assert apply([canonical]) == sorted([canonical, changed1, changed2, changed3])


def test_assimilate_coalescence():
    canonical = [["g", "uh", "d"], ["y", "ih", "r"]]
    changed   = [["g", "uh"], ["jh", "ih", "r"]]
    assert apply([canonical]) == sorted([canonical, changed])


def test_consonant_cluster():
    canonical = [["f", "ae", "k", "t", "s"], ["t", "r", "uh"]]
    changed1 = [["f", "ae", "k", "s"], ["t", "r", "uh"]]
    changed2 = [["f", "ae", "k", "t", "s"], ["r", "uh"]]
    changed3 = [["f", "ae", "k", "s"], ["r", "uh"]]
    assert apply([canonical]) == sorted([canonical, changed1, changed2, changed3])


def test_seq_order():
    canonical = [["f", "ae", "k", "t"], ["b", "ae", "d"]]
    changed1 = [["f", "ae", "k", "p"], ["b", "ae", "d"]]
    changed2 = [["f", "ae", "k"], ["b", "ae", "d"]]
    assert apply([canonical]) == sorted([canonical, changed1, changed2])


def test_seq_order_2():
    canonical = [["f", "ae", "k", "t", "ch", "ae", "t"], ["b", "ae", "d"]]
    changed1 = [["f", "ae", "k", "ch", "ae", "t"], ["b", "ae", "d"]]
    changed2 = [["f", "ae", "k", "t", "ch", "ae", "p"], ["b", "ae", "d"]]
    changed3 = [["f", "ae", "k", "ch", "ae", "p"], ["b", "ae", "d"]]
    assert apply([canonical]) == sorted([canonical, changed1, changed2, changed3])
