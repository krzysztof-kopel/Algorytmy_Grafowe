from queue import PriorityQueue


def dijkstra(graph):
    # graph = adj_list
    queue = PriorityQueue()
    queue.put((-float('inf'), 1))
    while not queue.empty():
        best_min, vertex = queue.get()
