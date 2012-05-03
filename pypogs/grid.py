from pypogs import piece

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

POINTS_PER_LINE_CLEARED = 10
EXTRA_LINE_MULTIPLIER = 2

MAX_TICKS_PER_DROP = 22
MIN_TICKS_PER_DROP = 2

class Grid(object):

    def __init__(self, player_id = 0):
        self._next_piece = piece.Piece()
        self._game_over = False
        self._grid = [0] * GRID_SIZE
        self._player_id = player_id
        self._current_piece = None
        self._lines_cleared = 0
        self._score = 0
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

            if (piece_row >= 0 and piece_row < piece.ROWS and
                piece_col >= 0 and piece_col < piece.COLUMNS):
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
        for row in range(piece.ROWS):
            for col in range(piece.COLUMNS):
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
        for row in range(piece.ROWS):
            for col in range(piece.COLUMNS):
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
            self._score += (lines_cleared_this_round * POINTS_PER_LINE_CLEARED *
                            (EXTRA_LINE_MULTIPLIER ** (lines_cleared_this_round - 1)))
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

    def _decrement_counter_to_clear_blocks(self):
        self._counter_to_clear_blocks -= 1
        if self._counter_to_clear_blocks <= 0:
            self._clear_marked_lines()

    def _set_ticks_per_drop(self):
        self._ticks_per_drop = max(MAX_TICKS_PER_DROP - self._level,
                                   MIN_TICKS_PER_DROP)

