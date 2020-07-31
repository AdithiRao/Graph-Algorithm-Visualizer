rom copy import deepcopy
from heapq import heappush, heappop, heapify
from graphAlgos.graphClass import GraphSearchBase
from constants import *


class GREEDYBFS(GraphSearchBase):
    def __init__(self, start, target, grid, weights, heuristic):
        super().__init__(start, target, grid)
        self.pq = []
        heappush(self.pq, (heuristic(start), start, 0))
        self.weights = weights
        self.heuristic = heuristic

    # Returns (found, alg_done, curr_spath_node, n_node_dir)
    def one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return

        self.finding_shortest_path = True
        if self.pq:
            _, (curr_row, curr_col), curr_weight = self.pq[0]
            self.shortest_path_length = curr_weight
            self.curr_node = (curr_row, curr_col)
            if (curr_row, curr_col) == self.target:
                self.grid[curr_row][curr_col] = FOUND
                self.generate_shortest_path()
                self.finding_shortest_path = False
                self.drawing_shortest_path = True
                return
            self.grid_updates()
            heappop(self.pq)

            for dir in self.directions:
                if curr_row+dir[0] >= 0 and curr_row+dir[0] < grid_height and \
                curr_col+dir[1] >= 0 and curr_col+dir[1] < grid_width and \
                (curr_row+dir[0], curr_col+dir[1]) not in self.visited_set \
                and self.weights[curr_row+dir[0]][curr_col+dir[1]] != 0:
                    el_weight = self.heuristic(curr_row+dir[0], curr_col+dir[1])
                    actual_weight = self.weights[curr_row+dir[0]][curr_col+dir[1]] +\
                                    curr_weight
                    heappush(self.pq, (el_weight, (curr_row+dir[0], curr_col+dir[1]), actual_weight))
                    self.visited_set.add((curr_row+dir[0], curr_col+dir[1]))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col)
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
