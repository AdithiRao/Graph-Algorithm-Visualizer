#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids

'''
@Kanvi
TODO: add to theme.json file to make a theme for GUI elements
TODO: Add ability to add numbers to graph to indicate weights- need to have both positive and negative weights
      before we can implement more advanced graph search algorithms
TODO: Dijkstras

@Adithi
TODO: Improve color scheme
TODO: Add ability to add walls- we can also do the prebuilt maze feature

@General
TODO: When weights are added as a feature, we need to make sure they cannot dfs or bfs
      cannot be clicked
TODO: Create a README
TODO: Stylize main.py and add comments to other files
TODO: Change the icons for start and end (if possible, or else j make prettier)
TODO: Make the currently running algorithm reset if either the target or start changes (they
        should be able to pick up and change source and dest while running)
TODO: Make the number of grid lines an dynamic feature based on rows and cols
TODO: ^ Based on this, if the window gets resized during the game, the grid should auto-adjust
     (make more/less rows and columns)-- By default the screen should be a rectangle though
TODO: Algos to add: Dijkstras, A*, Bellman Ford, Johnsons, Swarm algorithm, bidirectional swarm algorithm
TODO: Allow them to step through one box at a time with a description of what is going on (what was being
      visited on the previous round)

'''
import pygame
import pygame_gui

from constants import *
from currGraphAlgo import CurrGraphAlgorithm

grid = []
for row in range(ROWS):
    grid.append([])
    grid[row] = [0]*COLS

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Graph Algorithm Visualizer")

manager = pygame_gui.UIManager(WINDOW_SIZE)
# manager = pygame_gui.UIManager(WINDOW_SIZE, 'theme.json')

#indicates that the session is still active
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

curr_alg = CurrGraphAlgorithm()

start_pos = (ROWS//2,COLS//3)
target_pos = (ROWS//2,COLS*2//3)
start_dragging = False
target_dragging = False
algo_selected = False
adding_weights = False
curr_spath_node = None

algorithms_list = ["Depth First Search", "Breadth First Search", "Dijkstra's Algorithm", "A*"]
algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(algorithms_list,
                        "Choose an Algorithm!",
                        pygame.Rect((BUTTON_MARGIN, GRID_SIZE[1] + BUTTON_MARGIN), BUTTON_SIZE),
                        manager=manager)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN*2 + BUTTON_WIDTH, GRID_SIZE[1] + BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Start!',
                                            manager=manager)
reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN*3 + BUTTON_WIDTH*2, GRID_SIZE[1] + BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Reset',
                                            manager=manager)
weight_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN, GRID_SIZE[1] + BUTTON_HEIGHT + 2*BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Add Weights',
                                            manager=manager)
done_weights_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN*2 + BUTTON_WIDTH, GRID_SIZE[1] + BUTTON_HEIGHT + 2*BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Done Adding Weights',
                                            manager=manager)
# -------- Main Program Loop -----------
while not done:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():  # User did some action
        if event.type == pygame.QUIT:  # If user clicked close
            done = True

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithms_dropdown:
                    algo_selected = True
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button and algo_selected:
                    curr_alg.update_algorithm((start_pos, target_pos, algorithms_dropdown.selected_option))
                if event.ui_element == reset_button:
                    curr_alg = CurrGraphAlgorithm()
                    grid = curr_alg.newGrid()
                if event.ui_element == weight_button:
                    adding_weights = True
                if event.ui_element == done_weights_button:
                    adding_weights = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            print("Click ", pos, "Grid coordinates: ", row, column)

            if (column == start_pos[1] and row == start_pos[0] and not curr_alg.running):
                start_dragging = True
                start_offset_x = ((MARGIN + WIDTH) * start_pos[1]) - pos[0]
                start_offset_y = ((MARGIN + HEIGHT) * start_pos[0]) - pos[1]

            if (column == target_pos[1] and row == target_pos[0] and not curr_alg.running):
                target_dragging = True
                target_offset_x = ((MARGIN + WIDTH) * target_pos[1]) - pos[0]
                target_offset_y = ((MARGIN + HEIGHT) * target_pos[0]) - pos[1]

            # if (adding_weights):
            #     grid[row][column] = WEIGHTED

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

        manager.process_events(event)

    manager.update(time_delta)

    if curr_alg.running:
        (found, alg_done, curr_spath_node, n_node_dir) = curr_alg.instance.one_step()
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
                                 [(MARGIN + WIDTH) * column + MARGIN + (7/16)*WIDTH,
                                  (MARGIN + HEIGHT) * row + MARGIN + (7/16)*HEIGHT,
                                  WIDTH/8,
                                  HEIGHT/8])
            elif grid[row][column] == VISITED_1_STEP_AGO:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + (3/8)*WIDTH,
                                  (MARGIN + HEIGHT) * row + MARGIN + (3/8)*HEIGHT,
                                  WIDTH/4,
                                  HEIGHT/4])
            elif grid[row][column] == VISITED_2_STEPS_AGO:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + WIDTH/3,
                                  (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/3,
                                  WIDTH/3,
                                  HEIGHT/3])
            elif grid[row][column] == VISITED_3_STEPS_AGO:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + WIDTH/4,
                                  (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/4,
                                  WIDTH/2,
                                  HEIGHT/2])
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

            if curr_spath_node and n_node_dir:
                (curr_spath_row, curr_spath_col) = curr_spath_node
                start_x_pos = (MARGIN + WIDTH)*curr_spath_col+ MARGIN
                start_y_pos = (MARGIN + HEIGHT) * curr_spath_row + MARGIN
                #right arrow
                if n_node_dir == (0, 1):
                    pygame.draw.polygon(screen, ARROW_COLOR,
                    ((start_x_pos, start_y_pos),
                    (start_x_pos+WIDTH, start_y_pos+HEIGHT//2),
                    (start_x_pos, start_y_pos+HEIGHT)))
                elif n_node_dir == (0, -1):
                    pygame.draw.polygon(screen, ARROW_COLOR,
                    ((start_x_pos+WIDTH, start_y_pos),
                    (start_x_pos, start_y_pos+HEIGHT//2),
                    (start_x_pos+WIDTH, start_y_pos+HEIGHT)))
                #up
                elif n_node_dir == (-1, 0):
                    pygame.draw.polygon(screen, ARROW_COLOR,
                    ((start_x_pos, start_y_pos+HEIGHT),
                    (start_x_pos+WIDTH//2, start_y_pos),
                    (start_x_pos+WIDTH, start_y_pos+HEIGHT)))
                elif n_node_dir == (1, 0):
                    pygame.draw.polygon(screen, ARROW_COLOR,
                    ((start_x_pos, start_y_pos),
                    (start_x_pos+WIDTH//2, start_y_pos+HEIGHT),
                    (start_x_pos+WIDTH, start_y_pos)))


    # draw start and target nodes
    pygame.draw.circle(screen, START_COLOR, ((MARGIN + WIDTH) * start_pos[1] + \
                       WIDTH//2,(MARGIN + HEIGHT) * start_pos[0] + HEIGHT//2), WIDTH//2)
    pygame.draw.circle(screen, TARGET_COLOR, ((MARGIN + WIDTH) * target_pos[1] +\
                       WIDTH//2, (MARGIN + HEIGHT) * target_pos[0] + HEIGHT//2), WIDTH//2)
    # Limit frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    manager.draw_ui(screen)
    pygame.display.flip()


pygame.quit()
