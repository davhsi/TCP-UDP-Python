class Router:
    def __init__(self, name):
        self.name = name
        self.routes = {}   # Destination and cost
        self.neighbors = {}

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor.name] = cost
        self.routes[neighbor.name] = cost

    def update_routes(self):
        for neighbor, cost in self.neighbors.items():
            for dest, dest_cost in self.routes.items():
                new_cost = cost + dest_cost
                if dest not in self.routes or new_cost < self.routes[dest]:
                    self.routes[dest] = new_cost

# Setup routers
A, B, C = Router("A"), Router("B"), Router("C")
A.add_neighbor(B, 1)
B.add_neighbor(C, 2)
A.add_neighbor(C, 4)

# Propagate updates (simulated iteration)
for _ in range(3):
    A.update_routes()
    B.update_routes()
    C.update_routes()

# Show routes
print("Routes from A:", A.routes)
print("Routes from B:", B.routes)
print("Routes from C:", C.routes)
