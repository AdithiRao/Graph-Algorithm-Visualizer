from constants import *
from collections import deque


class DIJKSTRAS:
    def __init__(self, start, target, grid):
        self.visited_set = set()
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.order_visited = []
        self.queue = deque()
        self.queue.append(start)
        self.VISITED_1_STEP_AGO = None
        self.VISITED_2_STEPS_AGO = None
        self.VISITED_3_STEPS_AGO = None
        self.VISITED_A_WHILE_AGO = None
        self.target = target
        self.grid = grid

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
        return (False, False)
