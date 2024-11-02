from graph_input import load_directed_graph, to_adjacency_list
from ford_fulkerson import ford_fulkerson_dfs, edmonds_karp
from datetime import datetime

file_name = input("Podaj nazwę pliku z grafem: ")
vertex_number, edges = load_directed_graph(file_name, "lab2\\flow_example_graphs")
graph = to_adjacency_list(vertex_number, edges, directed=True, flow_field=False)

with open(f"flow_example_graphs\\{file_name}") as file:
    answer = int(file.readline().split()[-1])

print(f"Wynik prawidłowy: {answer}")
print(f"Wynik algorytmu Edmondsa-Karpa: W TRAKCIE LICZENIA", end="")
time_start = datetime.now()
endmonds_carp_result = edmonds_karp(graph)
time_end = datetime.now()
time_result = round((time_end - time_start).total_seconds() * 1000, 2)
print("\b" * 18, f"{edmonds_karp(graph)} (czas: {time_result} ms)", sep="")

print(f"Wynik metody Forda-Fulkersona z algorytmem DFS: W TRAKCIE LICZENIA", end="")
time_start = datetime.now()
ford_fulkerson_result = ford_fulkerson_dfs(graph)
time_end = datetime.now()
time_result = round((time_end - time_start).total_seconds() * 1000, 2)
print("\b" * 18, f"{ford_fulkerson_dfs(graph)} (czas: {time_result} ms)", sep="")
