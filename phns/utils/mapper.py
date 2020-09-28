# flake8: noqa


class Dictionary:
    """Wrapper on phonemes dictionary

    Provides simple interface on list of phonemes to translate them from/to ids

    Attributes:
        all_phns (List[str]): List of phonemes to map into dictionaries
    """

    def __init__(self, all_phns):
        self.phn_to_id = {phn: idx for idx, phn in enumerate(all_phns)}
        self.id_to_phn = {idx: phn for phn, idx in self.phn_to_id.items()}
        self.total = len(self.phn_to_id)

    def __len__(self):
        return self.total


# fmt: off
TIMIT_TO_CMU = {
    "aa":   "aa",
    "ae":   "ae",
    "ah":   "ah",
    "ao":   "ao",
    "aw":   "aw",
    "ax":   "ah",
    "ax-h": "ah",
    "axr":  "er",
    "ay":   "ay",
    "b":    "b",
    "bcl":  "sil",
    "ch":   "ch",
    "d":    "d",
    "dcl":  "sil",
    "dh":   "dh",
    "dx":   "d",
    "eh":   "eh",
    "el":   "l",
    "em":   "m",
    "en":   "n",
    "eng":  "ng",
    "epi":  "sil",
    "er":   "er",
    "ey":   "ey",
    "f":    "f",
    "g":    "g",
    "gcl":  "sil",
    "h#":   "sil",
    "hh":   "hh",
    "hv":   "hh",
    "ih":   "ih",
    "ix":   "ih",
    "iy":   "iy",
    "jh":   "jh",
    "k":    "k",
    "kcl":  "sil",
    "l":    "l",
    "m":    "m",
    "n":    "n",
    "ng":   "ng",
    "nx":   "n",
    "ow":   "ow",
    "oy":   "oy",
    "p":    "p",
    "pau":  "sil",
    "pcl":  "sil",
    "q":    "sil",
    "r":    "r",
    "s":    "s",
    "sh":   "sh",
    "t":    "t",
    "tcl":  "sil",
    "th":   "th",
    "uh":   "uh",
    "uw":   "uw",
    "ux":   "uw",
    "v":    "v",
    "w":    "w",
    "y":    "y",
    "z":    "z",
    "zh":   "zh"
}

ARPABET_TO_ONE_LETTER = {
    "aa":  "a",
    "ae":  "@",
    "ah":  "A",
    "ao":  "c",
    "aw":  "W",
    "ax":  "x",
    "ay":  "Y",
    "b":   "b",
    "ch":  "C",
    "cl":  "-",
    "d":   "d",
    "dh":  "D",
    "dx":  "F",
    "eh":  "E",
    "el":  "L",
    "en":  "N",
    "epi": "=",
    "er":  "R",
    "ey":  "e",
    "f":   "f",
    "g":   "g",
    "hh":  "h",
    "ih":  "I",
    "ix":  "X",
    "iy":  "i",
    "jh":  "J",
    "k":   "k",
    "l":   "l",
    "m":   "m",
    "n":   "n",
    "ng":  "G",
    "ow":  "o",
    "oy":  "O",
    "p":   "p",
    "r":   "r",
    "s":   "s",
    "sh":  "S",
    "sil": "_",
    "t":   "t",
    "th":  "T",
    "uh":  "U",
    "uw":  "u",
    "v":   "v",
    "w":   "w",
    "y":   "y",
    "z":   "z",
    "zh":  "Z"
}

ARPABET_CONSONANTS = {
    "b", "ch", "d", "dh", "dx", "el", "em", "en", "f", "g", "hh", "jh", "k", "l", "m",
    "n", "ng", "n", "p", "q", "r", "s", "sh", "t", "th", "v", "w", "wh", "y", "z", "zh"
}

ARPABET_VOWELS = {
    "aa", "ae", "ah", "ao", "aw", "ay", "eh", "er", "ey", "ih", "iy", "ow", "oy", "uh", "uw"
}
# fmt: off


def timit_to_cmu(data):
    """Converts string representation of phonemes into CMU format 61 -> 40

    https://github.com/awni/speech/blob/master/examples/timit/phones.60-48-39.map
    With modifications:
    61->40:
        - keep ao, zh
        - replace dx with d
        - set q as sil (was empty in awni)
    Difference with CMU: presence of SIL

    Args:
        data (List(str)): List of phonemes to map

    Returns:
        List of phonemes in CMU format
    """
    return [TIMIT_TO_CMU[str(phn)] for phn in data]


def single_char_encode(phns):
    """Converts string representation of phonemes into single letter representation

    https://en.wikipedia.org/wiki/ARPABET
    ARPABET covers CMU but bigger (47 > 40)

    Args:
        data (List(str)): List of phonemes to map

    Returns:
        List of phonemes in single letter representation
    """
    return "".join([ARPABET_TO_ONE_LETTER[str(phn)] for phn in phns])


CMU_DICTIONARY = Dictionary(["BLANK"] + sorted(list(set(TIMIT_TO_CMU.values()))))
