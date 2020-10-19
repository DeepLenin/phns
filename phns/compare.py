import numpy as np
from diff_match_patch import diff_match_patch

from . import utils
from .utils.viterbi import viterbi


def closest(
    phns_or_logprobs,
    graph,
    tensor_dict=None,
    threshold=1,
    clip=0.01,
    ignore=["BLANK", "sil"],
    debug=False,
):
    """Finding closest target path in all available variants by provided logprobs or spoken phonemes

    Method does following:

    - Translate input (logprobs or phonemes) to emissions matrix
    - Run viterbi on emissions
    - Traverse through all pronounced phonemes by user to check their correctness
    - Find error rate

    Args:
        phns_or_logprobs (np.array|List[String]): Logprobs matrix or spoken phonemes list
        graph (phns.Graph): Graph with all variants of target pronounciation
        tensor_dict (phns.utils.Dictionary): Object with phonemes mapping information
        ignore (List[String]): List of dictionary values to ignore when calculating errors
            Defaults to BLANK and sil
        threshold (float): Value from 0 to 1. Using to check if matched phoneme
            higher than this threshold to find errors
        clip (float): Value from 0 to 1. Using to clip predictions from below.

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
            - "dmp_cer": error rate according to diff_match_patch
    """

    dmp = diff_match_patch()

    # Translate input (logprobs or phonemes) to emissions matrix
    log_threshold = np.log(threshold)
    if tensor_dict:  # logits with dimensions TxD (time step X dict)
        emissions = __tensor_to_emissions__(phns_or_logprobs, graph, tensor_dict)
        emissions = np.clip(emissions, np.log(clip), None)
        # may be use not an argmax but taking into account previous immediate error
        # so we can compare to use with threshold
        argmax_phns = [
            tensor_dict.id_to_phn[code] for code in phns_or_logprobs.argmax(axis=1)
        ]
    else:
        emissions = np.log(__phns_to_emissions__(phns_or_logprobs, graph))
        argmax_phns = phns_or_logprobs

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
        # private
        "match": match.tolist(),
        "argmax_phns": argmax_phns,
        "graph": graph,
        "threshold": threshold,
        "log_threshold": log_threshold,
        "ignore": ignore,
    }

    # Traverse through all pronounced phonemes by user to check their correctness
    prev_node_idx = None  # to ignore blanks/sil
    matched_targets = {}  # for correct error placement
    for step_idx in range(len(argmax_phns)):
        node_idx = meta["match"][step_idx]
        node = meta["graph"].nodes[node_idx]
        node_phn = str(node.value)
        node_logprob = emissions[step_idx][node_idx]
        argmax_phn = str(meta["argmax_phns"][step_idx])

        threshold_failed = node_logprob < meta["log_threshold"]
        match_failed = threshold_failed and argmax_phn != node_phn

        if threshold_failed and argmax_phn in meta["ignore"]:
            continue

        # Check if started not from beginning, adding all missed steps to errors and target
        if prev_node_idx is None:
            __traverse_tip__("root", node_idx, meta)
        # If distance from prev phoneme to current more than one through
        # graph - we need to find shortest path and add extra phonemes in
        # it to errors
        elif graph.distance_matrix[prev_node_idx, node_idx] > 1:
            __traverse_shortest_path__("normal", prev_node_idx, node_idx, meta)

        if prev_node_idx != node_idx:
            meta["target"].append(node_phn)

        target_position = len(meta["target"]) - 1
        if not match_failed and target_position not in matched_targets:
            matched_targets[target_position] = step_idx
        prev_node_idx = node_idx

        error_position = target_position + 1
        if target_position not in matched_targets:
            error_position -= 1

        inserts = meta["inserts"].get(error_position, [])
        if match_failed or (target_position in matched_targets and inserts):
            # to prevent accumulating the same error in inserts
            if not inserts or inserts[-1] != argmax_phn:
                inserts.append(argmax_phn)
                meta["inserts"][error_position] = inserts
                meta["errors"] += 1

    # Check if user pronounced all needed phonemes by traversing (finding
    # shortest path) to tail from last match
    __traverse_tip__("tail", prev_node_idx, meta)

    if tensor_dict:
        meta["preds"] = __get_preds__(emissions, meta)
        meta["single_char_target"] = utils.single_char_encode(meta["target"])
        meta["single_char_preds"] = utils.single_char_encode(meta["preds"])
        meta["dmp_diff"] = dmp.diff_main(
            meta["single_char_target"], meta["single_char_preds"]
        )
        meta["dmp_errors"] = dmp.diff_levenshtein(meta["dmp_diff"])

    meta["matched_targets"] = matched_targets
    if not debug:
        keep_keys = ["inserts", "deletes", "replaces", "target", "errors", "dmp_errors"]
        for key in list(meta.keys()):
            if key not in keep_keys:
                del meta[key]

    idxs_to_clean = []
    target_len = len(meta["target"])
    for idx in meta["inserts"]:
        if idx in meta["deletes"] or (idx not in matched_targets and idx < target_len):
            if idx in meta["deletes"]:
                del meta["deletes"][idx]
                meta["errors"] -= 1
            idxs_to_clean.append(idx)
            meta["replaces"][idx] = meta["inserts"][idx]

    for idx in idxs_to_clean:
        del meta["inserts"][idx]

    # Find error rate
    meta["cer"] = meta["errors"] / len(meta["target"])
    meta["cmu_cer"] = meta["errors"] / graph.max_length
    if tensor_dict:
        meta["dmp_cer"] = meta["dmp_errors"] / graph.max_length
    return meta


def __get_preds__(logprobs, meta):
    result = []
    for step_idx, (step_logprobs, matched) in enumerate(zip(logprobs, meta["match"])):
        if step_logprobs[matched] < meta["log_threshold"]:
            result.append(meta["argmax_phns"][step_idx])
        else:
            result.append(str(meta["graph"].nodes[matched].value))
    result = [phn for phn in result if phn not in meta["ignore"]]
    result = utils.remove_doubles(result)
    return result


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


def __traverse_tip__(kind, state_index, meta):
    if kind == "tail":
        tip_indexes = [tail.index for tail in meta["graph"].tails]
    else:
        tip_indexes = [root.index for root in meta["graph"].roots]

    if state_index and state_index not in tip_indexes:
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


def __tensor_to_emissions__(logprobs, graph, tensor_dict):
    emissions = np.empty((logprobs.shape[0], len(graph.nodes)), logprobs.dtype)
    for i, node in enumerate(graph.nodes):
        emissions[:, i] = logprobs[:, tensor_dict.phn_to_id[str(node.value)]]
    return emissions


# TODO: Move to graph modules
def __phns_to_emissions__(spoken_phns, graph):
    emissions = np.full((len(spoken_phns), len(graph.nodes)), 0.5)

    indexes = {}
    for i, phn in enumerate(spoken_phns):
        if phn in indexes:
            indexes[phn].append(i)
        else:
            indexes[phn] = [i]

    for node in graph.nodes:
        if node.value in indexes:
            emissions[indexes[node.value], node.index] = 1

    return emissions
