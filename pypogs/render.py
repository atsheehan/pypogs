import pygame

FONT_FILENAME = "resources/font.ttf"

class MenuPositions(object):

    def __init__(self, screen_width, screen_height):
        self._screen_width = screen_width
        self._screen_height = screen_height

        self._title_box_font = pygame.font.Font(FONT_FILENAME, 70)
        self._title_box_x = 0
        self._title_box_y = 0
        self._title_box_width = self._screen_width
        self._title_box_height = self._screen_height / 4

        self._menu_font = pygame.font.Font(FONT_FILENAME, 35)
        self._menu_x = 0
        self._first_menu_y = (self._title_box_y + self._title_box_height +
                              (self._screen_height / 10))
        self._menu_width = self._screen_width
        self._menu_height = self._screen_height / 10
        self._menu_spacing = 0

    @property
    def title_box_width(self):
        return self._title_box_width

    @property
    def title_box_height(self):
        return self._title_box_height

    @property
    def title_box_x(self):
        return self._title_box_x

    @property
    def title_box_y(self):
        return self._title_box_y

    @property
    def title_box_font(self):
        return self._title_box_font

    @property
    def menu_font(self):
        return self._menu_font

    @property
    def menu_x(self):
        return self._menu_x

    @property
    def first_menu_y(self):
        return self._first_menu_y

    @property
    def menu_width(self):
        return self._menu_width

    @property
    def menu_height(self):
        return self._menu_height

    @property
    def menu_spacing(self):
        return self._menu_spacing

class GamePositions(object):

    def __init__(self, screen_width, screen_height, player_count = 1):
        self._player_count = player_count
        self._screen_width = screen_width
        self._screen_height = screen_height

        if player_count == 1:
            self._block_size = 32
            self._block_edge_thickness = 4
            self._grid_thickness = 8
            self._text_box_font_size = 40
            self._area_width = self._screen_width
            self._area_height = self._screen_height
            self._anchors = [(0, 0)]
        elif player_count == 2:
            self._block_size = 24
            self._block_edge_thickness = 4
            self._grid_thickness = 4
            self._text_box_font_size = 24
            self._area_width = (self._screen_width // 2)
            self._area_height = self._screen_height
            self._anchors = [(0, 0), (self._area_width, 0)]
        elif player_count == 3:
            self._block_size = 24
            self._block_edge_thickness = 4
            self._grid_thickness = 4
            self._text_box_font_size = 24
            self._area_width = (self._screen_width // 3)
            self._area_height = self._screen_height
            self._anchors = [(0, 0),
                             (self._area_width, 0),
                             (self._area_width * 2, 0)]
        elif player_count == 4:
            self._block_size = 16
            self._block_edge_thickness = 2
            self._grid_thickness = 2
            self._text_box_font_size = 16
            self._area_width = (self._screen_width // 2)
            self._area_height = (self._screen_height // 2)
            self._anchors = [(0, 0),
                             (self._area_width, 0),
                             (0, self._area_height),
                             (self._area_width, self._area_height)]
        elif player_count == 5:
            self._block_size = 16
            self._block_edge_thickness = 2
            self._grid_thickness = 2
            self._text_box_font_size = 16
            self._area_width = (self._screen_width // 3)
            self._area_height = (self._screen_height // 2)
            self._anchors = [(0, 0),
                             (self._area_width, 0),
                             (self._area_width * 2, 0),
                             (0, self._area_height),
                             (self._area_width, self._area_height)]

        elif player_count == 6:
            self._block_size = 16
            self._block_edge_thickness = 2
            self._grid_thickness = 2
            self._text_box_font_size = 16
            self._area_width = (self._screen_width // 3)
            self._area_height = (self._screen_height // 2)
            self._anchors = [(0, 0),
                             (self._area_width, 0),
                             (self._area_width * 2, 0),
                             (0, self._area_height),
                             (self._area_width, self._area_height),
                             (self._area_width * 2, self._area_height)]
        else:
            raise ValueError('Unsupported number of players.')

        self._calculate_positions()

    def grid_x(self, player):
        return self._anchors[player][0] + self._grid_x

    def grid_y(self, player):
        return self._anchors[player][1] + self._grid_y

    def next_piece_x(self, player):
        return self._anchors[player][0] + self._next_piece_x

    def next_piece_y(self, player):
        return self._anchors[player][1] + self._next_piece_y

    def lines_box_x(self, player):
        return self._anchors[player][0] + self._lines_box_x

    def lines_box_y(self, player):
        return self._anchors[player][1] + self._lines_box_y

    def score_box_x(self, player):
        return self._anchors[player][0] + self._score_box_x

    def score_box_y(self, player):
        return self._anchors[player][1] + self._score_box_y

    def level_box_x(self, player):
        return self._anchors[player][0] + self._level_box_x

    def level_box_y(self, player):
        return self._anchors[player][1] + self._level_box_y

    @property
    def block_size(self):
        return self._block_size

    @property
    def grid_width(self):
        return self._grid_width

    @property
    def grid_height(self):
        return self._grid_height

    @property
    def grid_thickness(self):
        return self._grid_thickness

    @property
    def block_edge_thickness(self):
        return self._block_edge_thickness

    @property
    def next_piece_width(self):
        return self._next_piece_width

    @property
    def next_piece_height(self):
        return self._next_piece_height

    @property
    def text_box_width(self):
        return self._text_box_width

    @property
    def text_box_height(self):
        return self._text_box_height

    @property
    def text_box_font(self):
        return self._text_box_font

    def _calculate_positions(self):
        self._grid_width = 10 * self._block_size
        self._grid_height = 20 * self._block_size
        self._grid_x = (self._area_width - self._grid_width) // 2
        self._grid_y = (self._area_height - self._grid_height) // 2
        self._next_piece_width = 5 * self._block_size
        self._next_piece_height = 5 * self._block_size
        self._next_piece_x = (13 * (self._area_width // 16)) - (self._next_piece_width // 2)
        self._next_piece_y = (self._area_height // 4) - (self._next_piece_height // 2)
        self._text_box_width = self._grid_x // 2
        self._text_box_height = self._area_height // 10
        self._text_box_font = pygame.font.Font(FONT_FILENAME, self._text_box_font_size)
        self._lines_box_x = (self._grid_x // 2) - (self._text_box_width // 2)
        self._lines_box_y = (self._area_height // 2) - (self._text_box_height // 2)
        self._score_box_x = (self._grid_x // 2) - (self._text_box_width // 2)
        self._score_box_y = (self._area_height // 4) - (self._text_box_height // 2)
        self._level_box_x = (self._grid_x // 2) - (self._text_box_width // 2)
        self._level_box_y = (3 * self._area_height // 4) - (self._text_box_height // 2)

def render_text_centered(surface, font, x, y, width, height, text, color):
    font_surface = font.render(text, False, color)
    blit_x = x + (width - font_surface.get_width()) // 2
    blit_y = y + (height - font_surface.get_height()) // 2
    surface.blit(font_surface, (blit_x, blit_y))
