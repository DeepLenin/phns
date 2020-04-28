import os
import itertools
from copy import deepcopy
from . import heuristics
from .graph import Graph
from .utils import cmu, deep_phn


def __split__(text):
    return text.lower()    \
        .replace(".", "")  \
        .replace("\n", "") \
        .replace("?", "")  \
        .replace(",", "")  \
        .replace(";", "")  \
        .replace(":", "")  \
        .replace("\"", "") \
        .replace("!", "")  \
        .replace("-", " ") \
        .split()


def from_text(text, missing_handler=lambda _: False, apply_heuristics=True):
    words = __split__(text)

    if not callable(missing_handler):
        raise TypeError("missing_handler should be callable")

    skip = False
    graph = Graph()

    for word in words:
        transcription = deepcopy(cmu.get(word)) or deep_phn(missing_handler(word))
        if transcription:
            graph.attach(transcription)
        else:
            skip = True

    if not skip:
        if apply_heuristics:
            graph = heuristics.apply(graph)
        return graph
