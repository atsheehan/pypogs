from pygame.locals import *

JOY_X_AXIS = 0
JOY_Y_AXIS = 1

JOY_SELECT_BUTTON = 2

def is_select_event(event):
    return ((event.type == KEYDOWN and
             event.key == K_RETURN)
            or
            (event.type == JOYBUTTONDOWN and
             event.button == JOY_SELECT_BUTTON))
