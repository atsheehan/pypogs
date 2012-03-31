from piece import Piece

class PlayerArea(object):

    GRID_ROWS = 20
    GRID_COLUMNS = 10
    GRID_SIZE = GRID_ROWS * GRID_COLUMNS

    INITIAL_X = 3
    INITIAL_Y = 0

    current_piece = None
    next_piece = None
    ticks_per_drop = 20
    current_x = INITIAL_X
    current_y = INITIAL_Y

    def __init__(self):
        self.next_piece = Piece()
        self.drop_counter = self.ticks_per_drop
        self.grid = [0] * self.GRID_SIZE

    def tick(self):
        if self.current_piece is None:
            self._activate_next_piece()
        else:
            if self.drop_counter == 0:
                self.drop_counter = self.ticks_per_drop
                self.current_y += 1

                if self._current_piece_collision():
                    self.current_y -= 1
                    self._attach_current_piece_to_grid()
            else:
                self.drop_counter -= 1

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

                    if grid_row >= self.GRID_ROWS or grid_row < 0 or grid_col >= self.GRID_COLUMNS or grid_col < 0:
                        return True

                    # TODO check for collision with other piece
        return False
                    
    def _attach_current_piece_to_grid(self):

        for row in range(Piece.ROWS):
            for col in range(Piece.COLUMNS):
                piece_value = self.current_piece.value_at(row, col)

                if piece_value != 0:
                    grid_col = self.current_x + col
                    grid_row = self.current_y + row
                    grid_index = (grid_row * self.GRID_COLUMNS) + grid_col

                    self.grid[grid_index] = piece_value
        
        self.current_piece = None

    def _activate_next_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        self.drop_counter = self.ticks_per_drop

    def render(self, surface):
        pygame.draw.rect()

    def handle_event(self, event):
        pass

    
