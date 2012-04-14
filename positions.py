class Positions(object):

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

    NEXT_PIECE_WIDTH = 6 * BLOCK_SIZE
    NEXT_PIECE_HEIGHT = 6 * BLOCK_SIZE

    NEXT_PIECE_X = (3 * (AREA_WIDTH / 4)) - (NEXT_PIECE_WIDTH / 2)
    NEXT_PIECE_Y = (AREA_WIDTH / 4) - (NEXT_PIECE_HEIGHT / 2)

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




