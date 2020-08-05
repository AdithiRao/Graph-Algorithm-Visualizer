from collections import deque
from graphAlgos.graphClass import GraphSearchBase
from constants import *


class BFS(GraphSearchBase):
    def __init__(self, start, target, grid, walls):
        super().__init__(start, target, grid)
        self.queue = deque()
        self.queue.append((start,0))
        self.walls = walls

    def one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
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
                self.grid[curr_row][curr_col] = FOUND
                self.generate_shortest_path()
                self.finding_shortest_path = False
                self.drawing_shortest_path = True
                return
            self.queue.popleft()

            for dir in self.directions:
                if curr_row+dir[0] >= 0 and curr_row+dir[0] < grid_height and \
                curr_col+dir[1] >= 0 and curr_col+dir[1] < grid_width and \
                (curr_row+dir[0], curr_col+dir[1]) not in self.visited_set \
                and self.walls[curr_row+dir[0]][curr_col+dir[1]] != 0:
                    self.queue.append(((curr_row+dir[0], curr_col+dir[1]), curr_len+1))
                    self.visited_set.add((curr_row+dir[0], curr_col+dir[1]))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col)
            self.finding_shortest_path = True
        else:
            self.finding_shortest_path = False
            self.drawing_shortest_path = False
