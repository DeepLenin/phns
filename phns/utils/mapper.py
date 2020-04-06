# https://github.com/awni/speech/blob/master/examples/timit/phones.60-48-39.map
M_61_48 = {'aa': 'aa', 'ae': 'ae', 'ah': 'ah', 'ao': 'ao', 'aw': 'aw', 'ax': 'ax', 'ax-h': 'ax', 'axr': 'er', 'ay': 'ay', 'b': 'b', 'bcl': 'vcl', 'ch': 'ch', 'd': 'd', 'dcl': 'vcl', 'dh': 'dh', 'dx': 'dx', 'eh': 'eh', 'el': 'el', 'em': 'm', 'en': 'en', 'eng': 'ng', 'epi': 'epi', 'er': 'er', 'ey': 'ey', 'f': 'f', 'g': 'g', 'gcl': 'vcl', 'h#': 'sil', 'hh': 'hh', 'hv': 'hh', 'ih': 'ih', 'ix': 'ix', 'iy': 'iy', 'jh': 'jh', 'k': 'k', 'kcl': 'cl', 'l': 'l', 'm': 'm', 'n': 'n', 'ng': 'ng', 'nx': 'n', 'ow': 'ow', 'oy': 'oy', 'p': 'p', 'pau': 'sil', 'pcl': 'cl', 'r': 'r', 's': 's', 'sh': 'sh', 't': 't', 'tcl': 'cl', 'th': 'th', 'uh': 'uh', 'uw': 'uw', 'ux': 'uw', 'v': 'v', 'w': 'w', 'y': 'y', 'z': 'z', 'zh': 'zh'}
M_48_39 = {'aa': 'aa', 'ae': 'ae', 'ah': 'ah', 'ao': 'aa', 'aw': 'aw', 'ax': 'ah', 'er': 'er', 'ay': 'ay', 'b': 'b', 'vcl': 'sil', 'ch': 'ch', 'd': 'd', 'dh': 'dh', 'dx': 'dx', 'eh': 'eh', 'el': 'l', 'm': 'm', 'en': 'n', 'ng': 'ng', 'epi': 'sil', 'ey': 'ey', 'f': 'f', 'g': 'g', 'sil': 'sil', 'hh': 'hh', 'ih': 'ih', 'ix': 'ih', 'iy': 'iy', 'jh': 'jh', 'k': 'k', 'cl': 'sil', 'l': 'l', 'n': 'n', 'ow': 'ow', 'oy': 'oy', 'p': 'p', 'r': 'r', 's': 's', 'sh': 'sh', 't': 't', 'th': 'th', 'uh': 'uh', 'uw': 'uw', 'v': 'v', 'w': 'w', 'y': 'y', 'z': 'z', 'zh': 'sh'}

# https://en.wikipedia.org/wiki/ARPABET
M_39_ONE_LETTER = {'aa': 'a', 'ae': '@', 'ah': 'A', 'ao': 'c', 'aw': 'W', 'ax': 'x', 'ay': 'Y', 'b': 'b', 'ch': 'C', 'cl': '-', 'd': 'd', 'dh': 'D', 'dx': 'F', 'eh': 'E', 'el': 'L', 'en': 'N', 'epi': '=', 'er': 'R', 'ey': 'e', 'f': 'f', 'g': 'g', 'hh': 'h', 'ih': 'I', 'ix': 'X', 'iy': 'i', 'jh': 'J', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'ng': 'G', 'ow': 'o', 'oy': 'O', 'p': 'p', 'r': 'r', 's': 's', 'sh': 'S', 'sil': '_', 't': 't', 'th': 'T', 'uh': 'U', 'uw': 'u', 'v': 'v', 'vcl': '+', 'w': 'w', 'y': 'y', 'z': 'z', 'zh': 'Z' }


# TODO: document phonems in different models/datasets
def remap(data):
    result = []
    for phn in data:
        # dx is missing from awni 39 phonemes
        if phn == 'dx':
            result.append('d')
        # in case we override phoneme target and use SIL symbol
        elif phn == 'sil':
            result.append(phn)
        elif phn != 'q':
            result.append(M_48_39[M_61_48[phn]])
    return result


def single_char_encode(phns):
    return ''.join([M_39_ONE_LETTER[phn] for phn in phns])
