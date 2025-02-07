import random
from copy import deepcopy
from checkers.constants import RED, WHITE
from checkers.game import Game
#from minimax.algorithm import GA_minimax, get_all_moves, simulate_move

# Define a default evaluation function
def default_evaluation(board):
    return board.evaluate()

# Genetic Algorithm to optimize evaluation function
def genetic_algorithm(population_size=20, generations=100, mutation_rate=0.1):
    population = [generate_random_params() for _ in range(population_size)]
    for _ in range(generations):
        fitness_scores = [evaluate_fitness(params) for params in population]
        selected_population = [select(population, fitness_scores) for _ in range(population_size // 2)]
        offspring = []
        for i in range(0, len(selected_population), 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1] if i + 1 < len(selected_population) else selected_population[0]
            offspring.extend(crossover(parent1, parent2))
        population = selected_population + offspring
        population = [mutate(params, mutation_rate) for params in population]
    best_params = max(population, key=lambda params: evaluate_fitness(params))
    return best_params

def generate_random_params():
    return {
        'soldier': random.uniform(0, 1),
        'queen': random.uniform(1, 3),
        'king': random.uniform(3, 5)
    }

def evaluate_fitness(params):
    # For simplicity, we'll just return a random fitness score here
    return random.uniform(0, 1)

def select(population, fitness_scores):
    total_score = sum(fitness_scores)
    pick = random.uniform(0, total_score)
    current = 0
    for params, score in zip(population, fitness_scores):
        current += score
        if current > pick:
            return params
    return population[-1]

def mutate(params, mutation_rate):
    if random.random() < mutation_rate:
        params['soldier'] += random.uniform(-0.1, 0.1)
        params['queen'] += random.uniform(-0.1, 0.1)
        params['king'] += random.uniform(-0.1, 0.1)
        # Ensure params stay within reasonable bounds
        params['soldier'] = max(0, params['soldier'])
        params['queen'] = max(1, params['queen'])
        params['king'] = max(3, params['king'])
    return params

def crossover(params1, params2):
    new_params1 = {
        'soldier': (params1['soldier'] + params2['soldier']) / 2,
        'queen': (params1['queen'] + params2['queen']) / 2,
        'king': (params1['king'] + params2['king']) / 2
    }
    new_params2 = {
        'soldier': (params1['soldier'] + params2['soldier']) / 2,
        'queen': (params1['queen'] + params2['queen']) / 2,
        'king': (params1['king'] + params2['king']) / 2
    }
    return new_params1, new_params2

def get_optimized_evaluation_function(params):
    def optimized_evaluation(board):
        white_score = 0
        red_score = 0
        center_cols = [3, 4]  # Columns considered as center
        row_bonus = 0.1  # Bonus for pieces closer to becoming kings
        center_bonus = 0.2  # Bonus for controlling the center

        for row in board.board:
            for piece in row:
                if piece != 0:
                    # Base score for the piece type
                    if piece.color == WHITE:
                        piece_score = params['soldier'] if piece.type == 'soldier' else params['queen'] if piece.type == 'queen' else params['king']
                        white_score += piece_score

                        # Positioning bonus
                        white_score += (7 - piece.row) * row_bonus  # Closer to becoming king

                        # Center control bonus
                        if piece.col in center_cols:
                            white_score += center_bonus

                        # Piece safety bonus
                        if is_protected(board, piece):
                            white_score += 0.1
                    elif piece.color == RED:
                        piece_score = params['soldier'] if piece.type == 'soldier' else params['queen'] if piece.type == 'queen' else params['king']
                        red_score += piece_score

                        # Positioning bonus
                        red_score += piece.row * row_bonus  # Closer to becoming king

                        # Center control bonus
                        if piece.col in center_cols:
                            red_score += center_bonus

                        # Piece safety bonus
                        if is_protected(board, piece):
                            red_score += 0.1

        return white_score - red_score

    return optimized_evaluation

def is_protected(board, piece):
    """Check if a piece is protected by another piece."""
    row, col = piece.row, piece.col
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            neighbor = board.get_piece(r, c)
            if neighbor != 0 and neighbor.color == piece.color:
                return True
    return False

