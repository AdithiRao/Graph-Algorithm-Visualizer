
NOT_VISITED = 0
CURR_VISITING = 1
VISITED_1_STEP_AGO = 2
VISITED_2_STEPS_AGO = 3
VISITED_3_STEPS_AGO = 4
VISITED_A_WHILE_AGO = 5
FOUND = 6

class DFS:
    def __init__(self, start, target, grid):
        self.visited_set = set()
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.order_visited = []
        self.stack = [start]
        self.target = target
        self.grid = grid

    def grid_updates(self):
        if len(self.order_visited) > 0:
            (recently_visited_x, recently_visited_y) = self.order_visited[-1]
            self.grid[recently_visited_x][recently_visited_y] = VISITED_1_STEP_AGO
        if len(self.order_visited) > 1:
            print("here")
            (past_visited_x, past_visited_y) = self.order_visited[-2]
            self.grid[past_visited_x][past_visited_y] = VISITED_2_STEPS_AGO
        if len(self.order_visited) > 2:
            (past_visited_x, past_visited_y) = self.order_visited[-3]
            self.grid[past_visited_x][past_visited_y] = VISITED_3_STEPS_AGO
        if len(self.order_visited) > 3:
            (past_visited_x, past_visited_y) = self.order_visited[-4]
            self.grid[past_visited_x][past_visited_y] = VISITED_A_WHILE_AGO

    def dfs_one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        #print(len(self.visited_set))
        print(len(self.order_visited))
        if len(self.visited_set) == grid_height*grid_width:
            return (False, True)
        while self.stack:
            curr_row, curr_col = self.stack.pop()
            if (curr_row, curr_col) in self.visited_set:
                continue
            self.grid_updates()
            if (curr_row, curr_col) == self.target:
                self.grid[curr_row][curr_col] = FOUND
                return (True, True)
            self.visited_set.add((curr_row, curr_col))
            self.grid[curr_row][curr_col] = CURR_VISITING
            self.order_visited.append((curr_row, curr_col))
            for dir in self.directions:
                if curr_row+dir[0] >= 0 and curr_row+dir[0] < grid_width and \
                curr_col+dir[1] >= 0 and curr_col+dir[1] < grid_height:
                    if (curr_row+dir[0], curr_col+dir[1]) not in self.visited_set:
                        self.stack.append((curr_row+dir[0], curr_col+dir[1]))
            break
        return (False, False)
