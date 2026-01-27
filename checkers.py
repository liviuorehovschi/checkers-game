class CheckersBoard:
    """
    A class to represent a Checkers game board.

    Attributes
    ----------
    board : list
        A 2D list representing the game board.
    current_player : str
        The current player ('R' for Red or 'B' for Black).
    multi_capture_in_progress : bool
        Flag to track if multiple captures are in progress.
    """

    def __init__(self):
        """
        Initializes the CheckersBoard with a starting board layout, 
        sets the current player to 'R' (Red), and sets the multi-capture 
        flag to False.
        """
        self.board = self.create_board()
        self.current_player = 'R'
        self.multi_capture_in_progress = False

    def create_board(self):
        """
        Creates the initial layout of the checkers board.

        Returns
        -------
        list
            A 2D list representing the initial state of the game board.
        """
        board = []
        for row in range(8):
            board.append([])
            for col in range(8):
                # Alternating cells have checkers pieces, determined by the row and column numbers
                if col % 2 != row % 2:
                    if row < 3:
                        board[row].append('B')  # Black pieces in the first three rows
                    elif row > 4:
                        board[row].append('R')  # Red pieces in the last three rows
                    else:
                        board[row].append(' ')  # Empty space
                else:
                    board[row].append(' ')  # Empty space
        return board

    def is_valid_move(self, start, end):
        """
        Checks if a move is valid.

        Parameters
        ----------
        start : tuple
            The starting position (row, col) of the piece.
        end : tuple
            The ending position (row, col) of the move.

        Returns
        -------
        bool
            True if the move is valid, False otherwise.
        """
        start_row, start_col = start
        end_row, end_col = end
        moving_piece = self.board[start_row][start_col]
        target_piece = self.board[end_row][end_col]

        if target_piece != ' ':
            return False  # Can't move to a cell that's already occupied

        row_direction = end_row - start_row
        col_distance = abs(end_col - start_col)

        # Logic for normal pieces
        if moving_piece in ['R', 'B']:
            # Simple move
            if abs(row_direction) == 1 and col_distance == 1:
                if moving_piece == 'R' and row_direction == -1:
                    return True
                if moving_piece == 'B' and row_direction == 1:
                    return True

            # Capture move
            elif abs(row_direction) == 2 and col_distance == 2:
                mid_row = (start_row + end_row) // 2
                mid_col = (start_col + end_col) // 2
                mid_piece = self.board[mid_row][mid_col]
                if mid_piece == ' ' or mid_piece[0] == moving_piece[0]:
                    return False  # Can't capture your own piece or jump over an empty space
                return True

        # Queen move logic
        elif moving_piece in ['RQ', 'BQ']:
            # Simple move for queen
            if abs(row_direction) == 1 and col_distance == 1:
                return True  # Allow one-step moves in any direction

            # Capture move for queen
            elif abs(row_direction) == 2 and col_distance == 2:
                mid_row = (start_row + end_row) // 2
                mid_col = (start_col + end_col) // 2
                mid_piece = self.board[mid_row][mid_col]
                if mid_piece == ' ' or mid_piece[0] == moving_piece[0]:
                    return False  # Can't capture your own piece or jump over an empty space
                return True

        return False
    def move_piece(self, start, end):
        # Check if the current player must capture and if the move is a capture move
        if self.must_capture() and not self.is_capture_move(start, end):
            return False, self.current_player, False, True

        # Check if the move is valid
        if not self.is_valid_move(start, end):
            return False, self.current_player, False, False

        start_row, start_col = start
        end_row, end_col = end
        moving_piece = self.board[start_row][start_col]

        # Move the piece
        self.board[start_row][start_col] = ' '
        self.board[end_row][end_col] = moving_piece

        # Handle capture move
        if abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.board[mid_row][mid_col] = ' '  # Remove the captured piece

            further_captures = self.check_captures_from_position(end_row, end_col)
            if not further_captures:
                self.current_player = 'B' if self.current_player == 'R' else 'R'
                self.multi_capture_in_progress = False
            else:
                self.multi_capture_in_progress = True
        else:
            self.current_player = 'B' if self.current_player == 'R' else 'R'
            self.multi_capture_in_progress = False

        # Promote to queen if the piece reaches the opposite end
        if end_row == 0 and moving_piece == 'R':
            self.board[end_row][end_col] = 'RQ'
        elif end_row == 7 and moving_piece == 'B':
            self.board[end_row][end_col] = 'BQ'

        # Check if the game is over
        if self.is_game_over():
            return True, self.current_player, False, False

        return True, self.current_player, False, False
    def get_possible_captures(self, player):
        """
        Gets all possible captures for a given player.

        Parameters
        ----------
        player : str
            The player ('R' for Red, 'B' for Black) for whom to find captures.

        Returns
        -------
        list
            A list of tuples representing all possible captures.
        """
        captures = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col].startswith(player):
                    captures += self.check_captures_from_position(row, col)
        return captures

    def check_captures_from_position(self, row, col):
        """
        Checks for possible captures from a specific position on the board.

        Parameters
        ----------
        row : int
            The row number of the position.
        col : int
            The column number of the position.

        Returns
        -------
        list
            A list of tuples representing possible capture moves from the given position.
        """
        captures = []
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dr, dc in directions:
            end_row, end_col = row + dr, col + dc
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.is_valid_move((row, col), (end_row, end_col)):
                    captures.append(((row, col), (end_row, end_col)))
        return captures

    def is_capture_move(self, start, end):
        """
        Checks if a move is a capture move.

        Parameters
        ----------
        start : tuple
            The starting position (row, col) of the piece.
        end : tuple
            The ending position (row, col) of the move.

        Returns
        -------
        bool
            True if the move is a capture move, False otherwise.
        """
        return abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 2

    def must_capture(self):
        """
        Checks if the current player must make a capture move.

        Returns
        -------
        bool
            True if a capture move is available and mandatory, False otherwise.
        """
        return bool(self.get_possible_captures(self.current_player))

    def has_pieces(self, player):
        """
        Checks if a player has any pieces left on the board.

        Parameters
        ----------
        player : str
            The player ('R' for Red, 'B' for Black) to check.

        Returns
        -------
        bool
            True if the player has pieces on the board, False otherwise.
        """
        return any(player in cell for row in self.board for cell in row)

    def has_valid_moves(self, player):
        """
        Determines if the given player has any valid moves left.

        This function checks all pieces belonging to the player and determines if any of them can make a valid move. 
        This includes both regular moves and capture moves.

        Parameters
        ----------
        player : str
            The player ('R' for Red, 'B' for Black) to check for valid moves.

        Returns
        -------
        bool
            True if the player has at least one valid move, False otherwise.
        """
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                # Check if the piece belongs to the player
                if piece.startswith(player):
                    # If the piece is a queen, check for regular moves in all directions
                    if 'Q' in piece:
                        if self.check_regular_moves_from_position(row, col):
                            return True
                    else:
                        # For non-queen pieces, determine the direction of movement based on the player
                        direction = 1 if player == 'B' else -1
                        for dc in (-1, 1):  # Check both diagonal directions
                            end_row, end_col = row + direction, col + dc
                            if 0 <= end_row < 8 and 0 <= end_col < 8:
                                # Check for a regular move (empty target cell)
                                if self.board[end_row][end_col] == ' ':
                                    return True
                                # Check for a possible capture move
                                if 0 <= end_row + direction < 8 and 0 <= end_col + dc < 8:
                                    if self.board[end_row + direction][end_col + dc] == ' ' \
                                            and self.board[end_row][end_col] != ' ' \
                                            and self.board[end_row][end_col][0] != player:
                                        return True
        # If no valid moves are found, return False
        return False

    def check_regular_moves_from_position(self, row, col):
        """
        Finds all regular (non-capture) moves from a given position.

        This function is used to find all possible regular moves for a queen piece from a given position.

        Parameters
        ----------
        row : int
            The row number of the position to check from.
        col : int
            The column number of the position to check from.

        Returns
        -------
        list
            A list of tuples representing possible regular moves from the given position.
        """
        moves = []
        piece = self.board[row][col]

        # Directions for queen
        if piece in ['RQ', 'BQ']:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        # Directions for normal pieces
        elif piece == 'R':
            directions = [(-1, -1), (-1, 1)]
        elif piece == 'B':
            directions = [(1, -1), (1, 1)]
        else:
            return moves  # Return empty list for empty cell or unrecognized piece

        for dr, dc in directions:
            end_row, end_col = row + dr, col + dc
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.board[end_row][end_col] == ' ':
                    moves.append(((row, col), (end_row, end_col)))

        return moves
    
    def is_game_over(self):
        """
        Checks if the game is over, which occurs when either player has no valid moves.

        The game is considered over if one of the players cannot make a valid move. This could be 
        because they have no pieces left or because their pieces are blocked from making any moves.

        Returns
        -------
        bool
            True if the game is over, False otherwise.
        """
        # Check if either player has no valid moves
        if not self.has_valid_moves('R') or not self.has_valid_moves('B'):
            return True
        return False
    

    def apply_move(self, move):
        """
        Applies a move on the board.

        This method moves a piece from the start position to the end position.
        It handles capture moves by removing the captured piece and checks for 
        further possible captures, enabling multi-capture sequences.

        Args:
            move (tuple): A tuple containing start and end positions of the move.

        Returns:
            tuple: The position of the captured piece, if any; otherwise None.
        """
        start_pos, end_pos = move
        moving_piece = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = ' '
        self.board[end_pos[0]][end_pos[1]] = moving_piece
        
        captured_piece_pos = None
        if abs(start_pos[0] - end_pos[0]) == 2:
            # Handle capture move
            mid_row = (start_pos[0] + end_pos[0]) // 2
            mid_col = (start_pos[1] + end_pos[1]) // 2
            captured_piece_pos = (mid_row, mid_col)
            self.board[mid_row][mid_col] = ' '

            # Check for further captures
            further_captures = self.check_captures_from_position(end_pos[0], end_pos[1])
            self.multi_capture_in_progress = bool(further_captures)
        else:
            self.multi_capture_in_progress = False

        return captured_piece_pos

    def undo_move(self, move, captured_piece_pos=None):
        """
        Reverts a move on the board.

        This method is particularly useful for undoing moves during the process
        of evaluating future game states (as in the minimax algorithm).

        Args:
            move (tuple): A tuple containing start and end positions of the move.
            captured_piece_pos (tuple, optional): Position of the piece captured in the move, if any.
        """
        start_pos, end_pos = move
        moving_piece = self.board[end_pos[0]][end_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = ' '
        self.board[start_pos[0]][start_pos[1]] = moving_piece

        if captured_piece_pos:
            # Restore the captured piece
            captured_piece_color = 'R' if self.current_player == 'B' else 'B'
            self.board[captured_piece_pos[0]][captured_piece_pos[1]] = captured_piece_color

        self.multi_capture_in_progress = False

    def get_possible_moves(self, player):
        """
        Gets all possible moves for a given player.

        This includes both regular and capture moves, with priority given to
        captures if available.

        Args:
            player (str): The player ('R' for Red, 'B' for Black) for whom to find moves.

        Returns:
            list: A list of tuples representing all possible moves for the player.
        """
        if self.multi_capture_in_progress:
            # Handle multi-capture scenario
            return self.get_possible_captures(player)
        else:
            moves = []
            captures = self.get_possible_captures(player)
            if captures:
                # Prioritize captures
                return captures

            for row in range(8):
                for col in range(8):
                    if self.board[row][col].startswith(player):
                        moves.extend(self.check_regular_moves_from_position(row, col))
            return moves

    def print_board(self):
        """
        Prints the current state of the board.

        This function is primarily for debugging purposes to visualize the board state at any point in time.
        """
        for row in self.board:
            print(' '.join(row))
        print()


def test_game():
    """
    A simple function to test the CheckersBoard class.

    This function initializes a new game of Checkers, prints the initial board state,
    allows for manual testing of moves (if needed), and then prints the final state of the board.
    This is useful for quick checks and debugging.
    """
    game = CheckersBoard()
    print("Initial Board State:")
    game.print_board()

    # Here, you can add test moves to simulate a game scenario.
    print("Final Board State After Test Moves:")
    game.print_board()

if __name__ == '__main__':
    test_game()
