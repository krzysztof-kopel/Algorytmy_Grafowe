from algorithm_comparator import compare_algorithms
from graph_input import to_adjacency_list, load_graph, make_all_edges_unit
from consistency import edmonds_karp_consistency
from stoer_wagner import stoer_wagner

print("Lab3 - Spójność krawędziowa")
file_name = input("Podaj nazwę pliku z grafem: ")
vertex_number, edges = load_graph(file_name, "lab3\\graphs-lab3")
edges = make_all_edges_unit(edges)
graph = to_adjacency_list(vertex_number, edges, directed=False)

with open(f"graphs-lab3\\{file_name}") as file:
    answer = int(file.readline().split()[-1])

print(f"Wynik prawidłowy: {answer}")
compare_algorithms([stoer_wagner, edmonds_karp_consistency], ["Stoera-Wagnera", "Edmondsa-Karpa (wielokrotnie wywołanego)"], graph)
