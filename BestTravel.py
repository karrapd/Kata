import itertools


def choose_best_sum(t, k, ls):
    possible_options = []
    for subset in itertools.combinations(ls, k):
        s = sum(subset)
        if s <= t:
            possible_options.append(s)
    if len(possible_options) > 0:
        return sorted(possible_options)[-1]
    return None
