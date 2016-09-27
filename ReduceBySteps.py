from functools import reduce


def gcdi(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def lcmu(a, b):
    return abs(a*b // gcdi(a, b))


def som(a, b):
    return a+b


def maxi(a, b):
    return max(a, b)


def mini(a, b):
    return min(a, b)


def oper_array(fct, arr, init):
    return [reduce(fct, arr[:i], init) for i in range(1, len(arr)+1)]
