import editdistance


def closest(phns, variants):
    best = { "cer": float("inf") }
    for variant in variants:
        comparison = compare(phns, variant)
        if comparison["cer"] < best["cer"]:
            best = comparison
            best["phns"] = variant
    return best


def compare(phns1, phns2):
    distance = editdistance.eval(__flatten__(phns1), __flatten__(phns2))
    return {
        "distance": distance,
        "cer": distance/len(phns1)
    }


def __flatten__(lst):
    if isinstance(lst[0], list):
        return [item for sublist in lst for item in sublist]
    else:
        return lst
