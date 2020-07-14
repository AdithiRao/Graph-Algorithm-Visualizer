
NOT_VISITED = 0
JUST_VISITED = 1
VISITED = 2
CURR_VISITING = 3
FOUND = 4

class DFS:
    def __init__(self, start, target, grid):
        self.visited_set = set()
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
        self.order_visited = []
        self.stack = [start]
        self.target = target
        self.grid = grid

    def dfs_one_step(self):
        grid_height = len(self.grid)
        grid_width = len(self.grid[0])
        print(len(self.visited_set))
        if len(self.visited_set) == grid_height*grid_width:
            return (False, True)
        while self.stack:
            curr_x, curr_y = self.stack.pop()
            if (curr_x, curr_y) in self.visited_set:
                continue
            if len(self.order_visited) > 0:
                (recently_visited_x, recently_visited_y) = self.order_visited[-1]
                self.grid[recently_visited_x][recently_visited_y] = JUST_VISITED
            if len(self.order_visited) > 1:
                (past_visited_x, past_visited_y) = self.order_visited[-2]
                self.grid[past_visited_x][past_visited_y] = VISITED

            if (curr_x, curr_y) == self.target:
                self.grid[curr_x][curr_y] = FOUND
                return (True, True)
            self.visited_set.add((curr_x, curr_y))
            self.grid[curr_x][curr_y] = CURR_VISITING
            self.order_visited.append((curr_x, curr_y))
            for dir in self.directions:
                if curr_x+dir[0] >= 0 and curr_x+dir[0] < grid_width and \
                curr_y+dir[1] >= 0 and curr_y+dir[1] < grid_height:
                    if (curr_x+dir[0], curr_y+dir[1]) not in self.visited_set:
                        self.stack.append((curr_x+dir[0], curr_y+dir[1]))
            break
        return (False, False)
