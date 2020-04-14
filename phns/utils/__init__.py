from .cmu import cmu, Phn
from .mapper import timit_to_cmu, single_char_encode

__all__ = [
    "cmu",
    "deep_str",
    "deep_phn",
    "flatten",
    "remove_doubles",
    "single_char_encode",
    "timit_to_cmu",
]


def flatten(lst):
    if isinstance(lst[0], list):
        return [item for sublist in lst for item in sublist]
    else:
        return lst


def remove_doubles(arr):
    res = [arr[0]]
    for el in arr[1:]:
        if el == res[-1]:
            continue
        res.append(el)
    return res


def deep_str(obj):
    if isinstance(obj, list):
        return [deep_str(subobj) for subobj in obj]
    else:
        return str(obj)


def deep_phn(obj):
    if isinstance(obj, list):
        return [deep_phn(subobj) for subobj in obj]
    else:
        return Phn(obj)
