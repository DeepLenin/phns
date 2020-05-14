import itertools
import os

from . import contractions
from .list_ext import flatten
from .phn import Phn

CMU_PATH = os.path.dirname(os.path.realpath(__file__))
CMU_PATH += "/../vendor/cmudict/cmudict.dict"

CMU = {}
for line in open(CMU_PATH).readlines():
    parts = line.strip().split(" ")
    word = parts[0]
    transcription = [Phn(phn) for phn in parts[1:]]
    if "(" in word:
        word = word.split("(")[0]
    if word not in CMU:
        CMU[word] = [transcription]
    else:
        if transcription not in CMU[word]:
            CMU[word].append(transcription)

for contraction, bag_of_words in contractions.FROM_CONTRACTIONS.items():
    if contraction not in CMU:
        raise f"CMU is missing word: {contraction}"
    for words in bag_of_words:
        transcriptions = itertools.product(*[CMU[word] for word in words])
        for transcription in transcriptions:
            transcription = flatten(transcription)
            if transcription not in CMU[contraction]:
                CMU[contraction].append(transcription)
