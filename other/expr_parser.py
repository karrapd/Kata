
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


def build_tree(tokens):
    if len(tokens) == 1:
        return ConstNode(float(tokens[0]))

    prios = [get_priority(t) for t in tokens]
    min_pos, _ = min(enumerate(prios), key=lambda x: x[1])
    left = build_tree(tokens[:min_pos])
    right = build_tree(tokens[min_pos+1:])
    return OpNode(tokens[min_pos], left, right)


def print_tree(root, indent=''):
    if type(root) is OpNode:
        print('{}{}'.format(indent, root.op))
        print_tree(root.left, indent + '   ')
        print_tree(root.right, indent + '   ')
        return

    print('{}{}'.format(indent, root.value))


def main():
    tokens = tokenize(sys.argv[1])
    print(tokens)
    root = build_tree(tokens)
    print_tree(root)
    print('result = {:.5f}'.format(root.eval()))


if __name__ == '__main__':
    main()
