from phns.graph import Graph, __find_index_of_first_diff__


def test_graph_init():
    graph = Graph()
    assert graph.root
    assert graph.root.type == "<ROOT>"
    assert graph.root.out_edges == []
    assert graph.last_node == graph.root
    assert list(iter(graph)) == [graph.root]


def test_graph_add_phn_to_root():
    graph = Graph()
    phn = "a"
    next_node = graph.add_phn(phn)

    assert list(iter(graph)) == [graph.root, next_node]
    assert graph.root.out_edges[0].value == phn


def test_attach_single():
    graph = Graph()
    pronunciations = [list("hey")]

    graph.attach(pronunciations)

    edge_values = [node.out_edges[0].value for node in graph if node.out_edges]
    assert edge_values == ["h", "e", "y"]
    assert graph.last_node.type == "<WORD>"


def test_attach_multi():
    graph = Graph()
    pronunciations = [list("hello"), list("halo")]

    graph.attach(pronunciations)

    # h -> e ->
    for node in graph:
        for edge in node.out_edges:
            if edge.value == "h":
                next_edges = edge.to_node.out_edges
                [ne.value for ne in next_edges]

    edge_values = [node.out_edges[0].value for node in graph if node.out_edges]
    assert edge_values == ["h", "e", "y"]
    assert graph.last_node.type == "<WORD>"


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
