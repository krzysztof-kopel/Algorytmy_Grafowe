import networkx as nx

from graph_input import load_graph, load_directed_graph


def file_to_nx(file_path: str, directed: bool) -> nx.Graph:
    if not directed:
        vertex_number, edges = load_graph(file_path)
        graph = nx.Graph()
    else:
        vertex_number, edges = load_directed_graph(file_path)
        graph = nx.DiGraph()
    graph.add_nodes_from([i for i in range(1, vertex_number + 1)])
    for start, end, capacity in edges:
        graph.add_edge(start, end, capacity=capacity)

    return graph

file_name = input("Podaj nazwę pliku z grafem: ")
graph = file_to_nx(f"..\\lab7\\graphs-lab7\\{file_name}", True)
print(f"Planarność: {nx.check_planarity(graph)[0]}")

source = int(input("Podaj numer wierzchołka źródłowego: "))
destination = int(input("Podaj numer wierzchołka docelowego: "))
print(f"Maksymalny przepływ między wierzchołkami {source} i {destination}: {nx.algorithms.flow.maximum_flow(graph, source, destination)}")
