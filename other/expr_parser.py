
import sys
import math


class ExprException(Exception):
    pass


class _Node:
    def copy(self):
        raise NotImplemented('abstract method')

    def eval(self):
        raise NotImplemented('abstract method')

    def differentiate(self):
        raise NotImplemented('abstract method')

    def dump(self, indent):
        raise NotImplemented('abstract method')


class _OpNode(_Node):
    __OPS = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x/y,
        '^': lambda x, y: x**y
    }

    def __init__(self, op, left, right):
        self.op = op
        self.func = self.__OPS[op]
        self.left = left
        self.right = right

    def eval(self):
        return self.func(self.left.eval(), self.right.eval())

    def copy(self):
        return _OpNode(self.op, self.left.copy(), self.right.copy())

    def differentiate(self):
        if self.op == '+':
            return _OpNode('+', self.left.differentiate(), self.right.differentiate())
        elif self.op == '-':
            return _OpNode('-', self.left.differentiate(), self.right.differentiate())
        elif self.op == '*':
            return _OpNode(
                '+',
                _OpNode('*', self.left.differentiate(), self.right.copy()),
                _OpNode('*', self.left.copy(), self.right.differentiate())
            )
        elif self.op == '/':
            return _OpNode(
               '/',
               _OpNode(
                    '-',
                    _OpNode('*', self.left.differentiate(), self.right.copy()),
                    _OpNode('*', self.left.copy(), self.right.differentiate())
                ),
               _OpNode('*', self.right.copy(), self.right.copy())
            )
        elif self.op == '^':
            return _OpNode(
                '*',
                _OpNode('^', self.left.copy(), self.right.copy()),
                _OpNode(
                    '+',
                    _OpNode(
                        '*',
                        self.right.differentiate(),
                        _FuncNode('log', [self.left.copy(), _ConstNode(math.e)])
                    ),
                    _OpNode(
                        '/',
                        _OpNode('*', self.right.copy(), self.left.differentiate()),
                        self.left.copy()
                    )
                )
            )

    def dump(self, indent=0):
        left = self.left.dump(indent+1)
        right = self.right.dump(indent+1)
        return '{}{}\n{}\n{}'.format('  '*indent, self.op, left, right)


class _ConstNode(_Node):
    def __init__(self, value):
        self.value = value

    def copy(self):
        return _ConstNode(self.value)

    def eval(self):
        return self.value

    def differentiate(self):
        return _ConstNode(0)

    def dump(self, indent=0):
        return '{}{}'.format('  '*indent, self.value)


class _FuncNode(_Node):
    FUNCTIONS = {
        'sin': lambda x: math.sin(x),
        'cos': lambda x: math.cos(x),
        'tan': lambda x: math.tan(x),
        'exp': lambda x: math.exp(x),
        'log': lambda x, y: math.log(x, y)
    }

    def __init__(self, func_name, children):
        self.func_name = func_name
        self.func = self.FUNCTIONS[func_name]
        self.children = children

    def copy(self):
        return _FuncNode(self.func_name, [c.copy() for c in self.children])

    def eval(self):
        try:
            return self.func(*[c.eval() for c in self.children])
        except TypeError:
            raise ExprException('{}: function arity is wrong'.format(self.func_name))

    def differentiate(self):
        if self.func_name == 'sin':
            return _FuncNode('cos', [c.differentiate() for c in self.children])
        elif self.func_name == 'cos':
            return _OpNode(
                '-',
                _ConstNode(0),
                _FuncNode('sin', [c.differentiate() for c in self.children])
            )
        elif self.func_name == 'tan':
            return _OpNode(
                '/',
                _ConstNode(1),
                _OpNode(
                    '^',
                    _FuncNode('cos', [c.differentiate() for c in self.children]),
                    _ConstNode(2)
                )
            )
        elif self.func_name == 'exp':
            return _OpNode(
                '*',
                _FuncNode('exp', [c.differentiate() for c in self.children]),
                self.children[0].differentiate()
            )
        elif self.func_name == 'log':
            return _OpNode(
                '/',
                _OpNode(
                    '-',
                    _OpNode(
                        '*',
                        _FuncNode('log', [self.children[1].copy(), _ConstNode(math.e)]),
                        _OpNode(
                            '/',
                            self.children[0].differentiate(),
                            self.children[0].copy()
                        )
                    ),
                    _OpNode(
                        '*',
                        _FuncNode('log', [self.children[0].copy(), _ConstNode(math.e)]),
                        _OpNode(
                            '/',
                            self.children[1].differentiate(),
                            self.children[1].copy()
                        )
                    )
                ),
                _OpNode(
                    '^',
                    _FuncNode('log', [self.children[1].copy(), _ConstNode(math.e)]),
                    _ConstNode(2)
                )
            )

    def dump(self, indent=0):
        return '{}{}()\n{}'.format(
            '  ' * indent,
            self.func_name,
            '\n'.join(c.dump(indent+1) for c in self.children)
        )


