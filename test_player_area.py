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

    def test_attempt_to_move_nonexistent_piece(self):
        """
        At various points in the game, the current piece is set to None.
        Verify that attempting to move the current piece when it doesn't
        exist does not throw an exception.
        """
        p = PlayerArea()
        p.current_piece = None

        p.handle_event(Event(KEYDOWN, { 'key': K_LEFT }))
        p.handle_event(Event(KEYDOWN, { 'key': K_RIGHT }))
        p.handle_event(Event(KEYDOWN, { 'key': K_DOWN }))
        p.handle_event(Event(KEYDOWN, { 'key': K_UP }))

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
                            "(%s, %s) block should be filled" % (point[0], point[1]))

    def test_that_pieces_stack_on_each_other(self):
        p = PlayerArea()

        # Drop two pieces consecutively.
        for i in range(2):
            p.current_piece = Piece(Piece.BLOCK_SHAPE)
            p.current_y = 0
            p.handle_event(Event(KEYDOWN, { 'key': K_UP }))

        filled_points = [(18, 4), (18, 5), (19, 4), (19, 5),
                         (16, 4), (16, 5), (17, 4), (17, 5)]
        for point in filled_points:
            self.assertTrue(p.value_at(point[0], point[1]) > 0,
                            "(%s, %s) block should be filled" % (point[0], point[1]))


    def test_clearing_full_lines_after_attaching_piece(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)

        # Fill some points along the bottom of the grid with an opening
        # in the middle that will be filled by the current piece.
        prefilled_points = [(18, 0), (18, 1), (18, 2), (18, 3),
                            (18, 6), (18, 7), (18, 8), (18, 9),
                            (19, 0), (19, 1), (19, 2), (19, 3),
                            (19, 6), (19, 7), (19, 8), (19, 9)]
        for point in prefilled_points:
            p.grid[(point[0] * PlayerArea.GRID_COLUMNS) + point[1]] = 1

        # Drop the current piece to the floor, which should fill in two
        # complete lines, so every block on the grid will be cleared out.
        p.handle_event(Event(KEYDOWN, { 'key': K_UP }))

        tick_til_lines_cleared(p)

        for row in range(PlayerArea.GRID_ROWS):
            for col in range(PlayerArea.GRID_COLUMNS):
                self.assertEqual(p.value_at(row, col), 0,
                                 "should be clear at point (%s, %s)" % (row, col))

        self.assertEqual(p.lines_cleared, 2)

    def test_clearing_line_should_drop_lines_above(self):
        """
        When clearing a line, all of the lines above it should be shifted
        down a row.
        """
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)

        prefilled_points = [(19, 0), (19, 1), (19, 2), (19, 3),
                            (19, 6), (19, 7), (19, 8), (19, 9)]
        for point in prefilled_points:
            p.grid[(point[0] * PlayerArea.GRID_COLUMNS) + point[1]] = 1

        p.handle_event(Event(KEYDOWN, { 'key': K_UP }))

        tick_til_lines_cleared(p)

        self.assertEqual(p.value_at(18, 4), 0, "block should not exist at (18, 4)")
        self.assertEqual(p.value_at(18, 5), 0, "block should not exist at (18, 5)")
        self.assertTrue(p.value_at(19, 4) > 0, "block should exist at (19, 4)")
        self.assertTrue(p.value_at(19, 5) > 0, "block should exist at (19, 5)")
        self.assertEqual(p.lines_cleared, 1)

    def test_clearing_the_top_line(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)

        for row in range(PlayerArea.GRID_ROWS):
            p.grid[row * PlayerArea.GRID_COLUMNS] = 1

        prefilled_points = [(19, 0), (19, 1), (19, 2), (19, 3),
                            (19, 6), (19, 7), (19, 8), (19, 9)]
        for point in prefilled_points:
            p.grid[(point[0] * PlayerArea.GRID_COLUMNS) + point[1]] = 1

        p.handle_event(Event(KEYDOWN, { 'key': K_UP }))

        tick_til_lines_cleared(p)

        self.assertEqual(p.value_at(0, 0), 0)
        self.assertTrue(p.value_at(1, 0) > 0)

    def test_rotating_the_piece_clockwise(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.L_SHAPE)
        p.current_x = 3
        p.current_y = 0

        blocks_before_rotate = [(0, 4), (1, 4), (2, 4), (2, 5)]
        for point in blocks_before_rotate:
            self.assertTrue(p.value_at(point[0], point[1]) > 0)

        p.handle_event(Event(KEYDOWN, { 'key': K_SPACE }))

        blocks_after_rotate = [(1, 4), (1, 5), (1, 6), (2, 4)]
        for point in blocks_after_rotate:
            self.assertTrue(p.value_at(point[0], point[1]) > 0)

    def test_handle_attempt_to_rotate_non_existent_current_piece(self):
        """
        At various points in the game the current piece will be set to None
        such as when it was just attached to the grid. In these situations,
        a rotate command would attempt to call a method on a non-existent object,
        so include a check for not None before attempting to rotate the piece.
        """
        p = PlayerArea()
        p.current_piece = None
        p.handle_event(Event(KEYDOWN, { 'key': K_SPACE }))
        self.assertIsNone(p.current_piece)

    def test_do_not_rotate_piece_if_the_next_position_is_in_conflict(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.L_SHAPE)
        p.current_x = 7

        blocks_before_rotate = [(0, 8), (1, 8), (2, 8), (2, 9)]
        for point in blocks_before_rotate:
            self.assertTrue(p.value_at(point[0], point[1]) > 0)

        p.handle_event(Event(KEYDOWN, { 'key': K_SPACE }))

        for point in blocks_before_rotate:
            self.assertTrue(p.value_at(point[0], point[1]) > 0)

    def test_blocks_in_full_line_are_marked_to_be_cleared(self):
        p = PlayerArea()
        p.current_piece = Piece(Piece.BLOCK_SHAPE)

        self.assertEqual(p.counter_to_clear_blocks, 0)

        # Fill some points along the bottom of the grid with an opening
        # in the middle that will be filled by the current piece.
        prefilled_points = [(18, 0), (18, 1), (18, 2), (18, 3),
                            (18, 6), (18, 7), (18, 8), (18, 9),
                            (19, 0), (19, 1), (19, 2), (19, 3),
                            (19, 6), (19, 7), (19, 8), (19, 9)]
        for point in prefilled_points:
            p.grid[(point[0] * PlayerArea.GRID_COLUMNS) + point[1]] = 1

        # Drop the current piece to the floor, which should fill in two
        # complete lines, so every block on the grid will be cleared out.
        p.handle_event(Event(KEYDOWN, { 'key': K_UP }))

        for row in (18, 19):
            for col in range(PlayerArea.GRID_COLUMNS):
                self.assertEqual(p.value_at(row, col), PlayerArea.BLOCK_TO_BE_CLEARED,
                                 "block should be marked at (%s, %s)" % (row, col))

        self.assertEqual(p.counter_to_clear_blocks, PlayerArea.TICKS_TO_CLEAR_BLOCKS)

    # def test_increment_level_after_clearing_a_number_of_rows(self):
    #     p = PlayerArea()
    #     p.lines_cleared = PlayerArea.LINES_TO_NEXT_LEVEL - 1

    #     self.assertEqual(p.level, 1)
    #     clear_line(p)
    #     self.assertEqual(p.level, 2)

# TODO:
# Test moving from level 1 to 2.
# Test increasing level while clearing multiple lines at once.
# Test do not increase past max level.

def print_grid(grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            print grid[(row * cols) + col],
        print

def tick_til_lines_cleared(area):
    """
    Once a line is marked to be cleared, there are a set number of ticks
    before those lines will actually be removed from the grid to allow
    time for the animation of the lines clearing. This helper method
    calls the tick() method on the player area enough times for the
    """
    while area.counter_to_clear_blocks > 0:
        area.tick()

if __name__ == '__main__':
    unittest.main()
