import pygame
from pygame.locals import *

from pypogs import render
from pypogs import events

import player_area

class Menu(object):
    def __init__(self, world, game_container, dimensions):
        self._positions = render.MenuPositions(dimensions[0], dimensions[1])
        self._world = world
        self._game_container = game_container
        self._init_screens()

    def _init_screens(self):
        single_player_option = ChangeScreenOption(self._positions,
                                                  'SINGLE',
                                                  self.change_screen)
        multi_player_option = ChangeScreenOption(self._positions,
                                                 'MULTI',
                                                 self.change_screen)
        settings_option = ChangeScreenOption(self._positions,
                                             'SETTINGS',
                                             self.change_screen)
        back_to_init_option = ChangeScreenOption(self._positions,
                                                 'BACK',
                                                 self.change_screen)
        quit_option = QuitOption(self._positions, self._world)

        choose_level_option = ChooseLevelOption(self._positions,
                                                player_area.INITIAL_LEVEL,
                                                player_area.MAX_LEVEL)

        choose_players_option = ChoosePlayersOption(self._positions, 2, 6)

        start_single_option = StartSingleOption(self._positions,
                                                self._world,
                                                self._game_container,
                                                choose_level_option.get_level)

        start_multi_option = StartMultiOption(self._positions,
                                              self._world,
                                              self._game_container,
                                              choose_level_option.get_level,
                                              choose_players_option.get_players)

        init_screen = Screen(self._positions, [single_player_option,
                                               multi_player_option,
                                               settings_option,
                                               quit_option])
        single_player_screen = Screen(self._positions, [start_single_option,
                                                        choose_level_option,
                                                        back_to_init_option])
        multi_player_screen = Screen(self._positions, [start_multi_option,
                                                       choose_level_option,
                                                       choose_players_option,
                                                       back_to_init_option])
        settings_screen = Screen(self._positions, [back_to_init_option])

        single_player_option.set_destination_screen(single_player_screen)
        multi_player_option.set_destination_screen(multi_player_screen)
        settings_option.set_destination_screen(settings_screen)
        back_to_init_option.set_destination_screen(init_screen)

        self._current_screen = init_screen

    def handle_event(self, event):
        if not self._world.in_menu():
            return

        self._current_screen.handle_event(event)

    def change_screen(self, new_screen):
        self._current_screen = new_screen

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
                                    'TEST', font_color)

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


# TODO: refactor some of these options

class StartSingleOption(object):
    def __init__(self, positions, world, game_container, get_level_method):
        self._positions = positions
        self._world = world
        self._game_container = game_container
        self._get_level_method = get_level_method

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
            # level = self._get_level_method()
            self._game_container.start_new_game(1)
            self._world.switch_to_game()

class StartMultiOption(object):
    def __init__(self, positions, world, game_container,
                 get_level_method, get_players_method):
        self._positions = positions
        self._world = world
        self._game_container = game_container
        self._get_level_method = get_level_method
        self._get_players_method = get_players_method

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
            # level = self._get_level_method()
            players = self._get_players_method()
            self._game_container.start_new_game(players)
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
    def __init__(self, positions, name, change_screen_method):
        self._positions = positions
        self._name = name
        self._change_screen_method = change_screen_method

    def set_destination_screen(self, dest):
        self._destination = dest

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
                                    self._name, font_color)
        return y + menu_height

    def handle_event(self, event):
        if events.is_select_event(event):
            self._change_screen_method(self._destination)

class ChoosePlayersOption(object):
    def __init__(self, positions, min_players, max_players):
        self._positions = positions
        self._min_players = min_players
        self._max_players = max_players
        self._selected_players = min_players

    def render(self, screen, x, y, is_selected):
        menu_width = self._positions.menu_width
        menu_height = self._positions.menu_height

        font = self._positions.menu_font
        if is_selected:
            font_color = (0, 255, 0)
        else:
            font_color = (255, 255, 255)

        text = "PLAYERS %d" % self._selected_players

        render.render_text_centered(screen, font, x, y,
                                    menu_width, menu_height,
                                    text, font_color)
        return y + menu_height

    def handle_event(self, event):
        if events.is_move_left_event(event):
            self._selected_players = max(self._min_players,
                                         self._selected_players - 1)
        elif events.is_move_right_event(event):
            self._selected_players = min(self._max_players,
                                         self._selected_players + 1)

    def get_players(self):
        return self._selected_players

class ChooseLevelOption(object):
    def __init__(self, positions, min_level, max_level):
        self._positions = positions
        self._min_level = min_level
        self._max_level = max_level
        self._selected_level = min_level

    def render(self, screen, x, y, is_selected):
        menu_width = self._positions.menu_width
        menu_height = self._positions.menu_height

        font = self._positions.menu_font
        if is_selected:
            font_color = (0, 255, 0)
        else:
            font_color = (255, 255, 255)

        text = "LEVEL %d" % self._selected_level

        render.render_text_centered(screen, font, x, y,
                                    menu_width, menu_height,
                                    text, font_color)
        return y + menu_height

    def handle_event(self, event):
        if events.is_move_left_event(event):
            self._selected_level = max(self._min_level,
                                       self._selected_level - 1)
        elif events.is_move_right_event(event):
            self._selected_level = min(self._max_level,
                                       self._selected_level + 1)

    def get_level(self):
        return self._selected_level
