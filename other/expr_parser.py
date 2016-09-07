
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


class _FuncNode(_Node):
    FUNCTIONS = {
        'sin': lambda x: math.sin(x),
        'cos': lambda x: math.cos(x),
        'tan': lambda x: math.tan(x),
        'exp': lambda x: math.exp(x)
    }

    def __init__(self, func_name, child):
        self.func_name = func_name
        self.func = self.FUNCTIONS[func_name]
        self.child = child

    def eval(self):
        return self.func(self.child.eval())

    def dump(self, indent=0):
        return '{}{}()\n{}'.format('  ' * indent, self.func_name, self.child.dump(indent+1))


class _VarNode(_Node):
    def __init__(self, variable):
        self.variable = variable

    def eval(self):
        return float(raw_input('Who is %s: ' % self.variable))

    def dump(self, indent=0):
        return '{}{}'.format('  '*indent, self.variable)


class ExpressionTree:
    __PRIORITIES = {
        '+': 1,  '-': 1,
        '/': 10, '*': 10
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
            elif c in '+-*/':
                if state != 'operator':
                    # append the the char we've seen so far
                    tokens.append(expr[token_start:i])
                    token_start = i
                state = 'operator'
            elif c in '()':
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
        Filter out any parens along with the priorities in respective positions.
        Returns: (filtered_tokens, filtered_priorities)
        '''
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
                        token_count +=1
                    if paren_count == 0:
                        break
                tokens[i] = '{}_{}'.format(tokens[i], token_count)

        # TODO: optimize this by including in the prev for -ae
        return list(zip(*[(t, p) for t, p in zip(tokens, priorities) if t not in '()']))

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
            return _FuncNode(tok_parts[0], self.__parse(tokens[1:], priorities[1:]))

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
        print self.__filter_parens(tokens, prios)
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