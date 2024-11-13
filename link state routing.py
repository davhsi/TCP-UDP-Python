import heapq

class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, u, v, cost):
        self.edges.setdefault(u, {})[v] = cost
        self.edges.setdefault(v, {})[u] = cost

    def shortest_paths(self, start):
        distances = {node: float('inf') for node in self.edges}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            current_dist, node = heapq.heappop(queue)
            if current_dist > distances[node]: continue
            for neighbor, weight in self.edges[node].items():
                dist = current_dist + weight
                if dist < distances[neighbor]:
                    distances[neighbor] = dist
                    heapq.heappush(queue, (dist, neighbor))
        return distances

# Setup graph
graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("B", "C", 2)
graph.add_edge("A", "C", 4)

# Find shortest paths from A
print("Shortest paths from A:", graph.shortest_paths("A"))
