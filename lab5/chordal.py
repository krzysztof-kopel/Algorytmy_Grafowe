from node_class import Node
from lex_bfs import lex_bfs

def is_chordal(graph: list[Node]) -> bool:
    lex_bfs_ordering = lex_bfs(graph)
    parent_neighbors = set()
    parent_neighbors.add(lex_bfs_ordering[0].idx)
    for i in range(1, len(lex_bfs_ordering)):
        vertex = lex_bfs_ordering[i]
        neighbors = list()
        for j in range(i):
            if lex_bfs_ordering[j].idx in vertex.out:
                neighbors.append(j)
        if neighbors[:-1] not in parent_neighbors:
            return False
        parent_neighbors = neighbors[:]
    return True
