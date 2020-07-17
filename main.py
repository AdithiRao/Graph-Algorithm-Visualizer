#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids

'''
@Kanvi
TODO: add good theme.json file to make a theme for GUI elements
TODO: Dijkstras

@Adithi
TODO: Improve color scheme
TODO: Add ability to add walls- we can also do the prebuilt maze feature

@General
TODO: When weights are added as a feature, we need to make sure they cannot dfs or bfs
      cannot be clicked - i don't think this is necessary, they just won't be considered?
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

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Graph Algorithm Visualizer")

manager = pygame_gui.UIManager(WINDOW_SIZE, 'theme.json')

#indicates that the session is still active
done = False

# Used to manage how fast the screen updates
time_elapsed_since_last_action = 0
clock = pygame.time.Clock()

curr_alg = CurrGraphAlgorithm()
grid = curr_alg.newGrid(NOT_VISITED) # initialize empty grid
weights = curr_alg.newGrid(1) # initialize weights

start_pos = (ROWS//2,COLS//3)
target_pos = (ROWS//2,COLS*2//3)
start_dragging = False
target_dragging = False
algo_selected = False
adding_weights = False
adding_walls = True
(found, alg_done, curr_spath_node, n_node_dir) = (False, False, None, None)

algorithms_list = ["Depth First Search", "Breadth First Search", "Dijkstra's Algorithm", "A*"]
algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(algorithms_list,
                        "Choose an Algorithm!",
                        pygame.Rect((BUTTON_MARGIN, GRID_SIZE[1] + BUTTON_MARGIN), BUTTON_SIZE),
                        manager=manager)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN*2 + BUTTON_WIDTH, GRID_SIZE[1] + BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Start!',
                                            manager=manager)
start_button.disable()                                            
reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN*3 + BUTTON_WIDTH*2, GRID_SIZE[1] + BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Reset',
                                            manager=manager)
weight_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN, GRID_SIZE[1] + BUTTON_HEIGHT + 2*BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Add Weights',
                                            manager=manager)
weight_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((BUTTON_MARGIN*2 + BUTTON_WIDTH, GRID_SIZE[1] + BUTTON_HEIGHT + 2*BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            manager=manager)
weight_text_entry.set_allowed_characters(['-','1','2','3','4','5','6','7','8','9','0'])
done_weights_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_MARGIN*3 + BUTTON_WIDTH*2, GRID_SIZE[1] + BUTTON_HEIGHT + 2*BUTTON_MARGIN),
                                            BUTTON_SIZE),
                                            text='Done Adding Weights',
                                            manager=manager)
done_weights_button.disable()

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
                    start_button.enable()

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button and algo_selected:
                    curr_alg.update_algorithm((start_pos, target_pos, algorithms_dropdown.selected_option), grid)
                if event.ui_element == reset_button:
                    curr_alg = CurrGraphAlgorithm()
                    grid = curr_alg.newGrid(NOT_VISITED)
                    weights = curr_alg.newGrid(1)
                if event.ui_element == weight_button:
                    adding_weights = True
                    adding_walls = False
                    start_button.disable()
                    weight_button.disable()
                    done_weights_button.enable()
                if event.ui_element == done_weights_button and weight_text_entry.get_text() != "":
                    adding_weights = False
                    adding_walls = True
                    weight_button.enable()
                    start_button.enable()
                    done_weights_button.disable()
                    for row in range(ROWS):
                        for col in range(COLS):
                            if grid[row][col] == TO_WEIGHT:
                                print(weight_text_entry.get_text())
                                weights[row][col] = int(weight_text_entry.get_text())
                    weight_text_entry.set_text("")
                    for row in range(ROWS):
                        grid[row] = [WEIGHTED if x == TO_WEIGHT else x for x in grid[row]]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            print("Click ", pos, "Grid coordinates: ", row, column)

            if (column == start_pos[1] and row == start_pos[0] and not curr_alg.running):
                start_dragging = True
                start_offset_x = ((MARGIN + WIDTH) * start_pos[1]) - pos[0]
                start_offset_y = ((MARGIN + HEIGHT) * start_pos[0]) - pos[1]

            elif (column == target_pos[1] and row == target_pos[0] and not curr_alg.running):
                target_dragging = True
                target_offset_x = ((MARGIN + WIDTH) * target_pos[1]) - pos[0]
                target_offset_y = ((MARGIN + HEIGHT) * target_pos[0]) - pos[1]

            elif (column < COLS and row < ROWS and column >= 0 and row >= 0):
                if adding_weights:
                    if grid[row][column] != TO_WEIGHT:
                        grid[row][column] = TO_WEIGHT
                    else:
                        grid[row][column] = NOT_VISITED
                if adding_walls:
                    if grid[row][column] != WALL:
                        grid[row][column] = WALL
                        weights[row][column] = 0
                    else:
                        grid[row][column] = NOT_VISITED

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
    time_elapsed_since_last_action += time_delta

    if curr_alg.running:
        if found and not alg_done:
            
            # set all cells that were visited to same color
            for row in range(ROWS):
                grid[row] = [VISITED_A_WHILE_AGO if x != NOT_VISITED and x != SHORTEST_PATH_NODE and x!= FOUND else x for x in grid[row]]
            
            if time_elapsed_since_last_action > 0.05:
                (found, alg_done, curr_spath_node, n_node_dir) = curr_alg.instance.one_step()
                time_elapsed_since_last_action = 0
        else:
            (found, alg_done, curr_spath_node, n_node_dir) = curr_alg.instance.one_step()
        grid = curr_alg.instance.grid
        if alg_done:
            curr_alg.algorithm_done()

    # Set the screen background
    screen.fill(BACKGROUND_COLOR)

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
            
            cell = grid[row][column]
            color = COLORS[cell]

            if cell == CURR_VISITING or cell == VISITED_1_STEP_AGO or cell == VISITED_2_STEPS_AGO or cell == VISITED_3_STEPS_AGO:
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + H_OFFSET[cell],
                                  (MARGIN + HEIGHT) * row + MARGIN + V_OFFSET[cell],
                                  H_SIZE[cell],
                                  V_SIZE[cell]])
            else:
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
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    manager.draw_ui(screen)
    pygame.display.flip()


pygame.quit()
