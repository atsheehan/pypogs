import time

import pygame

from pypogs import game_container
from pypogs import menu
from pypogs import render

################################################################################
#
# Module Constants

# Possible Supported Resolutions:
# 5:4 = 1280 x 1024
# 4:3 = 1280 x 960
# 16:10 = 1280 x 800
# 16:9 = 1280 x 720

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_DEPTH = 32
TICKS_PER_FRAME = 30
DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

GAME_STATE = 0
MENU_STATE = 1

################################################################################
#
# Class Definition

class World(object):

    def __init__(self):
        self._quit = False
        self._world_objects = []
        self._tick_last_frame = 0

        pygame.init()

        # TODO: play music
        # pygame.mixer.init()
        # pygame.mixer.music.load("music.ogg")
        # pygame.mixer.music.play()

        self._screen = pygame.display.set_mode(DIMENSIONS, 0, SCREEN_DEPTH)
        container = game_container.GameContainer(self, DIMENSIONS)
        game_menu = menu.Menu(self, container, DIMENSIONS)

        self._world_objects.append(container)
        self._world_objects.append(game_menu)

        self._game_state = MENU_STATE
        self._initialize_joysticks()

    def _initialize_joysticks(self):
        for id in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(id)
            joy.init()

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

    def _render(self):
        self._screen.fill((24, 24, 48))
        for obj in self._world_objects:
            obj.render(self._screen)
        pygame.display.update()

    def _wait_til_next_tick(self):
        while pygame.time.get_ticks() - self._tick_last_frame < TICKS_PER_FRAME:
            pass
        self._tick_last_frame = pygame.time.get_ticks()

    def run(self):
        frames = 0
        durations = {'tick': 0, 'events': 0, 'render': 0,
                     'wait': 0, 'work': 0, 'total': 0}

        while not self._quit:
            start = time.clock()
            self._tick()
            after_tick = time.clock()
            self._handle_events()
            after_event = time.clock()
            self._render()
            after_render = time.clock()
            self._wait_til_next_tick()
            after_wait = time.clock()

            frames += 1
            durations['tick'] += after_tick - start
            durations['events'] += after_event - after_tick
            durations['render'] += after_render - after_event
            durations['wait'] += after_wait - after_render
            durations['work'] += after_render - start
            durations['total'] += after_wait - start

        print 'frames', frames
        for k, v in durations.iteritems():
            print "%s, %f (%f)" % (k, v, v / durations['total'])
