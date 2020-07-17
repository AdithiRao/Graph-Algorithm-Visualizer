from constants import *


class DFS:
    def __init__(self, start, target, grid):
        self.visited_set = set()
        self.directions = [(1,0),(0,1),(-1,0),(0,-1)]
        self.order_visited = []
        self.stack = [start]
        self.target = target
        self.grid = grid
        self.drawing_shortest_path = False

    def step_through_shortest_path(self):
        if len(self.order_visited) > 0:
            (node_x, node_y) = self.order_visited.pop(0)
            self.grid[node_x][node_y] = SHORTEST_PATH_NODE
            if self.order_visited:
                (n_node_x, n_node_y) = self.order_visited[0]
                return (True, False, (node_x, node_y), (n_node_x-node_x, n_node_y-node_y))
            return (True, False, (node_x, node_y), None)
        return (True, True, None, None)

    def grid_updates(self):
        if len(self.order_visited) > 0:
            (recently_visited_x, recently_visited_y) = self.order_visited[-1]
            self.grid[recently_visited_x][recently_visited_y] = VISITED_1_STEP_AGO
        if len(self.order_visited) > 1:
            (past_visited_x, past_visited_y) = self.order_visited[-2]
            self.grid[past_visited_x][past_visited_y] = VISITED_2_STEPS_AGO
        if len(self.order_visited) > 2:
            (past_visited_x, past_visited_y) = self.order_visited[-3]
            self.grid[past_visited_x][past_visited_y] = VISITED_3_STEPS_AGO
        if len(self.order_visited) > 3:
            (past_visited_x, past_visited_y) = self.order_visited[-4]
            self.grid[past_visited_x][past_visited_y] = VISITED_A_WHILE_AGO

    def one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        if self.drawing_shortest_path:
            return self.step_through_shortest_path()
        if len(self.visited_set) == grid_height*grid_width:
            return (False, True, None, None)
        while self.stack:
            curr_row, curr_col = self.stack.pop()
            if (curr_row, curr_col) in self.visited_set:
                continue
            self.grid_updates()
            if (curr_row, curr_col) == self.target:
                self.grid[curr_row][curr_col] = FOUND
                self.drawing_shortest_path = True
                return (True, False, None, None)

            self.visited_set.add((curr_row, curr_col))
            self.grid[curr_row][curr_col] = CURR_VISITING
            self.order_visited.append((curr_row, curr_col))
            for dir in self.directions:
                if curr_row+dir[0] >= 0 and curr_row+dir[0] < grid_height and \
                curr_col+dir[1] >= 0 and curr_col+dir[1] < grid_width:
                    if (curr_row+dir[0], curr_col+dir[1]) not in self.visited_set:
                        self.stack.append((curr_row+dir[0], curr_col+dir[1]))
            break
        return (False, False, None, None)
