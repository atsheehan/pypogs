import pygame

class Positions(object):

    FONT_FILENAME = "font.ttf"

    def __init__(self, screen_width, screen_height, player_count = 1):
        self.player_count = player_count
        self.screen_width = screen_width
        self.screen_height = screen_height

        if player_count == 1:
            self.area_width = self.screen_width
            self.area_height = self.screen_height
            self.block_size = 32
            self.block_edge_thickness = 4
            self.grid_width = 10 * self.block_size
            self.grid_height = 20 * self.block_size
            self.grid_thickness = 8
            self.grid_x = (self.area_width - self.grid_width) / 2
            self.grid_y = (self.area_height - self.grid_height) / 2

            self.next_piece_width = 5 * self.block_size
            self.next_piece_height = 5 * self.block_size

            self.next_piece_x = (13 * (self.area_width / 16)) - (self.next_piece_width / 2)
            self.next_piece_y = (self.area_height / 4) - (self.next_piece_height / 2)

            self.text_box_width = self.grid_x / 2
            self.text_box_height = self.area_height / 10

            self.text_box_font_size = 40

            self.text_box_font = pygame.font.Font(self.FONT_FILENAME, self.text_box_font_size)

            self.lines_box_x = (self.grid_x / 2) - (self.text_box_width / 2)
            self.lines_box_y = (self.area_height / 2) - (self.text_box_height / 2)

            self.score_box_x = (self.grid_x / 2) - (self.text_box_width / 2)
            self.score_box_y = (self.area_height / 4) - (self.text_box_height / 2)

            self.level_box_x = (self.grid_x / 2) - (self.text_box_width / 2)
            self.level_box_y = (3 * self.area_height / 4) - (self.text_box_height / 2)

            self.anchors = [(0, 0)]

        elif player_count == 2:
            self.area_width = (self.screen_width / 2)
            self.area_height = self.screen_height
            self.block_size = 24
            self.block_edge_thickness = 4
            self.grid_width = 10 * self.block_size
            self.grid_height = 20 * self.block_size
            self.grid_thickness = 4
            self.grid_x = (self.area_width - self.grid_width) / 2
            self.grid_y = (self.area_height - self.grid_height) / 2

            self.next_piece_width = 5 * self.block_size
            self.next_piece_height = 5 * self.block_size

            self.next_piece_x = (13 * (self.area_width / 16)) - (self.next_piece_width / 2)
            self.next_piece_y = (self.area_height / 4) - (self.next_piece_height / 2)

            self.text_box_width = self.grid_x / 2
            self.text_box_height = self.area_height / 10

            self.text_box_font_size = 24

            self.text_box_font = pygame.font.Font(self.FONT_FILENAME, self.text_box_font_size)

            self.lines_box_x = (self.grid_x / 2) - (self.text_box_width / 2)
            self.lines_box_y = (self.area_height / 2) - (self.text_box_height / 2)

            self.score_box_x = (self.grid_x / 2) - (self.text_box_width / 2)
            self.score_box_y = (self.area_height / 4) - (self.text_box_height / 2)

            self.level_box_x = (self.grid_x / 2) - (self.text_box_width / 2)
            self.level_box_y = (3 * self.area_height / 4) - (self.text_box_height / 2)

            self.anchors = [(0, 0), (self.area_width, 0)]
        else:
            raise ValueError('Unsupported number of players.')

    def get_grid_x(self, player):
        return self.anchors[player][0] + self.grid_x

    def get_grid_y(self, player):
        return self.anchors[player][1] + self.grid_y

    def get_block_size(self):
        return self.block_size

    def get_grid_width(self):
        return self.grid_width

    def get_grid_height(self):
        return self.grid_height

    def get_grid_thickness(self):
        return self.grid_thickness

    def get_block_edge_thickness(self):
        return self.block_edge_thickness

    def get_next_piece_x(self, player):
        return self.anchors[player][0] + self.next_piece_x

    def get_next_piece_y(self, player):
        return self.anchors[player][1] + self.next_piece_y

    def get_next_piece_width(self):
        return self.next_piece_width

    def get_next_piece_height(self):
        return self.next_piece_height

    def get_text_box_width(self):
        return self.text_box_width

    def get_text_box_height(self):
        return self.text_box_height

    def get_lines_box_x(self, player):
        return self.anchors[player][0] + self.lines_box_x

    def get_lines_box_y(self, player):
        return self.anchors[player][1] + self.lines_box_y

    def get_score_box_x(self, player):
        return self.anchors[player][0] + self.score_box_x

    def get_score_box_y(self, player):
        return self.anchors[player][1] + self.score_box_y

    def get_level_box_x(self, player):
        return self.anchors[player][0] + self.level_box_x

    def get_level_box_y(self, player):
        return self.anchors[player][1] + self.level_box_y

    def get_text_box_font(self):
        return self.text_box_font
