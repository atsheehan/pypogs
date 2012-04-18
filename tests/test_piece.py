from piece import Piece
import unittest

class TestPiece(unittest.TestCase):
    
    def test_select_values_for_different_shapes(self):
        p = Piece(Piece.L_SHAPE)
        
        block_values = [(0, 1), (1, 1), (2, 1), (2, 2)]
        for point in block_values:
            self.assertEqual(3, p.value_at(point[0], point[1]),
                             "point should exist at (%s, %s)" % (point[0], point[1]))

        p = Piece(Piece.T_SHAPE)
        block_values = [(0, 2), (1, 1), (1, 2), (2, 2)]
        for point in block_values:
            self.assertEqual(2, p.value_at(point[0], point[1]),
                             "point should exist at (%s, %s)" % (point[0], point[1]))
        
    def test_rotate_piece_clockwise_through_all_rotations(self):
        p = Piece(Piece.T_SHAPE)
        
        rotations = [((0, 2), (1, 1), (1, 2), (2, 2)),
                     ((0, 2), (1, 1), (1, 2), (1, 3)),
                     ((0, 2), (1, 2), (1, 3), (2, 2)),
                     ((1, 1), (1, 2), (1, 3), (2, 2)),
                     ((0, 2), (1, 1), (1, 2), (2, 2))]
        for all_points in rotations:
            for point in all_points:
                self.assertEqual(p.value_at(point[0], point[1]), 2)
            p.rotate_clockwise()

    def test_rotate_piece_counter_clockwise_through_all_rotations(self):
        p = Piece(Piece.T_SHAPE)
        
        rotations = [((0, 2), (1, 1), (1, 2), (2, 2)),
                     ((1, 1), (1, 2), (1, 3), (2, 2)),
                     ((0, 2), (1, 2), (1, 3), (2, 2)),
                     ((0, 2), (1, 1), (1, 2), (1, 3)),
                     ((0, 2), (1, 1), (1, 2), (2, 2))]
        for all_points in rotations:
            for point in all_points:
                self.assertEqual(p.value_at(point[0], point[1]), 2)
            p.rotate_counter_clockwise()
        
