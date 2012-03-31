import unittest
import test_player_area

if __name__ == '__main__':
    test_suites = [
        unittest.TestLoader().loadTestsFromTestCase(test_player_area.TestPlayerArea)
        ]

    suite = unittest.TestSuite(test_suites)
    unittest.TextTestRunner().run(suite)
