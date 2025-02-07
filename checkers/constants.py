import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 9, 9
SQUARE_SIZE = WIDTH // COLS

# RGB Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Loading piece images
crown = pygame.transform.scale(pygame.image.load('crown.png'), (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
KING = pygame.transform.scale(pygame.image.load('king.png'), (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
QUEEN = pygame.transform.scale(pygame.image.load('queen.png'), (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
SOLDIER = pygame.transform.scale(pygame.image.load('soldier.png'), (SQUARE_SIZE - 10, SQUARE_SIZE - 10))