from copy import deepcopy
from constants import *

class GraphSearchBase:
    '''
    This is the base class on which all of the algorithms run. It initializes all of the relevant variables
    and has variable helper functions that are used by either some or all of the graph algorithms.
    '''
    def __init__(self, start, target, pickup, grid, weights):
        self.grid = grid
        self.start = start
        self.pickup = pickup
        self.target = target
        self.weights = weights

        self.curr_node = None
        self.n_node_dir = None
        self.VISITED = None
        self.drawing_shortest_path = False
        self.finding_shortest_path = False
        self.found = False
        self.shortest_path_length = 0

        self.visited_set = set()
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.grid_height = len(self.grid)
        self.grid_width = len(self.grid[0])
        self.shortest_path = []
        self.order_visited = []
        self.walls = []
        self.parents = deepcopy(grid) #will store the coordinates of the parent

    def within_boundaries(self, row, col):
        return row >= 0 and row < self.grid_height and \
                col >= 0 and col < self.grid_width \
                and self.weights[row][col] != 0 

    def valid_to_visit(self, row, col):
        return self.within_boundaries(row, col) and \
                (row, col) not in self.visited_set

    def done(self):
        curr_row, curr_col = self.target
        self.grid[curr_row][curr_col] = FOUND
        self.generate_shortest_path()
        self.finding_shortest_path = False
        self.drawing_shortest_path = True
        self.found = True
        finish = getattr(self, "finish", None)
        if callable(finish):
            self.finish()

    # This function deals with the repositioning of the target node
    def new_target(self, target):
        self.target = target
        curr_node_index = 0
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        while curr_node_index < len(self.order_visited) and self.order_visited[curr_node_index] != target:
            curr_row, curr_col = self.order_visited[curr_node_index]
            self.grid[curr_row][curr_col] = VISITED
            curr_node_index += 1
        self.shortest_path = []
        if not self.generate_shortest_path():
            self.found = False
            return False
        for node_r, node_c in self.shortest_path:
            self.grid[node_r][node_c] = SHORTEST_PATH_NODE
        self.found = True
        return True

    # Generates the shortest path from source to target based on self.parents
    def generate_shortest_path(self):
        node= self.target
        self.shortest_path_length = 0
        while node and node != self.start:
            (node_x, node_y) = node
            self.shortest_path.append(node)
            node = self.parents[node_x][node_y]
            if self.weights:
                self.shortest_path_length += self.weights[node_x][node_y]
            else:
                self.shortest_path_length += 1
        if node:
            self.shortest_path.append(node)
            return True
        else:
            return False

    # This function steps through the shortest path one node at a time, allowing for a clear animation
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

    # Updates the state of the nodes as necessary
    def grid_updates(self):
        if self.VISITED:
            (row, col) = self.VISITED
            self.grid[row][col] = VISITED
        if self.curr_node:
            (row, col) = self.curr_node
            self.grid[row][col] = CURR_VISITING
            self.VISITED = (row, col)
