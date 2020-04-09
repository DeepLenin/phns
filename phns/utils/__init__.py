from .cmu import cmu
from .mapper import remap, single_char_encode

__all__ = ["cmu", "remap", "remove_doubles", "single_char_encode", "flatten"]


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
