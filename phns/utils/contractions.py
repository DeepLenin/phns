TO_CONTRACTIONS = {("i", "am"): "i'm", ("she", "had"): "she'd"}
FROM_CONTRACTIONS = {}
for words, contraction in TO_CONTRACTIONS.items():
    FROM_CONTRACTIONS.setdefault(contraction, []).append(words)


def encode(word1, word2):
    if not word1 or not word2:
        return
    word1 = word1.lower()
    word2 = word2.lower()

    return TO_CONTRACTIONS.get((word1, word2))
