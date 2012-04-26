import time

import pygame

from pypogs import game_container
from pypogs import menu
from pypogs import render

TICKS_PER_FRAME = 30

GAME_STATE = 0
MENU_STATE = 1

class World(object):

    def __init__(self):
        self._quit = False
        self._world_objects = []
        self._game_state = MENU_STATE
        pygame.init()

    def in_game(self):
        return self._game_state == GAME_STATE

    def in_menu(self):
        return self._game_state == MENU_STATE

    def quit(self):
        self._quit = True

    def switch_to_game(self):
        self._game_state = GAME_STATE

    def switch_to_menu(self):
        self._game_state = MENU_STATE

    def _tick(self):
        for obj in self._world_objects:
            obj.tick()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            else:
                for obj in self._world_objects:
                    obj.handle_event(event)

    def _wait_til_next_tick(self):
        while pygame.time.get_ticks() - self._tick_last_frame < TICKS_PER_FRAME:
            pass
        self._tick_last_frame = pygame.time.get_ticks()

