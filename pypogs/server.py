import time

import pygame

from pypogs import game_container
from pypogs import menu
from pypogs import render
from pypogs import world

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_DEPTH = 32
TICKS_PER_FRAME = 30
DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

GAME_STATE = 0
MENU_STATE = 1

class Server(world.World):

    def __init__(self):
        world.World.__init__(self)

    def run(self):
        while not self._quit:
            self._tick()
            self._handle_events()
            self._wait_til_next_tick()
