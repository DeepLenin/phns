import numpy as np

from .utils.viterbi import viterbi


def traverse_shortest_path(kind, from_node_index, to_node_index, meta):
    graph = meta["graph"]
    start = graph.nodes[from_node_index]
    end = graph.nodes[to_node_index]
    if kind == "tail":
        start, end = end, start
        skip = True
    else:
        skip = False

    while True:
        next_start_index = graph.shortest_paths[start.index, end.index]

        if skip:
            # Skip first for tail traversing
            skip = False
        else:
            meta["deletes"].append((len(meta["target"]), start.value))
            meta["target"].append(start.value)

        if next_start_index == start.index:
            break

        start = graph.nodes[next_start_index]

    if kind == "tail":
        meta["deletes"].append((len(meta["target"]), end.value))
        meta["target"].append(end.value)


def add_state(state_index, phn, meta):
    state_node = meta["graph"].nodes[state_index]
    if state_node.value != phn:
        meta["replaces"].append((len(meta["target"]), phn))
    meta["target"].append(state_node.value)


def traverse_tip(kind, state_index, meta):
    if kind == "tail":
        tip_indexes = [tail.index for tail in meta["graph"].tails]
    else:
        tip_indexes = [root.index for root in meta["graph"].roots]

    if state_index not in tip_indexes:
        closest_tip_index = None
        tip_distance = float("inf")

        for tip_index in tip_indexes:
            if kind == "tail":
                new_distance = meta["graph"].distance_matrix[state_index, tip_index]
            else:
                new_distance = meta["graph"].distance_matrix[tip_index, state_index]

            if new_distance < tip_distance:
                closest_tip_index = tip_index
                tip_distance = new_distance

        traverse_shortest_path(kind, closest_tip_index, state_index, meta)


def closest(phns, graph):
    emissions = to_emissions(phns, graph)
    with np.errstate(divide='ignore'):
        match = viterbi(
            np.log(emissions),
            np.log(graph.transition_matrix),
            np.log(graph.initial_transitions)
        )

    meta = {
        "inserts": [],
        "deletes": [],
        "replaces": [],
        "target": [],
        # Debug
        "phns": phns,
        "match": match,
        "graph": graph
    }

    traverse_tip("root", match[0], meta)
    add_state(match[0], phns[0], meta)

    for prev_phn_index in range(len(phns) - 1):
        orig_phn_index = prev_phn_index + 1

        if match[prev_phn_index] == match[orig_phn_index]:
            if graph.nodes[match[orig_phn_index]].value != phns[orig_phn_index]:
                meta["inserts"].append((len(meta["target"]), phns[orig_phn_index]))

        else:
            if graph.distance_matrix[match[prev_phn_index], match[orig_phn_index]] != 1:
                traverse_shortest_path("normal", prev_phn_index, orig_phn_index, meta)
            add_state(match[orig_phn_index], phns[orig_phn_index], meta)

    traverse_tip("tail", match[-1], meta)

    # TODO: Replace ins+del on same index with replace
    for ins_index, val in meta["inserts"]:
        for del_index, val in meta["deletes"]:
            if ins_index == del_index:
                print(meta)
                import ipdb
                ipdb.set_trace()

    # TODO: Add cer to meta

    # TODO: Remove graph from meta if not debug
    # del meta["graph"]

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

    return meta


# TODO: Move to graph modules
def to_emissions(phns, graph):
    emissions = np.full((len(phns), len(graph.nodes)), 0.5)

    indexes = {}
    for i, phn in enumerate(phns):
        if phn in indexes:
            indexes[phn].append(i)
        else:
            indexes[phn] = [i]

    for node in graph.nodes:
        if node.value in indexes:
            emissions[indexes[node.value], node.index] = 1

    return emissions
