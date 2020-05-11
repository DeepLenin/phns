import os


class Phn:
    PHONEMES = {}

    def __new__(cls, val):
        if isinstance(val, Phn):
            return val
        _phn = val.lower().replace("0", "")
        if _phn not in cls.PHONEMES:
            instance = super(Phn, cls).__new__(cls)
            instance.__custom_init__(_phn)
            cls.PHONEMES[_phn] = instance
        return cls.PHONEMES[_phn]

    def __custom_init__(self, phoneme):
        self.__phoneme__ = phoneme
        self.val, self.stress = self.process()

    def process(self):
        """Splits cmu dict phoneme to phoneme and stress"""
        digit = None
        no_digits = []
        for char in self.__phoneme__.lower():
            if char.isdigit():
                digit = int(char)
            else:
                no_digits.append(char)
        return "".join(no_digits), digit

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        return other and self.val == other.val

    def __lt__(self, other):
        return self.val < other.val

    def __str__(self):
        return self.val

    def __repr__(self):
        return f'Phn("{self.__phoneme__}")'

    def __deepcopy__(self, memo={}):
        return self


CMU_PATH = os.path.dirname(os.path.realpath(__file__))
CMU_PATH += "/../vendor/cmudict/cmudict.dict"

CMU = {}
for line in open(CMU_PATH).readlines():
    parts = line.strip().split(" ")
    word = parts[0]
    transcription = [Phn(phn) for phn in parts[1:]]
    if "(" in word:
        word = word.split("(")[0]
    if word not in CMU:
        CMU[word] = [transcription]
    else:
        if transcription not in CMU[word]:
            CMU[word].append(transcription)
