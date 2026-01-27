import unittest
from checkers import CheckersBoard
from cpu import CPUPlayer

class TestCheckersGame(unittest.TestCase):
    """
    A test suite for the Checkers game.

    This class contains a series of unit tests to verify the functionality of the Checkers game, 
    including the initial setup of the board, the validation of moves, and the decision-making process 
    of the CPU player.
    """

    def setUp(self):
        """
        Set up method called before each test.

        Initializes a new CheckersBoard and a CPUPlayer instance to be used in the tests.
        """
        self.board = CheckersBoard()
        self.cpu_player = CPUPlayer(self.board, 'B')

    def test_initial_board_setup(self):
        """
        Test if the initial board is set up correctly.

        Verifies that the board has the correct number of rows and columns as per standard Checkers rules.
        """
        initial_board = self.board.create_board()
        self.assertEqual(len(initial_board), 8, "Board should have 8 rows")
        for row in initial_board:
            self.assertEqual(len(row), 8, "Each row should have 8 columns")
        # Additional checks can be implemented to verify the correct placement of pieces on the board

    def test_valid_move(self):
        """
        Test a valid move for a piece.

        Checks if the game correctly recognizes a valid move according to Checkers rules.
        """
        start_pos = (2, 3)  # Assuming a piece is at this position on the initial board
        end_pos = (3, 4)    # A potentially valid move position
        self.assertTrue(self.board.is_valid_move(start_pos, end_pos), "This should be a valid move")

    def test_invalid_move(self):
        """
        Test an invalid move for a piece.

        Ensures that the game correctly identifies and rejects invalid moves.
        """
        start_pos = (2, 3)  # Assuming a piece is at this position
        end_pos = (4, 5)    # An invalid move position
        self.assertFalse(self.board.is_valid_move(start_pos, end_pos), "This should be an invalid move")

    def test_cpu_player_decision(self):
        """
        Test CPU player's decision-making.

        Verifies that the CPU player is able to make a move, demonstrating the functioning of its AI logic.
        """
        cpu_move = self.cpu_player.choose_move()
        self.assertIsNotNone(cpu_move, "CPU should be able to make a move")

if __name__ == '__main__':
    unittest.main()
