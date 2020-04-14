import os
import itertools
from . import heuristics
from .utils import cmu


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


# TODO: add tests for missing_handler
def from_text(text, missing_handler=lambda _: False, apply_heuristics=True):
    words = __split__(text)

    if not callable(missing_handler):
        raise TypeError("missing_handler should be callable")

    cmu_phns = []
    skip = False

    for word in words:
        transcription = cmu.get(word) or missing_handler(word)
        if transcription:
            cmu_phns.append(transcription)
        else:
            skip = True

    if not skip:
        different_pronunciations = list(itertools.product(*cmu_phns))
        different_pronunciations = [list(pron) for pron in different_pronunciations]
        if apply_heuristics:
            different_pronunciations = heuristics.apply(different_pronunciations)
        return different_pronunciations
