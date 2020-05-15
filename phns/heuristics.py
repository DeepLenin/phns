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
    "confusion": {
        # Vowels
        (Phn("eh"), Phn("ih")),
        (Phn("eh"), Phn("ae")),
        (Phn("iy"), Phn("ey")),
        (Phn("uh"), Phn("er")),
        (Phn("ah"), Phn("eh")),
        (Phn("ow"), Phn("uh")),
        (Phn("ah"), Phn("uh")),
        (Phn("uh"), Phn("uw")),
        (Phn("aa"), Phn("ae")),
        # Consonants
        (Phn("t"), Phn("p")),
        (Phn("k"), Phn("p")),
        (Phn("d"), Phn("g")),
        (Phn("d"), Phn("b")),
        (Phn("th"), Phn("f")),
        (Phn("s"), Phn("f")),
        (Phn("v"), Phn("b")),
        (Phn("dh"), Phn("b")),
        (Phn("dh"), Phn("d")),
        (Phn("dh"), Phn("g")),
        (Phn("dh"), Phn("th")),
        (Phn("z"), Phn("s")),
        (Phn("z"), Phn("v")),
        (Phn("z"), Phn("dh")),
        (Phn("l"), Phn("m")),
        (Phn("l"), Phn("n")),
        (Phn("l"), Phn("r")),
    },
}


def apply(graph, confusion=False):
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

                if confusion:
                    for ph1, ph2 in RULES["confusion"]:
                        if current.value.val in (ph1.val, ph2.val):
                            new_phn = ph1 if current.value.val == ph2.val else ph2
                            graph.create_node_between(new_phn, before, after)

        triples = new_triples

    return graph
