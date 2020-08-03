from constants import *
import random
import copy

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

def choose_orientation(width, height):
    if width < height:
        return 1 #HORIZONTAL
    elif height < width:
        return 0
    return random.randrange(0,1,1)

def recursive_division_maze(start, target):
    grid = [[1 for col in range(COLS)] for row in range(ROWS)]
    orientation = choose_orientation(COLS, ROWS)
    solutions = []
    print("ROWS, COLS", ROWS, COLS)
    grid = divide(solutions, grid, orientation, 0, 0, COLS, ROWS, set())
    grid[start[0]][start[1]] = 1
    grid[target[0]][target[1]] = 1
    return solutions

def divide(solutions, grid, orientation, x, y, width, height, gaps,
           horizontal_boundary=None, vertical_boundary=None):
    print("new iteration", orientation)
    if width <= 3 or height <= 3:
        print("returning early", width, height)
        return grid

    horizontal = orientation == 1

    if horizontal:
        xpos = x
        px = xpos + random.randrange(width)
        if vertical_boundary:
            ypos = random.choice([random.randrange(y+1, vertical_boundary-1),
                          random.randrange(vertical_boundary+1, height-3)])
            horizontal_boundary = px
        else:
            ypos = y + 1+ random.randrange(height-3)
        py = ypos
        dx = 1
        dy = 0
        length = width
        vertical_boundary = None
    else:
        ypos = y
        py = ypos + random.randrange(height)
        if horizontal_boundary:
            xpos = random.choice([random.randrange(x+1, horizontal_boundary-1),
                          random.randrange(horizontal_boundary+1, width-3)])
            vertical_boundary = py
        else:
            xpos = x + 1 + random.randrange(width-3)
        px = xpos
        dx = 0
        dy = 1
        length = height
        horizontal_boundary = None
    # where will the wall be drawn from?
    # xpos = x + (0 if horizontal else random.randrange(width-2))
    # ypos = y + (random.randrange(height-2) if horizontal else 0)

    # where will the passage through the wall exist?
    # px = xpos + (random.randrange(width) if horizontal else 0)
    # py = ypos + (0 if horizontal else random.randrange(height))
    gaps.add((px, py))

    # what direction will the wall be drawn?
    # dx = 1 if horizontal else 0
    # dy = 0 if horizontal else 1

    # # how long will the wall be?
    # length = width if horizontal else height

    # what direction is perpendicular to the wall?
    # dir = 0 if horizontal else 1

    for i in range(length):
        if (xpos, ypos) not in gaps:
            print(xpos, ypos)
            grid[ypos][xpos] = 0
        xpos += dx
        ypos += dy

    solutions.append(copy.deepcopy(grid))
    nx, ny = x, y
    w, h = [width, ypos-y+1] if horizontal else [xpos-x+1, height]
    grid = divide(solutions, grid, choose_orientation(w, h), nx, ny, w, h, gaps,
            horizontal_boundary, vertical_boundary)

    #nx, ny = x, y
    # nx, ny = [x, py+1] if horizontal else [px+1, y]
    # w, h = [width, ypos-y+1] if horizontal else [xpos-x+1, height]
    # grid = divide(solutions, grid, choose_orientation(w, h), nx, ny, w, h, rec+1)

    # nx, ny = [x, ypos+1] if horizontal else [xpos+1, y]
    # w, h = [width, y+height-ypos-1] if horizontal else [x+width-xpos-1, height]
    # grid = divide(solutions, grid, choose_orientation(w, h), nx, ny, w, h)
    #
    nx, ny = [x, ypos+1] if horizontal else [xpos+1, y]
    w, h = [width, y+height-ypos-1] if horizontal else [x+width-xpos-1, height]
    grid = divide(solutions, grid, choose_orientation(w, h), nx, ny, w, h, gaps,
                 horizontal_boundary, vertical_boundary)
    return grid

def MENU_ROW(i):
    return GRID_SIZE[1] + (i-1)*BUTTON_HEIGHT + i*BUTTON_MARGIN

def MENU_COL(i):
    return i*BUTTON_MARGIN + (i-1)*BUTTON_WIDTH
