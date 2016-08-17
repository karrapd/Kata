
class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = set()

    def append_neighbor(self, neighbor):
        self.neighbors.add(neighbor)
        neighbor.neighbors.add(self)

    def __hash__(self):
        return self.value

    def __repr__(self):
        return '%d' % self.value


def dfs(node, visited, indent):
    if node in visited:
        print('{}already visited {}'.format(indent, node))
        return

    # print current node
    print('{}visited = {}'.format(indent, visited))
    print('{}at {}'.format(indent, node))
    visited.add(node)

    # go down on me
    for n in node.neighbors:
        print('{}going on {}'.format(indent, n))
        dfs(n, visited, indent + '   ')

    print('{}done with {}'.format(indent, node))


def bfs(start_node):
    visited = set()
    q = [(start_node, '')]

    while len(q) > 0:
        # pop queue
        node, indent = q[0]
        print('{}queue = {}'.format(indent, [x[0] for x in q]))
        del q[0]

        if node in visited:
            print('{}already visited {}'.format(indent, node))
            continue

        # print current node
        print('{}visited = {}'.format(indent, visited))
        print('{}at {}'.format(indent, node))
        visited.add(node)

        # expand visiting frontier
        for n in node.neighbors:
            print('{}adding {}'.format(indent, n))
            q.append((n, indent + '   '))

        print('{}done with {}'.format(indent, node))


def main():
    n = [Node(i) for i in range(7)]
    n[0].append_neighbor(n[1])
    n[0].append_neighbor(n[2])
    n[0].append_neighbor(n[4])
    n[1].append_neighbor(n[3])
    n[2].append_neighbor(n[6])
    n[3].append_neighbor(n[5])
    n[3].append_neighbor(n[6])
    n[4].append_neighbor(n[5])
    n[5].append_neighbor(n[6])
    print('DFS:')
    dfs(n[0], set(), '')
    print('\n\nBFS:')
    bfs(n[0])


if __name__ == '__main__':
    main()
