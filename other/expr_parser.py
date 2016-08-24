
import sys
import math


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


class _VarNode(_Node):
    __KNOWN_CONSTANTS = {
        'pi': math.pi,
        'e': math.e
    }

    def __init__(self, variable):
        self.variable = variable

        if self.variable in self.__KNOWN_CONSTANTS:
            self.value = self.__KNOWN_CONSTANTS.get(self.variable)
        else:
            self.value = float(raw_input('Who is %s: ' % self.variable))

    def eval(self):
        return self.value

    def dump(self, indent=0):
        return '{}{}'.format('  '*indent, self.value)


class ExpressionTree:
    __PRIORITIES = {
        '+': 1,  '-': 1,
        '/': 10, '*': 10
    }
    __PAREN_OFFSETS = {
        '(': 50,
        ')': -50
    }

    def __init__(self, expr):
        self.__root = self.__build(expr)

    def __tokenize(self, expr):
        state = 'none'
        tokens = []
        token_start = 0
        print expr

        for i, c in enumerate(expr):
            if c.isdigit() or c == '.':
                if state != 'number':
                    # append the the char we've seen so far
                    tokens.append(expr[token_start:i])
                    token_start = i
                state = 'number'
            elif c in '+-*/':
                if state != 'operator':
                    # append the the char we've seen so far
                    tokens.append(expr[token_start:i])
                    token_start = i
                state = 'operator'
            elif c in '()':
                if state != 'paren':
                    # append the the char we've seen so far
                    tokens.append(expr[token_start:i])
                    token_start = i
            elif c.isalpha():
                if state != 'alpha':
                    # append the the char we've seen so far
                    tokens.append(expr[token_start:i])
                    token_start = i
                state = 'alpha'
            else:
                raise Exception('something went wrong')

        # for the first element in tokens, both 'token_start' and 'i' have the same value, 0
        # this is why the first element that is appended to tokens is expr[0:0] = '', which we are deleting below
        del tokens[0]

        if token_start != len(expr):
            tokens.append(expr[token_start:])

        return tokens
        # return re.findall(r'(?:\d|\.)+|\*|\+|-|/|\)|\(', expr)

    def __get_priorities(self, tokens):
        prios = []
        prio_offset = 0

        for t in tokens:
            prio_offset += self.__PAREN_OFFSETS.get(t, 0)
            prios.append(prio_offset + self.__PRIORITIES.get(t, 1000))

        return prios

    def __filter_parens(self, tokens, priorities):
        '''
            Filter out any parens along with the priorities in respective positions.
            Returns: (filtered_tokens, filtered_priorities)
        '''
        return list(zip(*[(t, p) for t, p in zip(tokens, priorities) if t not in '()']))

    def __parse(self, tokens, priorities):

        # assuming expressions are always valid, if there's just one elem, it must be a constant
        if len(tokens) == 1:
            if tokens[0].isdigit():
                return _ConstNode(float(tokens[0]))
            else:
                return _VarNode(tokens[0])

        min_pos, _ = min(enumerate(priorities), key=lambda x: x[1])

        return _OpNode(
            tokens[min_pos],
            self.__parse(tokens[:min_pos], priorities[:min_pos]),
            self.__parse(tokens[min_pos+1:], priorities[min_pos+1:])
        )

    def __build(self, expr):
        tokens = self.__tokenize(expr)
        prios = self.__get_priorities(tokens)

        return self.__parse(*self.__filter_parens(tokens, prios))

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