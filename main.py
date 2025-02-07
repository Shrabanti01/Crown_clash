import pygame
from pygame.locals import *
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLUE
from checkers.game import Game
from minimax.algo import minimax
from minimax.algorithm import alpha_beta_minimax
from minimax.genetic_algorithm import genetic_algorithm, get_optimized_evaluation_function
from minimax.ga_minimax import GA_minimax
from PIL import Image
import imageio
import numpy as np

# Constants
FPS = 60
BACKGROUND_COLOR = (255, 240, 200)
BACKGROUND_COLORR = (255, 255, 255)
BUTTON_COLOR = (255, 150, 50)
BUTTON_HOVER_COLOR = (255, 255, 102)
TEXT_COLOR = (0, 0, 0)
SHADOW_COLOR = (100, 100, 100)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
BUTTON_FONT = pygame.font.SysFont("comicsans", 40)
TITLE_FONT = pygame.font.SysFont("comicsans", 50)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 80

background_image = pygame.transform.scale(pygame.image.load('background.jpg'), (WIDTH, HEIGHT))




def get_row_col_from_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def draw_text_center(text, font, color, surface, center, shadow=False):
    if shadow:
        shadow_color = (0, 0, 0)
        shadow_offset = (3, 3)
        shadow_text = font.render(text, True, shadow_color)
        shadow_rect = shadow_text.get_rect(center=(center[0] + shadow_offset[0], center[1] + shadow_offset[1]))
        surface.blit(shadow_text, shadow_rect)
    
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=center)
    surface.blit(textobj, textrect)

def draw_button(button_rect, text, hover):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(WIN, SHADOW_COLOR, button_rect.inflate(10, 10), border_radius=10)
    pygame.draw.rect(WIN, color, button_rect, border_radius=10)
    draw_text_center(text, BUTTON_FONT, TEXT_COLOR, WIN, button_rect.center)


def draw_opening_screen():
    WIN.blit(background_image, (0, 0))
    start_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_button(start_button_rect, 'Start', False)
    pygame.display.update()
    return start_button_rect

