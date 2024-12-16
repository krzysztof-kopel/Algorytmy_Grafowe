from graph_input import load_graph


class Node:
    def __init__(self, number):
        self.number = number
        self.edges = dict()
        self.inactive = False

    def del_edge(self, to):
        if to in self.edges.keys():
            del self.edges[to]


class Graph:
    def __init__(self, adj_list):
        self.adj_list = adj_list
        self.nodes = []
        self.size = 0
        for i in range(len(adj_list)):
            new_node = Node(i)
            self.nodes.append(new_node)
        for i in range(len(adj_list)):
            for j in range(len(adj_list[i])):
                self.add_edge(i, adj_list[i][j][0], adj_list[i][j][1], True)

        self.rank = len(adj_list)
        self.org_rank = self.rank

    def display_graph(self):
        print(f"Rozmiar: {int(self.size)}\nRząd: {self.rank}")
        for node in self.nodes:
            print(f"Wierzchołek numer {node.number}: ", end="")
            for neighbour in node.edges.items():
                print(f"{neighbour[0]}({neighbour[1]}) ", end=" ")
            if node.inactive:
                print("(Nieaktywny)", end="")
            print()
        print()


    def merge_vertices(self, x, y):
        self.nodes[x].del_edge(y)
        vertex_y = self.nodes[y]
        for edge in list(vertex_y.edges.items()):
            if edge[0] != x:
                self.add_edge(x, edge[0], edge[1], False)
                self.nodes[edge[0]].del_edge(y)
            vertex_y.del_edge(edge[0])
            self.size -= 1
        vertex_y.inactive = True
        self.rank -= 1

    def add_edge(self, start, to, weight, directed):
        start_node = self.nodes[start]
        to_node = self.nodes[to]
        start_node.edges[to] = start_node.edges.get(to, 0) + weight
        if not directed:
            to_node.edges[start] = to_node.edges.get(start, 0) + weight
        self.size += 1


if __name__ == "__main__":
    from graph_input import to_adjacency_list, load_graph
    adj_list = to_adjacency_list(*load_graph("path", "grafowe\\lab3\\graphs-lab3"))
    graph = Graph(adj_list)
    graph.display_graph()
    graph.add_edge(0,5, 4, False)
    graph.display_graph()
    graph.merge_vertices(0, 5)
    graph.display_graph()
