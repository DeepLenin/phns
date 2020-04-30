import itertools
from copy import deepcopy
from .utils.cmu import Phn
from .utils import single_char_encode, flatten, remove_doubles
from .utils.mapper import ARPABET_CONSONANTS

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
    }
}


def apply(graph):
    triples = list(graph.triples())

    while triples:
        new_triples = []
        for (before,current,after) in triples:

            if after:
                phn = RULES["assimilate_last"].get((current.value, after.value))
                if phn:
                    new_triples += graph.create_edges(current.from_node, after.to_node, phn, after.value)

                phn = RULES["assimilate_coalescence"].get((current.value, after.value))
                if phn:
                    new_triples += graph.create_edges(current.from_node, after.to_node, phn)

            if current.value == Phn("ah") and not current.value.stress:
                new_triples += graph.create_edges(current.from_node, current.to_node, None)

            if current.value.val in {"t", "d"} and before and after and \
               before.value.val in ARPABET_CONSONANTS and \
               after.value.val in ARPABET_CONSONANTS:
                new_triples += graph.create_edges(before.from_node, after.to_node, before.value, after.value)

        triples = new_triples

    return graph
