"""
Сочетания модификаторов:
    - "to be" + not
    - "to have" + not
    - "to do" + not
    - can + not
    - will + not
    - shall + not
    - modal verbs + [have, not, not + have]
"""

MODAL_VERBS = ["could", "should", "would", "ought", "might", "must", "need"]
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
ALIASES = {
    ("let", "us"): "let's",
    ("of", "course"): "'course",
    ("it", "was"): "'twas",
    ("it", "is"): "'tis",
}


def encode(word_idx, sentence):
    word1 = sentence[word_idx].lower()

    if "'" in word1:
        return word1, 0

    modifiers = [word1]
    for word in sentence[word_idx + 1 :]:
        word = word.lower()
        if word in MODIFIERS and __compatible__(modifiers, word):
            modifiers.append(word)
        else:
            if len(modifiers) == 1 and ALIASES.get((word1, word)):
                modifiers.append(word)
            break

    return "^".join(modifiers), len(modifiers) - 1


def decode(word):
    modifiers = word.split("^")

    variants = [modifiers]
    mod_len = len(modifiers)

    alias = ALIASES.get((modifiers[0], modifiers[1]))
    if alias:
        variants.append([alias, *modifiers[2:]])

    if mod_len == 2:
        word1, word2 = modifiers
        if word1 in MODAL_VERBS:
            if word2 == "not":
                variants.append([word1 + "n't"])
            elif word2 == "have":
                variants.append([word1 + "'ve"])
            else:
                raise ValueError(modifiers)
        elif word1 in MODIFIERS:
            if word2 == "not":
                if word1 in ["was", "were", "had", "do", "did", "does"]:
                    variants.append([word1 + "n't"])
                elif word1 == "shall":
                    variants.append(["shan't"])
                elif word1 == "will":
                    variants.append(["won't"])
                elif word1 == "can":
                    variants += [["can't"], ["cannot"]]
                elif word1 in ("am", "is", "are", "has", "have"):
                    if word1 != "am":
                        variants.append([word1 + "n't"])
                    variants.append(["ain't"])
                elif word1 == "dare":
                    variants.append(["daren't"])
                else:
                    raise ValueError(modifiers)
        else:
            if word2 == "am":
                if word1 == "i":
                    variants.append(["i'm"])
                else:
                    raise ValueError(modifiers)
            elif word2 in ["is", "has", "does", "was"]:
                variants.append([word1 + "'s"])
            elif word2 in ["are", "were"]:
                variants.append([word1 + "'re"])
            elif word2 in ["have"]:
                variants.append([word1 + "'ve"])
            elif word2 in ["will", "shall"]:
                variants.append([word1 + "'ll"])
            elif word2 in ["had", "did", "could", "would", "should"]:
                variants.append([word1 + "'d"])
            elif word2 in ["do", "can"]:
                pass
            elif not alias:
                raise ValueError(modifiers)
    elif mod_len == 3:
        word1, word2, word3 = modifiers
        if word2 in MODAL_VERBS and word3 == "have":
            if word2 in ["should", "would", "could"]:
                variants.append([word1 + "'d", word3])
            variants.append([word1, word2 + "'ve"])
        elif word3 == "not":
            if word2 in ("am", "is", "are", "has", "have"):
                variants.append([word1, "ain't"])
            if (
                word2
                in [
                    "is",
                    "are",
                    "were",
                    "was",
                    "have",
                    "has",
                    "had",
                    "do",
                    "did",
                    "does",
                ]
                + MODAL_VERBS
            ):
                variants.append([word1, word2 + "n't"])
            elif word2 == "can":
                variants += [[word1, "can't"], [word1, "cannot"]]
            elif word2 == "will":
                variants.append([word1, "won't"])
            elif word2 == "shall":
                variants.append([word1, "shan't"])
            else:
                raise ValueError(modifiers)

            if word2 == "am":
                if word1 == "i":
                    variants.append(["i'm", word3])
                else:
                    raise ValueError(modifiers)
            elif word2 in ["is", "has", "does", "was"]:
                variants.append([word1 + "'s", word3])
            elif word2 in ["are", "were"]:
                variants.append([word1 + "'re", word3])
            elif word2 in ["have"]:
                variants.append([word1 + "'ve", word3])
            elif word2 in ["will", "shall"]:
                variants.append([word1 + "'ll", word3])
            elif word2 in ["had", "did", "could", "would", "should"]:
                variants.append([word1 + "'d", word3])
            elif word2 in ["do", "can"]:
                pass
            else:
                raise ValueError(modifiers)
        else:
            raise ValueError(modifiers)
    elif mod_len == 4:
        word1, word2, word3, word4 = modifiers
        if word2 in MODAL_VERBS and word3 == "not" and word4 == "have":
            if word2 in ["should", "would", "could"]:
                variants.append([word1 + "'d", word3, word4])
            variants += [[word1, word2 + "n't", word4], [word1, word2 + "n't've"]]
        else:
            raise ValueError(modifiers)
    else:
        raise ValueError(modifiers)
    return variants


def __compatible__(modifiers, modifier):
    not_modifier = modifier == "not"

    if len(modifiers) == 1 and modifiers[0] not in MODIFIERS:
        return not (not_modifier)

    if not_modifier:
        return True

    if modifier == "have":
        if modifiers[-1] in MODAL_VERBS:
            return True
        if (
            modifiers[-1] == "not"
            and len(modifiers) > 1
            and modifiers[-2] in MODAL_VERBS
        ):
            return True

    return False
