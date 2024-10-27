from graph_input import load_graph, to_adjacency_list
from dijkstra import dijkstra

file_name = input("Podaj nazwę pliku z grafem: ")
vertex_number, edges = load_graph(file_name)
graph = to_adjacency_list(vertex_number, edges)

with open(f"..\\example_graphs\\{file_name}") as file:
    correct_answer = int(file.readline().split()[-1])
print(f"Wynik prawidłowy: {correct_answer}")

print(f"Wynik algorytmu Dijkstry: {dijkstra(graph)}")
