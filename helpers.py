
def negative_weights(grid):
    neg = False
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] < 0:
                neg = True
                return neg
    return neg

def no_weights(grid):
    no_weights = True
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != 0 or grid[row][col] != 1:
                no_weights = False
                return no_weights
    return no_weights
