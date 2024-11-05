from residual_network import ResidualNetwork


def edmonds_karp_consistency(graph):
    min_consistency = float('inf')
    for start in range(len(graph)):
        for end in range(start + 1, len(graph)):
            res_network = ResidualNetwork(graph, start, end)
            max_flow = 0

            while augmenting_path := res_network.bfs():
                max_flow += augmenting_path

            min_consistency = min(min_consistency, max_flow)

    return min_consistency
