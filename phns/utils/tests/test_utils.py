from phns.utils import deep_phn, deep_str, flatten, remove_doubles
from phns.utils.cmu import Phn


def test_flatten():
    orig = [[1, 2], [3, 4]]
    assert flatten(orig) == [1, 2, 3, 4]


def test_flatten_empty():
    orig = []
    assert flatten(orig) == []


def test_remove_doubles():
    orig = [1, 2, 2, 3, 4, 4, 2]
    assert remove_doubles(orig) == [1, 2, 3, 4, 2]


def test_remove_doubles_empty():
    orig = []
    assert remove_doubles(orig) == []


def test_deep_str():
    obj = [[1, 2, 3], [[1, 2], 3]]
    mapped = [["1", "2", "3"], [["1", "2"], "3"]]
    assert deep_str(obj) == mapped


def test_deep_phn():
    obj = [["ae", "t", "k"], [["er", "uh1"], "d"]]
    mapped = [[Phn("ae"), Phn("t"), Phn("k")], [[Phn("er"), Phn("uh1")], Phn("d")]]
    assert deep_phn(obj) == mapped