def draw_difficulty_screen():
    WIN.fill(BACKGROUND_COLOR)
    draw_text_center('DIFFICULTY LEVEL', TITLE_FONT, TEXT_COLOR, WIN, (WIDTH // 2, HEIGHT // 6))
    buttons = []
    for i, text in enumerate(['Easy', 'Medium', 'Hard', 'Very Hard']):
        button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 4 + i * (BUTTON_HEIGHT + 20), BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append((button_rect, text))
        draw_button(button_rect, text, False)
        

    
    how_to_play_button_rect = pygame.Rect(WIDTH - 230, HEIGHT - 100, 200, 60)
    
    
    
    draw_button(how_to_play_button_rect, 'How to Play', False)
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            draw_instructions_screen()  # Transition to instructions screen
    
    pygame.display.update()
    return buttons, how_to_play_button_rect




def draw_instructions_screen():
    WIN.fill(BACKGROUND_COLOR)  # Fill with background color
    
    # Title
    title_font = pygame.font.SysFont("comicsans", 50)
    title_text = title_font.render("Instructions", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
    WIN.blit(title_text, title_rect)
    
    # Instructions text
    instructions_font = pygame.font.SysFont("comicsans", 25)
    instructions_text = [
        "Rules:",
        "Soldier can move forward 1 cell","and capture opponent pieces."," It replaces the opponent's piece in that cell.",
        " Queen can move up, left, right 1 cell ","and capture opponent’s piece. ","It replaces the opponent's piece on that cell.",
        " King can move up, down, left, right 1 cell ","and capture opponent’s piece. ","It replaces the opponent's piece on that cell.",
        " When a soldier or queen reaches the ","opponent’s last row, it becomes king."," The game ends when all pieces are gone."
    ]
    
    line_spacing = 35
    start_y = HEIGHT // 4 + 50  # Adjusted starting Y position for content
    
    for i, line in enumerate(instructions_text):
        text_render = instructions_font.render(line, True, TEXT_COLOR)
        text_rect = text_render.get_rect(center=(WIDTH // 2, start_y + i * line_spacing))
        
        # Add extra space between every second line for better readability
        if i % 3 == 1:
            text_rect.y += 15
        
        WIN.blit(text_render, text_rect)
    
    # Close button
    close_button_rect = pygame.Rect(WIDTH - 80, 30, 50, 50)
    pygame.draw.rect(WIN, BUTTON_COLOR, close_button_rect, border_radius=15)
    close_text = instructions_font.render('X', True, (255, 255, 255))
    text_rect = close_text.get_rect(center=close_button_rect.center)
    WIN.blit(close_text, text_rect)
    
    pygame.display.update()
    
    return close_button_rect






def load_gif(filename):
    gif = imageio.get_reader(filename)
    return [np.array(frame) for frame in gif]

def resize_gif_frames(gif_frames, new_size=(WIDTH, HEIGHT)):
    resized_frames = []
    for frame in gif_frames:
        pil_image = Image.fromarray(frame)
        pil_image = pil_image.resize(new_size, resample=Image.BILINEAR)
        pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
        resized_frames.append(pygame_image)
    return resized_frames


def draw_winner_screen(winner, gif_filename_win, gif_filename_lose):
    WIN.fill(BACKGROUND_COLORR)
    
    if winner == "WHITE":
        winner_text = "You lose!!!"
        gif_filename = gif_filename_lose
    elif winner == "RED":
        winner_text = "You win!!!"
        gif_filename = gif_filename_win
    else:
        winner_text = "Unknown"
        gif_filename = None

    if gif_filename:
        gif_frames = resize_gif_frames(load_gif(gif_filename), (WIDTH, HEIGHT))
        frame_index, num_frames, clock, running = 0, len(gif_frames), pygame.time.Clock(), True

        # Define play_again_button_rect before the loop
        play_again_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if play_again_button_rect.collidepoint(pos):
                        return 'opening'

            WIN.blit(gif_frames[frame_index], (0, HEIGHT // 50))
            draw_text_center(winner_text, TITLE_FONT, TEXT_COLOR, WIN, (WIDTH // 2, HEIGHT // 10), shadow=True)
            draw_button(play_again_button_rect, 'Play Again', False)
            pygame.display.flip()
            frame_index = (frame_index + 1) % num_frames
            clock.tick(12)
        pygame.display.update()    
        
    return 'opening'


def main():
    run, clock, screen_state, buttons, how_to_play_button_rect = True, pygame.time.Clock(), 'opening', [], None

    while run:
        clock.tick(FPS)
        if screen_state == 'opening':
            button_rect = draw_opening_screen()
        elif screen_state == 'difficulty':
            buttons, how_to_play_button_rect = draw_difficulty_screen()
            screen_state = 'difficulty_screen'
        elif screen_state == 'instructions':
            close_button_rect = draw_instructions_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                
                if screen_state == 'difficulty_screen':
                    screen_state = 'opening'
                else:
                    run = False
            
                
                 
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if screen_state == 'opening' and button_rect.collidepoint(pos):
                    
                    screen_state = 'difficulty'
                elif screen_state == 'difficulty_screen':
                    for button_rect, text in buttons:
                        if button_rect.collidepoint(pos):
                            
                            game_loop(text)
                            screen_state = 'opening'
                    if how_to_play_button_rect.collidepoint(pos):
                        
                        screen_state = 'instructions'
                elif screen_state == 'instructions' and close_button_rect.collidepoint(pos):
                    
                    screen_state = 'difficulty'

        if screen_state == 'difficulty_screen':
            for button_rect, text in buttons:
                draw_button(button_rect, text, button_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.update()

    pygame.quit()
    return 'opening'

def game_loop(difficulty):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    optimized_params = genetic_algorithm()  # Optimize evaluation function parameters
    optimized_evaluation_function = get_optimized_evaluation_function(optimized_params)

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.turn == RED:  # Player's turn
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    print(f"Mouse clicked at ({row}, {col})")
                    game.select(row, col)
                    if game.winner() is not None:
                        if game.winner() == "WHITE":
                            
                            draw_winner_screen("WHITE", "win.gif", "lose.gif")
                            
                        else:
                            
                           draw_winner_screen("RED",  "win.gif", "lose.gif") 
                            
                        
                        pygame.time.delay(2000)
                        game.reset()  # Reset the game after displaying winner
                        return 'opening'  # Continue to next iteration of the loop

        if game.turn == WHITE and game.winner() is None:
            print("AI's Turn")
            if difficulty == 'Easy':
                print("using hybrid genetic and minimax algorithm")
                value, new_board = GA_minimax(game.get_board(), 4, True, float('-inf'), float('inf'), game, optimized_evaluation_function)
                game.ai_move(new_board)
            elif difficulty == 'Medium':
                print("using minimax")
                value, new_board = minimax(game.get_board(), 2, True, game)
                game.ai_move(new_board)
            elif difficulty == 'Hard':
                print("using alpha beta pruning")
                value, new_board = alpha_beta_minimax(game.get_board(), 3, float('-inf'), float('inf'), True, game)
                game.ai_move(new_board)
            elif difficulty == 'Very Hard':
                print("using fuzzy")
                game.ai_fuzzy_move()
                
        if game.winner():
            if game.winner() == "WHITE":
                            
                draw_winner_screen("WHITE", "win.gif", "lose.gif")
                            
            else:
                            
                draw_winner_screen("RED",  "win.gif", "lose.gif")             
                
                
            
            return 'opening'
            
        
        game.update()  # Update the game state and display
        game.draw_valid_moves(game.valid_moves)
        pygame.display.update()  # Update the display

    main()

if __name__ == "__main__":
    main()
