#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids

'''
TODO: Need to add arrow that shows path from start to target
TODO: When weights are added as a feature, we need to make sure they cannot dfs or bfs
      cannot be clicked
TODO: Create a README
TODO: Fix the alignment of the mini squares (do the math and make sure they are centered in
      their appropriate boxes)
TODO: Stylize main.py and add comments to other files
TODO: Add hover coloring for buttons
TODO: Change the icons for start and end (if possible, or else j make prettier)
TODO: Make the buttons a little prettier
TODO: Finish migrating all the constants over to constants.py and refactoring main.py accordingly
TODO: Make the currently running algorithm reset if either the target or start changes (they
        should be able to pick up and change source and dest while running)
TODO: Make the number of grid lines an dynamic feature based on rows and cols
TODO: ^ Based on this, if the window gets resized during the game, the grid should auto-adjust
     (make more/less rows and columns)-- By default the screen should be a rectangle though
TODO: Add ability to color graph to indicate weights- need to have both positive and negative weights
      before we can implement more advanced graph search algorithms
TODO: Add ability to add walls- we can also do the prebuilt maze feature
TODO: Algos to add: Dijkstras, A*, Bellman Ford, Johnsons, Swarm algorithm, bidirectional swarm algorithm
TODO: Allow them to step through one box at a time with a description of what is going on (what was being
      visited on the previous round)

'''
import pygame
from currGraphAlgo import CurrGraphAlgorithm
from animations import button
from constants import *

grid = []
for row in range(ROWS):
    grid.append([])
    grid[row] = [0]*COLS

pygame.init()


screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Graph Algorithm Visualizer")

#indicates that the session is still active
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

curr_alg = CurrGraphAlgorithm()

start_pos = (0,0)
target_pos = (12,10)
start_dragging = False
target_dragging = False



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

            if (column == start_pos[1] and row == start_pos[0]):
                start_dragging = True
                start_offset_x = ((MARGIN + WIDTH) * start_pos[1]) - pos[0]
                start_offset_y = ((MARGIN + HEIGHT) * start_pos[0]) - pos[1]

            if (column == target_pos[1] and row == target_pos[0]):
                target_dragging = True
                target_offset_x = ((MARGIN + WIDTH) * target_pos[1]) - pos[0]
                target_offset_y = ((MARGIN + HEIGHT) * target_pos[0]) - pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            start_dragging = False
            target_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if start_dragging:
                start_x = pos[0] + start_offset_x
                start_y = pos[1] + start_offset_y
                temp = (start_y // (HEIGHT + MARGIN), start_x // (WIDTH + MARGIN))
                if temp[0] < 0 or temp[1] < 0 or temp[0] >= ROWS or temp[1] >= COLS:
                    start_pos = start_pos
                else:
                    start_pos = temp
            if target_dragging:
                target_x = pos[0] + target_offset_x
                target_y = pos[1] + target_offset_y
                temp = (target_y // (HEIGHT + MARGIN), target_x // (WIDTH + MARGIN))
                if temp[0] < 0 or temp[1] < 0 or temp[0] >= ROWS or temp[1] >= COLS:
                    target_pos = target_pos
                else:
                    target_pos = temp

    if curr_alg.running:
        (found, alg_done) = curr_alg.instance.one_step()
        grid = curr_alg.instance.grid
        if alg_done:
            curr_alg.algorithm_done()


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
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + WIDTH/4,
                                  (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/4,
                                  WIDTH*(3/4),
                                  HEIGHT*(3/4)])
            elif grid[row][column] == VISITED_A_WHILE_AGO:
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
            elif grid[row][column] == SHORTEST_PATH_NODE:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

    # Draw menu buttons
    button(screen, "Start DFS", BUTTON_MARGIN, GRID_SIZE[1] + BUTTON_MARGIN, \
           BUTTON_WIDTH, BUTTON_HEIGHT,  WHITE, WHITE, \
           curr_alg.update_algorithm, start_pos, target_pos, "DFS")
    button(screen, "Start BFS", 2*BUTTON_MARGIN+BUTTON_WIDTH, GRID_SIZE[1] + \
           BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT,  WHITE, WHITE, \
           curr_alg.update_algorithm, start_pos, target_pos, "BFS")
    button(screen, "Start Dijkstras", 3*BUTTON_MARGIN+2*BUTTON_WIDTH, GRID_SIZE[1] + \
           BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT,  WHITE, WHITE, \
           curr_alg.update_algorithm, start_pos, target_pos, "DIJKSTRAS")
    button(screen, "Start A*", 4*BUTTON_MARGIN+3*BUTTON_WIDTH, GRID_SIZE[1] + \
           BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT,  WHITE, WHITE, \
           curr_alg.update_algorithm, start_pos, target_pos, "ASTAR")

    # draw start and target nodes
    pygame.draw.circle(screen, START_COLOR, ((MARGIN + WIDTH) * start_pos[1] + \
                       WIDTH//2,(MARGIN + HEIGHT) * start_pos[0] + HEIGHT//2), WIDTH//2)
    pygame.draw.circle(screen, TARGET_COLOR, ((MARGIN + WIDTH) * target_pos[1] +\
                       WIDTH//2, (MARGIN + HEIGHT) * target_pos[0] + HEIGHT//2), WIDTH//2)

    # Limit frames per second
    clock.tick(10)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


pygame.quit()
