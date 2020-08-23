from collections import deque
from graphAlgos.graphClass import GraphSearchBase
from constants import *


class BFS(GraphSearchBase):
    def __init__(self, start, target, pickup, grid, weights):
        super().__init__(start, target, pickup, grid, weights)
        self.queue = deque()
        self.queue.append((start,0))

    def finish(self):
        while self.queue:
            (curr_row, curr_col), curr_len = self.queue.popleft()
            self.curr_node = (curr_row, curr_col)
            self.order_visited.append(self.curr_node)

            for dir in self.directions:
                if self.valid_to_visit(curr_row+dir[0], curr_col+dir[1]):
                    self.queue.append(((curr_row+dir[0], curr_col+dir[1]), curr_len+1))
                    self.visited_set.add((curr_row+dir[0], curr_col+dir[1]))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col)

    def one_step(self):
        if self.drawing_shortest_path:
            self.step_through_shortest_path()
            return

        self.finding_shortest_path = True
        if self.queue:
            (curr_row, curr_col), curr_len = self.queue[0]
            self.shortest_path_length = curr_len + 1
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()

            if (curr_row, curr_col) == self.target:
                self.done()
                return
                
            self.order_visited.append(self.curr_node)
            self.queue.popleft()
            for dir in self.directions:
                if self.valid_to_visit(curr_row+dir[0], curr_col+dir[1]):
                    self.queue.append(((curr_row+dir[0], curr_col+dir[1]), curr_len+1))
                    self.visited_set.add((curr_row+dir[0], curr_col+dir[1]))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col) 

            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
