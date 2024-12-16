from collections import deque
from copy import deepcopy


class ResidualNetwork:

    def __init__(self, graph, start=0, end=None):
        self.start = start
        self.end = end if end is not None else len(graph) - 1
        connections = [[False for _ in range(len(graph))] for _ in range(len(graph))]
        new_edges = []
        self.org_graph = deepcopy(graph)
        for v in range(len(self.org_graph)):
            for u in self.org_graph[v]:
                if connections[u[0]][v]:
                    new_edges.append((v, (u[0], u[1])))
                    continue
                connections[u[0]][v] = True
                connections[v][u[0]] = True

        for v, edge in new_edges:
            self.org_graph.append([edge])
            self.org_graph[v].append((len(self.org_graph) - 1, edge[1]))
            self.org_graph[v].remove(edge)
        
        self.network = [[] for _ in range(len(self.org_graph))]

        for u in range(len(self.org_graph)):
            for v, capacity in self.org_graph[u]:
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
            v, capacity, backward_edge = self.network[start][i]
            if capacity == 0 or v in visited:
                continue
            min_edge = self.dfs(v, min(current_min, capacity), visited)
            if min_edge:
                # Update the flow in the residual network
                self.network[start][i][1] -= min_edge
                # Update the flow in the residual network for the backward edge
                backward_edge[1] += min_edge
                visited.remove(start)
                return min_edge

        return False

    def bfs(self):
        queue = deque()
        curr_vertex = self.start
        curr_min = float('inf')

        visited = set()
        edges_en_route = []

        while curr_vertex != self.end:
            for i in range(len(self.network[curr_vertex])):
                new_vertex_name = self.network[curr_vertex][i][0]
                new_vertex_capacity = self.network[curr_vertex][i][1]
                new_edges_en_route = edges_en_route[:]

                if new_vertex_capacity == 0 or new_vertex_name in visited:
                    continue

                visited.add(new_vertex_name)
                new_edges_en_route.append(self.network[curr_vertex][i])
                new_vertex_min = min(curr_min, new_vertex_capacity)
                queue.append((new_vertex_name, new_vertex_min, new_edges_en_route))
            if len(queue) == 0:
                break
            curr_vertex, curr_min, edges_en_route = queue.popleft()
        if curr_vertex != self.end:
            return False

        for edge in edges_en_route:
            # Update'ujemy przepływ w sieci rezydualnej
            edge[1] -= curr_min
            # Update'ujemy przepływ w sieci rezydualnej dla krawędzi wstecznej
            edge[2][1] += curr_min

        return curr_min
