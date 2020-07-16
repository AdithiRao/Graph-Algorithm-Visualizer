# button starter code: https://pythonprogramming.net/pygame-button-function-events/?completed=/pygame-button-function/
import pygame
from constants import TEXT_COLOR

def text_objects(text, font):
    textSurface = font.render(text, True, TEXT_COLOR)
    return textSurface, textSurface.get_rect()

def button(screen, msg, x, y, width, height, inactive_color, active_color, action=None, *args):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            action(args)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    smallText = pygame.font.Font("freesansbold.ttf",15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x + (width/2)), (y + (height/2)) )
    screen.blit(textSurf, textRect)
