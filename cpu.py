from checkers import CheckersBoard

class CPUPlayer:
    def __init__(self, board, color):
        """
        Initialize a CPU player for checkers.

        Args:
            board (CheckersBoard): The current state of the checkers board.
            color (str): The color ('R' or 'B') that the CPU player is controlling.
        """
        self.board = board
        self.color = color

    def evaluate_board(self):
        """
        Evaluate the current board state from the perspective of the CPU player.

        The board is evaluated by assigning scores to pieces based on their type and position.
        The CPU's pieces are positively scored, and the opponent's pieces are negatively scored.

        Returns:
            int: An integer score representing the board state's value.
        """
        score = 0
        for row in self.board.board:
            for cell in row:
                if cell == self.color:
                    score += 100  # Assign 100 points for each piece of CPU's color
                elif cell == f"{self.color}Q":
                    score += 175  # Assign 175 points for each king of CPU's color
                elif cell in ['R', 'B'] and cell != self.color:
                    score -= 100  # Subtract points for opponent's pieces
                elif cell in ['RQ', 'BQ'] and cell[0] != self.color:
                    score -= 175  # Subtract more points for opponent's kings
        return score

    def get_possible_moves(self):
        """
        Get all possible moves for the CPU player based on the current board state.

        This includes both regular and capture moves, prioritizing captures if available.

        Returns:
            list: A list of moves where each move is represented as a tuple (start_pos, end_pos).
        """
        return self.board.get_possible_moves(self.color)

    def minimax(self, depth, alpha, beta, maximizing_player):
        """
        The minimax algorithm with alpha-beta pruning for optimizing CPU player moves.

        This method recursively explores possible moves up to a given depth and evaluates
        the board state to choose the best move.

        Args:
            depth (int): The maximum depth of the recursion.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.
            maximizing_player (bool): True if the current recursion level is maximizing, False otherwise.

        Returns:
            tuple: A tuple containing the evaluation score and the best move.
        """
        # Base case: max depth reached or game over
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board(), None

        # Maximizing player logic
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_possible_moves():
                captured_piece_pos = self.board.apply_move(move)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, not self.board.multi_capture_in_progress)
                self.board.undo_move(move, captured_piece_pos)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return max_eval, best_move
        else:
            # Minimizing player logic
            min_eval = float('inf')
            best_move = None
            for move in self.get_possible_moves():
                captured_piece_pos = self.board.apply_move(move)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, self.board.multi_capture_in_progress)
                self.board.undo_move(move, captured_piece_pos)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return min_eval, best_move

    def choose_move(self):
        """
        Choose the best move for the CPU player.

        The best move is selected using the minimax algorithm with a specified depth.

        Returns:
            tuple: The chosen move as a tuple of start and end positions.
        """
        _, best_move = self.minimax(depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=self.color == 'R')
        return best_move

# Testing the CPU player independently
if __name__ == '__main__':
    # Initialize a game board
    board = CheckersBoard()
    cpu_player = CPUPlayer(board, 'B')
    next_move = cpu_player.choose_move()
    print("CPU chooses to move:", next_move)
