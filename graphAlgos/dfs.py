from graphAlgos.graphClass import GraphSearchBase
from constants import *


class DFS(GraphSearchBase):
    def __init__(self, start, target, pickup, grid, weights):
        super().__init__(start, target, pickup, grid, weights)
        self.stack = [(start,0)]

    def finish(self):
        while self.stack:
            ((curr_row, curr_col), curr_len) = self.stack.pop()
            self.order_visited.append(self.curr_node)

            self.visited_set.add((curr_row, curr_col))
            for dir in self.directions:
                if self.valid_to_visit(curr_row+dir[0], curr_col+dir[1]):
                    self.stack.append(((curr_row+dir[0], curr_col+dir[1]), curr_len))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col)

    def one_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return

        self.finding_shortest_path = True
        if self.stack:
            ((curr_row, curr_col), curr_len) = self.stack[-1]
            self.shortest_path_length = curr_len + 1
            self.curr_node = (curr_row, curr_col)
            self.order_visited.append(self.curr_node)
            self.grid_updates()
            if (curr_row, curr_col) == self.target:
                self.done()
                return
            self.stack.pop()

            self.visited_set.add((curr_row, curr_col))
            for dir in self.directions:
                if self.valid_to_visit(curr_row+dir[0], curr_col+dir[1]):
                    self.stack.append(((curr_row+dir[0], curr_col+dir[1]), curr_len+1))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col) #this is wrong
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
