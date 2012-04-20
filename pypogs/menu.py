import pygame
from pygame.locals import *

from pypogs import render

JOY_X_AXIS = 0
JOY_Y_AXIS = 1

JOY_SELECT_BUTTON = 2

class Menu(object):
    def __init__(self, world, game_container, dimensions):
        self._positions = render.MenuPositions(dimensions[0], dimensions[1])
        self._world = world
        self._entries = [{'name': 'START', 'handler': self._start_event},
                         {'name': 'MULTI', 'handler': self._multi_event},
                         {'name': 'QUIT', 'handler': self._quit_event}]
        self._selected_index = 0
        self._game_container = game_container
        self._player_count = 2

    def _multi_event(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self._join_multiplayer_game()
        elif event.type == JOYBUTTONDOWN and event.button == JOY_SELECT_BUTTON:
            self._join_multiplayer_game()

    def _join_multiplayer_game(self):
        pass

    def _start_event(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self._start_new_game()
        elif event.type == JOYBUTTONDOWN and event.button == JOY_SELECT_BUTTON:
            self._start_new_game()

    def _start_new_game(self):
        self._game_container.start_new_game(self._player_count)
        self._world.switch_to_game()

    def _quit_event(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self._post_quit_event()
        elif event.type == JOYBUTTONDOWN and event.button == JOY_SELECT_BUTTON:
            self._post_quit_event()

    def _post_quit_event(self):
        pygame.event.post(pygame.event.Event(QUIT, {}))

    def handle_event(self, event):
        if not self._world.in_menu():
            return

        if event.type == KEYDOWN:
            self._handle_key_event(event)
        elif event.type == JOYBUTTONDOWN:
            self._handle_joy_button_event(event)
        elif event.type == JOYAXISMOTION:
            self._handle_joy_axis_event(event)

    def _handle_key_event(self, event):
        if event.key == K_DOWN:
            self._select_next_entry()
        elif event.key == K_UP:
            self._select_prev_entry()
        else:
            self._entries[self._selected_index]['handler'](event)

    def _handle_joy_button_event(self, event):
        if event.button == JOY_ROTATE_BUTTON:
            pass

    def _handle_joy_axis_event(self, event):
        if event.value < 0.1 and event.value > -0.1:
            return

        if event.axis == JOY_Y_AXIS:
            if event.value > 0:
                self._select_next_entry()
            else:
                self._select_prev_entry()

    def _select_next_entry(self):
        self._selected_index = min(len(self._entries) - 1, self._selected_index + 1)

    def _select_prev_entry(self):
        self._selected_index = max(0, self._selected_index - 1)

    def tick(self):
        pass

    def render(self, screen):
        if not self._world.in_menu():
            return

        title_font = self._positions.title_box_font
        title_x = self._positions.title_box_x
        title_y = self._positions.title_box_y
        title_width = self._positions.title_box_width
        title_height = self._positions.title_box_height

        menu_font = self._positions.menu_font
        menu_x = self._positions.menu_x
        menu_y = self._positions.first_menu_y
        menu_width = self._positions.menu_width
        menu_height = self._positions.menu_height
        menu_spacing = self._positions.menu_spacing

        font_color = (255, 255, 255)
        selected_color = (0, 255, 0)

        render.render_text_centered(screen, title_font, title_x, title_y,
                                    title_width, title_height,
                                    'PYPOGS', font_color)

        for i, entry in enumerate(self._entries):
            if i == self._selected_index:
                color = selected_color
            else:
                color = font_color

            render.render_text_centered(screen, menu_font, menu_x, menu_y,
                                        menu_width, menu_height,
                                        entry['name'], color)
            menu_y += menu_spacing

