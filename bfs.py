from copy import deepcopy
from collections import deque
from constants import *


class BFS:
    def __init__(self, start, target, grid):
        self.visited_set = set()
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.queue = deque()
        self.start = start
        self.queue.append(start)
        self.VISITED_1_STEP_AGO = None
        self.VISITED_2_STEPS_AGO = None
        self.VISITED_3_STEPS_AGO = None
        self.VISITED_A_WHILE_AGO = None
        self.target = target
        self.grid = grid
        self.parents = deepcopy(grid) #will store the coordinates of the parent
        self.shortest_path = []
        self.drawing_shortest_path = False

    def generate_shortest_path(self):
        node_x, node_y = self.target
        while (node_x, node_y) != self.start:
            self.shortest_path.append((node_x, node_y))
            (node_x, node_y) = self.parents[node_x][node_y]
        self.shortest_path.append((node_x, node_y))

    def step_through_shortest_path(self):
        if len(self.shortest_path) > 0:
            (node_x, node_y) = self.shortest_path.pop()
            self.grid[node_x][node_y] = SHORTEST_PATH_NODE
            if self.shortest_path:
                (n_node_x, n_node_y) = self.shortest_path[-1]
                return (True, False, (node_x, node_y), (n_node_x-node_x, n_node_y-node_y))
            return (True, False, (node_x, node_y), None)
        return (True, True, None, None)

    def grid_updates(self):
        if self.VISITED_A_WHILE_AGO:
            (row, col) = self.VISITED_A_WHILE_AGO
            self.grid[row][col] = VISITED_A_WHILE_AGO
        if self.VISITED_3_STEPS_AGO:
            (row, col) = self.VISITED_3_STEPS_AGO
            self.grid[row][col] = VISITED_3_STEPS_AGO
            self.VISITED_A_WHILE_AGO = self.VISITED_3_STEPS_AGO
        if self.VISITED_2_STEPS_AGO:
            (row, col) = self.VISITED_2_STEPS_AGO
            self.grid[row][col] = VISITED_2_STEPS_AGO
            self.VISITED_3_STEPS_AGO = self.VISITED_2_STEPS_AGO
        if self.VISITED_1_STEP_AGO:
            (row, col) = self.VISITED_1_STEP_AGO
            self.grid[row][col] = VISITED_1_STEP_AGO
            self.VISITED_2_STEPS_AGO = self.VISITED_1_STEP_AGO
        if self.queue:
            (row, col) = self.queue[0]
            self.grid[row][col] = CURR_VISITING
            self.VISITED_1_STEP_AGO = self.queue[0]

    def one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        if self.drawing_shortest_path:
            return self.step_through_shortest_path()
        if len(self.visited_set) == grid_height*grid_width:
            return (False, True, None, None)
        while self.queue:
            curr_row, curr_col = self.queue[0]
            if self.queue[0] == self.target:
                self.grid[curr_row][curr_col] = FOUND
                self.generate_shortest_path()
                self.drawing_shortest_path = True
                return (True, False, None, None)
            self.grid_updates()
            self.queue.popleft()

            for dir in self.directions:
                if curr_row+dir[0] >= 0 and curr_row+dir[0] < grid_height and \
                curr_col+dir[1] >= 0 and curr_col+dir[1] < grid_width and \
                (curr_row+dir[0], curr_col+dir[1]) not in self.visited_set:
                    self.queue.append((curr_row+dir[0], curr_col+dir[1]))
                    self.visited_set.add((curr_row+dir[0], curr_col+dir[1]))
                    self.parents[curr_row+dir[0]][curr_col+dir[1]] = (curr_row, curr_col)
            break
        return (False, False, None, None)
