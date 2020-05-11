from phns.graph import Graph
from phns.heuristics import apply
from phns.utils import deep_phn, flatten


def create_graph_and_check(canonical, *changed):
    graph = Graph()
    canonical = deep_phn(canonical)
    changed = [deep_phn(it) for it in changed]
    for word in canonical:
        graph.attach([word])
    apply(graph)
    canonical = [flatten(canonical), *[flatten(it) for it in changed]]
    assert sorted(canonical) == sorted(graph.to_list())


def test_assimilate_without_changes():
    canonical = [["dh", "ah1"], ["b", "oy"]]  # the boy
    create_graph_and_check(canonical)


def test_assimilate_with_one_change():
    canonical = [["f", "ae", "t"], ["b", "oy"]]  # fat boy
    changed = [["f", "ae", "p"], ["b", "oy"]]
    create_graph_and_check(canonical, changed)


def test_assimilate_with_two_changes():
    # fat boy good boy
    canonical = [["f", "ae", "t"], ["b", "oy"], ["g", "uh", "d"], ["b", "oy"]]
    changed1 = [["f", "ae", "t"], ["b", "oy"], ["g", "uh"], ["b", "oy"]]
    changed2 = [["f", "ae", "p"], ["b", "oy"], ["g", "uh", "d"], ["b", "oy"]]
    changed3 = [["f", "ae", "p"], ["b", "oy"], ["g", "uh"], ["b", "oy"]]
    create_graph_and_check(canonical, changed1, changed2, changed3)


def test_assimilate_coalescence():
    canonical = [["g", "uh", "d"], ["y", "ih", "r"]]
    changed = [["g", "uh"], ["jh", "ih", "r"]]
    create_graph_and_check(canonical, changed)


def test_consonant_cluster():
    canonical = [["f", "ae", "k", "t", "s"], ["t", "r", "uh"]]
    changed1 = [["f", "ae", "k", "s"], ["t", "r", "uh"]]
    changed2 = [["f", "ae", "k", "t", "s"], ["r", "uh"]]
    changed3 = [["f", "ae", "k", "s"], ["r", "uh"]]
    create_graph_and_check(canonical, changed1, changed2, changed3)


def test_seq_order():
    canonical = [["f", "ae", "k", "t"], ["b", "ae", "d"]]
    changed1 = [["f", "ae", "k", "p"], ["b", "ae", "d"]]
    changed2 = [["f", "ae", "k"], ["b", "ae", "d"]]
    create_graph_and_check(canonical, changed1, changed2)


def test_seq_order_2():
    canonical = [["f", "ae", "k", "t", "ch", "ae", "t"], ["b", "ae", "d"]]
    changed1 = [["f", "ae", "k", "ch", "ae", "t"], ["b", "ae", "d"]]
    changed2 = [["f", "ae", "k", "t", "ch", "ae", "p"], ["b", "ae", "d"]]
    changed3 = [["f", "ae", "k", "ch", "ae", "p"], ["b", "ae", "d"]]
    create_graph_and_check(canonical, changed1, changed2, changed3)


def test_consonant_cluster_doubles():
    canonical = [["t", "eh", "k", "s", "t", "s"]]
    changed = [["t", "eh", "k", "s"]]
    create_graph_and_check(canonical, changed)


def test_unstressed_ah():
    canonical = [["p", "ah0", "l", "iy1", "s"]]
    changed = [["p", "l", "iy1", "s"]]
    create_graph_and_check(canonical, changed)


def test_skips_word_ah():
    canonical = [["ah"], ["p", "ah0", "l", "iy1", "s"]]
    changed = [["ah"], ["p", "l", "iy1", "s"]]
    create_graph_and_check(canonical, changed)


def test_new_triples_with_neighboring_none():
    canonical = [["ah", "n", "t", "y"]]
    changed1 = [["ah", "n", "y"]]
    changed2 = [["ah", "n", "ch"]]
    create_graph_and_check(canonical, changed1, changed2)
