from constants import *
import pygame.gfxdraw
import random
import math
import copy

# Returns True if there are no weights on the grid
def no_weights(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != 0 and grid[row][col] != 1:
                return False
    return True

# Returns True if there are any highlighted cells
def highlighted(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == TO_WEIGHT:
                return True
    return False

# Returns True if the point is in range of the grid
def check_in_bounds(point):
    row = point[0]
    column = point[1]
    if column < COLS and row < ROWS and column >= 0 and row >= 0:
        return True
    else:
        return False

# Returns True if there are any negative weights on the grid
def negative_weights(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] < 0:
                return True
    return False

# Creates random positive weights in the range 1-99 for the entire grid
def arb_pos_weights():
    return [[random.randrange(1,99,1) for col in range(COLS)] for row in range(ROWS)]

# Creates arbitrary negative and positive weights in the range -99:1, 1:99
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

# Recursively divides the grid board to create a maze
def recursive_division_maze(start, target):
    grid = [[1 for col in range(COLS)] for row in range(ROWS)]
    orientation = choose_orientation(COLS, ROWS)
    solutions = []
    print("ROWS, COLS", ROWS, COLS)
    grid = divide(solutions, grid, orientation, 0, 0, COLS, ROWS, set())
    grid[start[0]][start[1]] = 1
    grid[target[0]][target[1]] = 1
    return solutions

# Helper method used for recursive_division_maze: chooses the orientation to split across
def choose_orientation(width, height):
    if width < height:
        return 1 #HORIZONTAL
    elif height < width:
        return 0
    return random.randrange(0,1,1)

# Recursive method used for recursive_division_maze- currently broken
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

# Gives the appropriate height corresponding to the row num in the button menu
def MENU_ROW(i):
    return GRID_SIZE[1] + (i-1)*BUTTON_HEIGHT + i*BUTTON_MARGIN

# Gives the appropriate width corresponding to the col num in the button menu
def MENU_COL(i):
    return i*BUTTON_MARGIN + (i-1)*BUTTON_WIDTH

# Returns the rectangle coordinates for a mini square corresponding to the row, col parameters passed in
def base_square(row, col):
    return ((MARGIN + WIDTH) * col + MARGIN + (3*WIDTH)//8, 
                                        (MARGIN + HEIGHT) * row + MARGIN + (3*HEIGHT)//8, 
                                        WIDTH//4, 
                                        HEIGHT//4, 
                                        0)

# Initializes all the sizes_and_steps entries to be of size base square and have a step count of 0
def init_sizes_and_steps(sizes_and_steps):
    for row in range(ROWS):
        for col in range(COLS):
            sizes_and_steps[row][col] = base_square(row, col)
    # return sizes_and_steps

# Returns (r,g,b) of the linear interpolation between the two rgb color vectors passed in
def lerp(v0, v1, t):
    return (max(min(math.floor((1-t)*v0[0]+t*v1[0]), 255), 0), 
            max(min(math.floor((1-t)*v0[1]+t*v1[1]), 255), 0), 
            max(min(math.floor((1-t)*v0[2]+t*v1[2]), 255),0))

# Grows the cell coordinates to create a more visually appealing graphic 
def grow(left, top, width, height, step, left_pos_to_reach, top_pos_to_reach, state):
    if state == DONE_PICKUP_VISITING or state == DONE_VISITING:
        if width == WIDTH or height == HEIGHT:
            return (left, top, WIDTH, HEIGHT, END_COLOR[state])

        new_left = max(left-(WIDTH_GROWTH_STEP_SIZE/2), left_pos_to_reach)
        new_top = max(top-(HEIGHT_GROWTH_STEP_SIZE/2), top_pos_to_reach)
        new_width = min(width+WIDTH_GROWTH_STEP_SIZE, WIDTH)
        new_height = min(height+HEIGHT_GROWTH_STEP_SIZE, HEIGHT)
        
        rgb = (float(COLORS[state].r), float(COLORS[state].g), float(COLORS[state].b))
        target_rgb = (float(END_COLOR[state].r), float(END_COLOR[state].g), float(END_COLOR[state].b))
        new_color = lerp(rgb, target_rgb, step/NUM_COLOR_STEPS)
        print(new_color)
        return (new_left, new_top, new_width, new_height, new_color)
    # Drawing path animation
    else: 
        if width == SP_WIDTH or height == SP_HEIGHT:
            return (left, top, SP_WIDTH, SP_HEIGHT,  COLORS[SHORTEST_PATH_NODE])
        
        new_left = max(left-(WIDTH_SP_GROWTH_STEP_SIZE/2), left_pos_to_reach)
        new_top = max(top-(HEIGHT_SP_GROWTH_STEP_SIZE/2), top_pos_to_reach)
        new_width = min(width+WIDTH_SP_GROWTH_STEP_SIZE, SP_WIDTH)
        new_height = min(height+HEIGHT_SP_GROWTH_STEP_SIZE, SP_HEIGHT)
        return (new_left, new_top, new_width, new_height, COLORS[SHORTEST_PATH_NODE])


# Draws a rectangle with rounded corners
#citation: https://stackoverflow.com/questions/61523241/pygame-button-with-rounded-corners-border-radius-argument-does-not-work
def draw_rounded_rect(surface, rect, color, corner_radius):
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)
