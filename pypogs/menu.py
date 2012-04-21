import pygame
from pygame.locals import *

from pypogs import render
from pypogs import events

class Menu(object):
    def __init__(self, world, game_container, dimensions):
        self._positions = render.MenuPositions(dimensions[0], dimensions[1])
        self._world = world
        self._game_container = game_container
        self._screens = []

        start_single_option = StartSingleOption(self._positions,
                                                self._world,
                                                self._game_container)
        quit_option = QuitOption(self._positions, self._world)

        init_screen = Screen(self._positions, [start_single_option,
                                               quit_option])

        self._screens.append(init_screen)
        self._current_screen = self._screens[0]

    def handle_event(self, event):
        if not self._world.in_menu():
            return

        self._current_screen.handle_event(event)

    def tick(self):
        pass

    def render(self, screen):
        if not self._world.in_menu():
            return

        self._render_title(screen)
        self._current_screen.render(screen)

    def _render_title(self, screen):
        title_font = self._positions.title_box_font
        title_x = self._positions.title_box_x
        title_y = self._positions.title_box_y
        title_width = self._positions.title_box_width
        title_height = self._positions.title_box_height
        font_color = (255, 255, 255)

        render.render_text_centered(screen, title_font, title_x, title_y,
                                    title_width, title_height,
                                    'PYPOGS', font_color)

class Screen(object):
    def __init__(self, positions, options):
        self._positions = positions
        self._options = options
        self._selected_index = 0

    def render(self, screen):
        x = self._positions.menu_x
        y = self._positions.first_menu_y
        option_spacing = self._positions.menu_spacing

        for i, option in enumerate(self._options):
            is_selected = (i == self._selected_index)
            last_y = option.render(screen, x, y, is_selected)
            y = last_y + option_spacing

    def handle_event(self, event):
        if events.is_move_up_event(event):
            self._move_to_prev_entry()
        elif events.is_move_down_event(event):
            self._move_to_next_entry()
        else:
            self._options[self._selected_index].handle_event(event)

    def _move_to_next_entry(self):
        self._selected_index = min(self._selected_index + 1,
                                   len(self._options) - 1)

    def _move_to_prev_entry(self):
        self._selected_index = max(self._selected_index - 1, 0)

class StartSingleOption(object):
    def __init__(self, positions, world, game_container):
        self._positions = positions
        self._world = world
        self._game_container = game_container

    def render(self, screen, x, y, is_selected):
        menu_width = self._positions.menu_width
        menu_height = self._positions.menu_height

        font = self._positions.menu_font
        if is_selected:
            font_color = (0, 255, 0)
        else:
            font_color = (255, 255, 255)

        render.render_text_centered(screen, font, x, y,
                                    menu_width, menu_height,
                                    'START', font_color)
        return y + menu_height

    def handle_event(self, event):
        if events.is_select_event(event):
            self._game_container.start_new_game(1)
            self._world.switch_to_game()

class QuitOption(object):
    def __init__(self, positions, world):
        self._positions = positions
        self._world = world

    def render(self, screen, x, y, is_selected):
        menu_width = self._positions.menu_width
        menu_height = self._positions.menu_height

        font = self._positions.menu_font
        if is_selected:
            font_color = (0, 255, 0)
        else:
            font_color = (255, 255, 255)

        render.render_text_centered(screen, font, x, y,
                                    menu_width, menu_height,
                                    'QUIT', font_color)
        return y + menu_height

    def handle_event(self, event):
        if events.is_select_event(event):
            self._world.quit()

class ChangeScreenOption(object):
    def __init__(self):
        pass

    def render(self, screen, x, y):
        pass

    def on_event(self, event):
        pass
