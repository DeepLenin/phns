import os


class Phn:
    PHONEMES = {}

    def __new__(cls, val):
        if isinstance(val, Phn):
            return val

        _phn = val.lower()
        _phn = val.replace("0", "")
        if _phn not in cls.PHONEMES:
            cls.PHONEMES[_phn] = super(Phn, cls).__new__(cls)
        return cls.PHONEMES[_phn]

    def __init__(self, phoneme):
        self.__phoneme__ = phoneme
        self.val, self.stress = self.process()

    def process(self):
        """Splits cmu dict phoneme to phoneme and stress"""

        digit = None
        no_digits = []
        for ch in self.__phoneme__.lower():
            if ch.isdigit():
                digit = int(ch)
            else:
                no_digits.append(ch)
        return "".join(no_digits), digit

    def __lt__(self, other):
        return self.val < other.val

    def __str__(self):
        return self.val

    def __repr__(self):
        return f"Phn(\"{self.__phoneme__}\")"

    def __deepcopy__(self, memo={}):
        return self

cmu_path = os.path.dirname(os.path.realpath(__file__))
cmu_path += "/../vendor/cmudict/cmudict.dict"

cmu = {}
for line in open(cmu_path).readlines():
    parts = line.strip().split(" ")
    word = parts[0]
    if "(" in word:
        word = word.split("(")[0]
    if word not in cmu:
        cmu[word] = []

    cmu[word].append([Phn(phn) for phn in parts[1:]])
