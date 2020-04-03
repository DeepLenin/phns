import os

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

    # TODO: Do not remove digits if need stress level
    def no_digit(x):
        return not x.isdigit()
    cmu[word].append(
        ["".join(filter(no_digit, phn.lower())) for phn in parts[1:]]
    )
