import pygame
from pygame.locals import *

from pypogs import render
from pypogs import events
from pypogs import grid

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
        resume_game_option = ResumeGameOption(self._positions,
                                              self._world)
        leave_game_option = ChangeScreenOption(self._positions,
                                               'NEW GAME',
                                               self.change_screen)

        quit_option = QuitOption(self._positions, self._world)

        choose_level_option = ChooseLevelOption(self._positions,
                                                grid.INITIAL_LEVEL,
                                                grid.MAX_LEVEL)

        choose_players_option = ChoosePlayersOption(self._positions, 2, 6)

        start_single_option = StartSingleOption(self._positions,
                                                self._world,
                                                self._game_container,
                                                choose_level_option.get_level,
                                                self.change_screen)

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

        in_game_screen = Screen(self._positions, [resume_game_option,
                                                  leave_game_option,
                                                  quit_option])

        single_player_option.set_destination_screen(single_player_screen)
        multi_player_option.set_destination_screen(multi_player_screen)
        settings_option.set_destination_screen(settings_screen)
        back_to_init_option.set_destination_screen(init_screen)
        start_single_option.set_destination_screen(in_game_screen)
        leave_game_option.set_destination_screen(init_screen)

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


class SingleLineOption(object):
    """
    Represents an option in the menu that can be rendered as a single
    line of text.
    """

    def __init__(self, positions, text_method):
        self._positions = positions
        self._text_method = text_method

    def render(self, screen, x, y, is_selected):
        menu_width = self._positions.menu_width
        menu_height = self._positions.menu_height

        font = self._positions.menu_font
        if is_selected:
            font_color = (0, 255, 0)
        else:
            font_color = (255, 255, 255)

        text = self._text_method()
        render.render_text_centered(screen, font, x, y,
                                    menu_width, menu_height,
                                    text, font_color)
        return y + menu_height



class StartMultiOption(SingleLineOption):
    def __init__(self, positions, world, game_container,
                 get_level_method, get_players_method):
        SingleLineOption.__init__(self, positions, lambda : 'START')
        self._world = world
        self._game_container = game_container
        self._get_level_method = get_level_method
        self._get_players_method = get_players_method

    def handle_event(self, event):
        if events.is_select_event(event):
            players = self._get_players_method()
            self._game_container.start_new_game(players)
            self._world.switch_to_game()

class QuitOption(SingleLineOption):
    def __init__(self, positions, world):
        SingleLineOption.__init__(self, positions, lambda : 'QUIT')
        self._world = world

    def handle_event(self, event):
        if events.is_select_event(event):
            self._world.quit()

class ResumeGameOption(SingleLineOption):
    def __init__(self, positions, world):
        SingleLineOption.__init__(self, positions, lambda : 'RESUME')
        self._world = world

    def handle_event(self, event):
        if events.is_select_event(event):
            self._world.switch_to_game()

class ChangeScreenOption(SingleLineOption):
    def __init__(self, positions, name, change_screen_method):
        SingleLineOption.__init__(self, positions, lambda : name)
        self._change_screen_method = change_screen_method

    def set_destination_screen(self, dest):
        self._destination = dest

    def handle_event(self, event):
        if events.is_select_event(event):
            self._change_screen_method(self._destination)


class StartSingleOption(SingleLineOption):
    def __init__(self, positions, world, game_container,
                 get_level_method, change_screen_method):
        SingleLineOption.__init__(self, positions, lambda : 'START')
        self._world = world
        self._game_container = game_container
        self._get_level_method = get_level_method
        self._change_screen_method = change_screen_method

    def set_destination_screen(self, dest):
        self._destination = dest

    def handle_event(self, event):
        if events.is_select_event(event):
            self._game_container.start_new_game(1)
            self._change_screen_method(self._destination)
            self._world.switch_to_game()


class ChoosePlayersOption(SingleLineOption):
    def __init__(self, positions, min_players, max_players):
        SingleLineOption.__init__(self, positions,
                                  lambda : ("PLAYERS %d" %
                                            self._selected_players))
        self._min_players = min_players
        self._max_players = max_players
        self._selected_players = min_players

    def handle_event(self, event):
        if events.is_move_left_event(event):
            self._selected_players = max(self._min_players,
                                         self._selected_players - 1)
        elif events.is_move_right_event(event):
            self._selected_players = min(self._max_players,
                                         self._selected_players + 1)

    def get_players(self):
        return self._selected_players

class ChooseLevelOption(SingleLineOption):
    def __init__(self, positions, min_level, max_level):
        SingleLineOption.__init__(self, positions,
                                  lambda : ("LEVEL %d" %
                                            self._selected_level))
        self._min_level = min_level
        self._max_level = max_level
        self._selected_level = min_level

    def handle_event(self, event):
        if events.is_move_left_event(event):
            self._selected_level = max(self._min_level,
                                       self._selected_level - 1)
        elif events.is_move_right_event(event):
            self._selected_level = min(self._max_level,
                                       self._selected_level + 1)

    def get_level(self):
        return self._selected_level
