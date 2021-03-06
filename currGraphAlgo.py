import math
from graphAlgos.bfs import BFS
from graphAlgos.dfs import DFS
from graphAlgos.dijkstras import DIJKSTRAS
from graphAlgos.astar import ASTAR
from graphAlgos.bellmanFord import BELLMANFORD
from graphAlgos.johnsons import JOHNSONS
from graphAlgos.greedyBFS import GREEDYBFS
from constants import ROWS, COLS, MARGIN, WIDTH, HEIGHT, COLORS, WHITE

class CurrGraphAlgorithm():
    '''
    This class is used to deal with the running of any algorithm: the instance variable
    will always refer to the current running algorithm. 
    '''
    def __init__(self):
        self.running = False
        self.alg_chosen = False
        self.alg_name = ""
        self.description = ""
        self.instance = None
        self.heuristic = "Heuristic: Euclidean Dst."

    def newGrid(self, initial):
        grid = []
        for row in range(ROWS):
            grid.append([])
            grid[row] = [initial]*COLS
        return grid

    # Updates description of the algorithm that was chosen
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
        elif alg == "A*":
            self.description = "A* uses a priority queue and a heuristic to guide" \
                                " the searching process."
        elif alg == "Greedy BFS":
            self.description = "Greedy BFS is very similar to A*- however it only uses a heuristic to"\
                                "guide the searching process rather than also considering the elements' weight."                     
        elif alg == "Bellman Ford":
            self.description = "Bellman Ford is an algorithm capable of dealing with negative weights. It uses k-hop distances"\
                                "to determine if a node is caught in a negative cycle. "
        elif alg == "Johnsons":
            self.description = "Johnsons solves the All-Pairs-Shortest-Paths problem."
        
        if alg == "Greedy BFS" or alg == "A*":
            if self.heuristic == "Heuristic: Euclidean Dst.":
                self.description += " Here the heuristic is straight line distance."
            elif self.heuristic == "Heuristic: Manhattan Dst.":
                 self.description += " Here the heuristic is taxicab distance."
            elif self.heuristic == "Heuristic: Chebyshev Dst.":
                self.description += " Here the heuristic is chebyshev distance."
            elif self.heuristic == "Heuristic: Octile Dst.":
                self.description += " Here the heuristic is octile distance."

    def start_algorithm(self, params, grid, weights):
        self.running = True
        (start, target, pickup) = params
        if self.heuristic == "Heuristic: Euclidean Dst.":
            heuristic = lambda pt,tar: math.sqrt((tar[0]-pt[0])**2 + (tar[1]-pt[1])**2)
        elif self.heuristic == "Heuristic: Manhattan Dst.":
            heuristic = lambda pt,tar: abs(tar[0]-pt[0]) + abs(tar[1]-pt[1])
        elif self.heuristic == "Heuristic: Chebyshev Dst.":
            heuristic = lambda pt,tar: (abs(tar[0]-pt[0]) + abs(tar[1]-pt[1])) + (-1) * min(abs(tar[0]-pt[0]), abs(tar[1]-pt[1]))
        elif self.heuristic == "Heuristic: Octile Dst.":
            heuristic = lambda pt,tar: (abs(tar[0]-pt[0]) + abs(tar[1]-pt[1])) + (math.sqrt(2)-2) * min(abs(tar[0]-pt[0]), abs(tar[1]-pt[1]))
        if pickup == (-1, -1):
            pickup = None
        if self.alg_name == "Breadth First Search":
            self.instance = BFS(start, target, pickup, grid, weights) #weights will j be walls
        elif self.alg_name == "Depth First Search":
            self.instance = DFS(start, target, pickup, grid, weights) #weights will j be walls
        elif self.alg_name == "Dijkstra's":
            self.instance = DIJKSTRAS(start, target, pickup, grid, weights)
        elif self.alg_name == "A*":
            self.instance = ASTAR(start, target, pickup, grid, weights, heuristic)
        elif self.alg_name == "Bellman Ford":
            self.instance = BELLMANFORD(start, target, pickup, grid, weights)
        elif self.alg_name == "Johnsons":
            self.instance = JOHNSONS(start, target, pickup, grid, weights)
        elif self.alg_name == "Greedy BFS":
            self.instance = GREEDYBFS(start, target, pickup, grid, weights, heuristic)

    def algorithm_done(self):
        self.running = False
        self.instance = None
