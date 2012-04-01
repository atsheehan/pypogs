import unittest
import test_player_area
import test_piece

if __name__ == '__main__':
    test_suites = [
        unittest.TestLoader().loadTestsFromTestCase(test_player_area.TestPlayerArea),
        unittest.TestLoader().loadTestsFromTestCase(test_piece.TestPiece)
        ]

    suite = unittest.TestSuite(test_suites)
    unittest.TextTestRunner().run(suite)
