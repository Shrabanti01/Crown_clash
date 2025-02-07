import pygame
from pygame.locals import *
from .constants import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE, GREY
from .piece import Piece

pygame.init()
pygame.mixer.init()


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 13
        self.red_kings = self.white_kings = 0
        self.turn = WHITE
        self.create_board()

    def draw_cubes(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    '''
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
    '''
    def evaluate(self):
        white_score = 0
        red_score = 0

        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == WHITE:
                        if piece.type == 'soldier':
                            white_score += 1
                        elif piece.type == 'queen':
                            white_score += 3
                        elif piece.type == 'king':
                            white_score += 5
                    elif piece.color == RED:
                        if piece.type == 'soldier':
                            red_score += 1
                        elif piece.type == 'queen':
                            red_score += 3
                        elif piece.type == 'king':
                            red_score += 5

        return white_score - red_score

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        if piece:
            # Check if the target cell is occupied
            target_piece = self.get_piece(row, col)
            if target_piece != 0:
                # Remove the captured piece
                self.remove([target_piece])
            #print(f"Before move - Piece position: ({piece.row}, {piece.col}), Board state:")
            self.board[piece.row][piece.col] = 0  
            self.board[row][col] = piece  
            piece.move(row, col) 
            #print(f"After move - Piece position: ({piece.row}, {piece.col}), Board state:")

            if row == 0 or row == ROWS - 1:
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1


    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row == 0:
                        self.board[row].append(Piece(row, col, 'king', WHITE))
                    elif row == 1:
                        self.board[row].append(Piece(row, col, 'queen', WHITE))
                    elif row == 2:
                        self.board[row].append(Piece(row, col, 'soldier', WHITE))
                    elif row == 6:
                        self.board[row].append(Piece(row, col, 'soldier', RED))
                    elif row == 7:
                        self.board[row].append(Piece(row, col, 'queen', RED))
                    elif row == 8:
                        self.board[row].append(Piece(row, col, 'king', RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_cubes(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        
        for piece in pieces:
            if piece != 0:
                self.board[piece.row][piece.col] = 0
                
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1


    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 

    def get_valid_moves(self, piece):
        moves = {}
        row, col = piece.row, piece.col

        if piece.type == 'soldier':
            if piece.color == RED:
                moves.update(self._get_moves(row - 1, col, -1, piece.color))
            else:
                moves.update(self._get_moves(row + 1, col, 1, piece.color))
        elif piece.type == 'queen':
            moves.update(self._get_moves(row, col - 1, 0, piece.color))  # left
            moves.update(self._get_moves(row, col + 1, 0, piece.color))  # right
            if piece.color == RED:
               moves.update(self._get_moves(row - 1, col, 0, piece.color))  # up
            else:
               moves.update(self._get_moves(row + 1, col, 0, piece.color))  # down
        elif piece.type == 'king':
            moves.update(self._get_moves(row - 1, col, 0, piece.color))  # up
            moves.update(self._get_moves(row + 1, col, 0, piece.color))  # down
            moves.update(self._get_moves(row, col - 1, 0, piece.color))  # left
            moves.update(self._get_moves(row, col + 1, 0, piece.color))  # right
            # Diagonals
            moves.update(self._get_moves(row - 1, col - 1, 0, piece.color))  # up-left
            moves.update(self._get_moves(row - 1, col + 1, 0, piece.color))  # up-right
            moves.update(self._get_moves(row + 1, col - 1, 0, piece.color))  # down-left
            moves.update(self._get_moves(row + 1, col + 1, 0, piece.color))  # down-right
            #print(f"Valid moves for {piece.color} {piece.type} at ({row}, {col}): {moves}")  # Debugging print
        return moves

    def _get_moves(self, row, col, direction, color):
        moves = {}
        if 0 <= row < ROWS and 0 <= col < COLS:
            current = self.board[row][col]
            if current == 0:
                moves[(row, col)] = []
            elif current.color != color:
                moves[(row, col)] = [current]

        return moves                    
                      
                      
  