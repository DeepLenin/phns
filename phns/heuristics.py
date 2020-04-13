import itertools
from copy import deepcopy
from .utils import single_char_encode, flatten
from .utils.mapper import ARPABET_CONSONANTS

RULES = {
    'assimilate_last': {
        ('t', 'b'): 'p', # fat boy
        ('d', 'b'): 'b', # good boy
        ('n', 'm'): 'm', # ten men
        ('t', 'k'): 'k', # that cat
        ('t', 'g'): 'k', # that girl
        ('d', 'k'): 'g', # good concert
        ('d', 'g'): 'g', # good girl
        ('n', 'k'): 'ng', # own car
        ('n', 'g'): 'ng', # been going
        ('s', 'sh'): 'sh', # this shiny
        ('z', 'sh'): 'zh', # cheese shop
    },
    'assimilate_coalescence': {
        ('t', 'y'): 'ch', # last year
        ('d', 'y'): 'jh', # would you
    }
}


def apply(pronunciations):
    result = {}
    for pronunciation in pronunciations:
        modifications = find_modifications(pronunciation)

        # [[None replace1] [None replace2]]
        # product
        # [[None None] [replace1 None] [None replace2] [replace1 replace2]]

        if not modifications:
            new_pronunciations = [ pronunciation ]
        else:
            replace_sequences = itertools.product(*modifications)
            new_pronunciations = []

            # TODO: add test for order of seq
            # TODO: add test for elision
            for seq in replace_sequences:
                new_pronunciation = deepcopy(pronunciation)
                seq = [step for step in seq if step]
                seq.sort(key=lambda x: x[:2])
                seq.reverse()

                for step in seq:
                    word_id, phn_id, heuristic, data = step

                    if heuristic == 'assimilate_last':
                        new_pronunciation[word_id][phn_id] = data

                    if heuristic == 'assimilate_coalescence':
                        del new_pronunciation[word_id][phn_id]
                        new_pronunciation[word_id+1][0] = data

                    if heuristic == 'consonant_cluster':
                        del new_pronunciation[word_id][phn_id]

                new_pronunciations.append(new_pronunciation)


        for new_pronunciation in new_pronunciations:
            result[single_char_encode(flatten(new_pronunciation))] = new_pronunciation

    return list(result.values())



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
                for heuristic in ['assimilate_last', 'assimilate_coalescence']:
                    data = RULES[heuristic].get((phn, next_phn))
                    if data:
                        modifications.append([None, [word_id, phn_id, heuristic, data]])

            if phn in {'t','d'} and prev_phn in ARPABET_CONSONANTS and next_phn in ARPABET_CONSONANTS:
                modifications.append([None, [word_id, phn_id, 'consonant_cluster', None]])

    return modifications
