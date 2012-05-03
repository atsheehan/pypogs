import random

BLOCK_SHAPE = 0
T_SHAPE = 1
L_SHAPE = 2
REV_L_SHAPE = 3
I_SHAPE = 4
SQUIGGLY_SHAPE = 5
REV_SQUIGGLY_SHAPE = 6

SHAPES = 7
ROTATIONS = 4
ROWS = 4
COLUMNS = 4

SHAPE_OFFSET = ROTATIONS * ROWS * COLUMNS
ROTATIONS_OFFSET = ROWS * COLUMNS

class Piece(object):

    def __init__(self, shape_index = None):
        if shape_index is None:
            self.shape_index = random.randrange(SHAPES)
        else:
            self.shape_index = shape_index

        self.rotation = 0

    def value_at(self, row, col):
        return self.values[(self.shape_index * SHAPE_OFFSET) +
                           (self.rotation * ROTATIONS_OFFSET) +
                           (row * COLUMNS) + col]

    def rotate_clockwise(self):
        self.rotation += 1
        if self.rotation >= ROTATIONS:
            self.rotation = 0

    def rotate_counter_clockwise(self):
        self.rotation -= 1
        if self.rotation < 0:
            self.rotation = ROTATIONS - 1

    values = (
        # Block shape

        0, 1, 1, 0,
        0, 1, 1, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,

        0, 1, 1, 0,
        0, 1, 1, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,

        0, 1, 1, 0,
        0, 1, 1, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,

        0, 1, 1, 0,
        0, 1, 1, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,

        # T shape
        0, 0, 2, 0,
        0, 2, 2, 0,
        0, 0, 2, 0,
        0, 0, 0, 0,

        0, 0, 2, 0,
        0, 2, 2, 2,
        0, 0, 0, 0,
        0, 0, 0, 0,

        0, 0, 2, 0,
        0, 0, 2, 2,
        0, 0, 2, 0,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 2, 2, 2,
        0, 0, 2, 0,
        0, 0, 0, 0,

        # L shape
        0, 3, 0, 0,
        0, 3, 0, 0,
        0, 3, 3, 0,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 3, 3, 3,
        0, 3, 0, 0,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 3, 3, 0,
        0, 0, 3, 0,
        0, 0, 3, 0,

        0, 0, 0, 0,
        0, 0, 3, 0,
        3, 3, 3, 0,
        0, 0, 0, 0,

        # Reverse-L shape
        0, 0, 4, 0,
        0, 0, 4, 0,
        0, 4, 4, 0,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 4, 0, 0,
        0, 4, 4, 4,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 4, 4, 0,
        0, 4, 0, 0,
        0, 4, 0, 0,

        0, 0, 0, 0,
        4, 4, 4, 0,
        0, 0, 4, 0,
        0, 0, 0, 0,

        # I shape
        0, 0, 5, 0,
        0, 0, 5, 0,
        0, 0, 5, 0,
        0, 0, 5, 0,

        0, 0, 0, 0,
        0, 0, 0, 0,
        5, 5, 5, 5,
        0, 0, 0, 0,

        0, 5, 0, 0,
        0, 5, 0, 0,
        0, 5, 0, 0,
        0, 5, 0, 0,

        0, 0, 0, 0,
        5, 5, 5, 5,
        0, 0, 0, 0,
        0, 0, 0, 0,

        # Squiggly shape
        0, 0, 6, 0,
        0, 6, 6, 0,
        0, 6, 0, 0,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 6, 6, 0,
        0, 0, 6, 6,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 0, 6, 0,
        0, 6, 6, 0,
        0, 6, 0, 0,

        0, 0, 0, 0,
        6, 6, 0, 0,
        0, 6, 6, 0,
        0, 0, 0, 0,

        # Reverse-squiggly shape
        0, 7, 0, 0,
        0, 7, 7, 0,
        0, 0, 7, 0,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 0, 7, 7,
        0, 7, 7, 0,
        0, 0, 0, 0,

        0, 0, 0, 0,
        0, 7, 0, 0,
        0, 7, 7, 0,
        0, 0, 7, 0,

        0, 0, 0, 0,
        0, 7, 7, 0,
        7, 7, 0, 0,
        0, 0, 0, 0
        )


