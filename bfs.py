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
        self.VISITED_1_STEP_AGO = []
        self.VISITED_2_STEPS_AGO = []
        self.VISITED_3_STEPS_AGO = []
        self.VISITED_A_WHILE_AGO = []
        self.target = target
        self.grid = grid

    def grid_updates(self):
        if self.VISITED_A_WHILE_AGO:
            for (row, col) in self.VISITED_A_WHILE_AGO:
                self.grid[row][col] = VISITED_A_WHILE_AGO
        if self.VISITED_3_STEPS_AGO:
            for (row, col) in self.VISITED_3_STEPS_AGO:
                self.grid[row][col] = VISITED_3_STEPS_AGO
            self.VISITED_A_WHILE_AGO = deepcopy(self.VISITED_3_STEPS_AGO)
        if self.VISITED_2_STEPS_AGO:
            for (row, col) in self.VISITED_2_STEPS_AGO:
                self.grid[row][col] = VISITED_2_STEPS_AGO
            self.VISITED_3_STEPS_AGO = deepcopy(self.VISITED_2_STEPS_AGO)
        if self.VISITED_1_STEP_AGO:
            for (row, col) in self.VISITED_1_STEP_AGO:
                self.grid[row][col] = VISITED_1_STEP_AGO
            self.VISITED_2_STEPS_AGO = deepcopy(self.VISITED_1_STEP_AGO)
        if self.queue:
            self.VISITED_1_STEP_AGO = []
            for (row, col) in self.queue:
                if (row, col) not in self.visited_set:
                    self.grid[row][col] = CURR_VISITING
                    self.VISITED_1_STEP_AGO.append((row, col))

    def one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        if len(self.visited_set) == grid_height*grid_width:
            return (False, True)
        while self.queue:
            num_elements = len(self.queue)
            self.grid_updates()
            while num_elements > 0:
                curr_row, curr_col = self.queue.popleft()
                if (curr_row, curr_col) in self.visited_set:
                    num_elements -= 1
                    continue
                if (curr_row, curr_col) == self.target:
                    self.grid[curr_row][curr_col] = FOUND
                    return (True, True)

                self.visited_set.add((curr_row, curr_col))
                self.order_visited.append((curr_row, curr_col))
                for dir in self.directions:
                    if curr_row+dir[0] >= 0 and curr_row+dir[0] < grid_width and \
                    curr_col+dir[1] >= 0 and curr_col+dir[1] < grid_height:
                        if (curr_row+dir[0], curr_col+dir[1]) not in self.visited_set:
                            self.queue.append((curr_row+dir[0], curr_col+dir[1]))
                num_elements -= 1
            break
        return (False, False)
