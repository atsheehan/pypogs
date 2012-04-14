import pygame

class Positions(object):

    FONT_FILENAME = "font.ttf"

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    AREA_WIDTH = SCREEN_WIDTH
    AREA_HEIGHT = SCREEN_HEIGHT

    BLOCK_SIZE = 32

    BLOCK_EDGE_THICKNESS = 4

    GRID_WIDTH = 10 * BLOCK_SIZE
    GRID_HEIGHT = 20 * BLOCK_SIZE

    GRID_THICKNESS = 8

    GRID_X = (AREA_WIDTH - GRID_WIDTH) / 2
    GRID_Y = (AREA_HEIGHT - GRID_HEIGHT) / 2

    NEXT_PIECE_WIDTH = 5 * BLOCK_SIZE
    NEXT_PIECE_HEIGHT = 5 * BLOCK_SIZE

    NEXT_PIECE_X = (13 * (AREA_WIDTH / 16)) - (NEXT_PIECE_WIDTH / 2)
    NEXT_PIECE_Y = (AREA_HEIGHT / 4) - (NEXT_PIECE_HEIGHT / 2)

    TEXT_BOX_WIDTH = GRID_X / 2
    TEXT_BOX_HEIGHT = AREA_HEIGHT / 10

    TEXT_BOX_FONT_SIZE = 40

    LINES_BOX_X = (GRID_X / 2) - (TEXT_BOX_WIDTH / 2)
    LINES_BOX_Y = (AREA_HEIGHT / 2) - (TEXT_BOX_HEIGHT / 2)

    SCORE_BOX_X = (GRID_X / 2) - (TEXT_BOX_WIDTH / 2)
    SCORE_BOX_Y = (AREA_HEIGHT / 4) - (TEXT_BOX_HEIGHT / 2)

    LEVEL_BOX_X = (GRID_X / 2) - (TEXT_BOX_WIDTH / 2)
    LEVEL_BOX_Y = (3 * AREA_HEIGHT / 4) - (TEXT_BOX_HEIGHT / 2)



    def __init__(self):
        self._text_box_font = pygame.font.Font(self.FONT_FILENAME, self.TEXT_BOX_FONT_SIZE)

    def grid_x(self, player):
        return self.GRID_X

    def grid_y(self, player):
        return self.GRID_Y

    def block_size(self):
        return self.BLOCK_SIZE

    def grid_width(self):
        return self.GRID_WIDTH

    def grid_height(self):
        return self.GRID_HEIGHT

    def grid_thickness(self):
        return self.GRID_THICKNESS

    def block_edge_thickness(self):
        return self.BLOCK_EDGE_THICKNESS

    def next_piece_x(self):
        return self.NEXT_PIECE_X

    def next_piece_y(self):
        return self.NEXT_PIECE_Y

    def next_piece_width(self):
        return self.NEXT_PIECE_WIDTH

    def next_piece_height(self):
        return self.NEXT_PIECE_HEIGHT

    def lines_box_x(self):
        return self.LINES_BOX_X

    def lines_box_y(self):
        return self.LINES_BOX_Y

    def text_box_width(self):
        return self.TEXT_BOX_WIDTH

    def text_box_height(self):
        return self.TEXT_BOX_HEIGHT

    def lines_box_x(self):
        return self.LINES_BOX_X

    def lines_box_y(self):
        return self.LINES_BOX_Y

    def score_box_x(self):
        return self.SCORE_BOX_X

    def score_box_y(self):
        return self.SCORE_BOX_Y

    def level_box_x(self):
        return self.LEVEL_BOX_X

    def level_box_y(self):
        return self.LEVEL_BOX_Y

    def text_box_font(self):
        return self._text_box_font
