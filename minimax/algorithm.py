from copy import deepcopy
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

def alpha_beta_minimax(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position
    
    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation, _ = alpha_beta_minimax(move, depth-1, alpha, beta, False, game)
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation, _ = alpha_beta_minimax(move, depth-1, alpha, beta, True, game)
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move

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
            #print(f"Generated move: {move} for piece at {piece.row}, {piece.col}")
    return moves


