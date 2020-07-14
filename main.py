
#Grid creation citation: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
import pygame
from dfs import DFS

GRID_SIZE = [526, 526]
# GRID_SIZE = [300,300]

MENU_HEIGHT = 200
WINDOW_SIZE = [GRID_SIZE[0], GRID_SIZE[1] + MENU_HEIGHT]
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 25

# Grid variables
WIDTH = 20
HEIGHT = 20
MARGIN = 1

ROWS = (GRID_SIZE[0] - MARGIN) // (HEIGHT+MARGIN)
COLS = (GRID_SIZE[1] - MARGIN) // (WIDTH+MARGIN)

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

start_dfs = False
running_dfs = False
start_pos = (0,0)
target_pos = (12,10)
start_dragging = False
target_dragging = False

# button starterr code: https://pythonprogramming.net/pygame-button-function-events/?completed=/pygame-button-function/

def text_objects(text, font):
    textSurface = font.render(text, True, GRID_COLOR)
    return textSurface, textSurface.get_rect()

def button(screen, msg, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    smallText = pygame.font.Font("freesansbold.ttf",15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x + (width/2)), (y + (height/2)) )
    screen.blit(textSurf, textRect)

def start_DFS():
    global start_dfs
    clear_grid()
    start_dfs = True

def clear_grid():
    global ROWS
    global COLS
    global MARGIN
    global WIDTH
    global HEIGHT
    global COLORS
    global WHITE
    global screen
    global grid
    grid = []
    for row in range(ROWS):
        grid.append([])
        grid[row] = [0]*COLS
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

    if start_dfs:
        dfs = DFS(start_pos, target_pos, grid)
        start_dfs = False
        running_dfs = True

    if running_dfs:
        (found, DFSdone) = dfs.dfs_one_step()
        grid = dfs.grid
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
                # print("here")
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

    # Draw menu buttons
    button(screen, "Start DFS", BUTTON_MARGIN, GRID_SIZE[1] + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT,  WHITE, WHITE, start_DFS)

    # draw start and target nodes
    pygame.draw.circle(screen, START_COLOR, ((MARGIN + WIDTH) * start_pos[1] + WIDTH/2,(MARGIN + HEIGHT) * start_pos[0] + HEIGHT/2), WIDTH/2)
    pygame.draw.circle(screen, TARGET_COLOR, ((MARGIN + WIDTH) * target_pos[1] + WIDTH/2, (MARGIN + HEIGHT) * target_pos[0] + HEIGHT/2), WIDTH/2)

    # Limit frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
