from phns.graph import Graph, __find_index_of_first_diff__
from phns.utils import deep_str


def test_graph_init():
    graph = Graph()
    assert graph.roots == []
    assert graph.tails == []


def test_graph_add_phn_to_root():
    graph = Graph()
    phn = "a"
    node = graph.__add_phn__(phn)

    assert graph.roots[0].value == phn
    assert graph.roots == [node]


def test_attach_single():
    graph = Graph()
    pronunciations = [list("hey")]
    graph.attach(pronunciations)
    assert graph.to_list() == pronunciations


def test_attach_multi():
    graph = Graph()
    pronunciations = [list("hello"), list("halo")]
    graph.attach(pronunciations)
    assert sorted(graph.to_list()) == sorted(pronunciations)


def test_attach_multi_different_ending():
    graph = Graph()
    pronunciations = [list("hi"), list("ho")]
    graph.attach(pronunciations)
    assert sorted(graph.to_list()) == sorted(pronunciations)


def test_attach_multi_three():
    graph = Graph()
    pronunciations = [list("hi"), list("ho"), list("hu")]
    graph.attach(pronunciations)
    assert sorted(graph.to_list()) == sorted(pronunciations)


def test_attach_multi_different_beginning():
    graph = Graph()
    pronunciations = [list("am"), list("om")]
    graph.attach(pronunciations)
    assert sorted(graph.to_list()) == sorted(pronunciations)


def test_attach_multi_different_beginning_and_length():
    graph = Graph()
    pronunciations = [list("wat"), list("hwat")]
    graph.attach(pronunciations)
    assert sorted(graph.to_list()) == sorted(pronunciations)


def test_attach_multi_omission():
    graph = Graph()
    pronunciations = [list("what"), list("wat")]
    graph.attach(pronunciations)
    assert sorted(graph.to_list()) == sorted(pronunciations)


def test_attach_multi_different_beginning_and_ending():
    graph = Graph()
    pronunciations = [list("am"), list("ofi")]
    graph.attach(pronunciations)
    assert sorted(graph.to_list()) == sorted(pronunciations)


def test_find_index_of_first_diff():
    str_a = "abcdefg"
    str_b = "abcgfed"

    found = __find_index_of_first_diff__([str_a, str_b])
    assert found == 3


def test_find_index_of_first_diff_on_shorter():
    str_a = "asdf"
    str_b = "asd"

    found = __find_index_of_first_diff__([str_a, str_b])
    assert found == 3


def test_find_index_of_first_diff_on_different():
    str_a = "asdf"
    str_b = "bce"

    found = __find_index_of_first_diff__([str_a, str_b])
    assert found == 0


def test_find_index_of_first_diff_on_multiple():
    str_a = "asdf"
    str_b = "asde"
    str_c = "asfg"
    str_d = "asrt"

    found = __find_index_of_first_diff__([str_a, str_b, str_c, str_d])
    assert found == 2


def test_iter():
    graph = Graph()
    pronunciations = [list("hello"), list("halo")]
    graph.attach(pronunciations)
    assert sorted([node.value for node in graph]) == sorted(list("helloa"))


def test_triples():
    graph = Graph()
    pronunciations = [list("hello"), list("halo")]
    graph.attach(pronunciations)
    strings = ["".join([node.value for node in triple if node]) for triple in graph.triples()]
    assert sorted(strings) == sorted(["he", "ha", "hel", "hal", "ell", "llo", "alo", "lo"])


def test_triples_empty_edges():
    graph = Graph()
    pronunciations = [list("wat"), list("what")]
    graph.attach(pronunciations)
    strings = ["".join([node.value for node in triple if node]) for triple in graph.triples()]
    assert sorted(strings) == sorted(['wa', 'wh', 'wha', 'wat', 'hat', 'at'])


def test_calculate_distances():
    graph = Graph()
    pronunciations = [list("wat"), list("what")]
    graph.attach(pronunciations)
    graph.calculate_distances()
    expected_distances = {
        ("w", "h"): 1,
        ("h", "a"): 1,
        ("w", "a"): 1,
        ("a", "t"): 1,
        ("h", "t"): 2,
        ("w", "t"): 2
    }
    for (node1, node2), distance in graph.distances.items():
        print(node1.value, node2.value, distance)
        assert expected_distances[(node1.value, node2.value)] == distance
