import os
import itertools
from .utils import cmu

DEBUG = os.getenv("DEBUG", True)


def split(text):
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
        .split(" ")


def from_text(text):
    words = split(text)

    cmu_phns = []
    missed_words = []

    for word in words:
        if word not in cmu:
            if DEBUG:
                print("word not in dict: ", word)
                missed_words.append(word)
            continue
        cmu_phns.append(cmu[word])

    return list(itertools.product(*cmu_phns))
