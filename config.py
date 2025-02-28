import pygame

# Kích thước màn hình
WIDTH, HEIGHT = 540, 660
GRID_SIZE = WIDTH // 9

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (30, 144, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Nút bấm
solve_button = pygame.Rect(20, 550, 140, 40)
import_button = pygame.Rect(240, 550, 130, 40)
a_star_button = pygame.Rect(170, 550, 60, 40)
reset_button = pygame.Rect(380, 550, 140, 40)
test_button = pygame.Rect(440, 600, 80, 40)
generate_button = pygame.Rect(20, 600, 100, 40)
check_button = pygame.Rect(130, 600, 100, 40)

# Font chữ
pygame.font.init()
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)