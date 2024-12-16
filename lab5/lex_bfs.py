from node_class import Node
from graph_input import load_graph

def partition_set(node_set: set[int], vertex: Node):
    # Funkcja dzieli node_set na set tych wierzchołków, które nie sąsiadują z vertex i set tych, które sąsiadują, po
    # czym zwraca je w tej kolejności.
    neighbor_set = set()
    foreign_set = set()
    while len(node_set) != 0:
        next_node = node_set.pop()
        if next_node in vertex.out:
            neighbor_set.add(next_node)
        else:
            foreign_set.add(next_node)
    return foreign_set, neighbor_set


def lex_bfs(graph: list[Node], start_index=0) -> list[Node]:
    # Wersja o najgorszej złożoności obliczeniowej

    # node_sets -> lista zbiorów, gdzie każdy zbiór zawiera wierzchołki mające takie same (leksykograficznie) zbiory poprzedników
    result_ordering = []
    node_sets = [set(), {start_index}]
    for node in graph:
        if node.idx != start_index:
            node_sets[0].add(node.idx)

    while len(node_sets) != 0:
        current_node = node_sets[-1].pop()
        result_ordering.append(current_node)
        new_node_sets_list = []
        if len(node_sets[-1]) == 0:
            node_sets.pop()

        for i in range(len(node_sets)):
            set_1, set_2 = partition_set(node_sets[i], graph[current_node])
            if len(set_1) != 0:
                new_node_sets_list.append(set_1)
            if len(set_2) != 0:
                new_node_sets_list.append(set_2)

        node_sets = new_node_sets_list

    return result_ordering


def check_lex_bfs(graph, vs):
    n = len(graph)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n - 1):
        ni = graph[vs[i]].out
        for j in range(i + 1, n):
            nj = graph[vs[j]].out

            conflicting = [pi[v] for v in nj - ni if pi[v] < i]
            if conflicting:
                viable = [pi[v] for v in ni - nj]
                if not viable or min(conflicting) <= min(viable):
                    return False

    return True


if __name__ == "__main__":
    graph_name = input("Podaj nazwę pliku z grafem: ")
    rank, edges = load_graph(graph_name, "lab5\\graphs-lab5\\chordal")
    graph = [Node(i) for i in range(rank)]
    for (u, v, _) in edges:
        graph[u - 1].connect_to(v - 1)
        graph[v - 1].connect_to(u - 1)
    lex_bfs_ordering = lex_bfs(graph)
    print(lex_bfs_ordering)
    print(check_lex_bfs(graph, lex_bfs_ordering))
