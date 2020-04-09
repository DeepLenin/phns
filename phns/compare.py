import editdistance
from .utils import flatten, remove_doubles


def closest(phns, variants):
    best = {"cer": float("inf")}
    for variant in variants:
        comparison = compare(phns, variant)
        if comparison["cer"] < best["cer"]:
            best = comparison
            best["phns"] = variant
    return best


def compare(phns1, phns2):
    _p1 = remove_doubles(flatten(phns1))
    _p2 = remove_doubles(flatten(phns2))
    distance = editdistance.eval(_p1, _p2)
    return {
        "distance": distance,
        "cer": distance/len(phns1)
    }
