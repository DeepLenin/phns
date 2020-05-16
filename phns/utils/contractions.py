import itertools

TO_CONTRACTIONS = {
    ("i", "am"): "i'm",
    ("i", "had"): "i'd",
    ("i", "would"): "i'd",
    ("i", "should"): "i'd",
    ("i", "could"): "i'd",
    ("i", "will"): "i'll",
    ("i", "have"): "i've",
    ("you", "are"): "you're",
    ("you", "were"): "you're",
    ("you", "had"): "you'd",
    ("you", "would"): "you'd",
    ("you", "could"): "you'd",
    ("you", "should"): "you'd",
    ("you", "will"): "you'll",
    ("you", "have"): "you've",
    ("he", "is"): "he's",
    ("he", "was"): "he's",
    ("he", "has"): "he's",
    ("he", "had"): "he'd",
    ("he", "would"): "he'd",
    ("he", "could"): "he'd",
    ("he", "should"): "he'd",
    ("he", "will"): "he'll",
    ("she", "is"): "she's",
    ("she", "has"): "she's",
    ("she", "was"): "she's",
    ("she", "had"): "she'd",
    ("she", "would"): "she'd",
    ("she", "could"): "she'd",
    ("she", "should"): "she'd",
    ("she", "will"): "she'll",
    ("it", "is"): "it's",
    ("it", "has"): "it's",
    ("it", "was"): "it's",
    ("it", "would"): "it'd",
    ("it", "could"): "it'd",
    ("it", "should"): "it'd",
    ("it", "will"): "it'll",
    ("we", "are"): "we're",
    ("we", "were"): "we're",
    ("we", "had"): "we'd",
    ("we", "should"): "we'd",
    ("we", "could"): "we'd",
    ("we", "would"): "we'd",
    ("we", "will"): "we'll",
    ("we", "have"): "we've",
    ("they", "are"): "they're",
    ("they", "were"): "they're",
    ("they", "had"): "they'd",
    ("they", "would"): "they'd",
    ("they", "could"): "they'd",
    ("they", "should"): "they'd",
    ("they", "will"): "they'll",
    ("they", "have"): "they've",
    ("there", "is"): "there's",
    ("there", "has"): "there's",
    ("there", "was"): "there's",
    ("there", "will"): "there'll",
    ("there", "had"): "there'd",
    ("there", "would"): "there'd",
    ("there", "could"): "there'd",
    ("there", "should"): "there'd",
    ("is", "not"): "isn't",
    ("are", "not"): "aren't",
    ("do", "not"): "don't",
    ("does", "not"): "doesn't",
    ("was", "not"): "wasn't",
    ("were", "not"): "weren't",
    ("did", "not"): "didn't",
    ("have", "not"): "haven't",
    ("has", "not"): "hasn't",
    ("will", "not"): "won't",
    ("had", "not"): "hadn't",
    ("can", "not"): "can't",
    ("could", "not"): "couldn't",
    ("must", "not"): "mustn't",
    ("might", "not"): "mightn't",
    ("need", "not"): "needn't",
    ("should", "not"): "shouldn't",
    ("ought", "not"): "oughtn't",
    ("would", "not"): "wouldn't",
    ("what", "is"): "what's",
    ("how", "is"): "how's",
    ("where", "is"): "where's",
}

MODIFIERS = {
    "am",
    "is",
    "are",
    "was",
    "were",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "can",
    "could",
    "will",
    "would",
    "shall",
    "should",
    "not",
}

FROM_CONTRACTIONS = {}
for words, contraction in TO_CONTRACTIONS.items():
    FROM_CONTRACTIONS.setdefault(contraction, []).append(words)


def encode(word_idx, sentence):
    word1 = sentence[word_idx].lower()

    if "'" in word1:
        # TODO: decode can return different modifiers: I'd -> would, could ...
        # word1, mod = decode(word1)
        # modifiers = [None, mod]
        modifiers = [None]
    else:
        modifiers = [None]

    for word in sentence[word_idx + 1 :]:
        word = word.lower()
        if word in MODIFIERS and compatible(modifiers, word):
            modifiers.append(word)
        else:
            break

    modifiers.pop(0)
    modifiers = [word1] + modifiers

    return "^".join(modifiers), len(modifiers) - 1


def decode(word):
    modifiers = word.split("^")

    variants = []
    mod_len = len(modifiers)
    for mod_idx in range(mod_len):
        mod1 = modifiers[mod_idx]
        mod2 = None
        mod3 = None

        if mod_idx < mod_len - 1:
            mod2 = modifiers[mod_idx + 1]
            if mod_idx < mod_len - 2:
                mod3 = modifiers[mod_idx + 2]

        if mod2 and compatible(mod1, mod2):
            variants.append((mod_idx, mod_idx + 1))
            if mod3 and compatible([mod1, mod2], mod3):
                variants.append((mod_idx, mod_idx + 1, mod_idx + 2))
    variants = itertools.product(*[[None, variant] for variant in variants])
    filtered = []
    for variant in variants:
        var = [it for it in variant if it]
        compressed = compress(modifiers, var)
        if compressed:
            filtered.append(compressed)

    return filtered


def compress(modifiers, compressions):
    prev = None
    for current in reversed(sorted(compressions)):
        if prev and prev[0] > current[-1]:
            # Similar to compatible

            prev = current
        else:
            return


def compatible(modifiers, modifier):
    """
    word, word, word, current, word1, word2
    1. Сurrent - обычное слово. Смотрим вперед до следующего не-модификатора.
        И создаем перебор всех комбинаций последовательных модификаторов не длиней 3
    2. Current - уже контракшн - мы должны декодировать чтоб понять можно ли
        его еще модифицировать (при декодировании получим модификатор и проверим
        можно ли его модифицировать)

    Модификаторы:
        - "to be" (am, is, are, was, were)
        - "to have" (have, has, had)
        - "to do" (do, does, did)
        - can
        - could
        - will
        - would
        - shall
        - should
        - not
    Сочетания модификаторов:
        - "to be" + not
        - "to have" + not
        - "to do" + not
        - can + not
        - will + not
        - shall + not
        - could + [have, not, not + have]
        - would + [have, not, not + have]
        - should + [have, not, not + have]
    """
