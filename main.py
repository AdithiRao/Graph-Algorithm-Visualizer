
#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
import pygame
from dfs import DFS

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (255, 179, 230)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 1

ROWS = 25
COLS = 25

NOT_VISITED = 0
JUST_VISITED = 1
VISITED = 2
CURR_VISITING = 3
FOUND = 4

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(ROWS):
    grid.append([])
    for column in range(COLS):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
# grid[1][5] = 1

pygame.init()

WINDOW_SIZE = [526, 526]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Graph Algorithm Visualizer")

done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

start_dfs = True
running_dfs = False
start_pos = (0,0)
target_pos = (24,24)
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
        #     # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
        #     # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
        #     # Set that location to one
        #     grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)
        if start_dfs:
            DFS = DFS(start_pos, target_pos, grid)
            start_dfs = False
            running_dfs = True

        if running_dfs:
            if DFS.dfs_one_step():
                running_dfs = False
            grid = DFS.grid
    # Set the screen background
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    for row in range(ROWS):
        for column in range(COLS):
            color = WHITE
            if grid[row][column] == JUST_VISITED:
                color = GREEN
            elif grid[row][column] == VISITED:
                color = BLACK
            elif grid[row][column] == CURR_VISITING:
                color = RED
            elif grid[row][column] == FOUND:
                color = BACKGROUND_COLOR
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    print(running_dfs)
    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
