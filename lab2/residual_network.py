class ResidualNetwork:

    def __init__(self, graph, start=0, end=None):
        self.start = start
        self.end = end if end is not None else len(graph) - 1
        connections = [[False for _ in range(len(graph))] for _ in range(len(graph))]
        new_edges = []
        for v in range(len(graph)):
            for u in graph[v]:
                if connections[u[0]][v]:
                    new_edges.append((v, (u[0], u[1])))
                    continue
                connections[u[0]][v] = True
                connections[v][u[0]] = True

        for v, edge in new_edges:
            graph.append([edge])
            graph[v].append((len(graph) - 1, edge[1]))
            graph[v].remove(edge)


        self.org_graph = graph
        self.network = [[] for _ in range(len(graph))]

        for u in range(len(graph)):
            for v, capacity in graph[u]:
                forward_edge = [v, capacity, None]
                backward_edge = [u, 0, forward_edge]
                forward_edge[2] = backward_edge
                self.network[u].append(forward_edge)
                self.network[v].append(backward_edge)

    def dfs(self, start, current_min=float('inf'), visited=None):
        if visited is None:
            visited = set()

        if start == self.end:
            return current_min

        visited.add(start)

        for i in range(len(self.network[start])):
            if self.network[start][i][1] == 0 or self.network[start][i][0] in visited:
                continue
            min_edge = self.dfs(self.network[start][i][0], min(current_min, self.network[start][i][1]), visited)
            if min_edge:
                # Update'ujemy przepływ w sieci rezydualnej
                self.network[start][i][1] -= min_edge
                # Update'ujemy przepływ w sieci rezydualnej dla krawędzi wstecznej
                self.network[start][i][2][1] += min_edge
                visited.remove(start)
                return min_edge

        visited.remove(start)
        return False
