from .cmu import cmu
from .mapper import remap, single_char_encode

__all__ = ["cmu", "remap", "single_char_encode", "flatten"]


def flatten(lst):
    if isinstance(lst[0], list):
        return [item for sublist in lst for item in sublist]
    else:
        return lst
