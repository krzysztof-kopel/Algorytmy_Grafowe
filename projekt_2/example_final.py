from data import runtests
from collections import deque

class Board:
    def __init__(self, n: int, m: int, holes: list[tuple[int, int]], pieces: list[tuple[str, int, int]]):
        self.height = n
        self.width = m
        self.holes = set(holes)
        self.pieces = {}
        for ptype, row, col in pieces:
            self.pieces[(row, col)] = ptype

    def verify(self, i: int, j: int) -> bool:
        return 0 <= i < self.height and 0 <= j < self.width

    def is_occupied(self, i: int, j: int) -> bool:
        return (i, j) in self.holes or (i, j) in self.pieces

    def king_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        moves = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                new_i, new_j = i + di, j + dj
                if self.verify(new_i, new_j) and not self.is_occupied(new_i, new_j):
                    moves.append((new_i, new_j))
        return moves

    def knight_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        candidate_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                           (-2, -1), (-1, -2), (1, -2), (2, -1)]
        moves = []
        for di, dj in candidate_moves:
            new_i, new_j = i + di, j + dj
            if self.verify(new_i, new_j) and not self.is_occupied(new_i, new_j):
                moves.append((new_i, new_j))
        return moves

    def sliding_moves(self, i: int, j: int, directions: list[tuple[int, int]]) -> list[tuple[int, int]]:
        moves = []
        for di, dj in directions:
            step = 1
            while True:
                new_i = i + step * di
                new_j = j + step * dj
                if not self.verify(new_i, new_j) or self.is_occupied(new_i, new_j):
                    break
                moves.append((new_i, new_j))
                step += 1
        return moves

    def generate_all_next_moves(self) -> list['Board']:
        next_boards = []
        for (i, j), piece in list(self.pieces.items()):
            moves = []
            if piece == 'k':
                moves = self.king_moves(i, j)
            elif piece == 'n':
                moves = self.knight_moves(i, j)
            elif piece == 'r':
                moves = self.sliding_moves(i, j, [(0, 1), (0, -1), (1, 0), (-1, 0)])
            elif piece == 'b':
                moves = self.sliding_moves(i, j, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
            elif piece == 'q':
                moves = self.sliding_moves(i, j, [(0, 1), (0, -1), (1, 0), (-1, 0),
                                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])
            for new_i, new_j in moves:
                new_board = Board(self.height, self.width, list(self.holes), [])
                new_board.pieces = self.pieces.copy()
                new_board.pieces[(new_i, new_j)] = piece
                del new_board.pieces[(i, j)]
                next_boards.append(new_board)
        return next_boards

class Node:
    def __init__(self, board: Board):
        self.board = board
        self.neighbors = set()
        self.key = tuple(sorted(self.board.pieces.items()))

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return isinstance(other, Node) and self.key == other.key

    def delete_and_go_to_next(self) -> 'Node':
        if not self.neighbors:
            return self
        next_start = self.neighbors.pop()
        next_start.neighbors.remove(self)
        for neighbor in list(self.neighbors):
            neighbor.neighbors.remove(self)
        return next_start

    def max_matching(self) -> int:
        component = set()
        node_stack = [self]
        while node_stack:
            current_node = node_stack.pop()
            if current_node in component:
                continue
            component.add(current_node)
            for neighbor in current_node.neighbors:
                if neighbor not in component:
                    node_stack.append(neighbor)
        component_nodes = list(component)
        node_to_index = {node: i for i, node in enumerate(component_nodes)}
        num_nodes = len(component_nodes)
        adjacency_list = [[] for _ in range(num_nodes)]
        for i, node in enumerate(component_nodes):
            for neighbor in node.neighbors:
                if neighbor in component:
                    j = node_to_index[neighbor]
                    if j not in adjacency_list[i]:
                        adjacency_list[i].append(j)
                        adjacency_list[j].append(i)
        matching = edmonds(adjacency_list, num_nodes)
        matching = [x for x in matching if x != -1]
        matching_size = len(matching) // 2
        return matching_size

def edmonds(adj: list[list[int]], num_vertices: int) -> list[int]:
    matching = [-1] * num_vertices
    parent = [-1] * num_vertices
    base = list(range(num_vertices))
    used = [False] * num_vertices
    blossom = [False] * num_vertices
    q = deque()

    def mark_blossom_path(v: int, lca_base: int, child: int) -> None:
        while base[v] != lca_base:
            blossom[base[v]] = blossom[base[matching[v]]] = True
            parent[v] = child
            child = matching[v]
            v = parent[matching[v]]

    def find_lowest_common_ancestor(a: int, b: int) -> int:
        used_bases = [False] * num_vertices
        while True:
            a = base[a]
            used_bases[a] = True
            if matching[a] == -1:
                break
            a = parent[matching[a]]
        while True:
            b = base[b]
            if used_bases[b]:
                return b
            b = parent[matching[b]]

    def find_augmenting_path(root: int) -> int:
        used[:] = [False] * num_vertices
        parent[:] = [-1] * num_vertices
        for i in range(num_vertices):
            base[i] = i
        q.clear()
        q.append(root)
        used[root] = True
        while q:
            current = q.popleft()
            for neighbor in adj[current]:
                if base[current] == base[neighbor] or matching[current] == neighbor:
                    continue
                if neighbor == root or (matching[neighbor] != -1 and parent[matching[neighbor]] != -1):
                    blossom[:] = [False] * num_vertices
                    lca_base = find_lowest_common_ancestor(current, neighbor)
                    mark_blossom_path(current, lca_base, neighbor)
                    mark_blossom_path(neighbor, lca_base, current)
                    for i in range(num_vertices):
                        if blossom[base[i]]:
                            base[i] = lca_base
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif parent[neighbor] == -1:
                    parent[neighbor] = current
                    if matching[neighbor] == -1:
                        return neighbor
                    used[matching[neighbor]] = True
                    q.append(matching[neighbor])
        return -1

    for vertex in range(num_vertices):
        if matching[vertex] == -1:
            augmenting_end = find_augmenting_path(vertex)
            if augmenting_end != -1:
                current = augmenting_end
                while current != -1:
                    parent_vertex = parent[current]
                    next_vertex = matching[parent_vertex] if parent_vertex != -1 else -1
                    matching[current] = parent_vertex
                    matching[parent_vertex] = current
                    current = next_vertex
    return matching

def construct_graph(start_vertex: Node) -> None:
    generated_nodes = {start_vertex}
    node_map = {start_vertex: start_vertex}
    stack = [start_vertex]
    while stack:
        current_vertex = stack.pop()
        next_boards = current_vertex.board.generate_all_next_moves()
        for board in next_boards:
            next_node = Node(board)
            if next_node in generated_nodes:
                next_node = node_map[next_node]
            else:
                generated_nodes.add(next_node)
                node_map[next_node] = next_node
                stack.append(next_node)
            current_vertex.neighbors.add(next_node)
            next_node.neighbors.add(current_vertex)

def solve(n: int, m: int, holes: list[tuple[int, int]], pieces: list[tuple[str, int, int]]) -> bool:

    holes = [(i - 1, j - 1) for (i, j) in holes]
    pieces = [(ptype, i - 1, j - 1) for (ptype, i, j) in pieces]

    start_vertex = Node(Board(n, m, holes, pieces))
    construct_graph(start_vertex)

    max_matching_before = start_vertex.max_matching()
    start_vertex = start_vertex.delete_and_go_to_next()
    max_matching_after = start_vertex.max_matching()

    return max_matching_after != max_matching_before

runtests(solve)
