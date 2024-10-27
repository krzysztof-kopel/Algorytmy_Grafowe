from queue import PriorityQueue


def dijkstra(graph, start=0, end=1):
    # graph = adj_list
    queue = PriorityQueue()
    queue.put((-float('inf'), start, float('inf')))
    results = [-float('inf')] * len(graph)
    results[start] = float('inf')
    final_result = float('inf')

    while not queue.empty():
        prev_min, vertex, min_on_path = queue.get()
        prev_min *= -1
        for i in range(len(graph[vertex])):
            new_vertex, new_weight = graph[vertex][i]
            if min(new_weight, prev_min) > results[new_vertex]:
                results[new_vertex] = min(new_weight, prev_min)
                if new_vertex == end:
                    final_result = min(new_weight, min_on_path)
                queue.put((-min(new_weight, prev_min), new_vertex, min(min_on_path, new_weight)))

    return final_result
