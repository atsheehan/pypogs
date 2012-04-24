from pygame.locals import *

from pypogs import player_area
from pypogs import render

class GameContainer(object):

    def __init__(self, world, dimensions):
        self._player_areas = []
        self._world = world
        self._dimensions = dimensions

        self._is_online = False

    def render(self, screen):
        if not self._world.in_game():
            return

        for area in self._player_areas:
            area.render(screen)

    def tick(self):
        if not self._world.in_game():
            return

        if self._is_online:
            self._check_for_server_update()
        else:
            for area in self._player_areas:
                area.tick()

    def handle_event(self, event):
        if not self._world.in_game():
            return

        if event.type == KEYDOWN:
            self._handle_key_event(event.key)
        elif event.type == JOYBUTTONDOWN:
            self._handle_joy_button_down_event(event.button)

        if self._is_online:
            self._send_input_to_server(event)
        else:
            for area in self._player_areas:
                area.handle_event(event)

    def _handle_key_event(self, key):
        if key == K_ESCAPE:
            self._world.switch_to_menu()

    def _handle_joy_button_down_event(self, button):
        if button == 4:
            self._world.switch_to_menu()

    def start_new_game(self, player_count):
        del self._player_areas[:]
        posn = render.GamePositions(self._dimensions[0], self._dimensions[1],
                                    player_count)
        for player_id in range(player_count):
            new_area = player_area.PlayerArea(posn, player_id)
            self._player_areas.append(new_area)

    def _check_for_server_update(self):
        pass

    def _send_input_to_server(self):
        pass


