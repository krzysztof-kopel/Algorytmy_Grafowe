from algorithm_comparator import compare_algorithms
from graph_input import load_directed_graph, to_adjacency_list
from ford_fulkerson import ford_fulkerson_dfs, edmonds_karp

file_name = input("Podaj nazwę pliku z grafem: ")
vertex_number, edges = load_directed_graph(file_name, "lab2\\flow_example_graphs")
graph = to_adjacency_list(vertex_number, edges, directed=True, flow_field=False)

with open(f"flow_example_graphs\\{file_name}") as file:
    answer = int(file.readline().split()[-1])

print(f"Wynik prawidłowy: {answer}")
compare_algorithms([edmonds_karp, ford_fulkerson_dfs], ["Edmondsa-Karpa", "Forda-Fulkersona z wykorzystaniem DFS"], graph)
