import time

import pygame
from pygame import time

from pypogs import game_container
from pypogs import menu
from pypogs import render

# Possible Supported Resolutions:
# 5:4 = 1280 x 1024
# 4:3 = 1280 x 960
# 16:10 = 1280 x 800
# 16:9 = 1280 x 720

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_DEPTH = 32

DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

FRAME_RATE = 30

GAME_STATE = 0
MENU_STATE = 1

class Client(object):

    def __init__(self):
        self._quit = False
        self._game_state = MENU_STATE

        pygame.init()
        self._clock = time.Clock()
        self._screen = pygame.display.set_mode(DIMENSIONS, 0, SCREEN_DEPTH)

        container = game_container.GameContainer(self, DIMENSIONS)
        game_menu = menu.Menu(self, container, DIMENSIONS)

        self._world_objects = []
        self._world_objects.append(container)
        self._world_objects.append(game_menu)

        self._initialize_joysticks()

    def _initialize_joysticks(self):
        for id in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(id)
            joy.init()

    def in_game(self):
        return self._game_state == GAME_STATE

    def in_menu(self):
        return self._game_state == MENU_STATE

    def switch_to_game(self):
        self._game_state = GAME_STATE

    def switch_to_menu(self):
        self._game_state = MENU_STATE

    def quit(self):
        self._quit = True

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

    def _render(self):
        self._screen.fill((24, 24, 48))
        for obj in self._world_objects:
            obj.render(self._screen)
        pygame.display.update()

    def _wait_til_next_tick(self):
        self._clock.tick(FRAME_RATE)

    def run(self):
        while not self._quit:
            self._tick()
            self._handle_events()
            self._render()
            self._wait_til_next_tick()
