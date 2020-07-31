import math
from graphAlgos.bfs import BFS
from graphAlgos.dfs import DFS
from graphAlgos.dijkstras import DIJKSTRAS
from graphAlgos.astar import ASTAR
from graphAlgos.bellmanFord import BELLMANFORD
from graphAlgos.johnsons import JOHNSONS
from graphAlogs.greedyBFS import GREEDYBFS
from constants import ROWS, COLS, MARGIN, WIDTH, HEIGHT, COLORS, WHITE

class CurrGraphAlgorithm():
    def __init__(self):
        self.running = False
        self.alg_chosen = False
        self.alg_name = ""
        self.description = ""
        self.instance = None

    def newGrid(self, initial):
        grid = []
        for row in range(ROWS):
            grid.append([])
            grid[row] = [initial]*COLS
        return grid

    def update_description(self, alg):
        self.alg_name = alg
        self.alg_chosen = True
        if alg == "Breadth First Search":
            self.description = "BFS explores all nodes at a certain distance" \
                                " before moving onto the next depth level."
        elif alg == "Depth First Search":
            self.description = "DFS explores as far as possible in one direction" \
                                " before backtracking."
        elif alg == "Dijkstra's":
            self.description = "Dijkstra uses a priority queue to determine the" \
                               " smallest weight nodes to traverse next."
        elif alg == "A*: Euclidean Distance":
            self.description = "A* uses a priority queue and a heuristic to guide" \
                               " the searching process. Here the heuristic is straight"\
                               " line distance."
        elif alg == "A*: Manhattan Distance":
            self.description = "A* uses a priority queue and a heuristic to guide" \
                               " the searching process. Here the heuristic is taxicab"\
                               " distance."

    def start_algorithm(self, params, grid, weights):
        self.running = True
        (start, target) = params
        if self.alg_name == "Breadth First Search":
            self.instance = BFS(start, target, grid, weights) #weights will j be walls
        elif self.alg_name == "Depth First Search":
            self.instance = DFS(start, target, grid, weights) #weights will j be walls
        elif self.alg_name == "Dijkstra's":
            self.instance = DIJKSTRAS(start, target, grid, weights)
        elif self.alg_name == "A*: Euclidean Distance":
            heuristic = lambda r,c: math.sqrt((target[0]-r)**2 + (target[1]-c)**2)
            self.instance = ASTAR(start, target, grid, weights, heuristic)
        elif self.alg_name == "A*: Manhattan Distance":
            heuristic = lambda r,c: abs(target[0]-r) + abs(target[1]-c)
            self.instance = ASTAR(start, target, grid, weights, heuristic)
        elif self.alg_name == "Bellman Ford":
            self.instance = BELLMANFORD(start, target, grid, weights)
        elif self.alg_name == "Johnsons":
            self.instance = JOHNSONS(start, target, grid, weights)
        elif self.alg_name == "Greedy BFS":
            heuristic = lambda r,c: abs(target[0]-r) + abs(target[1]-c)
            self.instance = GREEDYBFS(start, target, grid, weights, heuristic)

    def algorithm_done(self):
        self.running = False
