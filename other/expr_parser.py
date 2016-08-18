
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
        '/': 10, '*': 10
    }

    def __init__(self, expr):
        self.__root = self.__build(expr)

    def __tokenize(self, expr):
        return re.findall(r'(?:\d|\.)+|\*|\+|-|/|\)|\(', expr)

    def __assign_priorities(self, tokens):

        prios = []
        noparen_tokens = []
        prio_offset = 0

        for t in tokens:
            if t == '(':
                prio_offset += 50
            elif t == ')':
                prio_offset -= 50
            else:
                prios.append(prio_offset + self.__PRIORITIES.get(t, 1000))
                noparen_tokens.append(t)

        return zip(noparen_tokens, prios)

    def __parse(self, toks_prios):
        # assuming expressions are always valid, if there's just one elem, it must be a constant
        if len(toks_prios) == 1:
            return _ConstNode(float(toks_prios[0][0]))

        min_pos, _ = min(enumerate(toks_prios), key=lambda x: x[1][1])

        return _OpNode(
            toks_prios[min_pos][0],
            self.__parse(toks_prios[:min_pos]),
            self.__parse(toks_prios[min_pos + 1:])
        )

    def __build(self, expr):
        tokens = self.__tokenize(expr)
        tokens_prios = self.__assign_priorities(tokens)
        print tokens_prios
        return self.__parse(tokens_prios)

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
