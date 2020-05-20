import os

from .phn import Phn

CMU_PATH = os.path.dirname(os.path.realpath(__file__))
CMU_PATH += "/../vendor/cmudict/cmudict.dict"

CMU = {}
for line in open(CMU_PATH).readlines():
    parts = line.strip().split(" ")
    word = parts[0]
    transcription = (Phn(phn) for phn in parts[1:])
    if "(" in word:
        word = word.split("(")[0]
    CMU.setdefault(word, set()).add(transcription)

ALIASES = {
    "them": "'em",
    "about": "'bout",
    "because": "'cause",
    "okay": "'kay",
    "ok": "okay",
    "until": "'til",
}
for original, alias in ALIASES.items():
    union = CMU[original].union(CMU[alias])
    CMU[original] = CMU[alias] = union
