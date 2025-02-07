import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from checkers.board import Board  # Assuming Board class from your game implementation
from minimax.algorithm import alpha_beta_minimax  # Import alpha_beta_minimax
from copy import deepcopy
import random

# Constants for colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
ROWS, COLS = 9, 9  # Example board size, adjust as per your game

# Fuzzy variables
piece_value = ctrl.Antecedent(np.arange(0, 11, 1), 'piece_value')
game_phase = ctrl.Antecedent(np.arange(0, 11, 1), 'game_phase')
move_strength = ctrl.Consequent(np.arange(0, 101, 1), 'move_strength')

# Define membership functions with sufficient overlap
piece_value['soldier'] = fuzz.trimf(piece_value.universe, [0, 2, 4])
piece_value['queen'] = fuzz.trimf(piece_value.universe, [3, 5, 7])
piece_value['king'] = fuzz.trimf(piece_value.universe, [6, 8, 10])

game_phase['very_early'] = fuzz.trimf(game_phase.universe, [0, 1, 3])
game_phase['early'] = fuzz.trimf(game_phase.universe, [2, 4, 6])
game_phase['midgame'] = fuzz.trimf(game_phase.universe, [5, 7, 9])
game_phase['late'] = fuzz.trimf(game_phase.universe, [8, 10, 10])
game_phase['endgame'] = fuzz.trimf(game_phase.universe, [9, 10, 10])

move_strength['very_weak'] = fuzz.trimf(move_strength.universe, [0, 15, 30])
move_strength['weak'] = fuzz.trimf(move_strength.universe, [20, 35, 50])
move_strength['medium'] = fuzz.trimf(move_strength.universe, [45, 60, 75])
move_strength['strong'] = fuzz.trimf(move_strength.universe, [70, 85, 100])
move_strength['very_strong'] = fuzz.trimf(move_strength.universe, [90, 100, 100])

# Define fuzzy rules to prioritize aggressive behavior, including captures
rules = [
    ctrl.Rule(game_phase['very_early'] & piece_value['soldier'], move_strength['very_strong']),
    ctrl.Rule(game_phase['very_early'] & piece_value['queen'], move_strength['very_strong']),
    ctrl.Rule(game_phase['very_early'] & piece_value['king'], move_strength['very_strong']),

    ctrl.Rule(game_phase['early'] & piece_value['soldier'], move_strength['very_strong']),
    ctrl.Rule(game_phase['early'] & piece_value['queen'], move_strength['very_strong']),
    ctrl.Rule(game_phase['early'] & piece_value['king'], move_strength['very_strong']),

    ctrl.Rule(game_phase['midgame'] & piece_value['soldier'], move_strength['very_strong']),
    ctrl.Rule(game_phase['midgame'] & piece_value['queen'], move_strength['very_strong']),
    ctrl.Rule(game_phase['midgame'] & piece_value['king'], move_strength['very_strong']),

    ctrl.Rule(game_phase['late'] & piece_value['soldier'], move_strength['very_strong']),
    ctrl.Rule(game_phase['late'] & piece_value['queen'], move_strength['very_strong']),
    ctrl.Rule(game_phase['late'] & piece_value['king'], move_strength['very_strong']),

    ctrl.Rule(game_phase['endgame'] & piece_value['soldier'], move_strength['very_strong']),
    ctrl.Rule(game_phase['endgame'] & piece_value['queen'], move_strength['very_strong']),
    ctrl.Rule(game_phase['endgame'] & piece_value['king'], move_strength['very_strong']),
    
    # Include rules to prioritize capturing moves
    ctrl.Rule(game_phase['very_early'] & (piece_value['soldier'] | piece_value['queen'] | piece_value['king']), move_strength['very_strong']),
    ctrl.Rule(game_phase['early'] & (piece_value['soldier'] | piece_value['queen'] | piece_value['king']), move_strength['very_strong']),
    ctrl.Rule(game_phase['late'] & (piece_value['soldier'] | piece_value['queen'] | piece_value['king']), move_strength['very_strong']),
    ctrl.Rule(game_phase['midgame'] & (piece_value['soldier'] | piece_value['queen'] | piece_value['king']), move_strength['very_strong']),
    ctrl.Rule(game_phase['endgame'] & (piece_value['soldier'] | piece_value['queen'] | piece_value['king']), move_strength['very_strong']),
    ctrl.Rule(piece_value['queen'] | piece_value['king'] | piece_value['soldier'], move_strength['very_strong']),  # Additional prioritization for queens and kings
]

