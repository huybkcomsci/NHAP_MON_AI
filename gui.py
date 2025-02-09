import pygame
import tkinter as tk
from tkinter import filedialog
from config import *
from solver import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
def load_sudoku_from_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        board = [[0 for _ in range(9)] for _ in range(9)]
        with open(file_path, 'r') as file:
            for i, line in enumerate(file.readlines()):
                numbers = list(map(int, line.strip().split()))
                for j, num in enumerate(numbers):
                    board[i][j] = num
        return board
    return None

def main():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solution = [[0 for _ in range(9)] for _ in range(9)]
    running = True
    selected = None
    
    while running:
        screen.fill(WHITE)
        highlight_area(board, selected)
        draw_numbers(board, solution)
        draw_grid()
        
        pygame.draw.rect(screen, GRAY, solve_button)
        pygame.draw.rect(screen, GRAY, import_button)
        pygame.draw.rect(screen, GRAY, a_star_button)
        pygame.draw.rect(screen, GRAY, reset_button)
        
        button_text = button_font.render("DFS", True, BLACK)
        screen.blit(button_text, (70, 560))
        
        import_text = button_font.render("Import", True, BLACK)
        screen.blit(import_text, (270, 560))
        
        a_star_text = button_font.render("A*", True, BLACK)
        screen.blit(a_star_text, (190, 560))
        
        reset_text = button_font.render("Reset", True, BLACK)
        screen.blit(reset_text, (425, 560))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if solve_button.collidepoint(x, y):
                    dfs_solve(board, solution)
                elif import_button.collidepoint(x, y):
                    new_board = load_sudoku_from_file()
                    if new_board:
                        board = new_board
                        solution = [[0 for _ in range(9)] for _ in range(9)]
                elif a_star_button.collidepoint(x, y):
                    a_star_solve(board, solution)
                elif reset_button.collidepoint(x, y):
                    board = [[0 for _ in range(9)] for _ in range(9)]
                    solution = [[0 for _ in range(9)] for _ in range(9)]
                else:
                    col, row = x // GRID_SIZE, y // GRID_SIZE
                    selected = (row, col)
            if event.type == pygame.KEYDOWN:
                if selected:
                    if event.unicode.isdigit() and event.unicode != '0':
                        board[selected[0]][selected[1]] = int(event.unicode)
                    elif event.key == pygame.K_BACKSPACE:
                        board[selected[0]][selected[1]] = 0
                    selected = None
    pygame.quit()

if __name__ == "__main__":
    main()
