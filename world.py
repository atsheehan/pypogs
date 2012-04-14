from player_area import PlayerArea
import pygame
import time

class World(object):

    # Possible Supported Resolutions:
    # 5:4 = 1280 x 1024
    # 4:3 = 1280 x 960
    # 16:10 = 1280 x 800
    # 16:9 = 1280 x 720

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    TICKS_PER_FRAME = 30

    quit = False
    player_areas = []
    tick_last_frame = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
        self.player_areas.append(PlayerArea())

    def tick(self):
        for area in self.player_areas:
            area.tick()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            else:
                for area in self.player_areas:
                    area.handle_event(event)

    def render(self):
        self.screen.fill((24, 24, 48))
        for area in self.player_areas:
            area.render(self.screen)
        pygame.display.update()

    def wait_til_next_tick(self):
        while pygame.time.get_ticks() - self.tick_last_frame < self.TICKS_PER_FRAME:
            pass
        self.tick_last_frame = pygame.time.get_ticks()

    def run(self):
        frames = 0
        durations = {'tick': [], 'events': [], 'render': [], 'wait': [], 'total': []}

        while not self.quit:
            start = time.clock()
            self.tick()
            after_tick = time.clock()
            self.handle_events()
            after_event = time.clock()
            self.render()
            after_render = time.clock()
            self.wait_til_next_tick()
            after_wait = time.clock()

            frames += 1
            durations['tick'].append(after_tick - start)
            durations['events'].append(after_event - after_tick)
            durations['render'].append(after_render - after_event)
            durations['wait'].append(after_wait - after_render)
            durations['total'].append(after_render - start)

        print 'frames', frames
        for k, v in durations.iteritems():
            print k, sum(v) / len(v)
