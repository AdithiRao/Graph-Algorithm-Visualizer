from pygame import Color

# GUI Initializations
GRID_SIZE = [1052, 200]
MENU_HEIGHT = 270
WINDOW_SIZE = [GRID_SIZE[0], GRID_SIZE[1] + MENU_HEIGHT]
BUTTON_WIDTH = 225
BUTTON_HEIGHT = 50
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
MINI_BUTTON_SIZE = (100, 50)
WEIGHT_TEXTBOX_SIZE = (50, 50)
WARNING_WINDOW_SIZE = (300, 200)
BUTTON_MARGIN = 15

# Grid cell sizes
WIDTH = 20
HEIGHT = 20
MARGIN = 1

# Number of rows and columns on grid
ROWS = (GRID_SIZE[1] - MARGIN) // (HEIGHT+MARGIN)
COLS = (GRID_SIZE[0] - MARGIN) // (WIDTH+MARGIN)

# Types of nodes 
NOT_VISITED = 0
FOUND = 1
SHORTEST_PATH_NODE = 2
TO_WEIGHT = 3
WEIGHTED = 4
WALL = 5
CURR_VISITING = 6
VISITED = 7
DONE_VISITING = 8

# Growth rate of square of a visited block- takes NUM_COLOR_STEPS to reach full WIDTH and HEIGHT
NUM_COLOR_STEPS = 15
WIDTH_GROWTH_STEP_SIZE = (3*WIDTH)//(4*NUM_COLOR_STEPS)
HEIGHT_GROWTH_STEP_SIZE = (3*HEIGHT)//(4*NUM_COLOR_STEPS)

# Growth rate of square of a shortest path block- takes NUM_SP_COLOR_STEPS to reach full WIDTH and HEIGHT
NUM_SP_COLOR_STEPS = 8
SP_WIDTH = WIDTH + 6*MARGIN
SP_HEIGHT = HEIGHT + 6*MARGIN
WIDTH_SP_GROWTH_STEP_SIZE = (SP_WIDTH - WIDTH//4)//NUM_SP_COLOR_STEPS
HEIGHT_SP_GROWTH_STEP_SIZE = (SP_HEIGHT - HEIGHT//4)//NUM_SP_COLOR_STEPS

# Grid lines and background of menu box color
BACKGROUND_COLOR = Color("#003d47")
# Colors of nodes that have been visited
COLORS = {}
COLORS[NOT_VISITED] = (255,255,255)
COLORS[VISITED] = Color("#ed7a0e")
COLORS[CURR_VISITING] = Color("#a8eb34")
COLORS[DONE_VISITING] = Color("#34ebbd")
COLORS[FOUND] = Color("#80aebe")
COLORS[SHORTEST_PATH_NODE] = Color("#05ffe6")
COLORS[TO_WEIGHT] = Color("#470f00")
COLORS[WEIGHTED] = Color("#61869b")
COLORS[WALL] = Color("#007e80")

# start, target, pickup node colors
START_COLOR = Color("#f3c9e4")
TARGET_COLOR = Color("#10a0cc")
PICKUP_COLOR = Color("#ff6600")

# Shortest path arrow color
ARROW_COLOR = Color("#05ffe6")

# Text used for drawing weights color
TEXT_COLOR = (30, 100, 120)
