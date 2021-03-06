#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids

'''
@Adithi
TODO: drawing the path for dfs
TODO: Add builtin graphs (one with negative cycles, maze, unreachable areas, 4x4 blocks)
TODO: Bellmanford color seems weird- one weird one
TODO: Need to figure out what to do with bellman ford negative cycles
TODO: Johnsons

TODO: Make the drawing speed of shortest path faster when more nodes 
TODO: Improve the rendering time, increase the max speed
TODO: Have an info popup showing how to use everything
TODO: Swarm, bidirectional swarm 
TODO: Get scroll bar to work on text box
TODO: Stylize main.py and add comments to other files
TODO: Add speed label to the speed slider
TODO: Redesign menu order/location/sizing
TODO: Documentation and unittests 


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

# Used to manage how fast the screen updates
time_elapsed_since_last_action1 = 0
time_elapsed_since_last_action2 = 0
clock = pygame.time.Clock()

curr_alg = CurrGraphAlgorithm()
grid = curr_alg.newGrid(NOT_VISITED) # initialize empty grid
sizes_and_steps = [[None for _ in range(COLS)] for _ in range(ROWS)]
init_sizes_and_steps(sizes_and_steps) 

weights = curr_alg.newGrid(1) # initialize weights
done = False

# Various animation run-time variables
font = pygame.font.SysFont('couriernewttf', 2*HEIGHT//3)
# start_pos = (ROWS//2,COLS//3)
# target_pos = (ROWS//2,COLS*2//3)
# pickup_pos = (-1, -1)
start_pos = (4,16)
target_pos = (4, 23)
pickup_pos = (2, 19)
start_dragging = False
target_dragging = False
pickup_dragging = False
algo_selected = False
adding_weights = False
building_mazes = []
adding_walls = True
speed = 0.001
path_drawing_speed = 0.05
step_to_be_made = False
highlighting = False
erase_highlighting = False
info_box_message = "Run an algorithm!"
shortest_pweight = ""
curr_node = None

# Button initializations
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

step_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(3) + BUTTON_WIDTH//4,
                                                    MENU_ROW(2)),
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

pickup_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MENU_COL(2),
                                            MENU_ROW(3)),
                                            BUTTON_SIZE),
                                            text='Add Pickup',
                                            manager=manager)

start_recentered = (start_pos[1], ROWS-start_pos[0]-1)
target_recentered = (target_pos[1], ROWS-target_pos[0]-1)
info_text = "Start: {} <br>Target: {} <br> <br>{}".format(start_recentered, target_recentered, info_box_message)
info_box = pygame_gui.elements.ui_text_box.UITextBox(html_text=info_text,
                                            relative_rect=pygame.Rect((MENU_COL(4),
                                            MENU_ROW(1)),
                                            INFO_BOX_SIZE),
                                            manager=manager)

example_graphs_list = ["Arbitrary Positive Weights", "Arbitrary Weights", "Negative Cycles",
                       "Maze: Rec Backtracking", "Maze: Rec Division"]
graphs_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(example_graphs_list,
                        "Builtin Graphs",
                        pygame.Rect((MENU_COL(1), MENU_ROW(3)), BUTTON_SIZE),
                        manager=manager)

heuristics_list = ["Heuristic: Euclidean Dst.", "Heuristic: Manhattan Dst.", "Heuristic: Chebyshev Dst.",
                    "Heuristic: Octile Dst."]
heuristics_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(heuristics_list,
                        "Heuristic: Euclidean Dst.",
                        pygame.Rect((MENU_COL(3), MENU_ROW(3)), BUTTON_SIZE),
                        manager=manager)
heuristics_dropdown.hide()
weights_warning_window = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect(((GRID_SIZE[0]-WARNING_WINDOW_SIZE[0])//2,
                                            (GRID_SIZE[1]-WARNING_WINDOW_SIZE[1]+ MENU_HEIGHT)//2),
                                            WARNING_WINDOW_SIZE),
                                            html_message="You have selected an search algorithm that "\
                                                      "does not work with weights. Please clear the "\
                                                      "weights on the grid or choose a different algorithm.",
                                            window_title="Weights Not Allowed",
                                            manager=manager)
weights_warning_window.hide()
neg_weights_warning_window = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect(((GRID_SIZE[0]-WARNING_WINDOW_SIZE[0])//2,
                                            (GRID_SIZE[1]-WARNING_WINDOW_SIZE[1]+ MENU_HEIGHT)//2),
                                            WARNING_WINDOW_SIZE),
                                            html_message="You have selected an search algorithm that"\
                                                      "does not work with negative weights. Please clear the"\
                                                      "negative weights on the grid or choose a different algorithm.",
                                            window_title="Negative Weights Not Allowed",
                                            manager=manager)
neg_weights_warning_window.hide()


# Enables all buttons
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
    pickup_button.enable()

# Disables all buttons
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
    pickup_button.disable()

def clear_path():
    global grid
    grid = curr_alg.newGrid(NOT_VISITED)

def clear_weights():
    global weights
    weights = curr_alg.newGrid(1)

# Draws all the nodes the color they're supposed to be
def draw_grid():
    global grid
    for row in range(ROWS):
        for column in range(COLS):
            color = WHITE
            pygame.draw.rect(screen,
                            color,
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH,
                            HEIGHT])

            #growing is messed up
            if grid[row][column] == VISITED: 
                sizes_and_steps[row][column] = base_square(row, column)
                grid[row][column] = DONE_VISITING
            elif grid[row][column] == PICKUP_VISITED:
                sizes_and_steps[row][column] = base_square(row, column)
                grid[row][column] = DONE_PICKUP_VISITING

            cell = grid[row][column]
            weight_cell = weights[row][column]
            if weight_cell == 0:
                color = COLORS[WALL]
            else:
                color = COLORS[cell]

            cell_left = (MARGIN + WIDTH) * column + MARGIN
            cell_top = (MARGIN + HEIGHT) * row + MARGIN

            if cell == DONE_PICKUP_VISITING or cell == DONE_VISITING:
                (left, top, width, height, step) = sizes_and_steps[row][column]
                (left, top, width, height, color) = grow(left, top, width, height, step,
                                                        cell_left, cell_top, cell)
                sizes_and_steps[row][column] = (left, top, width, height, min(step+1, NUM_COLOR_STEPS))
                rect = pygame.Rect(left, top, width, height)
                if width == WIDTH and height == HEIGHT:
                    draw_rounded_rect(screen, rect, color, 0)
                else:
                    draw_rounded_rect(screen, rect, color, min(width, height)//3)
            elif cell == SHORTEST_PATH_NODE and (row, column) != curr_node:
                target_left = cell_left #- 4*MARGIN
                target_top = cell_top  #- 4*MARGIN
                (left, top, width, height, step) = sizes_and_steps[row][column]
                if step == NUM_COLOR_STEPS:
                    (left, top, width, height, step) = base_square(row, column)
                (left, top, width, height, color) = grow(left, top, width, height, step,
                                                        target_left, target_top, SHORTEST_PATH_NODE)
                sizes_and_steps[row][column] = (left, top, width, height, min(step+1, NUM_SP_COLOR_STEPS))
                rect = pygame.Rect(left, top, width, height)
                if width == SP_WIDTH and height == SP_HEIGHT:
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

            if weight_cell != 0 and weight_cell != 1:
                surf = font.render(str(weight_cell), True, (0,0,0))
                rectangle = surf.get_rect()
                rectangle.center = ((MARGIN + WIDTH) * column + MARGIN + WIDTH/2, (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/2)
                screen.blit(surf, rectangle)

# Draws the shortest path arrow
def draw_arrow():
    global curr_node, curr_alg
    (curr_spath_row, curr_spath_col) = curr_node
    n_node_dir = curr_alg.instance.n_node_dir
    start_x_pos = (MARGIN + WIDTH)*curr_spath_col+ MARGIN
    start_y_pos = (MARGIN + HEIGHT) * curr_spath_row + MARGIN

    if n_node_dir == (0, 1): #right arrow
        pygame.draw.polygon(screen, ARROW_COLOR,
        ((start_x_pos, start_y_pos),
        (start_x_pos+WIDTH, start_y_pos+HEIGHT//2),
        (start_x_pos, start_y_pos+HEIGHT)))
    elif n_node_dir == (0, -1): #left arrow
        pygame.draw.polygon(screen, ARROW_COLOR,
        ((start_x_pos+WIDTH, start_y_pos),
        (start_x_pos, start_y_pos+HEIGHT//2),
        (start_x_pos+WIDTH, start_y_pos+HEIGHT)))
    elif n_node_dir == (-1, 0): #up arrow
        pygame.draw.polygon(screen, ARROW_COLOR,
        ((start_x_pos, start_y_pos+HEIGHT),
        (start_x_pos+WIDTH//2, start_y_pos),
        (start_x_pos+WIDTH, start_y_pos+HEIGHT)))
    elif n_node_dir == (1, 0): #down arrow
        pygame.draw.polygon(screen, ARROW_COLOR,
        ((start_x_pos, start_y_pos),
        (start_x_pos+WIDTH//2, start_y_pos+HEIGHT),
        (start_x_pos+WIDTH, start_y_pos)))

# start arrow code 
def draw_start():
    global start_pos
    center_x = (MARGIN + WIDTH) * start_pos[1] + WIDTH//2
    center_y = (MARGIN + HEIGHT) * start_pos[0] + HEIGHT//2
    points = [(center_x, center_y),(center_x - WIDTH // 2, center_y - HEIGHT // 2),(center_x + WIDTH // 2, center_y), (center_x - WIDTH // 2, center_y + HEIGHT // 2)]
    pygame.draw.polygon(screen, START_COLOR, points)

# draws pickup node if it is supposed to be on the board
def draw_pickup():
    global pickup_pos
    if pickup_pos != (-1, -1):
        pygame.draw.circle(screen, PICKUP_COLOR, ((MARGIN + WIDTH) * pickup_pos[1] + MARGIN + \
                    WIDTH//2,(MARGIN + HEIGHT) * pickup_pos[0] +MARGIN + HEIGHT//2), WIDTH//2, width=5)

# target star code
def draw_target():
    global target_pos
    num_points = 5
    points = []
    center_x = (MARGIN + WIDTH) * target_pos[1] + WIDTH//2
    center_y = (MARGIN + HEIGHT) * target_pos[0] + HEIGHT//2
    angle = (360/num_points) * 2
    for i in range(num_points*2 + 2):
        r = WIDTH/2
        if i % 2 == 0:
            r = r // 2 
        x = r * math.cos(angle * i) + center_x
        y = r * math.sin(angle * i) + center_y
        points.append((x,y))
    pygame.draw.polygon(screen, TARGET_COLOR, points)

#Updates the text box with start, target, pickup locations + the algo specific message
def update_text_box():
    start_recentered = (start_pos[1], ROWS-start_pos[0]-1)
    pickup_recentered = (pickup_pos[1], ROWS-pickup_pos[0]-1)
    target_recentered = (target_pos[1], ROWS-target_pos[0]-1)
    if pickup_pos == (-1, -1):
        info = "Start: {} <br>Target: {} <br> <br>".format(start_recentered, target_recentered)
    else:
        info = "Start: {} <br>Pickup: {} <br>Target: {} <br> <br>".format(start_recentered, pickup_recentered, target_recentered)
    info += info_box_message
    info_box.html_text = info
    info_box.rebuild()

# Drags pickup, target and start if it is an appropriate position
def drag(offset_x, offset_y, name):
    global start_pos, pickup_pos, target_pos, grid, weights, adding_weights, adding_walls
    pos = pygame.mouse.get_pos()
    x = pos[0] + offset_x
    y = pos[1] + offset_y
    temp = (y // (HEIGHT + MARGIN), x // (WIDTH + MARGIN))
    if check_in_bounds(temp) and weights[temp[0]][temp[1]] != 0:
        if name == "start":
            start_pos = temp  
        elif name == "pickup":
            pickup_pos = temp
        elif name == "target":
            target_pos = temp
        elif name == "highlight":
            if adding_weights:
                if highlighting and grid[temp[0]][temp[1]] != TO_WEIGHT:
                    grid[temp[0]][temp[1]] = TO_WEIGHT
                elif erase_highlighting:
                    grid[temp[0]][temp[1]] = NOT_VISITED
            elif adding_walls:
                if highlighting and weights[temp[0]][temp[1]] != 0 and temp != start_pos and temp != target_pos:
                    weights[temp[0]][temp[1]] = 0
                elif erase_highlighting:
                    weights[temp[0]][temp[1]] = 1

# Creates the appropriate maze 
def maze_options():
    global curr_alg, grid, weights, building_mazes
    curr_alg.algorithm_done()
    grid = curr_alg.newGrid(NOT_VISITED)
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

# Deals with all the weight related actions
def weight_action():
    global adding_weights, adding_walls, info_box_message, grid, weights
    if not adding_weights:
        adding_weights = True
        adding_walls = False
        start_button.disable()
        weight_text_entry.show()
        weight_button.set_text("Done")
    else:
        # A valid weight must be entered before being able to return to the normal mode
        if (weight_text_entry.get_text() == "" or int(weight_text_entry.get_text()) < -99 or int(weight_text_entry.get_text()) > 99) and highlighted(grid):
            info_box_message = "Enter a weight from -99 to 99"
        else:
            info_box_message = "Run an algorithm!"
            adding_weights = False
            adding_walls = True
            start_button.enable()
            weight_text_entry.hide()
            weight_button.set_text("Add Weights")
            for row in range(ROWS):
                for col in range(COLS):
                    if grid[row][col] == TO_WEIGHT:
                        weights[row][col] = int(weight_text_entry.get_text())
            weight_text_entry.set_text("")
            for row in range(ROWS):
                grid[row] = [NOT_VISITED if x == TO_WEIGHT else x for x in grid[row]]

# Starts the algorithm if the graph is of the right format for the alg chosen
def start_alg():
    global weights, adding_walls, adding_weights, size_and_steps, start_pos, target_pos, pickup_pos, grid
    if (not no_weights(weights)) and \
        (algorithms_dropdown.selected_option == "Breadth First Search" or\
        algorithms_dropdown.selected_option == "Depth First Search"):
        weights_warning_window.show()
        adding_walls = False
        disable_all()
        weight_button.disable()
        clear_weights_walls_button.disable()
    # Negative weights don't work with Dijkstras, A* or best first search
    elif negative_weights(weights) and \
        (algorithms_dropdown.selected_option == "Dijkstra's" or\
        algorithms_dropdown.selected_option == "A*" or\
        algorithms_dropdown.selected_option == "Greedy BFS"):
        neg_weights_warning_window.show()
        adding_walls = False
        disable_all()
        weight_button.disable()
        clear_weights_walls_button.disable()
    else:
        clear_path()
        init_sizes_and_steps(sizes_and_steps)
        curr_alg.start_algorithm((start_pos, target_pos, pickup_pos),
                                    grid, weights)
        adding_walls = False
        adding_weights = False
        weight_button.disable()
        clear_weights_walls_button.disable()

# Takes the appropriate algorithm step
def algo_step():
    global curr_alg, time_elapsed_since_last_action1, info_box_message, grid, curr_node, shortest_pweight, step_to_be_made
    # Algorithm is running (either calculating the shortest path or drawing it) and it is appropriate to take a step now based
    # on the time delay

    if curr_alg.running and time_elapsed_since_last_action1 > speed:
        if curr_alg.instance.drawing_shortest_path:
            # We are currently drawing the shortest path
            if time_elapsed_since_last_action1 > path_drawing_speed: #speed of path drawing
                curr_alg.instance.one_step()
                shortest_pweight = curr_alg.instance.shortest_path_length
                curr_node = curr_alg.instance.curr_node
                time_elapsed_since_last_action1 = 0
                info_box_message = "Now drawing shortest path of weight/length {}".format(shortest_pweight)
        else: #either needs to start or already started calculating the shortest path
            if speed != 0.1 or step_to_be_made:
                curr_alg.instance.one_step()
                shortest_pweight = curr_alg.instance.shortest_path_length
                curr_node = curr_alg.instance.curr_node
                if curr_alg.alg_name == 'Breadth First Search' or curr_alg.alg_name == 'Depth First Search':
                    info_box_message = "Iteration: {} <br>Now visiting: {}".format(shortest_pweight, (curr_node[1], ROWS-curr_node[0]-1))
                else:
                    info_box_message = "Weight: {} <br>Now visiting: {}".format(shortest_pweight, (curr_node[1], ROWS-curr_node[0]-1))
                if speed != 0.1:
                    time_elapsed_since_last_action1 = 0
                else:
                    step_to_be_made = False
        grid = curr_alg.instance.grid
    elif not curr_alg.running and curr_alg.alg_chosen and curr_alg.instance: #logic doesn't work
        if curr_alg.instance.found:
            shortest_pweight = curr_alg.instance.shortest_path_length
            info_box_message = "Done running {}. Shortest path found had weight {}".format(curr_alg.alg_name, shortest_pweight)
        else:
            info_box_message = "The target node could not be reached from the source vertex."

    elif not curr_alg.running and curr_alg.alg_chosen:
        info_box_message = curr_alg.description

    if curr_alg.instance and curr_alg.running and not curr_alg.instance.drawing_shortest_path and not curr_alg.instance.finding_shortest_path:
        curr_alg.running = False

    # If there was an algorithm running before and the target has changed 
    #  Then call new_target(target) -> can always check if target == curr_alg.instance.target
    # no_weights(grid) checks if any of the colors are on the board
  #  if not curr_alg.running and curr_alg.alg_chosen and (not no_weights(grid)) and curr_alg.alg_name != "Johnsons":
   #     start_dragging = False 
    if not curr_alg.running and curr_alg.alg_chosen and curr_alg.instance and target_pos != curr_alg.instance.target:
        if curr_alg.instance.new_target(target_pos): #this recalculates this way too often
            shortest_pweight = curr_alg.instance.shortest_path_length
            info_box_message = "Done running {}. Shortest path found had weight {}".format(curr_alg.alg_name, shortest_pweight)
        else:
            info_box_message = "The target node could not be reached from the source vertex."
        grid = curr_alg.instance.grid
        # curr_alg.instance.target = target_pos # Is this necessary?

# main game play while loop
def main():
    global done, time_elapsed_since_last_action1, time_elapsed_since_last_action2, clock, \
    curr_alg, grid, weights, sizes_and_steps, font, start_pos, target_pos, pickup_pos, \
    start_dragging, target_dragging, pickup_dragging, algo_selected, adding_weights, \
    building_mazes, adding_walls, speed, step_to_be_made, highlighting, erase_highlighting, \
    info_box_message, screen, manager, curr_node
   
    while not done:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():  # User did some action
            if event.type == pygame.QUIT:  # If user clicked close
                done = True

            # All the dropdown actions
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == algorithms_dropdown and not adding_weights:
                        algo_selected = True
                        start_button.enable()
                        grid = curr_alg.newGrid(NOT_VISITED)
                        curr_alg.update_description(algorithms_dropdown.selected_option)
                        curr_alg.algorithm_done()
                        if algorithms_dropdown.selected_option == "A*" or \
                            algorithms_dropdown.selected_option == "Greedy BFS":
                            heuristics_dropdown.show()
                        else:
                            heuristics_dropdown.hide()
                    elif event.ui_element == heuristics_dropdown:
                        curr_alg.heuristic = heuristics_dropdown.selected_option
                        curr_alg.update_description(algorithms_dropdown.selected_option)
                    elif event.ui_element == graphs_dropdown:
                        maze_options()
                        
                speed = speed_button.get_current_value()
                if speed == 0.1:
                    step_button.show()
                else:
                    step_button.hide()

                # Other button based actions
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == weights_warning_window.dismiss_button or \
                    event.ui_element == weights_warning_window.close_window_button:
                        weights_warning_window.hide()
                        adding_walls = True
                        enable_all()
                    elif event.ui_element == neg_weights_warning_window.dismiss_button or \
                    event.ui_element == neg_weights_warning_window.close_window_button:
                        neg_weights_warning_window.hide()
                        adding_walls = True
                        enable_all()
                    elif event.ui_element == start_button and algo_selected:
                        # Weights don't work with bfs or dfs
                        start_alg()
                    elif event.ui_element == clear_all_button:
                        curr_alg.algorithm_done() 
                        clear_path()
                        clear_weights()
                        adding_walls = True
                        adding_weights = False
                        weight_button.enable()
                        clear_weights_walls_button.enable()
                    elif event.ui_element == clear_path_button:
                        curr_alg.algorithm_done() 
                        clear_path()
                    elif event.ui_element == clear_weights_walls_button:
                        curr_alg.algorithm_done() 
                        clear_weights()
                    # Allows users to add weights to the grid
                    elif event.ui_element == weight_button:
                        weight_action()

                    elif event.ui_element == step_button:
                        step_to_be_made = True
                    # Pickup is the position to visit before the target is visited
                    elif event.ui_element == pickup_button:
                        if pickup_button.text == "Add Pickup":
                            pickup_button.set_text("Remove Pickup")
                            pickup_pos = (ROWS//4, COLS//2)
                        else:
                            pickup_button.set_text("Add Pickup")
                            pickup_pos = (-1, -1)
                        clear_path()

            # Part of the dragging functionality (source, target, pickup) is handled here, as well as highlighting
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)

                if column == target_pos[1] and row == target_pos[0] and not curr_alg.running:
                    # cannot move target in greedy bfs and A* cases
                    if curr_alg.alg_chosen and curr_alg.instance != None and (curr_alg.alg_name == "A*" or curr_alg.alg_name == "Greedy BFS"):
                        target_dragging = False
                    else:
                        target_dragging = True
                        target_offset_x = ((MARGIN + WIDTH) * target_pos[1]) - pos[0]
                        target_offset_y = ((MARGIN + HEIGHT) * target_pos[0]) - pos[1]

                elif (column == start_pos[1] and row == start_pos[0] and not curr_alg.running):
                    if curr_alg.alg_chosen and curr_alg.instance != None and curr_alg.alg_name != "Johnsons":
                        start_dragging = False
                    else:
                        start_dragging = True
                        start_offset_x = ((MARGIN + WIDTH) * start_pos[1]) - pos[0]
                        start_offset_y = ((MARGIN + HEIGHT) * start_pos[0]) - pos[1]

                elif (column == pickup_pos[1] and row == pickup_pos[0]):
                    if curr_alg.alg_chosen and curr_alg.instance != None and curr_alg.alg_name != "Johnsons":
                        pickup_dragging = False
                    else:
                        pickup_dragging = True
                        pickup_offset_x = ((MARGIN + WIDTH) * pickup_pos[1]) - pos[0]
                        pickup_offset_y = ((MARGIN + HEIGHT) * pickup_pos[0]) - pos[1]

                elif check_in_bounds((row, column)):
                    if adding_weights or adding_walls:
                        if adding_weights:
                            if grid[row][column] != TO_WEIGHT:
                                grid[row][column] = TO_WEIGHT
                                highlighting = True
                            else:
                                grid[row][column] = NOT_VISITED
                                erase_highlighting = True
                        elif adding_walls:
                            if weights[row][column] != 0:
                                weights[row][column] = 0
                                highlighting = True
                            else:
                                weights[row][column] = 1
                                erase_highlighting = True

            # Done dragging and highlighting
            elif event.type == pygame.MOUSEBUTTONUP:
                start_dragging = False
                target_dragging = False
                pickup_dragging = False
                highlighting = False
                erase_highlighting = False

            # Updates the position as the user moves an object or highlights cells
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if start_dragging:
                    drag(start_offset_x, start_offset_y, "start")
                elif target_dragging:
                    drag(target_offset_x, target_offset_y, "target")
                elif pickup_dragging:
                    drag(pickup_offset_x, pickup_offset_y, "pickup")           
                elif highlighting or erase_highlighting:
                    drag(0, 0, "highlight")
                        
            manager.process_events(event)

        manager.update(time_delta)
        time_elapsed_since_last_action1 += time_delta
        time_elapsed_since_last_action2 += time_delta

        if time_elapsed_since_last_action2 > 1 and building_mazes:
            weights = building_mazes.pop()
            time_elapsed_since_last_action2 = 0
            print("here", len(building_mazes))

        # takes the appropriate algorithm step if there is one currently running
        algo_step()

        # Set the screen background
        screen.fill(BACKGROUND_COLOR)

        #Updates the text box
        update_text_box()

        # Draws the grid with the weights and colors on display
        draw_grid()

        if curr_alg.running and curr_alg.instance.drawing_shortest_path:
            draw_arrow()

        # draw start, pickup and target nodes
        draw_start()
        draw_pickup()
        draw_target()
       

        # Limit frames per second
        clock.tick(100)

        # Go ahead and update the screen with what we've drawn.
        manager.draw_ui(screen)
        pygame.display.flip()


    pygame.quit()

if __name__ == '__main__':
    main()