class _VarNode(_Node):
    def __init__(self, variable):
        self.variable = variable

    def copy(self):
        return _VarNode(self.variable)

    def eval(self):
        return float(input('Who is %s: ' % self.variable))

    def differentiate(self):
        if self.variable == 'x':
            return _ConstNode(1)
        return _ConstNode(0)

    def dump(self, indent=0):
        return '{}{}'.format('  '*indent, self.variable)


class ExpressionTree:
    __PRIORITIES = {
        '+': 1,  '-': 1,
        '/': 10, '*': 10,
        '^': 20
    }
    __PAREN_OFFSETS = {
        '(': 50,
        ')': -50
    }
    __KNOWN_CONSTANTS = {
        'pi': math.pi,
        'e': math.e
    }

    def __init__(self, expr):
        if isinstance(expr, _Node):
            self.__root = expr
        else:
            self.__root = self.__build(expr)

    def __tokenize(self, expr):
        state = 'none'
        tokens = []
        token_start = 0

        for i in range(len(expr)):
            c = expr[i]
            if c.isdigit() or c == '.':
                if state != 'number':
                    # append the the char we've seen so far
                    tokens.append(expr[token_start:i])
                    token_start = i
                state = 'number'
            elif c in '+-*/^':
                if state != 'operator':
                    # append the the char we've seen so far
                    tokens.append(expr[token_start:i])
                    token_start = i
                state = 'operator'
            elif c in '(),':
                # append the the char we've seen so far
                tokens.append(expr[token_start:i])
                token_start = i
                state = 'paren'
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

    def __get_priorities(self, tokens):
        prios = []
        prio_offset = 0

        for t in tokens:
            prio_offset += self.__PAREN_OFFSETS.get(t, 0)
            prios.append(prio_offset + self.__PRIORITIES.get(t, 1000))

        return prios

    def __filter_parens(self, tokens, priorities):
        '''
        If tokens contain functions, determine arity.
        Filter out any parens along with the priorities in respective positions.
        Returns: (filtered_tokens, filtered_priorities)
        '''
        tokens_list = []
        priorities_list = []
        for i in range(len(tokens)):
            paren_count = 1
            token_count = 0
            if tokens[i] in _FuncNode.FUNCTIONS:
                for j in range(i+2, len(tokens)):
                    if tokens[j] == '(':
                        paren_count += 1
                    elif tokens[j] == ')':
                        paren_count -= 1
                    else:
                        token_count += 1
                    if paren_count == 0:
                        break
                tokens[i] = '{}_{}'.format(tokens[i], token_count)
            if tokens[i] not in '()':
                tokens_list.append(tokens[i])
                priorities_list.append(priorities[i])

        return (tokens_list, priorities_list)

    def __parse(self, tokens, priorities):
        # assuming expressions are always valid, if there's just one elem, it
        # must be a constant
        tok_parts = tokens[0].split('_')
        if len(tokens) == 1:
            if tokens[0].isdigit():
                return _ConstNode(float(tokens[0]))
            elif tokens[0] in self.__KNOWN_CONSTANTS:
                return _ConstNode(self.__KNOWN_CONSTANTS.get(tokens[0]))
            return _VarNode(tokens[0])
        elif tok_parts[0] in _FuncNode.FUNCTIONS and len(tokens) == 1 + int(tok_parts[1]):
            # split tokens by ',' and then send children as params for FuncNode
            children = []

            last_comma = 1
            # NOTE: should not do this as a general practice
            tokens.append(',')
            i = 1
            while i < len(tokens):
                tok_parts2 = tokens[i].split('_')
                if tok_parts2[0] in _FuncNode.FUNCTIONS:
                    i += int(tok_parts2[1]) + 1

                if tokens[i] == ',':
                    children.append(self.__parse(tokens[last_comma:i], priorities[last_comma:i]))
                    last_comma = i+1

                i += 1

            return _FuncNode(tok_parts[0], children)

        min_pos = 0
        min_val = 2**32
        i = 0
        while i < len(tokens):
            tok_parts = tokens[i].split('_')
            if tok_parts[0] in _FuncNode.FUNCTIONS:
                i += int(tok_parts[1])

            if priorities[i] < min_val:
                min_val = priorities[i]
                min_pos = i
            i += 1

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

    def differentiate(self):
        return ExpressionTree(self.__root.differentiate())

    def __str__(self):
        return self.__root.dump()


def main():
    tree = ExpressionTree(sys.argv[1])
    print('TREE:\n{}'.format(tree))
    diff_tree = tree.differentiate()
    print('differentiate_TREE: \n{}'.format(diff_tree))
    print('result = {:.5f}'.format(diff_tree.eval()))


if __name__ == '__main__':
    main()