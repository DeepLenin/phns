from .utils import single_char_encode

def apply(pronunciations):
    result = {}
    for pronunciation in pronunciations:
        for heuristic in speech_heuristics:
            new_pronunciations = heuristic(pronunciation)
            for new_pronunciation in new_pronunciations:
                result[single_char_encode(new_pronunciation)] = new_pronunciation
    return result.values()


def assimilate(pronunciation):
    result = [pronunciation]
    replacements = []
    for i in range(len(pronunciation)-1):
        word = pronunciation[i]
        next_word = pronunciation[i+1]
        
        phn1 = word[-1]
        phn2 = next_word[0]

        rules = {
            ('t', 'b'): ('p', 'b'), # fat boy
            ('d', 'b'): ('b'), # good boy
            ('n', 'm'): ('m') # ten men
        }

        replacements.append([identity, rules.get((phn1, phn2)).bind(i)])
        
        # [[identity, replace1], [identity, replace2]]
        # product apply
        # [[identity, identity] [replace1, identity], [identity replace2] [replace1 replace2]]

        if replace:
            

            fat boy will come:
                1. fat boy with good boy
                2. fap boy with good boy
                3. fat boy with goob boy
                4. fap boy with goob boy
            
