
import sys
import re


class _Node:
    def eval(self):
        raise NotImplemented('abstract method')

    def dump(self, indent):
        raise NotImplemented('abstract method')


class _OpNode(_Node):
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

    def dump(self, indent=0):
        left = self.left.dump(indent+1)
        right = self.right.dump(indent+1)
        return '{}{}\n{}\n{}'.format('  '*indent, self.op, left, right)


class _ConstNode(_Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def dump(self, indent=0):
        return '{}{}'.format('  '*indent, self.value)


class ExpressionTree:
    __PRIORITIES = {
        '+': 1,  '-': 1,
        '/': 10, '*': 10,
    }

    def __init__(self, expr):
        self.__root = self.__build(expr)

    def __tokenize(self, expr):
        return re.findall(r'(?:\d|\.)+|\*|\+|-|/', expr)

    def __parse(self, tokens):
        # assuming expressions are always valid, if there's just one elem, it must be a constant
        if len(tokens) == 1:
            return _ConstNode(float(tokens[0]))

        prios = [self.__PRIORITIES.get(t, 1000) for t in tokens]
        min_pos, _ = min(enumerate(prios), key=lambda x: x[1])

        return _OpNode(
            tokens[min_pos],
            self.__parse(tokens[:min_pos]),
            self.__parse(tokens[min_pos+1:])
        )

    def __build(self, expr):
        tokens = self.__tokenize(expr)
        return self.__parse(tokens)

    def eval(self):
        return self.__root.eval()

    def __str__(self):
        return self.__root.dump()


def main():
    tree = ExpressionTree(sys.argv[1])
    print('TREE:\n{}'.format(tree))
    print('result = {:.5f}'.format(tree.eval()))


if __name__ == '__main__':
    main()
