import numpy as np


def viterbi(emissions, transitions, initial=0):
    """Implements viterbi algorithm search

    https://en.wikipedia.org/wiki/Viterbi_algorithm

    Args:
        emissions (np.array): Emission matrix with probabilities of observings
            in states
        transitions (np.array): Matrix of transition probabilites from state i to j
        initial (np.array): Vector of initial probabilities

    Returns:
        List of indexes of matched states
    """
    steps_n, states_n = emissions.shape
    scores = np.empty((steps_n, states_n), "float64")
    backtrack = np.empty((steps_n, states_n), "int32")

    scores[0, :] = emissions[0, :] + initial
    backtrack[0, :] = 0

    for i in range(1, steps_n):
        scored_transitions = scores[i - 1, :] + transitions.T
        scores[i, :] = np.max(scored_transitions, 1) + emissions[i, :]
        backtrack[i, :] = np.argmax(scored_transitions, 1)

    match = np.empty(steps_n, "int32")
    match[-1] = np.argmax(scores[steps_n - 1, :])
    for i in reversed(range(1, steps_n)):
        match[i - 1] = backtrack[i, match[i]]

    return match