# Create fuzzy control system
move_ctrl = ctrl.ControlSystem(rules)
move_simulation = ctrl.ControlSystemSimulation(move_ctrl)

# Function to calculate fuzzy move strength
def calculate_fuzzy_move(board, row, col):
    piece = board.get_piece(row, col)
    if piece and piece.color == WHITE:  # Assuming AI controls WHITE pieces
        if piece.type == 'soldier':
            piece_value_value = 2
        elif piece.type == 'queen':
            piece_value_value = 5
        elif piece.type == 'king':
            piece_value_value = 8
        else:
            piece_value_value = 1
        
        total_pieces = sum(1 for r in range(ROWS) for c in range(COLS) if board.get_piece(r, c))
        game_phase_value = (total_pieces / (ROWS * COLS)) * 10
        
        move_simulation.input['piece_value'] = piece_value_value
        move_simulation.input['game_phase'] = game_phase_value
        
        try:
            move_simulation.compute()
            move_strength = move_simulation.output['move_strength']
        except ValueError as e:
            print(f"Error in fuzzy computation: {e}")
            move_strength = 0
        
        # Get all possible moves for the piece
        moves = board.get_valid_moves(piece)
        
        # Evaluate move strengths
        move_strengths = {}
        for move, skips in moves.items():
            if skips:  # Check if the move involves a capture
                move_strengths[move] = move_strength + random.uniform(20, 30)  # Adjust strength for capturing moves
            else:
                move_strengths[move] = move_strength + random.uniform(-10, 10)  # Randomize non-capture move strength
        
        return move_strengths
    
    return {}

def simulate_move(piece, move, board, skip):
    # Ensure piece is a valid piece object
    if piece:
        if skip:
            for skipped_piece in skip:
                board.remove([skipped_piece])
        board.move(piece, move[0], move[1])
    return board

def determine_best_fuzzy_move(board):
    best_moves = []
    best_strength = -1

    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(row, col)
            if piece and piece.color == WHITE:  # Assuming AI controls WHITE pieces
                move_strengths = calculate_fuzzy_move(board, row, col)
                for move, strength in move_strengths.items():
                    if strength > best_strength:
                        best_strength = strength
                        best_moves = [(row, col, move, move_strengths)]
                    elif strength == best_strength:
                        best_moves.append((row, col, move, move_strengths))

    if best_moves:
        best_move = random.choice(best_moves)
        row, col, move, move_strengths = best_move

        # Make a deepcopy of the board to simulate the move
        new_board = deepcopy(board)
        piece = new_board.get_piece(row, col)
        valid_moves = new_board.get_valid_moves(piece)
        skip = valid_moves[move] if move in valid_moves else []
        new_board = simulate_move(piece, move, new_board, skip)
        return new_board

    return None

# Example usage
if __name__ == '__main__':
    board = Board()  # Instantiate your Board class with initial setup
    game = None  # Initialize your game object as needed
    best_move = determine_best_fuzzy_move(board)
    print(f"Best fuzzy move: {best_move}")
    
    # Apply alpha-beta pruning for deeper move analysis
    alpha_beta_result, best_move = alpha_beta_minimax(board, 3, float('-inf'), float('inf'), True, game)
    print(f"Alpha-beta pruning result: {alpha_beta_result}, Best move: {best_move}")
