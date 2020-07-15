NOT_VISITED = 0
CURR_VISITING = 1
VISITED_1_STEP_AGO = 2
VISITED_2_STEPS_AGO = 3
VISITED_3_STEPS_AGO = 4
VISITED_A_WHILE_AGO = 5
FOUND = 6

from copy import deepcopy
from collections import deque
class BFS:
    def __init__(self, start, target, grid):
        self.visited_set = set()
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.order_visited = []
        self.queue = deque()
        self.queue.append(start)
        self.target = target
        self.grid = grid


    def grid_updates(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == CURR_VISITING:
                    self.grid[row][col] = VISITED_1_STEP_AGO
                elif self.grid[row][col] == VISITED_1_STEP_AGO:
                    self.grid[row][col] = VISITED_2_STEPS_AGO
                elif self.grid[row][col] == VISITED_2_STEPS_AGO:
                    self.grid[row][col] = VISITED_3_STEPS_AGO
                elif self.grid[row][col] == VISITED_3_STEPS_AGO:
                    self.grid[row][col] = VISITED_A_WHILE_AGO

    def bfs_one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        if len(self.visited_set) == grid_height*grid_width:
            return (False, True)
        while self.queue:
            num_elements = len(self.queue)
            self.grid_updates()
            while num_elements > 0:
                curr_x, curr_y = self.queue.popleft()
                if (curr_x, curr_y) in self.visited_set:
                    continue
                if (curr_x, curr_y) == self.target:
                    self.grid[curr_x][curr_y] = FOUND
                    return (True, True)
                self.visited_set.add((curr_x, curr_y))
                self.grid[curr_x][curr_y] = CURR_VISITING
                self.order_visited.append((curr_x, curr_y))
                for dir in self.directions:
                    if curr_x+dir[0] >= 0 and curr_x+dir[0] < grid_width and \
                    curr_y+dir[1] >= 0 and curr_y+dir[1] < grid_height:
                        if (curr_x+dir[0], curr_y+dir[1]) not in self.visited_set:
                            self.queue.append((curr_x+dir[0], curr_y+dir[1]))
                num_elements -= 1
            break
        return (False, False)
