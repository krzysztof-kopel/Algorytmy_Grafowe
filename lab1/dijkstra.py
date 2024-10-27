from queue import PriorityQueue


def dijkstra(graph, start=0, end=1):
    # graph = adj_list
    queue = PriorityQueue()
    queue.put((-float('inf'), start))
    results = [-float('inf')] * len(graph)
    results[start] = float('inf')
    parents = [(None, None)] * len(graph)

    while not queue.empty():
        prev_min, vertex = queue.get()
        prev_min *= -1
        for i in range(len(graph[vertex])):
            new_vertex, new_weight = graph[vertex][i]
            if min(new_weight, prev_min) > results[new_vertex]:
                results[new_vertex] = min(new_weight, prev_min)
                parents[new_vertex] = (vertex, new_weight)
                queue.put((-min(new_weight, prev_min), new_vertex))

    result = float('inf')
    i = end
    while i != start:
        result = min(result, parents[i][1])
        i = parents[i][0]
    return result
