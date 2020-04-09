from phns.utils import flatten, remove_doubles


def test_flatten():
    orig = [[1, 2], [3, 4]]
    assert flatten(orig) == [1, 2, 3, 4]


def test_remove_doubles():
    orig = [1, 2, 2, 3, 4, 4, 2]
    assert remove_doubles(orig) == [1, 2, 3, 4, 2]
