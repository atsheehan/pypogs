from world import World
from piece import Piece
import unittest

class TestWorld(unittest.TestCase):

    def test_set_current_piece_if_null_on_tick(self):
        """
        The current piece is the shape that the player moves around on the grid.
        If there is no piece set, it could mean that the game has just begun or
        that the current piece collided last round and was cemented onto the grid.
        In this case, the next_piece field becomes the current_piece and a new
        next_piece object is randomly generated. The drop counter should also be
        reset.
        """
        w = World()
        piece = Piece(Piece.BLOCK_SHAPE)

        w.current_piece = None
        w.next_piece = piece

        w.tick()

        self.assertEqual(w.current_piece, piece)
        self.assertEqual(w.drop_counter, w.ticks_per_drop)
        self.assertIsNotNone(w.next_piece)
        self.assertNotEqual(w.next_piece, piece)

    def test_decrementing_drop_counter(self):
        """
        A counter is used to determine when the current piece should drop
        down by a row. The counter should be decremented every tick, but
        the piece should not drop unless it hits zero. Verify that the counter
        is decremented and that the x and y coordinates of the piece do not
        change.
        """
        w = World()
        w.current_piece = Piece()

        drop_counter_before = w.drop_counter
        self.assertTrue(drop_counter_before > 0)

        x_before = w.current_x
        y_before = w.current_y

        w.tick()

        self.assertEqual(w.drop_counter, drop_counter_before - 1)
        self.assertEqual(w.current_x, x_before)
        self.assertEqual(w.current_y, y_before)
            
    def test_reset_the_counter_and_move_piece_down(self):
        w = World()
        w.current_piece = Piece()
        w.drop_counter = 0

        x_before = w.current_x
        y_before = w.current_y

        w.tick()

        self.assertEqual(w.drop_counter, w.ticks_per_drop)
        self.assertEqual(w.current_x, x_before)
        self.assertEqual(w.current_y, y_before + 1)

    def test_attaching_piece_to_bottom_of_grid(self):
        w = World()
        w.current_piece = Piece(Piece.BLOCK_SHAPE)
        w.current_y = 17
        w.current_x = w.INITIAL_X
        w.drop_counter = 0

        w.tick()

        self.assertIsNone(w.current_piece)
        
        for row in (18, 19):
            for col in (4, 5):
                index = (row * World.GRID_COLUMNS) + col
                self.assertNotEqual(w.grid[index], 0)

def print_grid(grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            print grid[(row * cols) + col],
        print

if __name__ == '__main__':
    unittest.main()
