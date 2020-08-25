from copy import deepcopy
from collections import deque
from constants import *
from collections import Counter

class GraphSearchBase:
    '''
    This is the base class on which all of the algorithms run. It initializes all of the relevant variables
    and has variable helper functions that are used by either some or all of the graph algorithms.

    Can move either pickup or target-> since pickup is a source for target, it cannot move. if target is moved, 
    then that is same as target moving

    Have different colors for pickup visited and target visited
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
        self.pickup_found = False
        self.found = False
        self.shortest_path_length = 0
        self.part1_length = 0

        self.visited_set = set()
        self.visited_set.add(start)
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.grid_height = len(self.grid)
        self.grid_width = len(self.grid[0])
        self.shortest_path = []
        self.shortest_path_p1 = []
        self.order_visited = []
        self.pickup_order_visited = []
        self.walls = []
        self.parents = [[None]*COLS for _ in range(ROWS)]#deepcopy(grid) #will store the coordinates of the parent
        # self.pickup_visited = set()

    def within_boundaries(self, row, col):
        return row >= 0 and row < self.grid_height and \
                col >= 0 and col < self.grid_width \
                and self.weights[row][col] != 0 

    def valid_to_visit(self, row, col):
        return self.within_boundaries(row, col) and \
                (row, col) not in self.visited_set

    def pickup_done(self):
        self.pickup_visited = set(self.visited_set)
        self.visited_set = set()
        self.visited_set.add(self.pickup)
        curr_row, curr_col = self.pickup
        self.grid[curr_row][curr_col] = FOUND
        self.generate_shortest_path()
        self.shortest_path_p1 = self.shortest_path
        self.part1_length = self.shortest_path_length
        self.shortest_path_length = 0
        self.parents = [[None]*COLS for _ in range(ROWS)]
        self.pickup_found = True
    
    # have found target
    def done(self):
        # print("target found")
        # print(self.parents[3][17])
        curr_row, curr_col = self.target
        self.grid[curr_row][curr_col] = FOUND
        self.visited_set = set(self.order_visited)
        # return
        self.generate_shortest_path()
        self.finding_shortest_path = False
        self.drawing_shortest_path = True
        self.found = True
        finish = getattr(self, "finish", None)
        if callable(finish):
            self.finish()

    # This function deals with the repositioning of the target node
    def new_target(self, target):
        #only want the new points visited to grow
        self.target = target
        curr_node_index = 0
        self.grid = [[DONE_PICKUP_VISITING if (row, col) in set(self.pickup_order_visited) else NOT_VISITED for col in range(COLS)] for row in range(ROWS)]
        visited = set()
        while curr_node_index < len(self.order_visited) and self.order_visited[curr_node_index] != target:
            curr_row, curr_col = self.order_visited[curr_node_index]
            visited.add((curr_row, curr_col))
            if (curr_row, curr_col) not in self.visited_set:
                self.grid[curr_row][curr_col] = VISITED
            else:
                self.grid[curr_row][curr_col] = DONE_VISITING
            curr_node_index += 1
        
        found = self.generate_shortest_path()
        self.visited_set = visited
        if not found:
            self.found = False
            return False
        for node_r, node_c in self.shortest_path:
            self.grid[node_r][node_c] = SHORTEST_PATH_NODE
        self.found = True
        return True

    # Generates the shortest path from source to target based on self.parents
    def generate_shortest_path(self):
        self.shortest_path_length = 0
        self.shortest_path = []
        if self.pickup: 
            if self.pickup_found:
                end_at = self.pickup
                start_at = self.target
            else:
                end_at = self.start
                start_at = self.pickup
        else:
            end_at = self.start
            start_at = self.target
        
        while start_at and start_at != end_at:
            #print(start_at, end_at)
            (node_x, node_y) = start_at
            self.shortest_path.append(start_at)
            start_at = self.parents[node_x][node_y]
            self.shortest_path_length += self.weights[node_x][node_y]

        if start_at:
            self.shortest_path.append(start_at)
            self.shortest_path += self.shortest_path_p1
            self.shortest_path_length += self.part1_length
            return True
        else:
            print("not found")
            return False

    # This function steps through the shortest path one node at a time, allowing for a clear animation
    def step_through_shortest_path(self):
       # print("stepping through shortest path")
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
        if self.pickup_found or not self.pickup:
            if self.VISITED:
                (row, col) = self.VISITED
                self.grid[row][col] = VISITED
        else:
            if self.VISITED:
                (row, col) = self.VISITED
                self.grid[row][col] = PICKUP_VISITED
        if self.curr_node:
            (row, col) = self.curr_node
            self.grid[row][col] = CURR_VISITING
            self.VISITED = (row, col)

    def one_step(self):
        if self.pickup and not self.pickup_found:
            # print("seeking pickup")
            self.pickup_step()
        else:
            # print("start seeking target")
            self.target_step()