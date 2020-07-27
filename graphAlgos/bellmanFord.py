from graphAlgos.graphClass import GraphSearchBase

class BELLMANFORD(GraphSearchBase):
    def __init__(self, start, target, grid, weights):
        super().__init__(start, target, grid)
        self.weights = weights
        self.vertex_dists = self.get_vertices(weights)
        self.vertex_dists[start] = 0
        self.num_vertices = len(self.vertex_dists)
        self.iteration = 0
        self.neg_cycle = False
        self.vertices_to_process = []
        self.shortest_path_length_thusfar = None

    def get_vertices(self, weights):
        vertices = {}
        non_walls = 0
        for row in range(len(weights)):
            for col in range(len(weights[row])):
                if weights[row][col] != 0:
                    vertices[(row, col)] = float('inf')
        return vertices

    def one_round(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        self.iteration += 1
        if self.iteration == self.num_vertices:
            self.neg_cycle = True
            self.finding_shortest_path = False
            return []
        new_vertex_dists = {}
        vertices_to_process = []
        for vertex in self.vertex_dists:
            (curr_row, curr_col) = vertex
            in_neighbors = []
            for dir in self.directions:
                neighbor = (curr_row+dir[0], curr_col+dir[1])
                if neighbor[0] >= 0 and neighbor[0] < grid_height and \
                neighbor[1] >= 0 and neighbor[1] < grid_width:
                    new_weight = self.vertex_dists[(neighbor[0],neighbor[1])]+self.weights[vertex[0]][vertex[1]]
                    new_vertex_dists[vertex] = min(self.vertex_dists[vertex],
                                                   new_weight)
                    if new_vertex_dists[vertex] == new_weight:
                        self.parents[curr_row][curr_col] = neighbor
            if new_vertex_dists[vertex] != float('inf'):
                vertices_to_process.append(vertex)
        if new_vertex_dists == self.vertex_dists: #no change
            self.finding_shortest_path = False
            self.drawing_shortest_path = True
            return []
        self.vertex_dists = new_vertex_dists
        return vertices_to_process

    def one_step(self):
        if not self.vertices_to_process:
            self.vertices_to_process = self.one_round()
        if self.neg_cycle:
            return
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return
        self.finding_shortest_path = True
        self.curr_node = self.vertices_to_process.pop()
        self.shortest_path_length_thusfar = self.vertex_dists[self.curr_node]
        self.grid_updates()
