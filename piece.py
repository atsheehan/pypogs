class Piece(object):
    BLOCK_SHAPE = 1
    ROWS = 4
    COLUMNS = 4

    values = [
        0, 1, 1, 0,
        0, 1, 1, 0,
        0, 0, 0, 0,
        0, 0, 0, 0
        ]

    def __init__(self, shape_index = None):
        pass

    def value_at(self, row, col):
        return self.values[(row * self.COLUMNS) + col]
        

