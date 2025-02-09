import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 540, 600
GRID_SIZE = WIDTH // 9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (30, 144, 255)
GREEN = (0, 128, 0)

# Fonts
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)

# Buttons
solve_button = pygame.Rect(20, 550, 140, 40)
import_button = pygame.Rect(240, 550, 130, 40)
a_star_button = pygame.Rect(170, 550, 60, 40)
reset_button = pygame.Rect(380, 550, 140, 40)
