import itertools
import re

from . import CMU, contractions
from .mapper import ARPABET_VOWELS
from .phn import Phn


def word(word):
    if "^" not in word:
        return fetch(word)

    variants = contractions.decode(word)
    result = dict()
    for variant in variants:
        words_transcriptions = []
        skip = False
        for w in variant:
            transcriptions = fetch(w)
            if not transcriptions:
                skip = True
                break
            words_transcriptions.append(transcriptions)

        if not skip:
            final_transcriptions = itertools.product(*words_transcriptions)
            for final_transcription in final_transcriptions:
                result[sum(final_transcription, tuple())] = variant
    return result


PARTS_PATTERN = re.compile(r"(.+?)(n't)?('re|'ve|'d|'ll|'s|')?$")


def fetch(full_word):
    result = CMU.get(full_word)
    if result or "'" not in full_word:
        return result

    word, not_part, suffix = PARTS_PATTERN.match(full_word).groups()

    transcriptions = CMU.get(word)
    if not transcriptions:
        return

    if not_part:
        __push_phonemes__(transcriptions, (Phn("n"), Phn("t")))

    # https://www.oxfordonlineenglish.com/english-contractions
    # https://pronunciationstudio.com/contractions/
    if suffix == "'ve":
        __push_phonemes__(transcriptions, (Phn("v"),))
    elif suffix == "'ll":
        __push_phonemes__(transcriptions, (Phn("l"),))
    elif suffix == "'d":
        __push_phonemes__(transcriptions, (Phn("d"),))
    elif suffix in ["'s", "'"]:
        # https://en.wikipedia.org/wiki/English_possessive (the same rules as for plural and contraction 's)
        for transcription in transcriptions:
            last_phn = transcription[-1].val
            if last_phn in ["s", "z", "sh", "zh", "ch", "jh"]:
                transcription += (Phn("ih"), Phn("z"))
            # TODO: Когда в конце слова может быть просто отдельный апостроф без продолжения
            elif suffix != "'":
                if last_phn in ["p", "t", "k", "f", "th"]:
                    transcription += (Phn("s"),)
                else:
                    transcription += (Phn("z"),)
    elif suffix == "'re":
        for transcription in transcriptions:
            # TODO: if the next word starts with vowel then we need to also add "r"?
            transcription += (Phn("ah"),)
    else:
        return
    return transcriptions


def __push_phonemes__(transcriptions, phonemes):
    for transcription in transcriptions:
        if transcription[-1].val in ARPABET_VOWELS:
            transcription += phonemes
        else:
            transcription += (Phn("ah"),) + phonemes
