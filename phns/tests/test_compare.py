import numpy as np

from phns.compare import closest
from phns.graph import Graph
from phns.utils import Dictionary


def assert_closest(canonical, closest):
    changed = []
    for k in ["target", "deletes", "inserts", "replaces"]:
        if canonical.get(k) != closest.get(k):
            changed.append(k)

    if changed:
        print("Target:", list(enumerate(closest["target"])))
        print("Match with argmax:", list(zip(closest["match"], closest["argmax_phns"])))
        print("Nodes:", list(enumerate(closest["graph"].nodes)))
        print("Matched targets:", closest["matched_targets"])
        for k in changed:
            print(f"Expected {k} to equal:\n", canonical[k])
            print("But got:\n", closest[k])
        assert False


def check_closest_phns(phns, pronunciations, expected_meta):
    graph = Graph()
    graph.attach(pronunciations)
    meta = closest(phns, graph, debug=True)
    assert_closest(expected_meta, meta)


def check_closest_tensor(
    tensor, tensor_dict, pronunciations, expected_meta={}, **kwargs
):
    graph = Graph()
    graph.attach(pronunciations)
    meta = closest(tensor, graph, tensor_dict=tensor_dict, debug=True, **kwargs)
    assert_closest(expected_meta, meta)


def test_phns_closest_no_tail():
    phns = ["hh", "ow", "l"]
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    check_closest_phns(
        phns,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {1: ["ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
    )


def test_tensor_closest_no_tail():
    phns = ["hh", "ow", "l"]
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    check_closest_phns(
        phns,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {1: ["ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
    )


def test_closest_no_longer_tail():
    phns = ["hh", "ow", "l"]
    pronunciations = {
        ("hh", "eh", "l", "ow", "uh"): 1,
        ("hh", "ah", "l", "ow", "uh"): 2,
    }
    check_closest_phns(
        phns,
        pronunciations,
        {
            "deletes": {3: "ow", 4: "uh"},
            "inserts": {},
            "replaces": {1: ["ow"]},
            "target": ["hh", "eh", "l", "ow", "uh"],
        },
    )


def test_closest_no_root():
    phns = ["ah", "t"]
    pronunciations = {("hh", "w", "ah", "t"): 1, ("w", "ah", "t"): 2}
    check_closest_phns(
        phns,
        pronunciations,
        {
            "deletes": {0: "w"},
            "inserts": {},
            "replaces": {},
            "target": ["w", "ah", "t"],
        },
    )


def test_closest_with_gap_in_middle():
    phns = ["hh", "ow"]
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    check_closest_phns(
        phns,
        pronunciations,
        {
            "deletes": {1: "eh", 2: "l"},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
    )


def test_closest_tensor_hol():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
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
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {1: ["ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hol_with_blank():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.5, 0.1, 0.1, 0.1, 0.1, 0.1],  # BLANK
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.01, 0.1, 0.1, 0.1, 0.1, 0.6],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {1: ["ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hol_with_not_ignored_blank():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.5, 0.1, 0.1, 0.1, 0.1, 0.1],  # BLANK
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.01, 0.1, 0.1, 0.1, 0.1, 0.6],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {1: ["BLANK", "ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
        ignore=[],
        threshold=0.4,
    )


def test_closest_tensor_hol_with_insufficient_threshold_with_replace():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
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
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {1: ["ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
    )


def test_closest_tensor_hha():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
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
            "deletes": {2: "l", 3: "ow"},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "ah", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hha_with_insufficient_threshold_with_insert():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
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
            "deletes": {2: "l", 3: "ow"},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "ah", "l", "ow"],
        },
    )


def test_closest_tensor_hol_with_sufficient_threshold():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.01, 0.01, 0.01, 0.5, 0.4, 0.1],  # h with threshold
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {1: ["ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_hol_with_insufficient_threshold():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.01, 0.01, 0.01, 0.5, 0.4, 0.1],  # h with insufficient threshold
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {0: ["ow"], 1: ["ow"]},
            "target": ["hh", "eh", "l", "ow"],
        },
    )


def test_closest_tensor_compresses_repeated_errors():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    np.seterr(divide="ignore")
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0, 0, 0, 0.5, 0.4, 0.1],  # error o (cause insufficient threshold for h)
            [0, 0, 0, 0.5, 0.4, 0.1],  # error o (cause insufficient threshold for h)
            [0, 0, 0, 0.5, 0.4, 0.1],  # error o (cause insufficient threshold for h)
            [0.1, 0.5, 0.1, 0.1, 0.1, 0.1],  # a
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
        ]
    )
    np.seterr(divide="warn")

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {},
            "inserts": {},
            "replaces": {0: ["ow"]},
            "target": ["hh", "ah", "l", "ow"],
        },
        threshold=0.5,
    )


def test_closest_tensor_when_first_step_is_ignored():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.4, 0.1, 0.1, 0.1, 0.2, 0.1],  # blnk
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {0: "hh"},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_when_last_step_is_ignored():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.4, 0.1, 0.1, 0.2, 0.1, 0.1],  # blnk
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_when_middle_step_is_ignored():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.5, 0.1, 0.1, 0.1, 0.1, 0.1],  # blank
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {2: "l"},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_when_first_step_is_ignored_and_no_errors():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.4, 0.1, 0.1, 0.1, 0.2, 0.1],  # blnk
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
    )


def test_closest_tensor_when_clip():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.8, 0.1, 0.1, 0.01, 0.1, 0.1],  #
            [0.8, 0.1, 0.1, 0.01, 0.1, 0.1],  #
            [0.8, 0.1, 0.1, 0.01, 0.1, 0.1],  #
            [0.8, 0.1, 0.1, 0.01, 0.1, 0.1],  #
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {},
            "inserts": {},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
        clip=0.1,
    )


def test_closest_tensor_when_helol():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {},
            "inserts": {},
            "replaces": {3: ["ow", "l"]},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
        clip=0.1,
    )


def test_closest_tensor_when_heol():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {2: ["ow"]},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
        clip=0.1,
    )


def test_closest_tensor_when_heol2():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {2: "l"},
            "inserts": {4: ["l"]},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
        clip=0.1,
    )


def test_closest_tensor_when_heol3():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.2],  # o
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {2: ["ow"]},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
        clip=0.1,
    )


def test_closest_tensor_when_heoal():
    tensor_dict = Dictionary(["BLANK", "ah", "eh", "ow", "hh", "l"])
    pronunciations = {("hh", "eh", "l", "ow"): 1, ("hh", "ah", "l", "ow"): 2}
    inp = np.log(
        [
            # blnk, a,   e,   o,   h,   l
            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],  # h
            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],  # e
            [0.1, 0.1, 0.1, 0.5, 0.1, 0.2],  # o
            [0.1, 0.5, 0.1, 0.1, 0.1, 0.2],  # a
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5],  # l
        ]
    )

    check_closest_tensor(
        inp,
        tensor_dict,
        pronunciations,
        {
            "deletes": {3: "ow"},
            "inserts": {2: ["ow", "ah"]},
            "replaces": {},
            "target": ["hh", "eh", "l", "ow"],
        },
        threshold=0.4,
        clip=0.1,
    )
