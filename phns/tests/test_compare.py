import numpy as np

from phns.compare import closest
from phns.graph import Graph
from phns.utils import Dictionary


def assert_closest(canonical, closest):
    for k in ["target", "deletes", "inserts", "replaces"]:
        assert canonical.get(k) == closest.get(k), k


def check_closest_phns(phns, pronunciations, expected_meta):
    graph = Graph()
    graph.attach(pronunciations)
    meta = closest(phns, graph)
    assert_closest(expected_meta, meta)


def check_closest_tensor(
    tensor, tensor_dict, pronunciations, expected_meta={}, **kwargs
):
    graph = Graph()
    graph.attach(pronunciations)
    meta = closest(tensor, graph, tensor_dict=tensor_dict, **kwargs)
    assert_closest(expected_meta, meta)


def test_phns_closest_no_tail():
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


def test_closest_tensor_hol():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hol_with_blank():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.5, 0.1, 0.1, 0.1, 0.1, 0.1],  # BLANK
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.0, 0.1, 0.1, 0.1, 0.1, 0.6],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hol_with_not_ignored_blank():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.5, 0.1, 0.1, 0.1, 0.1, 0.1],  # BLANK
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.0, 0.1, 0.1, 0.1, 0.1, 0.6],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {1: ["BLANK"]},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o"],
        },
        ignore=[],
        threshold=0.4,
    )


def test_closest_tensor_hol_with_insufficient_threshold_with_replace():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o"],
        },
    )


def test_closest_tensor_hha():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.5, 0.1, 0.1, 0.1, 0.1],  # a
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {2: "l", 3: "o"},
            "inserts": {},
            "replaces": {},
            "target": ["h", "a", "l", "o"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hha_with_insufficient_threshold_with_insert():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.5, 0.1, 0.1, 0.1, 0.1],  # a
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {2: "l", 3: "o"},
            "inserts": {},
            "replaces": {},
            "target": ["h", "a", "l", "o"],
        },
    )


def test_closest_tensor_hol_with_sufficient_threshold():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0, 0, 0, 0.5, 0.4, 0.1],  # h with threshold
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {},
            "replaces": {1: "o"},
            "target": ["h", "e", "l", "o"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hol_with_insufficient_threshold():
    tensor_dict = Dictionary(["BLANK", "a", "e", "o", "h", "l"])
    pronunciations = {tuple("helo"): 1, tuple("halo"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0, 0, 0, 0.5, 0.4, 0.1],  # h with insufficient threshold
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "o"},
            "inserts": {},
            "replaces": {0: "o", 1: "o"},
            "target": ["h", "e", "l", "o"],
        },
    )
