from player_area import PlayerArea
from pygame.event import Event
from piece import Piece
import unittest
from pygame.locals import *

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
        p.current_y = 18
        p.current_x = p.INITIAL_X
        p.drop_counter = 0

        p.tick()

        self.assertIsNone(p.current_piece)
        
        for row in (18, 19):
            for col in (4, 5):
                index = (row * PlayerArea.GRID_COLUMNS) + col
                self.assertNotEqual(p.grid[index], 0)

    def test_getting_the_value_on_the_grid(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_y = 0
        p.current_x = p.INITIAL_X

        # Assign some random values on the grid.
        for point in [(0, 9), (5, 8), (6, 2), (13, 0)]:
            index = (point[0] * p.GRID_COLUMNS) + point[1]
            p.grid[index] = 1

        occupied_points = [(0, 9), (5, 8), (6, 2), (13, 0), 
                           (0, 4), (0, 5), (1, 4), (1, 5)]
        empty_points = [(0, 0), (0, 3), (0, 6), (1, 3), (1, 6),
                        (10, 7), (7, 8), (15, 2), (19, 9)]
        for point in occupied_points:
            self.assertTrue(p.value_at(point[0], point[1]) > 0, 
                            "(%s, %s) does not contain a value" % (point[0], point[1]))
        for point in empty_points:
            self.assertEqual(p.value_at(point[0], point[1]), 0, 
                             "(%s, %s) contains a value" % (point[0], point[1]))

    def test_resetting_the_current_x_and_y_on_new_piece(self):
        """
        When a new piece is activated, the initial position should be reset to the
        top-center of the grid.
        """
        p = PlayerArea()
        p.current_piece = None
        p.current_y = 15
        p.current_x = 7

        p.tick()

        self.assertEqual(p.current_x, p.INITIAL_X)
        self.assertEqual(p.current_y, p.INITIAL_Y)

    def test_move_the_current_piece_to_the_left(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_x = 3
        
        p.handle_event(Event(KEYDOWN, { 'key': K_LEFT }))

        self.assertEqual(p.current_x, 2)

    def test_do_not_move_left_if_against_wall(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_x = -1

        p.handle_event(Event(KEYDOWN, { 'key': K_LEFT }))
        self.assertEqual(p.current_x, -1)

    def test_move_the_current_piece_to_the_right(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_x = 3
        
        p.handle_event(Event(KEYDOWN, { 'key': K_RIGHT }))

        self.assertEqual(p.current_x, 4)

    def test_do_not_move_right_if_against_wall(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_x = 7

        p.handle_event(Event(KEYDOWN, { 'key': K_RIGHT }))
        self.assertEqual(p.current_x, 7)

    def test_move_current_piece_down_should_reset_tick_counter(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_y = 0
        p.current_x = p.INITIAL_X
        p.drop_counter = 5

        p.handle_event(Event(KEYDOWN, { 'key': K_DOWN }))
        self.assertEqual(p.current_x, p.INITIAL_X)
        self.assertEqual(p.current_y, 1)
        self.assertEqual(p.drop_counter, p.ticks_per_drop)

    def test_dropping_a_piece_to_the_floor_should_attach_to_grid(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)
        p.current_y = 0

        p.handle_event(Event(KEYDOWN, { 'key': K_UP }))

        self.assertIsNone(p.current_piece, "should have attached the piece to the grid")

        filled_points = [(18, 4), (18, 5), (19, 4), (19, 5)]
        for point in filled_points:
            self.assertTrue(p.value_at(point[0], point[1]) > 0, 
                            "block should be filled")
        


def print_grid(grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            print grid[(row * cols) + col],
        print

if __name__ == '__main__':
    unittest.main()
