import itertools


def choose_best_sum(t, k, ls):
    possible_options = []
    for subset in itertools.combinations(ls, k):
        sum = 0
        for element in subset:
            sum += element
        if t-sum >= 0:
            possible_options.append(sum)
    if len(possible_options) > 0:
        return sorted(possible_options)[-1]
    return None