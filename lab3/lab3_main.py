from graph_input import to_adjacency_list, load_graph, make_all_edges_unit
from consistency import edmonds_karp_consistency

print("Lab3 - Spójność krawędziowa")
file_name = input("Podaj nazwę pliku z grafem: ")
vertex_number, edges = load_graph(file_name, "lab3\\graphs-lab3")
edges = make_all_edges_unit(edges)
graph = to_adjacency_list(vertex_number, edges, directed=False)

with open(f"graphs-lab3\\{file_name}") as file:
    answer = int(file.readline().split()[-1])

print(f"Wynik prawidłowy: {answer}")
print(f"Wynik algorytmu Edmondsa-Karpa: {edmonds_karp_consistency(graph)}")
