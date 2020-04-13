from phns.heuristics import apply


def test_assimilate_without_changes():
    canonical = [['dh', 'ah'], ['b', 'oy']] # the boy
    assert apply([canonical]) == [canonical]


def test_assimilate_with_one_change():
    canonical = [['f', 'ae', 't'], ['b', 'oy']] # fat boy
    changed   = [['f', 'ae', 'p'], ['b', 'oy']]
    assert apply([canonical]) == [canonical, changed]


def test_assimilate_with_two_changes():
    canonical = [['f', 'ae', 't'], ['b', 'oy'], ['g', 'uh', 'd'], ['b', 'oy']] # fat boy good boy
    changed1  = [['f', 'ae', 't'], ['b', 'oy'], ['g', 'uh', 'b'], ['b', 'oy']]
    changed2  = [['f', 'ae', 'p'], ['b', 'oy'], ['g', 'uh', 'd'], ['b', 'oy']]
    changed3  = [['f', 'ae', 'p'], ['b', 'oy'], ['g', 'uh', 'b'], ['b', 'oy']]

    assert apply([canonical]) == [canonical, changed1, changed2, changed3]

def test_assimilate_coalescence():
    canonical = [['g', 'uh', 'd'], ['y', 'ih', 'r']]
    changed   = [['g', 'uh'], ['jh', 'ih', 'r']]
    assert apply([canonical]) == [canonical, changed]
