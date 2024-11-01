class ResidualNetwork:

    def __init__(self, graph):
        self.org_graph = graph
        self.network = [[] for _ in range(len(graph))]

        for u in range(len(graph)):
            for v, capacity, flow_field in graph[u]:
                forward_edge = [v, capacity - flow_field, None]
                backward_edge = [u, flow_field, forward_edge]
                forward_edge[2] = backward_edge
                self.network[u].append(forward_edge)
                self.network[v].append(backward_edge)

    def dfs(self, start, end, current_min=float('inf'), visited=None):
        if visited is None:
            visited = set()

        if start == end:
            return current_min

        visited.add(start)

        for i in range(len(self.network[start])):
            if self.network[start][i][1] == 0 or self.network[start][i][0] in visited:
                continue
            min_edge = self.dfs(self.network[start][i][0], end, min(current_min, self.network[start][i][1]))
            if min_edge:
                # Update'ujemy przepływ w oryginalnym grafie
                # self.org_graph[start][i][2] += min_edge
                # Update'ujemy przepływ w sieci rezydualnej
                self.network[start][i][1] -= min_edge
                # Update'ujemy przepływ w sieci rezydualnej dla krawędzi wstecznej
                self.network[start][i][2][1] += min_edge
                visited.remove(start)
                return min_edge

        visited.remove(start)
        return False
