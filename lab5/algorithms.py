from lab5.lex_bfs import lex_bfs_nodes
from node_class import Node

def is_chordal(graph: list[Node]) -> bool:
    lex_bfs_ordering = lex_bfs_nodes(graph)
    predecessors = [set() for _ in range(len(graph))]
    for i in range(1, len(lex_bfs_ordering)):
        vertex = lex_bfs_ordering[i]
        neighbors = list()
        for j in range(i):
            if lex_bfs_ordering[j].idx in vertex.out:
                neighbors.append(lex_bfs_ordering[j].idx)
        if not set(neighbors[:-1]) <= predecessors[neighbors[-1]]:
            return False
        predecessors[lex_bfs_ordering[i].idx] = set(neighbors)
    return True

def max_clique(graph: list[Node]) -> int:
    lex_bfs_ordering = lex_bfs_nodes(graph)
    max_clique_size = 0
    for i in range(1, len(lex_bfs_ordering)):
        vertex = lex_bfs_ordering[i]
        neighbors = list()
        for j in range(i):
            if lex_bfs_ordering[j].idx in vertex.out:
                neighbors.append(lex_bfs_ordering[j].idx)
        max_clique_size = max(max_clique_size, len(neighbors) + 1)
    return max_clique_size

def coloring(graph: list[Node]) -> int:
    lex_bfs_ordering = lex_bfs_nodes(graph)
    max_color = 1
    for i, vertex in enumerate(lex_bfs_ordering):
        used_colors = set()
        for neighbor in vertex.out:
            if graph[neighbor].color is not None:
                used_colors.add(graph[neighbor].color)
        j = 1
        while j in used_colors:
            j += 1
        vertex.color = j
        max_color = max(max_color, j)
    return max_color

def min_vcover(graph: list[Node]) -> int:
    lex_bfs_ordering = lex_bfs_nodes(graph)[::-1]
    independent_set = set()
    for i, vertex in enumerate(lex_bfs_ordering):
        neighbors = vertex.out
        if len(neighbors.intersection(independent_set)) == 0:
            independent_set.add(vertex.idx)
    return len(graph) - len(independent_set)
