import editdistance
from .utils import flatten


def closest(phns, variants):
    best = {"cer": float("inf")}
    for variant in variants:
        comparison = compare(phns, variant)
        if comparison["cer"] < best["cer"]:
            best = comparison
            best["phns"] = variant
    return best


def compare(phns1, phns2):
    distance = editdistance.eval(flatten(phns1), flatten(phns2))
    return {
        "distance": distance,
        "cer": distance/len(phns1)
    }


