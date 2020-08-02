from constants import *
import random

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

def arb_pos_weights():
    return [[random.randrange(1,99,1) for col in range(COLS)] for row in range(ROWS)]

def arb_weights():
    return [[random.choices([random.randrange(-99,-1,1), random.randrange(1,99,1)])[0] \
            for col in range(COLS)] for row in range(ROWS)]

def no_other_neighbors_visited(grid, visited, new_el, old_el):
    (row, col) = new_el
    for dir in [(-1,0),(0,1),(1,0),(0,-1)]:
        if row+dir[0] >= 0 and row+dir[0] < len(grid) and \
        col+dir[1] >= 0 and col+dir[1] < len(grid[0]) and \
        (row+dir[0], col+dir[1]) in visited and \
        (row+dir[0], col+dir[1]) != old_el:
            return False
    return True

def recursive_backtracking_maze(start, target):
    grid = [[0 for col in range(COLS)] for row in range(ROWS)]
    stack = [start, target]
    visited = set()
    while stack:
        curr_row, curr_col = stack.pop()
        grid[curr_row][curr_col] = 1
        for dir in random.sample([(-1,0),(0,1),(1,0),(0,-1)], 4):
            new_el = (curr_row+dir[0], curr_col+dir[1])
            if new_el[0] >= 0 and new_el[0] < ROWS and \
            new_el[1] >= 0 and new_el[1] < COLS and \
            no_other_neighbors_visited(grid, visited, new_el, (curr_row, curr_col)):
                stack.append((curr_row, curr_col))
                stack.append((curr_row+dir[0], curr_col+dir[1]))
                break
            else:
                visited.add((curr_row+dir[0], curr_col+dir[1]))
        visited.add((curr_row, curr_col))
    grid[target[0]][target[1]] = 1
    return grid

def kruskals_algo_maze(start, target):
    def find(data, i):
        if i != data[i]:
            data[i] = find(data, data[i])
        return data[i]

    def union(data, i, j):
        pi, pj = find(data, i), find(data, j)
        if pi != pj:
            data[pi] = pj
        return
    #the set of all edges would be all blocks that are two steps away from
    #each other
    grid = [[0 for col in range(COLS)] for row in range(ROWS)]
    edges = set()
    ids = {}
    for curr_row in range(ROWS):
        for curr_col in range(COLS):
            ids[(curr_row, curr_col)] = -1
            for dir in [(-2,0),(0,2),(2,0),(0,-2)]:
                new_el = (curr_row+dir[0], curr_col+dir[1])
                if new_el[0] >= 0 and new_el[0] < ROWS and \
                new_el[1] >= 0 and new_el[1] < COLS:
                    #tuple format: (vertex1, vertex2, wall between)
                    if dir == (-2,0):
                        edges.add(((curr_row, curr_col), new_el, (curr_row-1, curr_col)))
                    elif dir == (0,2):
                        edges.add(((curr_row, curr_col), new_el, (curr_row, curr_col+1)))
                    elif dir == (2,0):
                        edges.add(((curr_row, curr_col), new_el, (curr_row+1, curr_col)))
                    elif dir == (0, -2):
                        edges.add(((curr_row, curr_col), new_el, (curr_row, curr_col-1)))

    #go through the edges in a random order
    for edge in random.sample(list(edges), len(edges)):
        #print(edge)
        v1, v2, wall = edge
        #print(ids[v1], ids[v2])
        if ids[v1] != ids[v2]:
            print("here")
            grid[v1[0]][v1[1]] = 1
            grid[v2[0]][v2[1]] = 1
            grid[wall[0]][wall[1]] = 1
            print(grid[v1[0]][v1[1]], grid[v2[0]][v2[1]])
            union(ids, v1, v2)
            union(ids, v1, wall)
    print(grid)
    return grid


def MENU_ROW(i):
    return GRID_SIZE[1] + (i-1)*BUTTON_HEIGHT + i*BUTTON_MARGIN

def MENU_COL(i):
    return i*BUTTON_MARGIN + (i-1)*BUTTON_WIDTH
