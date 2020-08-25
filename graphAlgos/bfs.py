from collections import deque
from graphAlgos.graphClass import GraphSearchBase
from constants import *


class BFS(GraphSearchBase):
    def __init__(self, start, target, pickup, grid, weights):
        super().__init__(start, target, pickup, grid, weights)
        self.queue = deque()
        self.queue.append((start,0))

    def add_neighbors(self, row, col, curr_len):
        for dir in self.directions:
            if self.valid_to_visit(row+dir[0], col+dir[1]):
                self.queue.append(((row+dir[0], col+dir[1]), curr_len+1))
                self.visited_set.add((row+dir[0], col+dir[1]))
                if not self.parents[row+dir[0]][col+dir[1]]:
                    self.parents[row+dir[0]][col+dir[1]] = (row, col)

    def finish(self):
        while self.queue:
            (curr_row, curr_col), curr_len = self.queue.popleft()
            self.curr_node = (curr_row, curr_col)
            self.order_visited.append(self.curr_node)

            self.add_neighbors(curr_row, curr_col, curr_len)

    def pickup_step(self):
        self.finding_shortest_path = True
        if self.queue:
            (curr_row, curr_col), curr_len = self.queue[0]
            self.shortest_path_length = curr_len + 1
            self.curr_node = (curr_row, curr_col)
            self.grid_updates()

            if (curr_row, curr_col) == self.pickup:
                self.queue = deque()
                self.queue.append((self.pickup, 0))
                self.pickup_done()
                return
                
            self.pickup_order_visited.append(self.curr_node)
            self.queue.popleft()
            self.add_neighbors(curr_row, curr_col, curr_len)
    
    def target_step(self):
       # print(self.start in self.visited_set)
       # print(self.pickup in self.visited_set)
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
            self.add_neighbors(curr_row, curr_col, curr_len)
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
