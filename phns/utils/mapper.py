# https://github.com/awni/speech/blob/master/examples/timit/phones.60-48-39.map with modifications:
# 61->40:
# - keep ao, zh
# - replace dx with d
# - set q as sil (was empty in awni)
# difference with CMU presence of SIL

TIMIT_TO_CMU = {
    'aa':   'aa',
    'ae':   'ae',
    'ah':   'ah',
    'ao':   'ao',
    'aw':   'aw',
    'ax':   'ah',
    'ax-h': 'ah',
    'axr':  'er',
    'ay':   'ay',
    'b':    'b',
    'bcl':  'sil',
    'ch':   'ch',
    'd':    'd',
    'dcl':  'sil',
    'dh':   'dh',
    'dx':   'd',
    'eh':   'eh',
    'el':   'l',
    'em':   'm',
    'en':   'n',
    'eng':  'ng',
    'epi':  'sil',
    'er':   'er',
    'ey':   'ey',
    'f':    'f',
    'g':    'g',
    'gcl':  'sil',
    'h#':   'sil',
    'hh':   'hh',
    'hv':   'hh',
    'ih':   'ih',
    'ix':   'ih',
    'iy':   'iy',
    'jh':   'jh',
    'k':    'k',
    'kcl':  'sil',
    'l':    'l',
    'm':    'm',
    'n':    'n',
    'ng':   'ng',
    'nx':   'n',
    'ow':   'ow',
    'oy':   'oy',
    'p':    'p',
    'pau':  'sil',
    'pcl':  'sil',
    'q':    'sil',
    'r':    'r',
    's':    's',
    'sh':   'sh',
    't':    't',
    'tcl':  'sil',
    'th':   'th',
    'uh':   'uh',
    'uw':   'uw',
    'ux':   'uw',
    'v':    'v',
    'w':    'w',
    'y':    'y',
    'z':    'z',
    'zh':   'zh'
}

# https://en.wikipedia.org/wiki/ARPABET
# ARPABET covers CMU but bigger (47 > 40)
ARPABET_TO_ONE_LETTER = {'aa': 'a', 'ae': '@', 'ah': 'A', 'ao': 'c', 'aw': 'W', 'ax': 'x', 'ay': 'Y', 'b': 'b', 'ch': 'C', 'cl': '-', 'd': 'd', 'dh': 'D', 'dx': 'F', 'eh': 'E', 'el': 'L', 'en': 'N', 'epi': '=', 'er': 'R', 'ey': 'e', 'f': 'f', 'g': 'g', 'hh': 'h', 'ih': 'I', 'ix': 'X', 'iy': 'i', 'jh': 'J', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'ng': 'G', 'ow': 'o', 'oy': 'O', 'p': 'p', 'r': 'r', 's': 's', 'sh': 'S', 'sil': '_', 't': 't', 'th': 'T', 'uh': 'U', 'uw': 'u', 'v': 'v', 'w': 'w', 'y': 'y', 'z': 'z', 'zh': 'Z' }

ARPABET_CONSONANTS = [ 'b', 'ch', 'd', 'dh', 'dx', 'el', 'em', 'en', 'f', 'g', 'hh', 'jh', 'k', 'l', 'm', 'n', 'ng', 'n', 'p', 'q', 'r', 's', 'sh', 't', 'th', 'v', 'w', 'wh', 'y', 'z', 'zh' ]



def timit_to_cmu(data):
    return [TIMIT_TO_CMU[phn] for phn in data]


def single_char_encode(phns):
    return ''.join([ARPABET_TO_ONE_LETTER[phn] for phn in phns])
