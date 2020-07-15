from enum import Enum
from bfs import BFS
from dfs import DFS
from constants import ROWS, COLS, MARGIN, WIDTH, HEIGHT, COLORS, WHITE

class CurrGraphAlgorithm():
    def __init__(self):
        self.running = False

    def newGrid(self):
        grid = []
        for row in range(ROWS):
            grid.append([])
            grid[row] = [0]*COLS
        for row in range(ROWS):
            for column in range(COLS):
                color = WHITE
                color = COLORS[grid[row][column]]
        return grid

    def update_algorithm(self, params):
        (start, target, alg) = params
        grid = self.newGrid()
        self.running = True
        if alg == "BFS":
            self.instance = BFS(start, target, grid)
        elif alg == "DFS":
            self.instance = DFS(start, target, grid)

    def algorithm_done(self):
        self.running = False
