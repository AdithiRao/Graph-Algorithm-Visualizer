
GRID_SIZE = [1052, 526]

MENU_HEIGHT = 200

WINDOW_SIZE = [GRID_SIZE[0], GRID_SIZE[1] + MENU_HEIGHT]
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 25

WIDTH = 20
HEIGHT = 20
MARGIN = 1

ROWS = (GRID_SIZE[1] - MARGIN) // (HEIGHT+MARGIN)
COLS = (GRID_SIZE[0] - MARGIN) // (WIDTH+MARGIN)

# start and target node variables
START_COLOR = (208, 229, 245)
TARGET_COLOR = (47, 93, 128)

NOT_VISITED = 0
CURR_VISITING = 1
VISITED_1_STEP_AGO = 2
VISITED_2_STEPS_AGO = 3
VISITED_3_STEPS_AGO = 4
VISITED_A_WHILE_AGO = 5
FOUND = 6
SHORTEST_PATH_NODE = 7

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
COLORS[SHORTEST_PATH_NODE] = (88, 204, 237)

TEXT_COLOR = (30, 100, 120)
