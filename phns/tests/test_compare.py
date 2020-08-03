from phns.compare import closest
from phns.graph import Graph

# from phns.utils import Dictionary


def assert_closest(canonical, closest):
    for k in ["target", "deletes", "inserts", "replaces"]:
        assert canonical.get(k) == closest.get(k), k


def check_closest_phns(phns, pronunciations, expected_meta):
    graph = Graph()
    graph.attach(pronunciations)
    meta = closest(phns, graph)
    assert_closest(expected_meta, meta)


def check_closest_tensor(
    tensor, tensor_dict, pronunciations, expected_meta, threshold=1
):
    graph = Graph()
    graph.attach(pronunciations)
    meta = closest(tensor, graph, tensor_dict=tensor_dict, threshold=threshold)
    assert_closest(expected_meta, meta)


def test_phns_closest_no_tail():
    phns = ["h", "o", "l"]
    # tensor_dict = Dictionary(["a", "e", "o" "h", "l"], blank=True)
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    check_closest_phns(
        phns,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o"],
        },
    )


def test_tensor_closest_no_tail():
    phns = ["h", "o", "l"]
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    check_closest_phns(
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
    check_closest_phns(
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
    check_closest_phns(
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
    check_closest_phns(
        phns,
        pronunciations,
        {
            "deletes": {1: "e", 2: "l", 3: "o"},
            "inserts": {},
            "replaces": {},
            "target": ["h", "e", "l", "o", "u"],
        },
    )
