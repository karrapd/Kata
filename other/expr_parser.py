
import sys
import re


class Node:
    def eval(self):
        raise NotImplemented('abstract method')


class OpNode(Node):
    __OPS = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x/y
    }

    def __init__(self, op, left, right):
        self.op = op
        self.func = self.__OPS[op]
        self.left = left
        self.right = right

    def eval(self):
        return self.func(self.left.eval(), self.right.eval())


class ConstNode(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


def tokenize(expr):
    return re.findall(r'(?:\d|\.)+|\*|\+|-|/', expr)


def get_priority(token):
    priorities = {
        '+': 1,
        '-': 1,
        '/': 10,
        '*': 10,
    }
    if token in priorities:
        return priorities[token]
    return 1000


def main():
    tokens = tokenize(sys.argv[1])
    print(tokens)


if __name__ == '__main__':
    main()
