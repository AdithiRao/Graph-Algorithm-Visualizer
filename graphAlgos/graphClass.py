from copy import deepcopy
from constants import *

class GraphSearchBase:
    def __init__(self, start, target, grid):
        self.grid = grid
        self.start = start
        self.target = target

        self.curr_node = None
        self.n_node_dir = None
        self.VISITED_1_STEP_AGO = None
        self.VISITED_2_STEPS_AGO = None
        self.VISITED_3_STEPS_AGO = None
        self.VISITED_A_WHILE_AGO = None
        self.drawing_shortest_path = False
        self.finding_shortest_path = False
        self.shortest_path_length = 0

        self.visited_set = set()
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.shortest_path = []
        self.parents = deepcopy(grid) #will store the coordinates of the parent

    def generate_shortest_path(self):
        node_x, node_y = self.target
        while (node_x, node_y) != self.start:
            self.shortest_path.append((node_x, node_y))
            (node_x, node_y) = self.parents[node_x][node_y]
        self.shortest_path.append((node_x, node_y))

    def step_through_shortest_path(self):
        if len(self.shortest_path) > 0:
            (node_x, node_y) = self.shortest_path.pop()
            self.curr_node = (node_x, node_y)
            self.grid[node_x][node_y] = SHORTEST_PATH_NODE
            if self.shortest_path:
                (n_node_x, n_node_y) = self.shortest_path[-1]
                self.n_node_dir = (n_node_x-node_x, n_node_y-node_y)
        else:
            self.curr_node = None
            self.drawing_shortest_path = False
            self.n_node_dir = None

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
        if self.curr_node:
            (row, col) = self.curr_node
            self.grid[row][col] = CURR_VISITING
            self.VISITED_1_STEP_AGO = (row, col)