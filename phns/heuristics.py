import itertools
from copy import deepcopy
from .utils import single_char_encode, flatten

def apply(pronunciations):
    result = {}
    for pronunciation in pronunciations:
        for heuristic in [assimilate]:
            new_pronunciations = heuristic(pronunciation)
            for new_pronunciation in new_pronunciations:
                result[single_char_encode(flatten(new_pronunciation))] = new_pronunciation
    return list(result.values())


def assimilate(pronunciation):
    replacements = []
    for i in range(len(pronunciation)-1):
        word = pronunciation[i]
        next_word = pronunciation[i+1]
        
        phn1 = word[-1]
        phn2 = next_word[0]

        rules = {
            ('t', 'b'): 'p', # fat boy
            ('d', 'b'): 'b', # good boy
            ('n', 'm'): 'm' # ten men
        }

        new_phn1 = rules.get((phn1, phn2))
        if new_phn1:
            replacements.append([None, [i, 'change_last', new_phn1]])

    # [[None replace1] [None replace2]]
    # product
    # [[None None] [replace1 None] [None replace2] [replace1 replace2]]
    replace_sequences = itertools.product(*replacements)
    result = []
    for seq in replace_sequences:
        new_pronunciation = deepcopy(pronunciation)
        for step in seq:
            if step:
                index, rule, data = step
            else:
                continue

            if rule == 'change_last':
                new_pronunciation[index][-1] = data

        result.append(new_pronunciation)

    return result
