from . import heuristics
from .graph import Graph
from .utils import contractions, deep_phn, transcribe


def __split__(text):
    return (
        text.lower()
        .replace(".", "")
        .replace("\n", "")
        .replace("?", "")
        .replace(",", "")
        .replace(";", "")
        .replace(":", "")
        .replace('"', "")
        .replace("!", "")
        .replace("-", " ")
        .replace("&", " and ")
        .split()
    )


def from_text(
    text,
    missing_handler=lambda _: False,
    apply_heuristics=True,
    apply_contractions=True,
    apply_confusion=False,
):
    words = __split__(text)

    if not callable(missing_handler):
        raise TypeError("missing_handler should be callable")

    skip = False
    graph = Graph()

    iterator = iter(range(len(words)))
    for word_idx in iterator:
        word = words[word_idx]

        if apply_contractions:
            contracted_word, to_skip = contractions.encode(word_idx, words)
            if contracted_word:
                # skip next `to_skip` word
                for _ in range(to_skip):
                    next(iterator)
                word = contracted_word

        transcription = transcribe.word(word) or deep_phn(missing_handler(word))
        if transcription:
            graph.attach(transcription)
        else:
            skip = True

    if not skip:
        if apply_heuristics:
            graph = heuristics.apply(graph, confusion=apply_confusion)
        return graph
