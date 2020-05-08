import numpy as np
from .utils.viterbi import viterbi


def closest(phns, graph):
    emissions = to_emissions(phns, graph)
    match = viterbi(np.log(emissions), np.log(graph.transition_matrix), np.log(graph.initial_transitions))

    # 1 -> 2 -> 3 -> 5
    #   -> 4 ->
    # hol -> 1,1,3 # 1,2,3
    # helo
    # 
    # we want to return
    # {
    #    target: helo,
    #    cer: 0.2,
    #    inserts: [o -> 1]
    #    deletes: [e -> 1, o -> 3]
    #
    # inserts + deletes in one index == replace
    # {
    #    target: helo,
    #    cer: 0.2,
    #    deletes: [o -> 3]
    #    replaces: [ e-o->1 ]
    #
    # helo -> 1 -> 2 -> 3 -> 5
    # 
    return [graph.nodes[i].value for i in match]


def to_emissions(phns, graph):
    emissions = np.full((len(graph.nodes), len(phns)), 1/2)

    indexes = {}
    for i, phn in enumerate(phns):
        if phn in indexes:
            indexes[phn].append(i)
        else:
            indexes[phn] = [i]
    
    for node in graph.nodes:
        if node.value in indexes:
            emissions[node.index, indexes[node.value]] = 1

    return emissions
