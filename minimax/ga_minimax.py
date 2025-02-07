from copy import deepcopy
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

import random
from copy import deepcopy
from checkers.constants import RED, WHITE

def GA_minimax(position, depth, alpha, beta, max_player, game, evaluation_function):
    if depth == 0 or position.winner() is not None:
        return evaluation_function(position) + random.uniform(-0.5, 0.5), position  # Add small randomness to evaluation
    
    if max_player:
        max_eval = float('-inf')
        best_moves = []
        for move in get_all_moves(position, WHITE, game):
            evaluation, _ = GA_minimax(move, depth-1, alpha, beta, False, game, evaluation_function)
            if evaluation > max_eval:
                max_eval = evaluation
                best_moves = [move]
            elif evaluation == max_eval:
                best_moves.append(move)
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, random.choice(best_moves) 
    else:
        min_eval = float('inf')
        best_moves = []
        for move in get_all_moves(position, RED, game):
            evaluation, _ = GA_minimax(move, depth-1, alpha, beta, True, game, evaluation_function)
            if evaluation < min_eval:
                min_eval = evaluation
                best_moves = [move]
            elif evaluation == min_eval:
                best_moves.append(move)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, random.choice(best_moves) 


def simulate_move(piece, move, board, game, skip):
    # Ensure piece is a valid piece object
    if piece:
        if skip:
            for skipped_piece in skip:
                board.remove([skipped_piece])
        board.move(piece, move[0], move[1])
    return board


def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # Create a deepcopy of the board to simulate the move
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
            random.shuffle(moves) 
            #print(f"Generated move: {move} for piece at {piece.row}, {piece.col}")
    return moves


