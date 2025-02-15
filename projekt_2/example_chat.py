from projekt_2.data import runtests

def in_board(r, c, N, M):
    return 1 <= r <= N and 1 <= c <= M

def generate_moves(piece_type, r, c, occupied, holes_set, N, M):
    """
    Generate legal moves for a piece at (r, c) of a given type.
    A move is legal if it stays on the board, does not land on a hole,
    and does not land on an occupied square.
    """
    moves = []
    if piece_type == 'k':  # King: one step in any direction.
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if in_board(nr, nc, N, M) and (nr, nc) not in holes_set and (nr, nc) not in occupied:
                    moves.append((nr, nc))
    elif piece_type == 'n':  # Knight: L-shaped moves.
        knight_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2),
                        (2, -1), (1, -2), (-2, -1), (-1, -2)]
        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if in_board(nr, nc, N, M) and (nr, nc) not in holes_set and (nr, nc) not in occupied:
                moves.append((nr, nc))
    else:
        # Sliding pieces: queen, rook, bishop.
        if piece_type == 'q':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece_type == 'r':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif piece_type == 'b':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions = []
        for dr, dc in directions:
            step = 1
            while True:
                nr, nc = r + dr * step, c + dc * step
                if not in_board(nr, nc, N, M):
                    break
                if (nr, nc) in holes_set:
                    break  # cannot land on a hole
                if (nr, nc) in occupied:
                    break  # cannot land on an occupied square
                moves.append((nr, nc))
                step += 1
    return moves

def solve(N, M, holes, pieces):
    """
    Fast version using a memoized depth-first search (DFS) with caching.
    Given:
      - N, M: board dimensions,
      - holes: list of unavailable squares,
      - pieces: list of tuples (piece_type, row, col) for the initial positions.
    Returns:
      True if Player 1 (the first to move) can force a win.
    """
    holes_set = set(holes)
    memo = {}

    def dfs(config, turn, visited):
        # Use the triple (config, turn, visited) as the memo key.
        # config is stored as a canonical (sorted) tuple.
        key = (config, turn, visited)
        if key in memo:
            return memo[key]

        # Occupied squares based on current configuration.
        occupied = {(r, c) for (_, r, c) in config}
        # Try moving each piece.
        for idx, (ptype, r, c) in enumerate(config):
            moves = generate_moves(ptype, r, c, occupied - {(r, c)}, holes_set, N, M)
            # Optional: you can sort moves here based on heuristics.
            for (nr, nc) in moves:
                # Update configuration: move piece idx to new position.
                new_config = list(config)
                new_config[idx] = (ptype, nr, nc)
                new_config.sort()
                new_config = tuple(new_config)
                # Enforce the no-repeat rule.
                if new_config in visited:
                    continue
                new_visited = visited | {new_config}
                # If the opponent cannot force a win from new_config, current player wins.
                if not dfs(new_config, 1 - turn, new_visited):
                    memo[key] = True
                    return True

        memo[key] = False
        return False

    initial_config = tuple(sorted(pieces))
    return dfs(initial_config, 0, frozenset({initial_config}))

runtests(solve)
