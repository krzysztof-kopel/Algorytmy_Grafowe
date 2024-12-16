from residual_network import ResidualNetwork


def ford_fulkerson_dfs(graph):
    # Uwzględniamy domyślnie, że zawsze start = wierzchołek 1, end = ostatni wierzchołek
    res_network = ResidualNetwork(graph)
    max_flow = 0

    while augmenting_path := res_network.dfs(0):
        max_flow += augmenting_path

    return max_flow


def edmonds_karp(graph):
    res_network = ResidualNetwork(graph)
    max_flow = 0

    while augmenting_path := res_network.bfs():
        max_flow += augmenting_path

    return max_flow
