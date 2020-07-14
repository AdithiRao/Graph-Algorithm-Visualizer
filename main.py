
#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
import pygame
from dfs import DFS

# WINDOW_SIZE = [526, 526]
WINDOW_SIZE = [300,300]
# Grid variables
WIDTH = 20
HEIGHT = 20
MARGIN = 1

ROWS = (WINDOW_SIZE[0] - MARGIN) // (HEIGHT+MARGIN)
COLS = (WINDOW_SIZE[1] - MARGIN) // (WIDTH+MARGIN)

NOT_VISITED = 0
CURR_VISITING = 1
VISITED_1_STEP_AGO = 2
VISITED_2_STEPS_AGO = 3
VISITED_3_STEPS_AGO = 4
VISITED_A_WHILE_AGO = 5
FOUND = 6

WHITE = (255,245,238)
GRID_COLOR = (255, 179, 230)
COLORS = {}
COLORS[NOT_VISITED] = WHITE #off-white
COLORS[CURR_VISITING] = (239,98,159)
COLORS[VISITED_1_STEP_AGO] = (239,105,159)
COLORS[VISITED_2_STEPS_AGO] = (239,160,161)
COLORS[VISITED_3_STEPS_AGO] = (238,190,162)
COLORS[VISITED_A_WHILE_AGO] = (238,205,163)
COLORS[FOUND] = (0,205,172)
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(ROWS):
    grid.append([])
    grid[row] = [0]*COLS

pygame.init()


screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Graph Algorithm Visualizer")

done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

start_dfs = True
running_dfs = False
start_pos = (0,0)
target_pos = (4,0)
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did some action
        if event.type == pygame.QUIT:  # If user clicked close
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            print("Click ", pos, "Grid coordinates: ", row, column)

    if start_dfs:
        DFS = DFS(start_pos, target_pos, grid)
        start_dfs = False
        running_dfs = True

    if running_dfs:
        (found, DFSdone) = DFS.dfs_one_step()
        grid = DFS.grid
        if DFSdone:
            running_dfs = False
    # Set the screen background
    screen.fill(GRID_COLOR)

    # Draw the grid
    for row in range(ROWS):
        for column in range(COLS):
            color = WHITE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            color = COLORS[grid[row][column]]
            # print(color)
            if grid[row][column] == CURR_VISITING:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + WIDTH/2,
                                  (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/2,
                                  WIDTH/4,
                                  HEIGHT/4])
            elif grid[row][column] == VISITED_1_STEP_AGO:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + WIDTH/3,
                                  (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/3,
                                  WIDTH/3,
                                  HEIGHT/3])
            elif grid[row][column] == VISITED_2_STEPS_AGO:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + WIDTH/4,
                                  (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/4,
                                  WIDTH/2,
                                  HEIGHT/2])
            elif grid[row][column] == VISITED_3_STEPS_AGO:
                print("here")
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + WIDTH/4,
                                  (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/4,
                                  WIDTH*(3/4),
                                  HEIGHT*(3/4)])
            elif grid[row][column] == VISITED_A_WHILE_AGO:
                # print("here")
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
            elif grid[row][column] == FOUND:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

    # Limit to 60 frames per second
    clock.tick(2)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
