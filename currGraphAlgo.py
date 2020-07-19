import math
from bfs import BFS
from dfs import DFS
from dijkstras import DIJKSTRAS
from astar import ASTAR
from constants import ROWS, COLS, MARGIN, WIDTH, HEIGHT, COLORS, WHITE

class CurrGraphAlgorithm():
    def __init__(self):
        self.running = False

    def newGrid(self, initial):
        grid = []
        for row in range(ROWS):
            grid.append([])
            grid[row] = [initial]*COLS
        return grid

    def update_algorithm(self, params, grid, weights):
        (start, target, alg) = params
        self.running = True
        if alg == "Breadth First Search":
            self.instance = BFS(start, target, grid)
        elif alg == "Depth First Search":
            self.instance = DFS(start, target, grid)
        elif alg == "Dijkstra's":
            self.instance = DIJKSTRAS(start, target, grid, weights)
        elif alg == "A*: Euclidean Distance":
            heuristic = lambda x,y: math.sqrt((target[0]-x)**2 + (target[1]-y)**2)
            self.instance = ASTAR(start, target, grid, weights, heuristic)
        elif alg == "A*: Manhattan Distance":
            print("here")
            heuristic = lambda x,y: abs(target[0]-x) + abs(target[1]-y)
            self.instance = ASTAR(start, target, grid, weights, heuristic)

    def algorithm_done(self):
        self.running = False
