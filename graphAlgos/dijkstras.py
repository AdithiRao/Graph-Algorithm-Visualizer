from copy import deepcopy
from heapq import heappush, heappop, heapify
from graphAlgos.graphClass import GraphSearchBase
from constants import *


class DIJKSTRAS(GraphSearchBase):
    '''
    
    '''
    def __init__(self, start, target, pickup, grid, weights):
        super().__init__(start, target, pickup, grid, weights)
        self.pq = []
        heappush(self.pq, (0, start))

    def add_neighbors(self, row, col, curr_weight):
        for dir in self.directions:
            if self.valid_to_visit(row+dir[0], col+dir[1]):
                el_weight = self.weights[row+dir[0]][col+dir[1]] +\
                            curr_weight
                heappush(self.pq, (el_weight, (row+dir[0], col+dir[1])))
                self.visited_set.add((row+dir[0], col+dir[1]))
                self.parents[row+dir[0]][col+dir[1]] = (row, col)

    def finish(self):
        while self.pq:
            curr_weight, (curr_row, curr_col) = heappop(self.pq)
            self.curr_node = (curr_row, curr_col)
            self.order_visited.append(self.curr_node)
    
            self.add_neighbors(curr_row, curr_col, curr_weight)

    # Returns (found, alg_done, curr_spath_node, n_node_dir)
    def pickup_step(self):
        self.finding_shortest_path = True
        if self.pq:
            curr_weight, (curr_row, curr_col) = self.pq[0]
            self.shortest_path_length = curr_weight
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()

            if (curr_row, curr_col) == self.pickup:
                self.pq = []
                heappush(self.pq, (0, self.pickup))
                self.pickup_done()
                return
                
            heappop(self.pq)
            self.pickup_order_visited.append(self.curr_node)
            self.add_neighbors(curr_row, curr_col, curr_weight)
    
    # Returns (found, alg_done, curr_spath_node, n_node_dir)
    def target_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return

        self.finding_shortest_path = True
        if self.pq:
            curr_weight, (curr_row, curr_col) = self.pq[0]
            self.shortest_path_length = curr_weight
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()
            if (curr_row, curr_col) == self.target:
                self.done()
                return

            heappop(self.pq)
            self.order_visited.append(self.curr_node)
            self.add_neighbors(curr_row, curr_col, curr_weight)
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
