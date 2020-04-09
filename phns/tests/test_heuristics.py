from phns.heuristics import assimilate


def test_assimilate_without_changes():
    canonical = [['t', 'h', 'e'], ['b', 'o', 'y']]
    assert assimilate(canonical) == [canonical]


def test_assimilate_with_one_change():
    canonical = [['f', 'a', 't'], ['b', 'o', 'y']]
    changed   = [['f', 'a', 'p'], ['b', 'o', 'y']]
    assert assimilate(canonical) == [canonical, changed]


def test_assimilate_with_two_changes():
    canonical = [['f', 'a', 't'], ['b', 'o', 'y'], ['g', 'o', 'o', 'd'], ['b', 'o', 'y']]
    changed1  = [['f', 'a', 't'], ['b', 'o', 'y'], ['g', 'o', 'o', 'b'], ['b', 'o', 'y']]
    changed2  = [['f', 'a', 'p'], ['b', 'o', 'y'], ['g', 'o', 'o', 'd'], ['b', 'o', 'y']]
    changed3  = [['f', 'a', 'p'], ['b', 'o', 'y'], ['g', 'o', 'o', 'b'], ['b', 'o', 'y']]

    assert assimilate(canonical) == [canonical, changed1, changed2, changed3]
