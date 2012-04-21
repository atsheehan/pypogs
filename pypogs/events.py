from pygame.locals import *

JOY_X_AXIS = 0
JOY_Y_AXIS = 1
AXIS_THRESHOLD = 10

JOY_SELECT_BUTTON = 2

def is_select_event(event):
    return ((event.type == KEYDOWN and
             event.key == K_RETURN)
            or
            (event.type == JOYBUTTONDOWN and
             event.button == JOY_SELECT_BUTTON))

def is_move_down_event(event):
    return ((event.type == KEYDOWN and
             event.key == K_DOWN)
            or
            (event.type == JOYAXISMOTION and
             event.axis == JOY_Y_AXIS and
             event.value > 0))

def is_move_up_event(event):
    return ((event.type == KEYDOWN and
             event.key == K_UP)
            or
            (event.type == JOYAXISMOTION and
             event.axis == JOY_Y_AXIS and
             event.value < 0))
