class Node:
    def __init__(self):
        self.edges = dict()

    def add_edge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight

    def del_edge(self, to):
        del self.edges[to]


class Graph:
    def __init__(self, adj_list):
        self.adj_list = adj_list
        self.nodes = []
        for i in range(len(adj_list)):
            curr_node = Node()
            for j in range(adj_list[i]):
                curr_node.add_edge(adj_list[i][j][0], adj_list[i][j][1])
            self.nodes.append(curr_node)
