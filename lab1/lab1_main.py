from graph_input import load_graph, to_adjacency_list
from dijkstra import dijkstra

vertex_number, edges = load_graph("clique1000")
graph = to_adjacency_list(vertex_number, edges)

print(f"Wynik algorytmu Dijkstry: {dijkstra(graph)}")
