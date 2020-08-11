from copy import deepcopy
from heapq import heappush, heappop, heapify
from graphAlgos.graphClass import GraphSearchBase
from constants import *


class ASTAR(GraphSearchBase):
    def __init__(self, start, target, pickup, grid, weights, heuristic):
        super().__init__(start, target, pickup, grid, weights)
        self.pq = []
        heappush(self.pq, (0, start, 0))
        self.heuristic = heuristic

    # Returns (found, alg_done, curr_spath_node, n_node_dir)
    def one_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return

        self.finding_shortest_path = True
        if self.pq:
            _, (curr_row, curr_col), curr_weight = self.pq[0]
            self.shortest_path_length = curr_weight
            self.curr_node = (curr_row, curr_col)
            self.order_visited.append(self.curr_node)
            self.grid_updates()
            if (curr_row, curr_col) == self.target:
                self.done()
                return
            heappop(self.pq)

            for dir in self.directions:
                if self.valid_to_visit(curr_row+dir[0], curr_col+dir[1]):
                    el_weight = self.weights[curr_row+dir[0]][curr_col+dir[1]] +\
                                curr_weight + self.heuristic(curr_row+dir[0], \
                                curr_col+dir[1])
                    actual_weight = self.weights[curr_row+dir[0]][curr_col+dir[1]] +\
                                    curr_weight
                    heappush(self.pq, (el_weight, (curr_row+dir[0], curr_col+dir[1]), actual_weight))
                    self.visited_set.add((curr_row+dir[0], curr_col+dir[1]))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col)
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
