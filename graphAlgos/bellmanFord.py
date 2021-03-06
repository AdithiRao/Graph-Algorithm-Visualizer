from graphAlgos.graphClass import GraphSearchBase
from constants import FOUND

class BELLMANFORD(GraphSearchBase):
    '''
    If a negative cycle is detected, then the nodes that are not reachable
    or are part of a negative weights cycle will display as a node that does
    not have a definitive shortest path and no shortest path will be drawn.
    '''
    def __init__(self, start, target, pickup, grid, weights):
        super().__init__(start, target, pickup, grid, weights)
        self.vertex_dists = self.get_vertices(weights)
        self.vertex_dists[start] = 0
        self.num_vertices = len(self.vertex_dists)
        self.iteration = 0
        self.neg_cycle = False
        self.vertices_to_process = [start]
        self.order_visited.append(start)
        self.shortest_path_length_thusfar = None

    def get_vertices(self, weights):
        vertices = {}
        non_walls = 0
        for row in range(len(weights)):
            for col in range(len(weights[row])):
                if weights[row][col] != 0:
                    vertices[(row, col)] = float('inf')
        return vertices

    def finish(self):
        while self.one_round() != []:
            continue
        self.grid_updates()

    def one_round(self):
        self.iteration += 1
        if self.iteration > self.num_vertices:
            self.neg_cycle = True
            self.finding_shortest_path = False
            return []
        new_vertex_dists = {}
        vertices_to_process = []
        for vertex in self.vertex_dists:
            (curr_row, curr_col) = vertex
            og_weight = self.vertex_dists[vertex]
            new_vertex_dists[vertex] = self.vertex_dists[vertex]
            for dir in self.directions:
                in_neighbor = (curr_row+dir[0], curr_col+dir[1])
                if self.within_boundaries(in_neighbor[0], in_neighbor[1]):
                    new_weight = self.vertex_dists[(in_neighbor[0],in_neighbor[1])]+self.weights[vertex[0]][vertex[1]]
                    new_vertex_dists[vertex] = min(new_vertex_dists[vertex],
                                                   new_weight)
                    if new_vertex_dists[vertex] == new_weight and new_weight != float('inf'):
                        self.parents[curr_row][curr_col] = in_neighbor
            if new_vertex_dists[vertex] != float('inf') and new_vertex_dists[vertex] != og_weight:
                self.order_visited.append(vertex)
                vertices_to_process.append(vertex)
        if new_vertex_dists == self.vertex_dists: #no change, then we are done
            return []
        self.vertex_dists = new_vertex_dists
        return vertices_to_process

    def pickup_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return
        if self.neg_cycle:
            self.finding_shortest_path = False
            return
        if not self.vertices_to_process:
            self.vertices_to_process = self.one_round()
        if self.vertices_to_process:
            self.finding_shortest_path = True
            self.curr_node = self.vertices_to_process.pop()
            self.shortest_path_length_thusfar = self.vertex_dists[self.curr_node]
            if self.curr_node == self.pickup:
                #need to reset a bunch of variables here
                self.pickup_order_visited = self.order_visited
                self.order_visited = [self.pickup]
                self.vertex_dists = self.get_vertices(self.weights)
                self.vertex_dists[self.pickup] = 0
                self.iteration = 0
                self.neg_cycle = False
                self.vertices_to_process = [self.pickup]
                self.shortest_path_length_thusfar = None
                self.pickup_done()
                return
            self.grid_updates()

    def target_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return
        if self.neg_cycle:
            self.finding_shortest_path = False
            return
        if not self.vertices_to_process:
            self.vertices_to_process = self.one_round()
        if self.vertices_to_process:
            self.finding_shortest_path = True
            self.curr_node = self.vertices_to_process.pop()
            self.shortest_path_length_thusfar = self.vertex_dists[self.curr_node]
            if self.curr_node == self.target:
                self.done()
                return
            self.grid_updates()
