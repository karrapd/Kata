# If you reverse the word emirp you will have the word prime.
# That idea is related with the purpose of this kata.
# We should select all the primes that when reversed are a different prime.
# The palindromic primes should be discarded.
# E.G: 13, 17 are prime numbers and the reversed respectively are 31, 71 which are also primes, so 13 and 17 are emirps
# But see the cases, 757, 787, 797, these are palindromic primes, so they do not enter in the sequence.
# Return: [number of emirps bellow n, largest emirp smaller than n, sum of all the emirps of the sequence bellow n]


class Emirps(object):

    def __init__(self, n):
        self.n = n

    def __is_prime(self, number):
        if number % 2 == 0 and number > 2:
            return False
        for i in range(3, int(number**0.5) + 1, 2):
            if number % i == 0:
                return False
        return True

    def __generate_primes(self):
        dict = {}
        primes = 2
        while primes < self.n:
            if primes not in dict:
                yield primes
                dict[primes * primes] = [primes]
            else:
                for num in dict[primes]:
                    dict.setdefault(num + primes, []).append(num)
                del dict[primes]
            primes += 1

    def __list_primes(self):
        return [x for x in list(self.__generate_primes())
                if self.__is_prime(int(str(x)[::-1])) and int(str(x)[::-1]) != x]

    def find_emirp(self):
        final_list = []
        primes_list = self.__list_primes()
        for element in primes_list:
            if element > self.n:
                break
            final_list.append(element)
        if final_list:
            return [len(final_list), sorted(final_list)[-1], sum(final_list)]
        return [0, 0, 0]

emirp = Emirps(500000)
print emirp.find_emirp()
