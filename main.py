#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids

'''
@Kanvi
TODO: Drag to highlight and enter weights into cells
TODO: add good theme.json file to make a theme for GUI elements
TODO: Swarm, bidirectional swarm (I couldn't find anything about these)- text me when you get here,
      I would do everything else first. Maybe just look up bidirectional search
TODO: Add speed label to the speed slider
TODO: Get scroll bar to work on text box
TODO: Add x and y axis with numbers 
TODO: Have an info popup showing how to use everything 
TODO: Change the icons for start and end (if possible, or else j make prettier)
TODO: Fix the rendering time
TODO: Fix color scheme of search to go with gui colors

@Adithi
TODO: Deal with case where the target is moved into an unreachable spot
TODO: Path should be cleared before being allowed to change algos
TODO: FIx a*, not working with the weights
TODO: drawing the path for dfs
TODO: If there were weights before and no longer are, need to address
TODO: Add builtin graphs (one with negative cycles, maze)
TODO: Somehow increase the max speed
TODO: Add feature to first visit other node
TODO: Johnsons

@General
TODO: Stylize main.py and add comments to other files


'''
import pygame
import pygame_gui


import time
from constants import *
from helpers import *
from currGraphAlgo import CurrGraphAlgorithm

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Graph Algorithm Visualizer")

manager = pygame_gui.UIManager(WINDOW_SIZE, 'theme.json', enable_live_theme_updates=True)

#indicates that the session is still active
done = False


# Used to manage how fast the screen updates
time_elapsed_since_last_action1 = 0
time_elapsed_since_last_action2 = 0
clock = pygame.time.Clock()

curr_alg = CurrGraphAlgorithm()
grid = curr_alg.newGrid(NOT_VISITED) # initialize empty grid
sizes_and_steps = [[None for _ in range(COLS)] for _ in range(ROWS)]
init_sizes_and_steps(sizes_and_steps) 

weights = curr_alg.newGrid(1) # initialize weights

font = pygame.font.SysFont('couriernewttf', 2*HEIGHT//3)
start_pos = (ROWS//2,COLS//3)
target_pos = (ROWS//2,COLS*2//3)
start_dragging = False
target_dragging = False
algo_selected = False
adding_weights = False
building_mazes = []
adding_walls = True
speed = 0.001
step_to_be_made = False

algorithms_list = ["Depth First Search", "Breadth First Search", "Dijkstra's",
                    "A*", "Bellman Ford", "Johnsons", "Greedy BFS"]
algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(algorithms_list,
                        "Choose an Algorithm!",
                        pygame.Rect((MENU_COL(1), MENU_ROW(1)), BUTTON_SIZE),
                        manager=manager)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(2), MENU_ROW(1)),
                                            BUTTON_SIZE),
                                            text='Start!',
                                            manager=manager)
start_button.disable()

clear_all_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(1),
                                            MENU_ROW(4)),
                                            BUTTON_SIZE),
                                            text='Clear All',
                                            manager=manager)
clear_weights_walls_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(2),
                                            MENU_ROW(4)),
                                            BUTTON_SIZE),
                                            text='Clear Weights/Walls',
                                            manager=manager)
clear_path_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(3),
                                            MENU_ROW(4)),
                                            BUTTON_SIZE),
                                            text='Clear Path',
                                            manager=manager)

speed_button = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(pygame.Rect((MENU_COL(3),
                                    MENU_ROW(1)),
                                    (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                    start_value=0.001,
                                    value_range=(0.1, 0.001),
                                    manager = manager)

step_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(4),
                                                    MENU_ROW(1)),
                                                    MINI_BUTTON_SIZE),
                                                    text='Step',
                                                    manager=manager)
step_button.hide()
weight_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(1),
                                            MENU_ROW(2)),
                                            BUTTON_SIZE),
                                            text='Add Weights',
                                            manager=manager)
weight_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((MENU_COL(2)+BUTTON_WIDTH//2 - WEIGHT_TEXTBOX_SIZE[0]//2, 
                                            MENU_ROW(2)+BUTTON_HEIGHT//5),
                                            WEIGHT_TEXTBOX_SIZE),
                                            manager=manager)
weight_text_entry.set_allowed_characters(['-','1','2','3','4','5','6','7','8','9','0'])
weight_text_entry.set_text_length_limit(3)
weight_text_entry.hide()
done_weights_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(1), MENU_ROW(2)),
                                            BUTTON_SIZE),
                                            text='Done Adding Weights',
                                            manager=manager)
