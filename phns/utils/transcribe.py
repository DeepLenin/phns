import itertools

from . import CMU, contractions


def word(word):
    if "^" not in word:
        return CMU.get(word)

    variants = contractions.decode(word)
    result = set()
    for variant in variants:
        words_transcriptions = []
        # TODO: add 's/'d/'ll/n't/'ve
        skip = False
        for w in variant:
            transcriptions = CMU.get(w)
            if not transcriptions:
                skip = True
                break
            words_transcriptions.append(transcriptions)

        if not skip:
            final_transcriptions = itertools.product(*words_transcriptions)
            for final_transcription in final_transcriptions:
                result.add(sum(final_transcription, tuple()))
    return result
