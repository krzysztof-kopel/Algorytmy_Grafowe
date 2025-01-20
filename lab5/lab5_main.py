from algorithm_comparator import compare_algorithms
from graph_input import load_graph
from lab5.algorithms import is_chordal, max_clique
from node_class import Node

folder_name = input("Podaj nazwę folderu, z którego chcesz wziąć graf (chordal, coloring, interval, maxclique, vcover): ")
file_name = input("Podaj nazwę pliku z grafem: ")


with open(f"graphs-lab5\\{folder_name}\\{file_name}") as file:
    answer = int(file.readline().split()[-1])
print(f"Wynik prawidłowy {folder_name}: {answer}")

rank, edges = load_graph(file_name, f"lab5\\graphs-lab5\\{folder_name}")
graph = [Node(i) for i in range(rank)]
for (u, v, _) in edges:
    graph[u - 1].connect_to(v - 1)
    graph[v - 1].connect_to(u - 1)
compare_algorithms([is_chordal, max_clique], ["sprawdzania, czy graf jest przekątniowy", "wyznacza rozmiaru największej kliki"], graph)
