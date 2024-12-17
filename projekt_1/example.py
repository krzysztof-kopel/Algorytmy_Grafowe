from queue import PriorityQueue
# from data import runtests

def to_adjacency_list(vertex_number, edges):
    adj_list = [[] for _ in range(vertex_number)]
    for edge in edges:
        added_edge = (edge[1] - 1, edge[2])
        adj_list[edge[0] - 1].append(added_edge)

        added_edge = (edge[0] - 1, edge[2])
        adj_list[edge[1] - 1].append(added_edge)

    return adj_list

def prim(graph: list[list[int]], start_index: int=0, both_sides: bool=True) -> set[tuple[int, int]]:
    # queue: (weight, edge_to, edge_from)
    queue = PriorityQueue()
    queue.put((0, start_index, None))
    edges_in_mst = set()
    visited = set()

    while len(edges_in_mst) < len(graph) - 1:
        _, edge_to, edge_from = queue.get()
        if edge_to in visited:
            continue
        visited.add(edge_to)

        if edge_from is not None:
            edges_in_mst.add((edge_from, edge_to))
            if both_sides:
                edges_in_mst.add((edge_to, edge_from))
        for destination, weight in graph[edge_to]:
            if destination not in visited:
                queue.put((weight, destination, edge_to))

    return edges_in_mst


# noinspection PyPep8Naming
def my_solve(N, streets, lords):
    graph = to_adjacency_list(N, streets)
    return list(prim(graph))

# runtests(my_solve)
