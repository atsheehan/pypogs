import game_container
import pygame
import render
import menu
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

    GAME_STATE = 0
    MENU_STATE = 1

    def __init__(self):
        self.quit = False
        self.world_objects = []
        self.tick_last_frame = 0

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("music.ogg")
        pygame.mixer.music.play()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
                                              0, 32)

        pos = render.Positions(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 2)
        container = game_container.GameContainer(self, pos)
        self.world_objects.append(container)
        self.world_objects.append(menu.Menu(self, container, pos))

        self.game_state = self.MENU_STATE

        for id in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(id)
            joy.init()

    def get_state(self):
        return self.game_state

    def set_state(self, new_state):
        self.game_state = new_state

    def tick(self):
        for obj in self.world_objects:
            obj.tick()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            else:
                for obj in self.world_objects:
                    obj.handle_event(event)

    def render(self):
        self.screen.fill((24, 24, 48))
        for obj in self.world_objects:
            obj.render(self.screen)
        pygame.display.update()

    def wait_til_next_tick(self):
        while pygame.time.get_ticks() - self.tick_last_frame < self.TICKS_PER_FRAME:
            pass
        self.tick_last_frame = pygame.time.get_ticks()

    def run(self):
        frames = 0
        durations = {'tick': 0, 'events': 0, 'render': 0, 'wait': 0, 'work': 0, 'total': 0}

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
            durations['tick'] += after_tick - start
            durations['events'] += after_event - after_tick
            durations['render'] += after_render - after_event
            durations['wait'] += after_wait - after_render
            durations['work'] += after_render - start
            durations['total'] += after_wait - start

        print 'frames', frames
        for k, v in durations.iteritems():
            print "%s, %f (%f)" % (k, v, v / durations['total'])
