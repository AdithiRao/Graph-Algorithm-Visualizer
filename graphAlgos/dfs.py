from graphAlgos.graphClass import GraphSearchBase
from constants import *


class DFS(GraphSearchBase):
    def __init__(self, start, target, pickup, grid, weights):
        super().__init__(start, target, pickup, grid, weights)
        self.stack = [(start,0)]

    def add_neighbors(self, row, col, curr_len):
        for dir in self.directions:
            if self.valid_to_visit(row+dir[0], col+dir[1]):
                self.stack.append(((row+dir[0], col+dir[1]), curr_len+1))
                self.parents[row+dir[0]][col+dir[1]] = (row, col) #double check this

    def finish(self):
        while self.stack:
            ((curr_row, curr_col), curr_len) = self.stack.pop()
            self.order_visited.append(self.curr_node)

            self.visited_set.add((curr_row, curr_col))
            for dir in self.directions:
                if self.valid_to_visit(curr_row+dir[0], curr_col+dir[1]):
                    self.stack.append(((curr_row+dir[0], curr_col+dir[1]), curr_len))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col)

    def pickup_step(self):
        self.finding_shortest_path = True
        if self.stack:
            ((curr_row, curr_col), curr_len) = self.stack[-1]
            self.shortest_path_length = curr_len + 1
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()
            
            if (curr_row, curr_col) == self.pickup:
                self.stack = []
                self.stack.append((self.pickup, 0))
                self.pickup_done()
                return

            self.pickup_order_visited.append(self.curr_node)
            self.stack.pop()
            self.visited_set.add((curr_row, curr_col))
            self.add_neighbors(curr_row, curr_col, curr_len)

    def target_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return

        self.finding_shortest_path = True
        if self.stack:
            ((curr_row, curr_col), curr_len) = self.stack[-1]
            print(curr_row, curr_col)
            self.shortest_path_length = curr_len + 1
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()
            if (curr_row, curr_col) == self.target:
                self.done()
                return

            self.order_visited.append(self.curr_node)
            self.stack.pop()
            self.visited_set.add((curr_row, curr_col))
            self.add_neighbors(curr_row, curr_col, curr_len)
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
