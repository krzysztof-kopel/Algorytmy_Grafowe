from queue import PriorityQueue
from data import runtests

class Node:
  def __init__(self, idx, weight=0):
    self.idx = idx
    self.out = dict()
    self.weight = weight # Używane tylko, gdy Node jest wierzchołkiem grafu konfliktów
    self.temp_weight = weight
    self.color = None

  def connect_to(self, v, weight=0):
    self.out[v] = weight


def to_adjacency_list(vertex_number, edges):
    adj_list = [[] for _ in range(vertex_number)]
    for edge in edges:
        added_edge = (edge[1] - 1, edge[2])
        adj_list[edge[0] - 1].append(added_edge)

        added_edge = (edge[0] - 1, edge[2])
        adj_list[edge[1] - 1].append(added_edge)

    return adj_list

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

def lex_bfs(graph: list[Node], start_index=0) -> list[int]:
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

def prim(graph: list[list[int]], start_index: int=0) -> set[tuple[int, int, int]]:
    # queue: (weight, edge_to, edge_from)
    queue = PriorityQueue()
    queue.put((0, start_index, None))
    edges_in_mst = set()
    visited = set()

    while len(edges_in_mst) < len(graph) - 1:
        weight, edge_to, edge_from = queue.get()
        if edge_to in visited:
            continue
        visited.add(edge_to)

        if edge_from is not None:
            edges_in_mst.add((edge_from, edge_to, weight))
        for destination, destination_weight in graph[edge_to]:
            if destination not in visited:
                queue.put((destination_weight, destination, edge_to))

    return edges_in_mst


def find_lords_subtrees(lords: list[list[int]], graph: list[Node]) -> list[tuple[set[int], int]]:
    result = []

    node_edges = [set() for _ in range(len(graph))]

    visited = set()

    start = 0
    for i in range(len(graph)):
        if len(graph[i].out) == 1:
            start = i

    def dfs(current: int):
        neighbours_list = list(graph[current].out)
        for neigh in neighbours_list:
            if neigh in visited:
                continue
            visited.add(neigh)
            node_edges[neigh].update(node_edges[current])
            node_edges[neigh].add((current, neigh, graph[current].out[neigh]))
            dfs(neigh)

    dfs(start)
    for i in range(len(lords)):
        lord = lords[i]
        lord_edges_sum = set()
        lord_edges_intersect = None
        for vertex in lord:
            lord_edges_sum.update(node_edges[vertex])
            if lord_edges_intersect is None:
                lord_edges_intersect = node_edges[vertex]
            else:
                lord_edges_intersect &= node_edges[vertex]

        lord_edges = list(lord_edges_sum - lord_edges_intersect)
        lord_sum = sum(map(lambda edge: edge[2], lord_edges))
        lord_set = set()
        for start, end, _ in lord_edges:
            lord_set.add(start)
            lord_set.add(end)
        result.append((lord_set, lord_sum))

    return result


def color_graph(graph: list[Node], ordering: list[int]):

    for index in ordering:
        node = graph[index]
        if node.temp_weight > 0:
            graph[index].color = 'red'

            for neighbor_idx in node.out:
                if ordering.index(neighbor_idx) < ordering.index(index):
                    continue
                graph[neighbor_idx].temp_weight -= node.temp_weight

    for index in reversed(ordering):
        node = graph[index]
        if node.color == 'red' and all(graph[i].color != 'blue' for i in node.out):
            node.color = 'blue'


# noinspection PyPep8Naming
def my_solve(N, streets, lords):
    for i in range(len(lords)):
        for j in range(len(lords[i])):
            lords[i][j] -= 1

    graph = to_adjacency_list(N, streets)

    mst_edges = prim(graph)
    graph = [Node(i) for i in range(N)]
    for edge_from, edge_to, weight in mst_edges:
        graph[edge_from].connect_to(edge_to, weight)
        graph[edge_to].connect_to(edge_from, weight)

    conflict_graph = [Node(i) for i in range(len(lords))]
    lords_data = find_lords_subtrees(lords, graph)
    for i in range(len(conflict_graph)):
        conflict_graph[i].weight = lords_data[i][1]
        conflict_graph[i].temp_weight = lords_data[i][1]
        for j in range(i + 1, len(conflict_graph)):
            if len(lords_data[i][0] & lords_data[j][0]) > 0:
                conflict_graph[i].connect_to(j)
                conflict_graph[j].connect_to(i)

    perfect_elimination_ordering = lex_bfs(conflict_graph)

    color_graph(conflict_graph, perfect_elimination_ordering[::-1])

    return sum(map(lambda nd: nd.weight, filter(lambda nd: nd.color == 'blue', conflict_graph)))

runtests(my_solve)
