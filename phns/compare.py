import numpy as np
from .utils.viterbi import viterbi


def closest(phns, graph):
    emissions = to_emissions(phns, graph)
    match = viterbi(np.log(emissions), np.log(graph.transition_matrix), np.log(graph.initial_transitions))

    inserts = []
    deletes = []
    replaces = []

    target = []

    first_node_idx = match.pop(0)
    root_indexes = [root.index for root in graph.roots]

    if first_node_idx not in root_indexes:
        root = None
        root_distance = float("inf")
        for root_index in root_indexes:
            new_distance = graph.distance_matrix[root_index, first_node_idx]
            if new_distance < distance:
                root = root_index
                distance = new_distance
        start = graph.nodes[root]
        end = graph.nodes[first_node_idx]
        while start != end:
            next_start_index = graph.shortest_paths[start.index, end.index]
            deletes.append((len(target), start.value))
            target.append(start.value)

            start = graph.nodes[next_start_index]

        if end.value != phns[0]:
            replaces.append((len(target), phns[0]))
        target.append(end.value)

    for prev_phn_idx in range(len(phns) - 1):
        orig_phn_idx = prev_phn_idx + 1

        if match[prev_phn_idx] == match[orig_phn_idx]:
            if graph.nodes[match[orig_phn_idx]].value != phns[orig_phn_idx]:
                inserts.append((len(target), phns[orig_phn_idx]))

        elif graph.distance_matrix[match[prev_phn_idx], match[orig_phn_idx]] == 1:
            if graph.nodes[match[orig_phn_idx]].value != phns[orig_phn_idx]:
                replaces.append((len(target), phns[orig_phn_idx]))
            target.append(graph.nodes[match[orig_phn_idx]].value)

        else:



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
