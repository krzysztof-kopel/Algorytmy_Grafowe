from queue import PriorityQueue
from graph_class import Graph


def stoer_wagner(adj_list: list[tuple[int]]):
    graph = Graph(adj_list)
    min_cut = float('inf')
    while graph.rank > 1:
        min_cut = min(min_cut, minimum_phase_cut(graph))
    return min_cut


def minimum_phase_cut(graph: Graph, start_vertex: int=0):
    set_s = [start_vertex]
    edges_to_s = [0] * graph.org_rank
    visited = set()
    visited.add(start_vertex)
    queue = PriorityQueue()
    for (vertex, edge_length) in graph.nodes[start_vertex].edges.items():
        edges_to_s[vertex] += edge_length
        queue.put((-edge_length, vertex))

    while len(set_s) < graph.rank:
        _, next_vertex = queue.get()
        if next_vertex in visited:
            continue
        visited.add(next_vertex)
        set_s.append(next_vertex)

        for (vertex, edge_length) in graph.nodes[next_vertex].edges.items():
            edges_to_s[vertex] += edge_length
            queue.put((-edges_to_s[vertex], vertex))

    last_vertex = set_s[-1]
    potential_result = 0
    for (_, weight) in graph.nodes[last_vertex].edges.items():
        potential_result += weight

    graph.merge_vertices(set_s[-1], set_s[-2])

    return potential_result
