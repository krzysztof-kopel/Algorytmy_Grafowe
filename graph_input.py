import dimacs


def load_graph(file_name, path="example_graphs"):
    vertex_number, edges = dimacs.loadWeightedGraph(f"..\\{path}\\{file_name}")
    return vertex_number, edges


def load_directed_graph(file_name, path="example_graphs"):
    vertex_number, directed_edges = dimacs.loadDirectedWeightedGraph(f"..\\{path}\\{file_name})")
    return vertex_number, directed_edges


# noinspection PyTypeChecker
def to_adjacency_list(vertex_number, edges, *, directed: bool=False, flow_field: bool=False):
    adj_list = [[] for _ in range(vertex_number)]
    for edge in edges:
        if flow_field:
            edge = [edge[1] - 1, edge[2], 0]
        else:
            edge = [edge[1] - 1, edge[2]]
        adj_list[edge[0] - 1].append(edge)

        if not directed:
            if flow_field:
                edge = [edge[0] - 1, edge[2], 0]
            else:
                edge = [edge[0] - 1, edge[2]]
            adj_list[edge[1] - 1].append(edge)
    return adj_list


if __name__ == "__main__":
    vertex_number, edges = load_graph("clique5")
    print(f"Wszystkich wierzchołków jest {vertex_number}")
    for edge in edges:
        print(f"{edge[0]} --{edge[2]}--> {edge[1]}")

    adj_list = to_adjacency_list(vertex_number, edges)
    print(f"Lista sąsiedztwa: {adj_list}")
