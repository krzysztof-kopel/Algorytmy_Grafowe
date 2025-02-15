#!/usr/bin/env python3
# Movement functions for pieces.
from projekt_2.data import runtests


def king_moves(i, j, N, M, holes, occupied):
    moves = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            new_i, new_j = i + di, j + dj
            if 1 <= new_i <= N and 1 <= new_j <= M and (new_i, new_j) not in holes and (new_i, new_j) not in occupied:
                moves.append((new_i, new_j))
    return moves


def knight_moves(i, j, N, M, holes, occupied):
    candidate_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                       (-2, -1), (-1, -2), (1, -2), (2, -1)]
    moves = []
    for di, dj in candidate_moves:
        new_i, new_j = i + di, j + dj
        if 1 <= new_i <= N and 1 <= new_j <= M and (new_i, new_j) not in holes and (new_i, new_j) not in occupied:
            moves.append((new_i, new_j))
    return moves


def sliding_moves(i, j, directions, N, M, holes, occupied):
    moves = []
    for di, dj in directions:
        step = 1
        while True:
            new_i = i + step * di
            new_j = j + step * dj
            if not (1 <= new_i <= N and 1 <= new_j <= M):
                break  # off the board
            if (new_i, new_j) in holes:
                break  # cannot land on a hole
            if (new_i, new_j) in occupied:
                break  # cannot land on a cell already occupied by another piece
            moves.append((new_i, new_j))
            step += 1
    return moves


def generate_moves_graph(N, M, holes, initial_pieces):
    """
    Generates the moves graph as a directed graph by exploring all legal moves.

    Returns:
      state_to_id : dict mapping a canonical state (tuple of pieces) to a unique id.
      graph_edges : list of directed edges (source_id, dest_id, move_label).
      state_depth : dict mapping state id to its "depth" (number of moves from the initial state).
    """
    holes = set(holes)
    initial_state = tuple(sorted(initial_pieces))
    state_to_id = {initial_state: 0}
    state_depth = {0: 0}
    graph_edges = []  # (source_id, dest_id, move_label)
    next_id = 1

    # Use DFS (without a depth limit) since the state space is finite (no repeated configurations allowed).
    stack = [initial_state]
    while stack:
        state = stack.pop()
        current_id = state_to_id[state]
        depth = state_depth[current_id]
        positions = {(i, j) for (s, i, j) in state}
        for idx, piece in enumerate(state):
            s, i, j = piece
            occupied = positions - {(i, j)}
            if s == 'k':
                targets = king_moves(i, j, N, M, holes, occupied)
            elif s == 'n':
                targets = knight_moves(i, j, N, M, holes, occupied)
            elif s == 'r':
                targets = sliding_moves(i, j, [(0, 1), (0, -1), (1, 0), (-1, 0)], N, M, holes, occupied)
            elif s == 'b':
                targets = sliding_moves(i, j, [(1, 1), (1, -1), (-1, 1), (-1, -1)], N, M, holes, occupied)
            elif s == 'q':
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                              (1, 1), (1, -1), (-1, 1), (-1, -1)]
                targets = sliding_moves(i, j, directions, N, M, holes, occupied)
            else:
                targets = []
            for new_i, new_j in targets:
                new_state_list = list(state)
                new_state_list[idx] = (s, new_i, new_j)
                new_state = tuple(sorted(new_state_list))
                move_label = f"{s}({i},{j})->({new_i},{new_j})"
                if new_state not in state_to_id:
                    state_to_id[new_state] = next_id
                    state_depth[next_id] = depth + 1
                    next_id += 1
                    stack.append(new_state)
                graph_edges.append((current_id, state_to_id[new_state], move_label))
    return state_to_id, graph_edges, state_depth


# Implementation of Edmonds' blossom algorithm for maximum matching in a general graph.
# Assumes vertices are numbered 0..n-1.
def blossom_maximum_matching(graph):
    # graph: dict mapping vertex to a set of neighbors.
    n = len(graph)
    match = [-1] * n  # match[v] = partner vertex or -1 if unmatched.
    p = [-1] * n  # parent in the alternating tree.
    base = list(range(n))
    used = [False] * n
    q = []
    blossom_flag = [False] * n  # used for marking blossoms

    def lca(a, b):
        nonlocal base, match, p, n
        used_path = [False] * n
        while True:
            a = base[a]
            used_path[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if used_path[b]:
                return b
            b = p[match[b]]

    def markPath(v, b, child):
        nonlocal base, match, p, blossom_flag
        while base[v] != b:
            blossom_flag[base[v]] = blossom_flag[base[match[v]]] = True
            p[v] = child
            child = match[v]
            v = p[match[v]]

    def findPath(root):
        nonlocal used, p, base, q, blossom_flag, n
        used[:] = [False] * n
        p[:] = [-1] * n
        for i in range(n):
            base[i] = i
        q.clear()
        q.append(root)
        used[root] = True
        qi = 0
        while qi < len(q):
            v = q[qi]
            qi += 1
            for u in graph[v]:
                if base[v] == base[u] or match[v] == u:
                    continue
                if u == root or (match[u] != -1 and p[match[u]] != -1):
                    blossom_flag[:] = [False] * n
                    cur = lca(v, u)
                    markPath(v, cur, u)
                    markPath(u, cur, v)
                    for i in range(n):
                        if blossom_flag[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[u] == -1:
                    p[u] = v
                    if match[u] == -1:
                        return u
                    used[match[u]] = True
                    q.append(match[u])
        return -1

    def augmentPath(finish):
        nonlocal match, p
        v = finish
        while v != -1:
            pv = p[v]
            w = match[pv] if pv != -1 else -1
            match[v] = pv
            match[pv] = v
            v = w

    for v in range(n):
        if match[v] == -1:
            finish = findPath(v)
            if finish != -1:
                augmentPath(finish)
    # Build matching as a dictionary with one copy per edge.
    matching = {}
    for v in range(n):
        if match[v] != -1 and v < match[v]:
            matching[v] = match[v]
    return matching


def solve(N, M, holes, initial_pieces):
    """
    1. Creates the moves graph for the given board configuration.
    2. Computes the number of edges in its maximum matching (using the blossom algorithm).
    3. Removes the starting vertex (vertex with id 0) from the graph.
    4. Computes the number of edges in the maximum matching on the modified graph.
    5. Returns True if the two matching sizes are equal, else False.
    """
    state_to_id, graph_edges, _ = generate_moves_graph(N, M, holes, initial_pieces)
    num_vertices = len(state_to_id)

    # Build undirected graph from directed edges.
    graph = {v: set() for v in range(num_vertices)}
    for u, v, _ in graph_edges:
        if u == v:
            continue
        graph[u].add(v)
        graph[v].add(u)

    # Compute maximum matching on the full graph.
    matching_full = blossom_maximum_matching(graph)
    full_matching_size = len(matching_full)

    # Remove the starting vertex (vertex 0).
    if 0 in graph:
        del graph[0]
    for v in graph:
        graph[v].discard(0)

    # Re-add vertex 0 as an isolated vertex to keep vertex numbering.
    graph[0] = set()

    matching_removed = blossom_maximum_matching(graph)
    removed_matching_size = len(matching_removed)

    return full_matching_size != removed_matching_size

runtests(solve)
