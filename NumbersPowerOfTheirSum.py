global_list = []


def build_list():
    global global_list
    for number in range(2, 500):
        for power in range(2, 50):
            test_power = number ** power
            sum = 0
            sum_gen = test_power
            while sum_gen > 0:
                sum += sum_gen % 10
                sum_gen //= 10
            if sum == number:
                global_list.append(test_power)
    print sorted(global_list)

build_list()
global_list = sorted(global_list)


def power_sumDigTerm(n):
    return global_list[n-1]