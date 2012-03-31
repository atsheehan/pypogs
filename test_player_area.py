from player_area import PlayerArea
from piece import Piece
import unittest

class TestPlayerArea(unittest.TestCase):

    def test_set_current_piece_if_null_on_tick(self):
        """
        The current piece is the shape that the player moves around on the grid.
        If there is no piece set, it could mean that the game has just begun or
        that the current piece collided last round and was cemented onto the grid.
        In this case, the next_piece field becomes the current_piece and a new
        next_piece object is randomly generated. The drop counter should also be
        reset.
        """
        p = PlayerArea()
        piece = Piece(Piece.BLOCK_SHAPE)

        p.current_piece = None
        p.next_piece = piece

        p.tick()

        self.assertEqual(p.current_piece, piece)
        self.assertEqual(p.drop_counter, p.ticks_per_drop)
        self.assertIsNotNone(p.next_piece)
        self.assertNotEqual(p.next_piece, piece)

    def test_decrementing_drop_counter(self):
        """
        A counter is used to determine when the current piece should drop
        down by a row. The counter should be decremented every tick, but
        the piece should not drop unless it hits zero. Verify that the counter
        is decremented and that the x and y coordinates of the piece do not
        change.
        """
        p = PlayerArea()
        p.current_piece = Piece()

        drop_counter_before = p.drop_counter
        self.assertTrue(drop_counter_before > 0)

        x_before = p.current_x
        y_before = p.current_y

        p.tick()

        self.assertEqual(p.drop_counter, drop_counter_before - 1)
        self.assertEqual(p.current_x, x_before)
        self.assertEqual(p.current_y, y_before)
            
    def test_reset_the_counter_and_move_piece_down(self):
        p = PlayerArea()
        p.current_piece = Piece()
        p.drop_counter = 0

        x_before = p.current_x
        y_before = p.current_y

        p.tick()

        self.assertEqual(p.drop_counter, p.ticks_per_drop)
        self.assertEqual(p.current_x, x_before)
        self.assertEqual(p.current_y, y_before + 1)

    def test_attaching_piece_to_bottom_of_grid(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_y = 17
        p.current_x = p.INITIAL_X
        p.drop_counter = 0

        p.tick()

        self.assertIsNone(p.current_piece)
        
        for row in (18, 19):
            for col in (4, 5):
                index = (row * PlayerArea.GRID_COLUMNS) + col
                self.assertNotEqual(p.grid[index], 0)

def print_grid(grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            print grid[(row * cols) + col],
        print

if __name__ == '__main__':
    unittest.main()
