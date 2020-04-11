import itertools
from copy import deepcopy
from .utils import single_char_encode, flatten

def apply(pronunciations):
    result = {}
    for pronunciation in pronunciations:
        modifications = []
        for heuristic in [assimilate, elision]:
            modifications.extend(heuristic(pronunciation))


        # [[None replace1] [None replace2]]
        # product
        # [[None None] [replace1 None] [None replace2] [replace1 replace2]]

        if not modifications:
            new_pronunciations = [ pronunciation ]
        else:
            replace_sequences = itertools.product(*modifications)
            new_pronunciations = []
            for seq in replace_sequences:
                new_pronunciation = deepcopy(pronunciation)
                for step in seq:
                    if step:
                        index, rule, data = step
                    else:
                        continue

                    if rule == 'change_last':
                        new_pronunciation[index][-1] = data

                    if rule == 'coalesce':
                        new_pronunciation[index][-1] = data
                        del new_pronunciation[index + 1][0]

                new_pronunciations.append(new_pronunciation)


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

        change_last_rules = {
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
        }

        new_phn1 = change_last_rules.get((phn1, phn2))
        if new_phn1:
            replacements.append([None, [i, 'change_last', new_phn1]])


        coalesce_rules = {
            ('t', 'y'): 'ch', # last year
            ('d', 'y'): 'jh', # would you
        }

        coalescent_phn = coalesce_rules.get((phn1, phn2))
        if coalescent_phn:
            replacements.append([None, [i, 'coalesce', coalescent_phn]])

    return replacements


def elision(pronunciation):
    return []
