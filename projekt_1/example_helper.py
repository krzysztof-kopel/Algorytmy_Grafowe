from graph_input import load_graph
from projekt_1.example import to_adjacency_list, prim

file_name = input("Podaj nazwę pliku: ")
graph = to_adjacency_list(*load_graph(file_name, "lab2\\flow_example_graphs"))
print(prim(graph, both_sides=False))
