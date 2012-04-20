import pygame
from pygame.locals import *

from pypogs import render
from pypogs import piece

################################################################################
#
# Module Constants

JOY_X_AXIS = 0
JOY_Y_AXIS = 1

JOY_ROTATE_BUTTON = 2

GRID_ROWS = 20
GRID_COLUMNS = 10
GRID_SIZE = GRID_ROWS * GRID_COLUMNS

INITIAL_X = 3
INITIAL_Y = 0

TICKS_TO_CLEAR_BLOCKS = 20
BLOCK_TO_BE_CLEARED = 8
GAME_OVER_BLOCK = 8

INITIAL_LEVEL = 1
MAX_LEVEL = 20
LINES_TO_NEXT_LEVEL = 10

MAX_TICKS_PER_DROP = 22
MIN_TICKS_PER_DROP = 2

# Rendering constants
OUTER_COLOR_OFFSET = 10

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

################################################################################
#
# Class Definition

class PlayerArea(object):

    def __init__(self, positions, player_id = 0):
        self._next_piece = piece.Piece()
        self._game_over = False
        self._grid = [0] * GRID_SIZE
        self._positions = positions
        self._player_id = player_id
        self._current_piece = None
        self._lines_cleared = 0
        self._current_x = INITIAL_X
        self._current_y = INITIAL_Y
        self._counter_to_clear_blocks = 0
        self._level = INITIAL_LEVEL
        self._set_ticks_per_drop()
        self._drop_counter = self._ticks_per_drop

    def tick(self):
        """
        Updates the player area after a tick.
        """
        if self._game_over:
            return

        if self._counter_to_clear_blocks > 0:
            self._decrement_counter_to_clear_blocks()
        elif self._current_piece is None:
            self._activate_next_piece()
        else:
            self._update_current_piece()

    def value_at(self, row, col):
        """
        Returns the value at the given row and column on the grid, including
        the value of the current piece if it is at that location.
        """
        if self._current_piece is not None:
            piece_row = row - self._current_y
            piece_col = col - self._current_x

            if (piece_row >= 0 and piece_row < piece.Piece.ROWS and
                piece_col >= 0 and piece_col < piece.Piece.COLUMNS):
                piece_value = self._current_piece.value_at(piece_row, piece_col)
                if piece_value != 0:
                    return piece_value

        return self._grid[row * GRID_COLUMNS + col]

    def _update_current_piece(self):
        """
        Updates the current piece on the grid after a tick by
        checking if it is time for the piece to drop by a row.
        """
        if self._drop_counter == 0:
            self._drop_current_piece_one_row()
        else:
            self._drop_counter -= 1

    def _drop_current_piece_one_row(self):
        """
        Drops the current piece down one row and checks for a collision.
        """
        if self._current_piece is None:
            return

        self._current_y += 1

        if self._current_piece_collision():
            self._current_y -= 1
            self._attach_current_piece_to_grid()

        self._drop_counter = self._ticks_per_drop


    def _current_piece_collision(self):
        """
        Checks if the current piece on the board is in collision (overlaps)
        another block on the grid or falls outside the edges of the grid.
        """
        for row in range(piece.Piece.ROWS):
            for col in range(piece.Piece.COLUMNS):
                piece_value = self._current_piece.value_at(row, col)

                if piece_value != 0:
                    grid_col = self._current_x + col
                    grid_row = self._current_y + row

                    # Check if the piece is outside of the grid boundaries.
                    if (grid_row >= GRID_ROWS or grid_row < 0 or
                        grid_col >= GRID_COLUMNS or grid_col < 0):
                        return True

                    # Check if a block is filled on the grid in that position.
                    if self._grid[(grid_row * GRID_COLUMNS) + grid_col] > 0:
                        return True
        return False

    def _attach_current_piece_to_grid(self):
        """
        Copy the currently active piece to the grid and check for any
        full lines.
        """
        self._copy_piece_to_grid(self._current_piece, self._current_x,
                                 self._current_y)
        self._mark_full_lines()
        self._current_piece = None

    def _copy_piece_to_grid(self, piece_to_copy, piece_x, piece_y):
        """
        Copy the given piece to the grid.
        """
        for row in range(piece.Piece.ROWS):
            for col in range(piece.Piece.COLUMNS):
                piece_value = piece_to_copy.value_at(row, col)

                if piece_value != 0:
                    grid_col = piece_x + col
                    grid_row = piece_y + row
                    grid_index = (grid_row * GRID_COLUMNS) + grid_col

                    self._grid[grid_index] = piece_value

    def _mark_full_lines(self):
        """
        Mark lines that contain a block in every column to be cleared.
        Update the total lines cleared and check if this increases the
        level.
        """
        row_marked = False
        lines_cleared_this_round = 0

        for row in range(GRID_ROWS):
            full_row = True
            row_index = row * GRID_COLUMNS

            for col in range(GRID_COLUMNS):
                value = self._grid[row_index + col]
                if value == 0:
                    full_row = False
                    continue

            if full_row:
                self._mark_line(row)
                row_marked = True
                lines_cleared_this_round += 1

        if row_marked:
            self._counter_to_clear_blocks = TICKS_TO_CLEAR_BLOCKS

        if lines_cleared_this_round > 0:
            self._lines_cleared += lines_cleared_this_round
            self._set_level()

    def _set_level(self):
        """
        Set the current level and falling speed of the pieces based on the
        number of lines cleared.
        """
        self._level = min((self._lines_cleared / LINES_TO_NEXT_LEVEL) + 1,
                         MAX_LEVEL)
        self._set_ticks_per_drop()

    def _mark_line(self, row):
        """
        Mark each block in a single line in the grid to be cleared.
        """
        row_index = row * GRID_COLUMNS
        for col in range(GRID_COLUMNS):
            self._grid[row_index + col] = BLOCK_TO_BE_CLEARED

    def _clear_marked_lines(self):
        """
        Remove marked lines from the grid completely, dropping all rows
        above the cleared line down.
        """
        for row in range(GRID_ROWS):
            if self._grid[row * GRID_COLUMNS] == BLOCK_TO_BE_CLEARED:
                self._clear_line(row);

    def _clear_line(self, row_to_clear):
        for row in range(row_to_clear, -1, -1):
            if row == 0:
                for col in range(GRID_COLUMNS):
                    self._grid[col] = 0
            else:
                prev_row_index = (row - 1) * GRID_COLUMNS
                row_index = row * GRID_COLUMNS

                for col in range(GRID_COLUMNS):
                    self._grid[row_index + col] = self._grid[prev_row_index + col]

    def _activate_next_piece(self):
        self._current_piece = self._next_piece
        self._next_piece = piece.Piece()
        self.drop_counter = self._ticks_per_drop
        self._current_x = INITIAL_X
        self._current_y = INITIAL_Y

        if self._current_piece_collision():
            self._set_game_over()

    def _set_game_over(self):
        self._game_over = True

        for row in range(GRID_ROWS):
            for col in range(GRID_COLUMNS):
                if self.value_at(row, col) > 0:
                    self._grid[row * GRID_COLUMNS + col] = GAME_OVER_BLOCK

        self._current_piece = None

    def render(self, surface):
        """Renders the player area onto the given screen."""
        grid_x = self._positions.get_grid_x(self._player_id)
        grid_y = self._positions.get_grid_y(self._player_id)

        next_x = self._positions.get_next_piece_x(self._player_id)
        next_y = self._positions.get_next_piece_y(self._player_id)

        lines_x = self._positions.get_lines_box_x(self._player_id)
        lines_y = self._positions.get_lines_box_y(self._player_id)
        level_x = self._positions.get_level_box_x(self._player_id)
        level_y = self._positions.get_level_box_y(self._player_id)
        score_x = self._positions.get_score_box_x(self._player_id)
        score_y = self._positions.get_score_box_y(self._player_id)
        text_box_width = self._positions.get_text_box_width()
        text_box_height = self._positions.get_text_box_height()

        font = self._positions.get_text_box_font()

        box_thickness = self._positions.get_grid_thickness()

        inner_frame_color = (0, 0, 0)
        outer_frame_color = (0, 64, 128)
        font_color = (255, 255, 255)


        self._render_frame(surface, lines_x, lines_y,
                           text_box_width, text_box_height, box_thickness,
                           inner_frame_color, outer_frame_color)

        render.render_text_centered(surface, font, lines_x, lines_y,
                                   text_box_width, text_box_height,
                                   str(self._lines_cleared),
                                   font_color)

        self._render_frame(surface, level_x, level_y,
                           text_box_width, text_box_height, box_thickness,
                           inner_frame_color, outer_frame_color)

        render.render_text_centered(surface, font, level_x, level_y,
                                   text_box_width, text_box_height,
                                   str(self._level),
                                   font_color)

        self._render_frame(surface, score_x, score_y,
                           text_box_width, text_box_height, box_thickness,
                           inner_frame_color, outer_frame_color)


        self._render_frame(surface, next_x, next_y,
                           self._positions.get_next_piece_width(),
                           self._positions.get_next_piece_height(),
                           box_thickness,
                           inner_frame_color, outer_frame_color)

        self._render_frame(surface, grid_x, grid_y,
                           self._positions.get_grid_width(),
                           self._positions.get_grid_height(),
                           box_thickness,
                           inner_frame_color, outer_frame_color)

        self._render_next_piece(surface, next_x, next_y)
        self._render_grid(surface, grid_x, grid_y)



    def _render_next_piece(self, surface, x, y):
        block_size = self._positions.get_block_size()
        block_edge_thickness = self._positions.get_block_edge_thickness()

        # Render the next piece in the middle of the box, which is half a block
        # away from the edge of the box.
        actual_x = x + (block_size / 2)
        actual_y = y + (block_size / 2)

        for row in range(piece.Piece.ROWS):
            for col in range(piece.Piece.COLUMNS):
                block_value = self._next_piece.value_at(row, col)
                if block_value > 0:
                    self._render_block(actual_x, actual_y, row, col, block_size,
                                       block_edge_thickness, block_value,
                                       surface)

    def _render_grid(self, surface, x, y):
        block_size = self._positions.get_block_size()
        block_edge_thickness = self._positions.get_block_edge_thickness()

        for row in range(GRID_ROWS):
            for col in range(GRID_COLUMNS):
                block_value = self.value_at(row, col)
                if block_value > 0:
                    self._render_block(x, y, row, col, block_size,
                                       block_edge_thickness, block_value,
                                       surface)

    def _render_frame(self, surface, x, y, width, height, frame_thickness,
                      inner_color, outer_color):
        outer_rect = pygame.Rect(x - frame_thickness, y - frame_thickness,
                                 width + (2 * frame_thickness),
                                 height + (2 * frame_thickness))
        inner_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(surface, outer_color, outer_rect)
        pygame.draw.rect(surface, inner_color, inner_rect)

    def _render_block(self, grid_x, grid_y, row, col, size,
                      edge_thickness, value, surface):

        left = grid_x + (col * size)
        top = grid_y + (row * size)

        inner_size = size - (2 * edge_thickness)

        outer_rect = pygame.Rect(left, top, size, size)
        inner_rect = pygame.Rect(left + edge_thickness,
                                 top + edge_thickness,
                                 inner_size, inner_size)

        outer_color = self._value_to_color(value + OUTER_COLOR_OFFSET,
                                           self._counter_to_clear_blocks)
        inner_color = self._value_to_color(value, self._counter_to_clear_blocks)

        pygame.draw.rect(surface, outer_color, outer_rect)
        pygame.draw.rect(surface, inner_color, inner_rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self._handle_key_event(event.key)
        elif event.type == JOYBUTTONDOWN:
            self._handle_joy_button_event(event.joy, event.button)
        elif event.type == JOYAXISMOTION:
            self._handle_joy_axis_event(event.joy, event.axis, event.value)

    def _handle_joy_button_event(self, id, button):
        if id != self._player_id:
            return

        if button == JOY_ROTATE_BUTTON:
            self._rotate_current_piece_clockwise()

    def _handle_joy_axis_event(self, id, axis, value):
        if value < 0.1 and value > -0.1:
            return

        if id != self._player_id:
            return

        if axis == JOY_X_AXIS:
            if value > 0:
                self._move_current_piece_right()
            else:
                self._move_current_piece_left()
        elif axis == JOY_Y_AXIS:
            if value > 0:
                self._drop_current_piece_one_row()
            else:
                self._drop_current_piece_to_floor()

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
        if self._current_piece is None:
            return

        self._current_x -= 1
        if self._current_piece_collision():
            self._current_x += 1

    def _move_current_piece_right(self):
        if self._current_piece is None:
            return

        self._current_x += 1
        if self._current_piece_collision():
            self._current_x -= 1

    def _drop_current_piece_to_floor(self):
        while self._current_piece is not None:
            self._drop_current_piece_one_row()

    def _rotate_current_piece_clockwise(self):
        if self._current_piece is not None:
            self._current_piece.rotate_clockwise()
            if self._current_piece_collision():
                self._current_piece.rotate_counter_clockwise()

    def _value_to_color(self, value, dimmer = 0):
        color = COLORS.get(value, (0, 0, 0))
        # Fix this hack.
        if dimmer > 0 and (value == BLOCK_TO_BE_CLEARED or
                           value == BLOCK_TO_BE_CLEARED + 10):
            pct_dimmed = float(dimmer) / float(TICKS_TO_CLEAR_BLOCKS)
            color = (color[0] * pct_dimmed,
                     color[1] * pct_dimmed,
                     color[2] * pct_dimmed)

        return color

    def _decrement_counter_to_clear_blocks(self):
        self._counter_to_clear_blocks -= 1
        if self._counter_to_clear_blocks <= 0:
            self._clear_marked_lines()

    def _set_ticks_per_drop(self):
        self._ticks_per_drop = max(MAX_TICKS_PER_DROP - self._level,
                                   MIN_TICKS_PER_DROP)

