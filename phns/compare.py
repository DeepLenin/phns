import numpy as np

from .utils.viterbi import viterbi


def closest(phns, graph, tensor_dict=None, threshold=1, ignore=["BLANK", "sil"]):
    """Finding closest target path in all available variants by provided logprobs or spoken phonemes

    Method does following:

    - Translate input (logprobs or phonemes) to emissions matrix
    - Run viterbi on emissions
    - Traverse through all pronounced phonemes by user to check their correctness
    - Find error rate

    Args:
        phns (np.array|List[String]): Logprobs matrix or spoken phonemes list
        graph (phns.Graph): Graph with all variants of target pronounciation
        tensor_dict (phns.utils.Dictionary): Object with phonemes mapping information
        ignore (List[String]): List of dictionary values to ignore when calculating errors
            Defaults to BLANK and sil
        threshold (float): Value from 0 to 1. Using to check if matched phoneme
            higher than this threshold to find errors

    Returns:
        meta (dict):
            - "inserts": extra phoneme errors
            - "deletes": missed phoneme errors
            - "replaces": combo of extra and missed phoneme error on same position
            - "target": matched target
            - "errors": amount of errors
            - "match": output of viterbi algorithm
            - "phns": input arg "phns"
            - "graph": input arg "graph"
            - "threshold": input arg "threshold"
            - "ignore": input arg "ignore"
            - "cer": error rate (total errors/matched target length)
            - "cmu_cer": error rate (total errors/graph length)
    """

    # Translate input (logprobs or phonemes) to emissions matrix
    orig_threshold = threshold
    threshold = np.log(threshold)
    if tensor_dict:  # logits with dimensions TxD (time step X dict)
        emissions = __tensor_to_emissions__(phns, graph, tensor_dict)
        # may be use not an argmax but taking into account previous immediate error
        # so we can compare to use with threshold
        phns = [tensor_dict.id_to_phn[code] for code in phns.argmax(axis=1)]
    else:
        emissions = np.log(__phns_to_emissions__(phns, graph))

    # Run viterbi on emissions
    with np.errstate(divide="ignore"):
        match = viterbi(
            emissions,
            np.log(graph.transition_matrix),
            np.log(graph.initial_transitions),
            np.log(graph.final_transitions),
        )

    meta = {
        "inserts": {},
        "deletes": {},
        "replaces": {},
        "target": [],
        "errors": 0,
        # Debug
        "phns": phns,
        "match": list(match),
        "graph": graph,
        "threshold": orig_threshold,
        "ignore": ignore,
    }

    # Check if person started not from beginning, adding all missed steps to errors and target
    __traverse_tip__("root", match[0], meta)
    # Check correctness of first matched state
    __check_step__(0, emissions, meta, "replaces")
    __append_step__(0, meta)

    # Traverse through all pronounced phonemes by user to check their correctness
    for prev_phn_index in range(len(phns) - 1):
        orig_phn_index = prev_phn_index + 1

        # # If same phoneme as in previous step matched - then user made a mistake
        # # Add it to "inserts" errors and we're staying on same step
        if match[prev_phn_index] == match[orig_phn_index]:
            __check_step__(orig_phn_index, emissions, meta, "inserts")
        else:
            # If distance from prev phoneme to current more than one through
            # graph - we need to find shortest path and add extra phonemes in
            # it to errors
            if graph.distance_matrix[match[prev_phn_index], match[orig_phn_index]] > 1:
                __traverse_shortest_path__(
                    "normal", match[prev_phn_index], match[orig_phn_index], meta
                )
            # Add state for current phoneme
            __check_step__(orig_phn_index, emissions, meta, "replaces")
            __append_step__(orig_phn_index, meta)

    # Check if user pronounced all needed phonemes by traversing (finding
    # shortest path) to tail from last match
    __traverse_tip__("tail", match[-1], meta)

    del meta["graph"]

    # Replace contiguous "deletes" and "inserts" errors into "replaces"
    for idx in meta["inserts"]:
        if idx in meta["deletes"]:
            del meta["deletes"][idx]
            phn = meta["inserts"][idx].pop()
            meta["replaces"][idx] = str(phn)
            meta["errors"] -= 1

    # Find error rate
    meta["cer"] = meta["errors"] / len(meta["target"])
    meta["cmu_cer"] = meta["errors"] / graph.max_length
    return meta


def __traverse_shortest_path__(kind, from_node_index, to_node_index, meta):
    graph = meta["graph"]
    start = graph.nodes[from_node_index]
    end = graph.nodes[to_node_index]
    if kind == "tail":
        start, end = end, start

    path = []
    predecessor = end
    while True:
        next_index = graph.shortest_paths[start.index, predecessor.index]
        if next_index == start.index:
            break
        predecessor = graph.nodes[next_index]
        path = [predecessor] + path

    if kind == "root":
        path = [start] + path
    elif kind == "tail":
        path.append(end)

    for node in path:
        meta["deletes"][len(meta["target"])] = str(node.value)
        meta["errors"] += 1
        meta["target"].append(str(node.value))


def __append_step__(step_index, meta):
    state_index = meta["match"][step_index]
    state_node = meta["graph"].nodes[state_index]
    meta["target"].append(str(state_node.value))


def __check_step__(step_index, emissions, meta, reason):
    state_index = meta["match"][step_index]
    argmax_phn = str(meta["phns"][step_index])
    state_phn = str(meta["graph"].nodes[state_index].value)
    state_logprob = emissions[step_index][state_index]

    if (
        state_logprob < meta["threshold"]
        and argmax_phn != state_phn
        and argmax_phn not in meta["ignore"]
    ):
        if reason == "inserts":
            meta[reason].setdefault(len(meta["target"]), []).append(argmax_phn)
        else:
            meta[reason][len(meta["target"])] = argmax_phn
        meta["errors"] += 1


def __traverse_tip__(kind, state_index, meta):
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

            if new_distance and new_distance < tip_distance:
                closest_tip_index = tip_index
                tip_distance = new_distance

        __traverse_shortest_path__(kind, closest_tip_index, state_index, meta)


def __tensor_to_emissions__(tensor, graph, tensor_dict):
    emissions = np.empty((tensor.shape[0], len(graph.nodes)), tensor.dtype)
    for i, node in enumerate(graph.nodes):
        emissions[:, i] = tensor[:, tensor_dict.phn_to_id[str(node.value)]]
    return emissions


# TODO: Move to graph modules
def __phns_to_emissions__(phns, graph):
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
