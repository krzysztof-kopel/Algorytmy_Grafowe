from residual_network import ResidualNetwork

def ford_fulkerson(graph):
    res_network = ResidualNetwork(graph)
    max_flow = 0

    while augmenting_path := res_network.dfs(0, 1):
        max_flow += augmenting_path

    return max_flow
