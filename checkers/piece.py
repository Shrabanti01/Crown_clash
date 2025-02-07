import pygame
from .constants import RED, WHITE, SQUARE_SIZE, GREY, KING, QUEEN, SOLDIER

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.type = type

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
    def make_king(self):
        self.king = True
        self.type = 'king'
    
    def draw(self, win):
        if self.type == 'king':
            image = KING
        elif self.type == 'queen':
            image = QUEEN
        else:
            image = SOLDIER
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        win.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    
    def _repr_(self):
        return str(self.color)