from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checkers import CheckersBoard
from cpu import CPUPlayer

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Game state storage (in-memory, resets on cold start)
games = {}

def get_game(session_id='default'):
    if session_id not in games:
        games[session_id] = {
            'board': CheckersBoard(),
            'mode': 'ai'
        }
    return games[session_id]

@app.route('/')
def index():
    """Serve the welcome/home page."""
    return render_template('welcome.html')

@app.route('/game')
def game():
    """Serve the game page."""
    game_state = get_game()
    return render_template('index.html', board=game_state['board'].board, current_player=game_state['board'].current_player)

@app.route('/move', methods=['POST'])
def move():
    """Handle player moves."""
    game_state = get_game()
    game = game_state['board']
    game_mode = game_state['mode']

    data = request.json
    start = tuple(data['start'])
    end = tuple(data['end'])

    valid_move, next_player, continue_turn, mandatory_capture = game.move_piece(start, end)

    response_data = generate_response(game, valid_move, continue_turn, mandatory_capture)

    # In AI mode, if it's CPU's turn and game not over, get CPU moves
    if valid_move and game_mode == 'ai' and not game.is_game_over() and game.current_player == 'B':
        cpu_moves = get_cpu_moves(game)
        response_data['cpu_moves'] = cpu_moves
        response_data['board'] = game.board
        response_data['current_player'] = game.current_player
        response_data['game_over'] = game.is_game_over()
        if response_data['game_over']:
            response_data['winner'] = 'R' if not game.has_pieces('B') or not game.has_valid_moves('B') else 'B'

    return jsonify(response_data)

def get_cpu_moves(game):
    """Gets all CPU moves and executes them, returning the move sequence for animation."""
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

def generate_response(game, valid_move, continue_turn, mandatory_capture):
    """Generates response data for the client."""
    game_over = game.is_game_over()
    winner = None
    no_legal_moves = False

    if game_over:
        winner = 'R' if not game.has_pieces('B') or not game.has_valid_moves('B') else 'B'
        no_legal_moves = not game.has_valid_moves(winner)

    return {
        'valid': valid_move,
        'board': game.board,
        'current_player': game.current_player,
        'continue_turn': continue_turn and not game_over,
        'mandatory_capture': mandatory_capture,
        'game_over': game_over,
        'winner': winner,
        'no_legal_moves': no_legal_moves
    }

@app.route('/reset', methods=['GET', 'POST'])
def reset_game():
    """Reset the game to its initial state."""
    game_state = get_game()
    game_state['board'] = CheckersBoard()

    if request.method == 'POST' and request.json:
        mode = request.json.get('mode', 'ai')
        if mode in ['ai', 'human']:
            game_state['mode'] = mode

    return jsonify({'success': True, 'mode': game_state['mode']})

@app.route('/start', methods=['POST'])
def start_game():
    """Start a new game with the specified mode."""
    game_state = get_game()
    game_state['board'] = CheckersBoard()

    data = request.json or {}
    mode = data.get('mode', 'ai')
    if mode in ['ai', 'human']:
        game_state['mode'] = mode

    return jsonify({'success': True, 'mode': game_state['mode']})

# For local development
if __name__ == '__main__':
    app.run(debug=True)
