import itertools
from copy import deepcopy
from .utils.cmu import Phn
from .utils import single_char_encode, flatten, remove_doubles
from .utils.mapper import ARPABET_CONSONANTS

RULES = {
    "assimilate_last": {
        ("t", "b"): "p",  # fat boy
        ("d", "b"): "b",  # good boy
        ("n", "m"): "m",  # ten men
        ("t", "k"): "k",  # that cat
        ("t", "g"): "k",  # that girl
        ("d", "k"): "g",  # good concert
        ("d", "g"): "g",  # good girl
        ("n", "k"): "ng",  # own car
        ("n", "g"): "ng",  # been going
        ("s", "sh"): "sh",  # this shiny
        ("z", "sh"): "zh",  # cheese shop
    },
    "assimilate_coalescence": {
        ("t", "y"): "ch",  # last year
        ("d", "y"): "jh",  # would you
    }
}


def apply(pronunciations):
    result = {}
    for pronunciation in pronunciations:
        modifications = find_modifications(pronunciation)

        if not modifications:
            new_pronunciations = [pronunciation]
        else:
            # [[None replace1] [None replace2]]
            # product
            # [[None None] [replace1 None] [None replace2] [replace1 replace2]]
            modifications = [[None, mod] for mod in modifications]
            replace_sequences = itertools.product(*modifications)
            new_pronunciations = []

            for i, seq in enumerate(replace_sequences):
                new_pronunciation = deepcopy(pronunciation)
                seq = [step for step in seq if step]
                seq.sort(key=lambda x: x[:2])
                seq.reverse()

                for step in seq:
                    word_id, phn_id, heuristic, data = step

                    if len(new_pronunciation[word_id]) <= phn_id:
                        # TODO: think about double check value of phoneme before modification
                        # In case if phoneme was deleted
                        # from the end of the word we ignore all other
                        # modifications
                        continue

                    if heuristic == "assimilate_last":
                        new_pronunciation[word_id][phn_id] = data

                    if heuristic == "assimilate_coalescence":
                        del new_pronunciation[word_id][phn_id]
                        new_pronunciation[word_id+1][0] = data

                    if heuristic == "consonant_cluster":
                        del new_pronunciation[word_id][phn_id]

                    if heuristic == "unstressed_ah":
                        del new_pronunciation[word_id][phn_id]

                new_pronunciations.append(new_pronunciation)


        for new_pronunciation in new_pronunciations:
            key = remove_doubles(flatten(new_pronunciation))
            key = single_char_encode(key)
            result[key] = [remove_doubles(word) for word in new_pronunciation]

    return sorted(list(result.values()))



def find_modifications(pronunciation):
    modifications = []

    for word_id in range(len(pronunciation)):
        word = pronunciation[word_id]

        for phn_id in range(len(word)):
            phn = word[phn_id]
            prev_phn = None
            next_phn = None

            if phn_id == 0:
                if word_id > 0:
                    prev_phn = pronunciation[word_id-1][-1]
            else:
                prev_phn = word[phn_id-1]


            if phn_id == len(word) - 1:
                if word_id < len(pronunciation)-1:
                    next_phn = pronunciation[word_id+1][0]
            else:
                next_phn = word[phn_id+1]


            if phn_id == len(word)-1 and next_phn:
                for heuristic in ["assimilate_last", "assimilate_coalescence"]:
                    data = RULES[heuristic].get((phn.val, next_phn.val))
                    if data:
                        modifications.append([word_id, phn_id, heuristic, Phn(data)])

            if phn.val in {"t", "d"} and \
               (prev_phn and prev_phn.val) in ARPABET_CONSONANTS and \
               (next_phn and next_phn.val) in ARPABET_CONSONANTS:
                modifications.append([word_id, phn_id, "consonant_cluster", None])

            if phn.val == 'ah' and not phn.stress and len(word) > 1:
                modifications.append([word_id, phn_id, "unstressed_ah", None])

    return modifications