done_weights_button.hide()
info_box = pygame_gui.elements.ui_text_box.UITextBox(html_text="Run an algorithm!",
                                            relative_rect=pygame.Rect((MENU_COL(4),
                                            MENU_ROW(2)),
                                            (WARNING_WINDOW_SIZE[0], 5*WARNING_WINDOW_SIZE[1]//7)),
                                            manager=manager)

example_graphs_list = ["Arbitrary Positive Weights", "Arbitrary Weights", "Negative Cycles",
                       "Maze: Rec Backtracking", "Maze: Rec Division"]
graphs_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(example_graphs_list,
                        "Builtin Graphs",
                        pygame.Rect((MENU_COL(1), MENU_ROW(3)), BUTTON_SIZE),
                        manager=manager)

heuristics_list = ["Heuristic: Euclidean Dst.", "Heuristic: Manhattan Dst."]
heuristics_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(heuristics_list,
                        "Heuristic: Euclidean Dst.",
                        pygame.Rect((MENU_COL(2), MENU_ROW(3)), BUTTON_SIZE),
                        manager=manager)
heuristics_dropdown.hide()
weights_warning_window = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect(((GRID_SIZE[0]-WARNING_WINDOW_SIZE[0])//2,
                                            (GRID_SIZE[1]-WARNING_WINDOW_SIZE[1])//2),
                                            WARNING_WINDOW_SIZE),
                                            html_message="You have selected an search algorithm that "\
                                                      "does not work with weights. Please clear the "\
                                                      "weights on the grid or choose a different algorithm.",
                                            window_title="Weights Not Allowed",
                                            manager=manager)
weights_warning_window.hide()
neg_weights_warning_window = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect(((GRID_SIZE[0]-WARNING_WINDOW_SIZE[0])//2,
                                            (GRID_SIZE[1]-WARNING_WINDOW_SIZE[1])//2),
                                            WARNING_WINDOW_SIZE),
                                            html_message="You have selected an search algorithm that"\
                                                      "does not work with negative weights. Please clear the"\
                                                      "negative weights on the grid or choose a different algorithm.",
                                            window_title="Negative Weights Not Allowed",
                                            manager=manager)
neg_weights_warning_window.hide()


def enable_all():
    start_button.enable()
    algorithms_dropdown.enable()
    weight_button.enable()
    clear_all_button.enable()
    clear_path_button.enable()
    clear_weights_walls_button.enable()
    heuristics_dropdown.enable()
    graphs_dropdown.enable()
    info_box.enable()
    step_button.enable()
    speed_button.enable()

def disable_all():
    start_button.disable()
    algorithms_dropdown.disable()
    weight_button.disable()
    clear_all_button.disable()
    clear_path_button.disable()
    clear_weights_walls_button.disable()
    heuristics_dropdown.disable()
    graphs_dropdown.disable()
    info_box.disable()
    step_button.disable()
    speed_button.disable()

# -------- Main Program Loop -----------
while not done:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():  # User did some action
        if event.type == pygame.QUIT:  # If user clicked close
            done = True

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithms_dropdown and not adding_weights:
                    algo_selected = True
                    start_button.enable()
                    curr_alg.update_description(algorithms_dropdown.selected_option)
                    curr_alg.instance = None
                    if algorithms_dropdown.selected_option == "A*" or \
                        algorithms_dropdown.selected_option == "Greedy BFS":
                        heuristics_dropdown.show()
                    else:
                        heuristics_dropdown.hide()
                elif event.ui_element == heuristics_dropdown:
                    curr_alg.heuristic = heuristics_dropdown.selected_option
                    curr_alg.update_description(algorithms_dropdown.selected_option)
                elif event.ui_element == graphs_dropdown:
                    if graphs_dropdown.selected_option == "Arbitrary Positive Weights":
                        weights = arb_pos_weights()
                    elif graphs_dropdown.selected_option == "Arbitrary Weights":
                        weights = arb_weights()
                    elif graphs_dropdown.selected_option == "Maze: Rec Backtracking":
                        weights = recursive_backtracking_maze(start_pos, target_pos)
                    elif graphs_dropdown.selected_option == "Maze: Rec Division":
                        building_mazes = recursive_division_maze(start_pos, target_pos)
                        building_mazes.reverse()
                        # for maze in building_mazes:
                        #     weights = maze
            speed = speed_button.get_current_value()
            if speed == 0.1:
                step_button.show()
            else:
                step_button.hide()

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == weights_warning_window.dismiss_button or \
                   event.ui_element == weights_warning_window.close_window_button:
                    weights_warning_window.hide()
                    adding_walls = True
                    enable_all()
                if event.ui_element == neg_weights_warning_window.dismiss_button or \
                   event.ui_element == neg_weights_warning_window.close_window_button:
                    neg_weights_warning_window.hide()
                    adding_walls = True
                    enable_all()
                if event.ui_element == start_button and algo_selected:
                    if (not no_weights(weights)) and \
                        (algorithms_dropdown.selected_option == "Breadth First Search" or\
                        algorithms_dropdown.selected_option == "Depth First Search"):
                        weights_warning_window.show()
                        adding_walls = False
                        disable_all()
                        weight_button.disable()
                        clear_weights_walls_button.disable()
                    elif negative_weights(weights) and \
                        algorithms_dropdown.selected_option == "Dijkstra's" or\
                        algorithms_dropdown.selected_option == "A*: Euclidean Distance" or\
                        algorithms_dropdown.selected_option == "A*: Manhattan Distance":
                        neg_weights_warning_window.show()
                        adding_walls = False
                        disable_all()
                        weight_button.disable()
                        clear_weights_walls_button.disable()
                    else:
                        grid = curr_alg.newGrid(NOT_VISITED)
                        init_sizes_and_steps(sizes_and_steps)
                        curr_alg.start_algorithm((start_pos, target_pos),
                                                    grid, weights)
                        adding_walls = False
                        adding_weights = False
                        weight_button.disable()
                        clear_weights_walls_button.disable()
                if event.ui_element == clear_all_button:
                    grid = curr_alg.newGrid(NOT_VISITED)
                    weights = curr_alg.newGrid(1)
                    adding_walls = True
                    adding_weights = False
                    weight_button.enable()
                    clear_weights_walls_button.enable()
                if event.ui_element == clear_path_button:
                    grid = curr_alg.newGrid(NOT_VISITED)
                if event.ui_element == clear_weights_walls_button:
                    weights = curr_alg.newGrid(1)
                if event.ui_element == weight_button:
                    adding_weights = True
                    adding_walls = False
                    start_button.disable()
                    weight_button.hide()
                    weight_text_entry.show()
                    done_weights_button.show()
                if event.ui_element == done_weights_button and weight_text_entry.get_text() != "":
                    adding_weights = False
                    adding_walls = True
                    done_weights_button.hide()
                    weight_text_entry.hide()
                    weight_button.show()
                    start_button.enable()
                    for row in range(ROWS):
                        for col in range(COLS):
                            if grid[row][col] == TO_WEIGHT:
                                weights[row][col] = int(weight_text_entry.get_text())
                    weight_text_entry.set_text("")
                    for row in range(ROWS):
                        grid[row] = [NOT_VISITED if x == TO_WEIGHT else x for x in grid[row]]
                    # if not no_weights(weights):
                    #
                    # if negative_weights(weights):

                if event.ui_element == step_button:
                    step_to_be_made = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

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
                    if weights[row][column] != 0:
                        weights[row][column] = 0
                    else:
                        weights[row][column] = 1

        elif event.type == pygame.MOUSEBUTTONUP:
            start_dragging = False
            target_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if start_dragging:
                start_x = pos[0] + start_offset_x
                start_y = pos[1] + start_offset_y
                temp = (start_y // (HEIGHT + MARGIN), start_x // (WIDTH + MARGIN))
                if temp[0] < 0 or temp[1] < 0 or temp[0] >= ROWS or temp[1] >= COLS or weights[temp[0]][temp[1]] == 0:
                    start_pos = start_pos
                else:
                    start_pos = temp
            if target_dragging:
                target_x = pos[0] + target_offset_x
                target_y = pos[1] + target_offset_y
                temp = (target_y // (HEIGHT + MARGIN), target_x // (WIDTH + MARGIN))
                if temp[0] < 0 or temp[1] < 0 or temp[0] >= ROWS or temp[1] >= COLS or weights[temp[0]][temp[1]] == 0:
                    target_pos = target_pos
                else:
                    target_pos = temp

        manager.process_events(event)

    manager.update(time_delta)
    time_elapsed_since_last_action1 += time_delta
    time_elapsed_since_last_action2 += time_delta
    if time_elapsed_since_last_action2 > 1 and building_mazes:
        weights = building_mazes.pop()
        time_elapsed_since_last_action2 = 0
        print("here", len(building_mazes))

    if curr_alg.running and time_elapsed_since_last_action1 > speed:
        if curr_alg.instance.drawing_shortest_path:

            # set all cells that were visited to same color
            # for row in range(ROWS):
            #     grid[row] = [VISITED_A_WHILE_AGO if x != NOT_VISITED and x != SHORTEST_PATH_NODE and x!= FOUND else x for x in grid[row]]

            # We are currently drawing the shortest path
            if time_elapsed_since_last_action1 > 0.05:
                curr_alg.instance.one_step()
                shortest_pweight = curr_alg.instance.shortest_path_length
                curr_node = curr_alg.instance.curr_node
                time_elapsed_since_last_action1 = 0
                info_box.html_text = "Now drawing shortest path of weight/length {}".format(shortest_pweight)
                info_box.rebuild()
        else: #either needs to start or already started calculating the shortest path
            if speed != 0.1 or step_to_be_made:
                curr_alg.instance.one_step()
                shortest_pweight = curr_alg.instance.shortest_path_length
                curr_node = curr_alg.instance.curr_node
                if curr_alg.alg_name == 'Breadth First Search' or curr_alg.alg_name == 'Depth First Search':
                    info_box.html_text = "Iteration: {} <br>Now visiting: {}".format(shortest_pweight, curr_node)
                else:
                    info_box.html_text = "Weight: {} <br>Now visiting: {}".format(shortest_pweight, curr_node)
                info_box.rebuild()
                if speed != 0.1:
                    time_elapsed_since_last_action1 = 0
                else:
                    step_to_be_made = False
        grid = curr_alg.instance.grid
    elif not curr_alg.running and curr_alg.alg_chosen and curr_alg.instance: #logic doesn't work
        if curr_alg.instance.found:
            info_box.html_text = "Done running {}. Shortest path found had weight {}".format(curr_alg.alg_name, shortest_pweight)
            info_box.rebuild()
        else:
            info_box.html_text = "The target node could not be reached from the source vertex."
            info_box.rebuild()
    elif not curr_alg.running and curr_alg.alg_chosen:
        info_box.html_text = curr_alg.description
        info_box.rebuild()

    if curr_alg.instance and curr_alg.running and not curr_alg.instance.drawing_shortest_path and not curr_alg.instance.finding_shortest_path:
        curr_alg.algorithm_done()

    #If there was an algorithm running before and the graph is not empty and the target has changed
    #  Then call new_target(target) -> can always check if target == curr_alg.instance.target
    if not curr_alg.running and curr_alg.alg_chosen and (not no_weights(grid)) and curr_alg.alg_name != "Johnsons":
        start_dragging = False 
    if not curr_alg.running and curr_alg.alg_chosen and not no_weights(grid) and curr_alg.instance and target_pos != curr_alg.instance.target:
        if curr_alg.alg_name != "A*" and curr_alg.alg_name != "Greedy BFS":
            curr_alg.instance.new_target(target_pos)
            grid = curr_alg.instance.grid
        else: #For heuristic based algorithms it does not make sense to set a new target
            target_dragging = False


    # Set the screen background
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    for row in range(ROWS):
        for column in range(COLS):
            #need to rewrite this part
            color = WHITE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

            cell = grid[row][column]
            weight_cell = weights[row][column]
            if weight_cell == 0:
                color = COLORS[WALL]
            else:
                color = COLORS[cell]

            cell_left = (MARGIN + WIDTH) * column + MARGIN
            cell_top = (MARGIN + HEIGHT) * row + MARGIN

            if cell == VISITED:
                (left, top, width, height, step) = sizes_and_steps[row][column]
                (left, top, width, height, color) = grow(left, top, width, height, step,
                                                        cell_left, cell_top, VISITED)
                sizes_and_steps[row][column] = (left, top, width, height, min(step+1, NUM_COLOR_STEPS))
                rect = pygame.Rect(left, top, width, height)
                if width == WIDTH and height == HEIGHT:
                    draw_rounded_rect(screen, rect, color, 0)
                else:
                    draw_rounded_rect(screen, rect, color, min(width, height)//3)
            elif cell == SHORTEST_PATH_NODE and (row, column) != curr_node:
                target_left = cell_left - 4*MARGIN
                target_top = cell_top  - 4*MARGIN
                (left, top, width, height, step) = sizes_and_steps[row][column]
                if step == NUM_COLOR_STEPS:
                    (left, top, width, height, step) = base_square(row, column)
                (left, top, width, height, color) = grow(left, top, width, height, step,
                                                        target_left, target_top, SHORTEST_PATH_NODE)
                sizes_and_steps[row][column] = (left, top, width, height, min(step+1, NUM_SP_COLOR_STEPS))
                rect = pygame.Rect(left, top, width, height)
                if width == WIDTH + 6*MARGIN and height == HEIGHT + 6*MARGIN:
                    draw_rounded_rect(screen, rect, color, 0)
                else:
                    draw_rounded_rect(screen, rect, color, min(width, height)//3)
            elif not (curr_alg.running and curr_alg.instance.drawing_shortest_path and (row, column) == curr_node):
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

            if weights[row][column] != 0 and weights[row][column] != 1:
                surf = font.render(str(weights[row][column]), True, (0,0,0))
                rectangle = surf.get_rect()
                rectangle.center = ((MARGIN + WIDTH) * column + MARGIN + WIDTH/2, (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/2)
                screen.blit(surf, rectangle)

    if curr_alg.running and curr_alg.instance.drawing_shortest_path:
        (curr_spath_row, curr_spath_col) = curr_node
        n_node_dir = curr_alg.instance.n_node_dir
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
    clock.tick(100)

    # Go ahead and update the screen with what we've drawn.
    manager.draw_ui(screen)
    pygame.display.flip()


pygame.quit()
