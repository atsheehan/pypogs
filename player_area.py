import pygame
from pygame.locals import *
from piece import Piece

class PlayerArea(object):

    GRID_ROWS = 20
    GRID_COLUMNS = 10
    GRID_SIZE = GRID_ROWS * GRID_COLUMNS

    INITIAL_X = 3
    INITIAL_Y = 0

    # Rendering constants

    BLOCK_SIZE = 32
    GRID_WIDTH = BLOCK_SIZE * GRID_COLUMNS
    GRID_HEIGHT = BLOCK_SIZE * GRID_ROWS
    
    current_piece = None
    next_piece = None
    ticks_per_drop = 20
    lines_cleared = 0
    current_x = INITIAL_X
    current_y = INITIAL_Y

    def __init__(self):
        self.next_piece = Piece()
        self.drop_counter = self.ticks_per_drop
        self.grid = [0] * self.GRID_SIZE

    def tick(self):
        """
        Updates the player area after a tick.
        """
        if self.current_piece is None:
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
        self._clear_full_lines()
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

    def _clear_full_lines(self):
        for row in range(self.GRID_ROWS):
            full_row = True
            row_index = row * self.GRID_COLUMNS

            for col in range(self.GRID_COLUMNS):
                value = self.grid[row_index + col]
                if value == 0:
                    full_row = False
                    continue

            if full_row:
                self._clear_line(row)

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

        self.lines_cleared += 1

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

        grid_rect = pygame.Rect(grid_x, grid_y, self.GRID_WIDTH, self.GRID_HEIGHT)
        pygame.draw.rect(surface, (0, 0, 0), grid_rect)

        block_rect = pygame.Rect(0, 0, self.BLOCK_SIZE, self.BLOCK_SIZE)
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLUMNS):
                if self.value_at(row, col) > 0:
                    block_rect.x = grid_x + (col * self.BLOCK_SIZE)
                    block_rect.y = grid_y + (row * self.BLOCK_SIZE)

                    pygame.draw.rect(surface, (0, 0, 255), block_rect)


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

    def _move_current_piece_left(self):
        self.current_x -= 1
        if self._current_piece_collision():
            self.current_x += 1

    def _move_current_piece_right(self):
        self.current_x += 1
        if self._current_piece_collision():
            self.current_x -= 1

    def _drop_current_piece_to_floor(self):
        while self.current_piece is not None:
            self._drop_current_piece_one_row()
