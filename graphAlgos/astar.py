from copy import deepcopy
from heapq import heappush, heappop, heapify
from graphAlgos.graphClass import GraphSearchBase
from constants import *


class ASTAR(GraphSearchBase):
    def __init__(self, start, target, pickup, grid, weights, heuristic):
        super().__init__(start, target, pickup, grid, weights)
        self.pq = []
        if pickup:
            heappush(self.pq, (heuristic(start, pickup), start, 0))
        else:
            heappush(self.pq, (heuristic(start, target), start, 0))
        self.heuristic = heuristic

    def add_neighbors(self, row, col, curr_weight, target):
        for dir in self.directions:
            if self.valid_to_visit(row+dir[0], col+dir[1]):
                el_weight = self.weights[row+dir[0]][col+dir[1]] +\
                            curr_weight + self.heuristic((row+dir[0], \
                            col+dir[1]), target)
                actual_weight = self.weights[row+dir[0]][col+dir[1]] +\
                                curr_weight
                heappush(self.pq, (el_weight, (row+dir[0], col+dir[1]), actual_weight))
                self.visited_set.add((row+dir[0], col+dir[1]))
                self.parents[row+dir[0]][col+dir[1]] = (row, col)

    def pickup_step(self):
        self.finding_shortest_path = True
        if self.pq:
            _, (curr_row, curr_col), curr_weight = self.pq[0]
            self.shortest_path_length = curr_weight
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()

            if (curr_row, curr_col) == self.pickup:
                self.pq = []
                heappush(self.pq, (0, self.pickup,0))
                self.pickup_done()
                return

            heappop(self.pq)
            self.pickup_order_visited.append(self.curr_node)
            self.add_neighbors(curr_row, curr_col, curr_weight, self.pickup)
           # self.visited_set.add((curr_row, curr_col)) #source doesnt get added otherwise
            

    # Returns (found, alg_done, curr_spath_node, n_node_dir)
    def target_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return

        self.finding_shortest_path = True
        if self.pq:
            _, (curr_row, curr_col), curr_weight = self.pq[0]
            self.shortest_path_length = curr_weight
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()
            if (curr_row, curr_col) == self.target:
                self.done()
                return

            heappop(self.pq)
            self.order_visited.append(self.curr_node)
            self.add_neighbors(curr_row, curr_col, curr_weight, self.target)
           # self.visited_set.add((curr_row, curr_col)) #source doesnt get added otherwise
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
