from graph_input import load_graph, to_adjacency_list
from dijkstra import dijkstra

file_name = input("Podaj nazwę pliku z grafem: ")
vertex_number, edges = load_graph(file_name)
graph = to_adjacency_list(vertex_number, edges)

print(f"Wynik algorytmu Dijkstry: {dijkstra(graph)}")
