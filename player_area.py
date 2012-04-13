import pygame
from pygame.locals import *
from piece import Piece

class PlayerArea(object):

    GRID_ROWS = 20
    GRID_COLUMNS = 10
    GRID_SIZE = GRID_ROWS * GRID_COLUMNS

    INITIAL_X = 3
    INITIAL_Y = 0

    TICKS_TO_CLEAR_BLOCKS = 20
    BLOCK_TO_BE_CLEARED = 8

    # Rendering constants

    OUTER_COLOR_OFFSET = 10
    BLOCK_EDGE_WIDTH = 4

    BLOCK_SIZE = 32
    INNER_BLOCK_SIZE = BLOCK_SIZE - (2 * BLOCK_EDGE_WIDTH)
    GRID_WIDTH = BLOCK_SIZE * GRID_COLUMNS
    GRID_HEIGHT = BLOCK_SIZE * GRID_ROWS

    GRID_EDGE_WIDTH = 8

    GRID_WIDTH_WITH_EDGE = GRID_WIDTH + (2 * GRID_EDGE_WIDTH)
    GRID_HEIGHT_WITH_EDGE = GRID_HEIGHT + (2 * GRID_EDGE_WIDTH)

    COLORS = {
        1: (0, 0, 255),
        2: (0, 255, 0),
        3: (255, 0, 0),
        4: (255, 255, 0),
        5: (0, 255, 255),
        6: (128, 255, 0),
        8: (128, 128, 128),
        7: (0, 255, 128),
        11: (0, 0, 128),
        12: (0, 128, 0),
        13: (128, 0, 0),
        14: (128, 128, 0),
        15: (0, 128, 128),
        16: (64, 128, 0),
        17: (0, 128, 64),
        18: (64, 64, 64)
        }


    current_piece = None
    next_piece = None
    ticks_per_drop = 20
    lines_cleared = 0
    current_x = INITIAL_X
    current_y = INITIAL_Y
    counter_to_clear_blocks = 0

    def __init__(self):
        self.next_piece = Piece()
        self.drop_counter = self.ticks_per_drop
        self.grid = [0] * self.GRID_SIZE

    def tick(self):
        """
        Updates the player area after a tick.
        """
        if self.counter_to_clear_blocks > 0:
            self._decrement_counter_to_clear_blocks()
        elif self.current_piece is None:
            self._activate_next_piece()
        else:
            self._update_current_piece()

    def value_at(self, row, col):
        """
        Returns the value at the given row and column on the grid, including
        the value of the current piece if it is at that location.
        """
        if self.current_piece is not None:
            piece_row = row - self.current_y
            piece_col = col - self.current_x

            if piece_row >= 0 and piece_row < Piece.ROWS and \
                    piece_col >= 0 and piece_col < Piece.COLUMNS:
                piece_value = self.current_piece.value_at(piece_row, piece_col)
                if piece_value != 0:
                    return piece_value

        return self.grid[row * self.GRID_COLUMNS + col]

    def _update_current_piece(self):
        """
        Updates the current piece on the grid after a tick by
        checking if it is time for the piece to drop by a row.
        """
        if self.drop_counter == 0:
            self._drop_current_piece_one_row()
        else:
            self.drop_counter -= 1

    def _drop_current_piece_one_row(self):
        """
        Drops the current piece down one row and checks for a collision.
        """
        if self.current_piece is None:
            return

        self.current_y += 1

        if self._current_piece_collision():
            self.current_y -= 1
            self._attach_current_piece_to_grid()

        self.drop_counter = self.ticks_per_drop


    def _current_piece_collision(self):
        """
        Checks if the current piece on the board is in collision (overlaps)
        another block on the grid or falls outside the edges of the grid.
        """
        for row in range(Piece.ROWS):
            for col in range(Piece.COLUMNS):
                piece_value = self.current_piece.value_at(row, col)

                if piece_value != 0:
                    grid_col = self.current_x + col
                    grid_row = self.current_y + row

                    # Check if the piece is outside of the grid boundaries.
                    if grid_row >= self.GRID_ROWS or grid_row < 0 or \
                            grid_col >= self.GRID_COLUMNS or grid_col < 0:
                        return True

                    # Check if a block is filled on the grid in that position.
                    if self.grid[(grid_row * self.GRID_COLUMNS) + grid_col] > 0:
                        return True
        return False

    def _attach_current_piece_to_grid(self):
        """
        Copies the currently active piece to the grid.
        """
        self._copy_piece_to_grid(self.current_piece, self.current_x, self.current_y)
        self._mark_full_lines()
        self.current_piece = None

    def _copy_piece_to_grid(self, piece, piece_x, piece_y):
        for row in range(Piece.ROWS):
            for col in range(Piece.COLUMNS):
                piece_value = piece.value_at(row, col)

                if piece_value != 0:
                    grid_col = piece_x + col
                    grid_row = piece_y + row
                    grid_index = (grid_row * self.GRID_COLUMNS) + grid_col

                    self.grid[grid_index] = piece_value

    def _mark_full_lines(self):
        row_marked = False

        for row in range(self.GRID_ROWS):
            full_row = True
            row_index = row * self.GRID_COLUMNS

            for col in range(self.GRID_COLUMNS):
                value = self.grid[row_index + col]
                if value == 0:
                    full_row = False
                    continue

            if full_row:
                self._mark_line(row)
                row_marked = True

        if row_marked:
            self.counter_to_clear_blocks = self.TICKS_TO_CLEAR_BLOCKS

    def _mark_line(self, row):
        row_index = row * self.GRID_COLUMNS
        for col in range(self.GRID_COLUMNS):
            self.grid[row_index + col] = self.BLOCK_TO_BE_CLEARED

        self.lines_cleared += 1

    def _clear_marked_lines(self):
        for row in range(self.GRID_ROWS):
            if self.grid[row * self.GRID_COLUMNS] == self.BLOCK_TO_BE_CLEARED:
                self._clear_line(row);

    def _clear_line(self, row_to_clear):
        for row in range(row_to_clear, -1, -1):
            if row == 0:
                for col in range(self.GRID_COLUMNS):
                    self.grid[col] = 0
            else:
                prev_row_index = (row - 1) * self.GRID_COLUMNS
                row_index = row * self.GRID_COLUMNS

                for col in range(self.GRID_COLUMNS):
                    self.grid[row_index + col] = self.grid[prev_row_index + col]

    def _activate_next_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        self.drop_counter = self.ticks_per_drop
        self.current_x = self.INITIAL_X
        self.current_y = self.INITIAL_Y

    def render(self, surface):
        """
        Renders the player area onto the given screen.
        """
        grid_x = (surface.get_width() - self.GRID_WIDTH) / 2
        grid_y = (surface.get_height() - self.GRID_HEIGHT) / 2

        outer_grid_rect = pygame.Rect(grid_x - self.GRID_EDGE_WIDTH,
                                      grid_y - self.GRID_EDGE_WIDTH,
                                      self.GRID_WIDTH_WITH_EDGE,
                                      self.GRID_HEIGHT_WITH_EDGE)
        grid_rect = pygame.Rect(grid_x, grid_y, self.GRID_WIDTH, self.GRID_HEIGHT)

        pygame.draw.rect(surface, (0, 64, 128), outer_grid_rect)
        pygame.draw.rect(surface, (0, 0, 0), grid_rect)

        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLUMNS):
                block_value = self.value_at(row, col)
                if block_value > 0:
                    self._render_block(grid_x, grid_y, row, col, block_value, surface)


    def _render_block(self, grid_x, grid_y, row, col, value, surface):
        left = grid_x + (col * self.BLOCK_SIZE)
        top = grid_y + (row * self.BLOCK_SIZE)

        outer_rect = pygame.Rect(left, top, self.BLOCK_SIZE, self.BLOCK_SIZE)
        inner_rect = pygame.Rect(left + self.BLOCK_EDGE_WIDTH,
                                 top + self.BLOCK_EDGE_WIDTH,
                                 self.INNER_BLOCK_SIZE,
                                 self.INNER_BLOCK_SIZE)

        outer_color = self._value_to_color(value + self.OUTER_COLOR_OFFSET, self.counter_to_clear_blocks)
        inner_color = self._value_to_color(value, self.counter_to_clear_blocks)

        pygame.draw.rect(surface, outer_color, outer_rect)
        pygame.draw.rect(surface, inner_color, inner_rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self._handle_key_event(event.key)

    def _handle_key_event(self, key):
        if key == K_LEFT:
            self._move_current_piece_left()
        elif key == K_RIGHT:
            self._move_current_piece_right()
        elif key == K_DOWN:
            self._drop_current_piece_one_row()
        elif key == K_UP:
            self._drop_current_piece_to_floor()
        elif key == K_SPACE:
            self._rotate_current_piece_clockwise()

    def _move_current_piece_left(self):
        if self.current_piece is None:
            return

        self.current_x -= 1
        if self._current_piece_collision():
            self.current_x += 1

    def _move_current_piece_right(self):
        if self.current_piece is None:
            return

        self.current_x += 1
        if self._current_piece_collision():
            self.current_x -= 1

    def _drop_current_piece_to_floor(self):
        while self.current_piece is not None:
            self._drop_current_piece_one_row()

    def _rotate_current_piece_clockwise(self):
        if self.current_piece is not None:
            self.current_piece.rotate_clockwise()
            if self._current_piece_collision():
                self.current_piece.rotate_counter_clockwise()

    def _value_to_color(self, value, dimmer = 0):
        color = self.COLORS.get(value, (0, 0, 0))
        # Fix this hack.
        if dimmer > 0 and (value == self.BLOCK_TO_BE_CLEARED or value == self.BLOCK_TO_BE_CLEARED + 10):
            pct_dimmed = float(dimmer) / float(self.TICKS_TO_CLEAR_BLOCKS)
            color = (color[0] * pct_dimmed, color[1] * pct_dimmed, color[2] * pct_dimmed)

        return color

    def _decrement_counter_to_clear_blocks(self):
        self.counter_to_clear_blocks -= 1
        if self.counter_to_clear_blocks <= 0:
            self._clear_marked_lines()
