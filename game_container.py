from pygame.locals import *
import player_area

class GameContainer(object):

    def __init__(self, world, positions):
        self.player_areas = []
        self.world = world
        self.positions = positions

    def render(self, screen):
        if self.world.get_state() != self.world.GAME_STATE:
            return

        for area in self.player_areas:
            area.render(screen)

    def tick(self):
        if self.world.get_state() != self.world.GAME_STATE:
            return

        if self.is_online:
            self._check_for_server_update()
        else:
            for area in self.player_areas:
                area.tick()

    def handle_event(self, event):
        if self.world.get_state() != self.world.GAME_STATE:
            return

        if event.type == KEYDOWN:
            self._handle_key_event(event.key)
        elif event.type == JOYBUTTONDOWN:
            self._handle_joy_button_down_event(event.button)

        if self.is_online:
            self._send_input_to_server(event)
        else:
            for area in self.player_areas:
                area.handle_event(event)

    def _handle_key_event(self, key):
        if key == K_ESCAPE:
            self.world.set_state(self.world.MENU_STATE)

    def _handle_joy_button_down_event(self, button):
        if button == 4:
            self.world.set_state(self.world.MENU_STATE)

    def start_new_game(self, player_count):
        del self.player_areas[:]
        for player_id in range(player_count):
            self.player_areas.append(player_area.PlayerArea(self.positions, player_id))

    def _check_for_server_update(self):
        pass

    def _send_input_to_server(self):
        pass


