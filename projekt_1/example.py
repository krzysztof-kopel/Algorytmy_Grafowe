from queue import PriorityQueue
from data import runtests

class Node:
  def __init__(self, idx, weight=0):
    self.idx = idx
    self.out = set()
    self.lords = set() # Używane tylko, gdy Node jest wierzchołkiem oryginalnego drzewa
    self.weight = weight # Używane tylko, gdy Node jest wierzchołkiem grafu konfliktów

  def connect_to(self, v, weight=0):
    if weight > 0:
        self.out.add((v, weight))
    else:
        self.out.add(v)


def to_adjacency_list(vertex_number, edges):
    adj_list = [[] for _ in range(vertex_number)]
    for edge in edges:
        added_edge = (edge[1] - 1, edge[2])
        adj_list[edge[0] - 1].append(added_edge)

        added_edge = (edge[0] - 1, edge[2])
        adj_list[edge[1] - 1].append(added_edge)

    return adj_list

def prim(graph: list[list[int]], start_index: int=0) -> set[tuple[int, int]]:
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


def find_lord_subtree(lord_number: int, controlled: set[int], graph: list[Node]) -> int:
    visited = set()
    subtree_vertices = set()
    lord_weight = 0

    def dfs(node: Node, parent: int):
        nonlocal lord_weight
        visited.add(node.idx)
        if node.idx in controlled:
            node.lords.add(lord_number)
            subtree_vertices.add(node.idx)
        for neighbor, weight in node.out:
            if neighbor == parent:
                continue
            if neighbor not in visited:
                dfs(graph[neighbor], node)
                if graph[neighbor].idx in subtree_vertices:
                    node.lords.add(lord_number)
                    subtree_vertices.add(node.idx)
                    lord_weight += weight

    start = graph[list(controlled)[0]]
    dfs(start, None)

    return lord_weight


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

    conflict_graph = []
    for i in range(len(lords)):
        conflict_graph.append(Node(i, find_lord_subtree(i, set(lords[i]), graph)))

    for node in graph:
        node_lords = list(node.lords)
        for i in range(len(node_lords)):
            for j in range(i + 1, len(node_lords)):
                conflict_graph[node_lords[i]].connect_to(node_lords[j])
                conflict_graph[node_lords[j]].connect_to(node_lords[i])

    return conflict_graph
    # 1. Graf konfliktów -> Done
    # 2. Lex-BFS
    # 3. Kolorowanie w kolejności Lex-BFS

streets = [
    (1, 2, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 8),
    (5, 6, 7),
    (1, 6, 9),
    (2, 5, 10)]
lords = [
    [1, 3],
    [2, 5],
    [4, 6]]

my_solve(6, streets, lords)
runtests(my_solve)
