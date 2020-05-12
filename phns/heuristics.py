from .utils.cmu import Phn
from .utils.mapper import ARPABET_CONSONANTS, ARPABET_VOWELS

RULES = {
    "assimilate_last": {
        (Phn("t"), Phn("b")): Phn("p"),  # fat boy
        (Phn("d"), Phn("b")): Phn("b"),  # good boy
        (Phn("n"), Phn("m")): Phn("m"),  # ten men
        (Phn("t"), Phn("k")): Phn("k"),  # that cat
        (Phn("t"), Phn("g")): Phn("k"),  # that girl
        (Phn("d"), Phn("k")): Phn("g"),  # good concert
        (Phn("d"), Phn("g")): Phn("g"),  # good girl
        (Phn("n"), Phn("k")): Phn("ng"),  # own car
        (Phn("n"), Phn("g")): Phn("ng"),  # been going
        (Phn("s"), Phn("sh")): Phn("sh"),  # this shiny
        (Phn("z"), Phn("sh")): Phn("zh"),  # cheese shop
    },
    "assimilate_coalescence": {
        (Phn("t"), Phn("y")): Phn("ch"),  # last year
        (Phn("d"), Phn("y")): Phn("jh"),  # would you
    },
}


def apply(graph):
    """Modifies graph according to heuristics

    Recursively matches and applies heuristics for every triplet of original
    and modified after heuristic application graph.

    Args:
        graph (Graph): Original graph

    Returns:
        Modified graph
    """
    triples = list(graph.triples())

    while triples:
        new_triples = []
        for (before, current, after) in triples:
            # NOTE: we don't apply heuristics to the first or the last phoneme
            # of a phrase
            if before and after:

                phn = RULES["assimilate_last"].get((current.value, after.value))
                if phn:
                    new_triples += graph.create_node_between(phn, before, after)

                phn = RULES["assimilate_coalescence"].get((current.value, after.value))
                if phn:
                    for out_node in after.out_nodes or [None]:
                        new_triples += graph.create_node_between(phn, before, out_node)

                if current.value == Phn("ah") and not current.value.stress:
                    new_triples += graph.create_edge(before, after)

                if (
                    current.value.val in {"t", "d"}
                    and before.value.val in ARPABET_CONSONANTS
                    and after.value.val in ARPABET_CONSONANTS
                ):
                    new_triples += graph.create_edge(before, after)

                if (
                    before.value.val == "ah"
                    and current.value.val == "v"
                    and after.value.val in ARPABET_CONSONANTS
                ):
                    new_triples += graph.create_edge(before, after)

                if (
                    current.value.val in ("ay", "ey", "iy", "oy")
                    and after.value.val in ARPABET_VOWELS
                ):
                    new_triples += graph.create_node_between(Phn("y"), current, after)

                if (
                    current.value.val in ("uw", "aw", "ow", "uh")
                    and after.value.val in ARPABET_VOWELS
                ):
                    new_triples += graph.create_node_between(Phn("w"), current, after)

        triples = new_triples

    return graph
