from flask import Flask, render_template, request, jsonify
from checkers import CheckersBoard
from cpu import CPUPlayer

# Initialize Flask app and create a new Checkers game instance
app = Flask(__name__)
game = CheckersBoard()
game_mode = 'ai'  # 'ai' or 'human' - default to AI opponent

@app.route('/')
def index():
    """
    Route to serve the main page of the Checkers game.

    Renders the index.html template with the current state of the game board
    and the current player.
    """
    return render_template('index.html', board=game.board, current_player=game.current_player)

@app.route('/move', methods=['POST'])
def move():
    """
    Route to handle player moves.

    Receives the move as JSON data, processes the move, and updates the game state.
    In AI mode, returns CPU moves separately so frontend can animate them.
    """
    global game_mode
    data = request.json
    start = tuple(data['start'])
    end = tuple(data['end'])

    valid_move, next_player, continue_turn, mandatory_capture = game.move_piece(start, end)

    response = generate_response(valid_move, continue_turn, mandatory_capture)
    response_data = response.get_json()

    # In AI mode, if it's CPU's turn and game not over, get CPU moves
    if valid_move and game_mode == 'ai' and not game.is_game_over() and game.current_player == 'B':
        cpu_moves = get_cpu_moves()
        response_data['cpu_moves'] = cpu_moves
        response_data['board'] = game.board
        response_data['current_player'] = game.current_player
        response_data['game_over'] = game.is_game_over()
        if response_data['game_over']:
            response_data['winner'] = 'R' if not game.has_pieces('B') or not game.has_valid_moves('B') else 'B'

    return jsonify(response_data)

def get_cpu_moves():
    """
    Gets all CPU moves and executes them, returning the move sequence for animation.

    Returns a list of moves where each move is {start: [row, col], end: [row, col]}
    """
    cpu_moves = []
    while game.current_player == 'B' and game.has_valid_moves('B'):
        cpu_player = CPUPlayer(game, 'B')
        cpu_move_start, cpu_move_end = cpu_player.choose_move()
        if cpu_move_start and cpu_move_end:
            cpu_moves.append({
                'start': list(cpu_move_start),
                'end': list(cpu_move_end)
            })
            game.move_piece(cpu_move_start, cpu_move_end)
        else:
            break
    return cpu_moves

def generate_response(valid_move, continue_turn, mandatory_capture):
    """
    Generates a JSON response to be sent back to the client.

    Includes information about the validity of the move, the game state, 
    and whether the game is over.

    Returns:
        jsonify: A Flask JSON response containing game state information.
    """
    game_over = game.is_game_over()
    winner = None
    no_legal_moves = False

    if game_over:
        # Determine the winner based on remaining pieces and valid moves
        winner = 'R' if not game.has_pieces('B') or not game.has_valid_moves('B') else 'B'
        no_legal_moves = not game.has_valid_moves(winner)

    return jsonify({
        'valid': valid_move,
        'board': game.board,
        'current_player': game.current_player,
        'continue_turn': continue_turn and not game_over,
        'mandatory_capture': mandatory_capture,
        'game_over': game_over,
        'winner': winner,
        'no_legal_moves': no_legal_moves
    })

@app.route('/reset', methods=['GET', 'POST'])
def reset_game():
    """
    Route to reset the game to its initial state.

    Re-initializes the game board and optionally sets the game mode.
    """
    global game, game_mode
    game = CheckersBoard()

    if request.method == 'POST' and request.json:
        mode = request.json.get('mode', 'ai')
        if mode in ['ai', 'human']:
            game_mode = mode

    return jsonify({'success': True, 'mode': game_mode})

if __name__ == '__main__':
    app.run(debug=True)
