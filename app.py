from flask import Flask, render_template, request, jsonify
from checkers import CheckersBoard
from cpu import CPUPlayer

app = Flask(__name__)

# Game state storage
games = {}

def get_game(session_id='default'):
    if session_id not in games:
        games[session_id] = {
            'board': CheckersBoard(),
            'mode': 'ai',
            'position_history': []
        }
    return games[session_id]


def position_key(board, current_player):
    """Deterministic key: full board layout + piece types (man vs queen) + side to move."""
    rows = []
    for row in board:
        rows.append(''.join(cell if cell != ' ' else '.' for cell in row))
    return '|'.join(rows) + ':' + current_player


def check_threefold_repetition(position_history, key):
    """True if this position has occurred 3 times at any point in the game."""
    return sum(1 for k in position_history if k == key) >= 3

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
    position_history = game_state['position_history']

    data = request.json
    start = tuple(data['start'])
    end = tuple(data['end'])

    valid_move, next_player, continue_turn, mandatory_capture = game.move_piece(start, end)

    draw_by_repetition = False
    if valid_move:
        key = position_key(game.board, game.current_player)
        position_history.append(key)
        if check_threefold_repetition(position_history, key):
            draw_by_repetition = True

    response_data = generate_response(game, valid_move, continue_turn, mandatory_capture)
    response_data['draw_by_repetition'] = draw_by_repetition

    # In AI mode, if it's CPU's turn and game not over, get CPU moves
    if valid_move and game_mode == 'ai' and not game.is_game_over() and not draw_by_repetition and game.current_player == 'B':
        cpu_moves = get_cpu_moves(game, position_history)
        response_data['cpu_moves'] = cpu_moves
        response_data['board'] = game.board
        response_data['current_player'] = game.current_player
        response_data['game_over'] = game.is_game_over()
        response_data['draw_by_repetition'] = check_threefold_after_cpu(position_history, game)
        if response_data['game_over'] and not response_data['draw_by_repetition']:
            response_data['winner'] = 'R' if not game.has_pieces('B') or not game.has_valid_moves('B') else 'B'
        elif response_data['draw_by_repetition']:
            response_data['game_over'] = True
            response_data['winner'] = None

    if draw_by_repetition and not response_data.get('cpu_moves'):
        response_data['game_over'] = True
        response_data['winner'] = None

    return jsonify(response_data)

def get_cpu_moves(game, position_history):
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
            key = position_key(game.board, game.current_player)
            position_history.append(key)
        else:
            break
    return cpu_moves


def check_threefold_after_cpu(position_history, game):
    """True if current position has occurred 3 times after CPU move sequence."""
    key = position_key(game.board, game.current_player)
    return check_threefold_repetition(position_history, key)

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
        'no_legal_moves': no_legal_moves,
        'draw_by_repetition': False
    }

@app.route('/reset', methods=['GET', 'POST'])
def reset_game():
    """Reset the game to its initial state."""
    game_state = get_game()
    game_state['board'] = CheckersBoard()
    game_state['position_history'] = []

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
    game_state['position_history'] = []

    data = request.json or {}
    mode = data.get('mode', 'ai')
    if mode in ['ai', 'human']:
        game_state['mode'] = mode

    return jsonify({'success': True, 'mode': game_state['mode']})

if __name__ == '__main__':
    app.run(debug=True)
