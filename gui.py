import pygame
from config import *

# Khởi tạo màn hình
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Giai Sudoku")

def highlight_area(board, selected):
    if selected:
        row, col = selected
        box_x, box_y = col // 3, row // 3
        for i in range(9):
            pygame.draw.rect(screen, LIGHT_BLUE, (i * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, LIGHT_BLUE, (col * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                pygame.draw.rect(screen, LIGHT_BLUE, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, DARK_BLUE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
def draw_grid():
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, WIDTH), thickness)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), thickness)

def draw_numbers(board, solution):
    for i in range(9):
        for j in range(9):
            if solution[i][j] != 0:
                color = GREEN
                text = font.render(str(solution[i][j]), True, color)
            else:
                color = BLACK
                text = font.render(" " if board[i][j] == 0 else str(board[i][j]), True, color)
            screen.blit(text, (j * GRID_SIZE + 20, i * GRID_SIZE + 10))
