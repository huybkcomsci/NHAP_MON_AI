import pygame
import time
import tkinter as tk
from tkinter import filedialog
import tracemalloc
import statistics
import random
from config import *
from gui import *
from solver import *

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

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

def generate_complete_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solution = [[0 for _ in range(9)] for _ in range(9)]
    if dfs_solve(board, solution, visualize=False, shuffle=True):
        return board
    else:
        return None

def generate_sudoku():
    complete = generate_complete_sudoku()
    if not complete:
        return None, None
    puzzle = [row.copy() for row in complete]
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    for k in range(40):
        i, j = cells[k]
        puzzle[i][j] = 0
    test_board = [row.copy() for row in puzzle]
    test_solution = [[0 for _ in range(9)] for _ in range(9)]
    if dfs_solve(test_board, test_solution, visualize=False):
        return puzzle, complete
    else:
        return generate_sudoku()

def run_performance_tests(initial_board, algorithm, runs=1000):
    times = []
    current_mems = []
    peak_mems = []
    success_count = 0

    for _ in range(runs):
        board_copy = [row.copy() for row in initial_board]
        solution_copy = [[0 for _ in range(9)] for _ in range(9)]

        start_time = time.time()
        tracemalloc.start()

        success = False
        if algorithm == "DFS":
            success = dfs_solve(board_copy, solution_copy, visualize=False)
        elif algorithm == "A*":
            success = a_star_solve(board_copy, solution_copy, visualize=False)

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tracemalloc.clear_traces()

        elapsed_time = (time.time() - start_time) * 1000  
        times.append(elapsed_time)
        current_mems.append(current_mem)
        peak_mems.append(peak_mem)

        if success:
            success_count += 1

    success_rate = (success_count / runs) * 100 

    stats = {
        "algorithm": algorithm,
        "runs": runs,
        "time_mean": statistics.mean(times),
        "time_std": statistics.stdev(times) if len(times) > 1 else 0,
        "current_mem_mean": statistics.mean(current_mems),
        "current_mem_std": statistics.stdev(current_mems) if len(current_mems) > 1 else 0,
        "peak_mem_mean": statistics.mean(peak_mems),
        "peak_mem_std": statistics.stdev(peak_mems) if len(peak_mems) > 1 else 0,
        "success_rate": success_rate,  
    }

    return stats

def print_stats(dfs_stats, a_star_stats):
    print("\n┌────────────────┬───────────────────────┬───────────────────────┐")
    print("│ {:14} │ {:21} │ {:21} │".format("Metric", "DFS", "A*"))
    print("├────────────────┼───────────────────────┼───────────────────────┤")

    dfs_time = f"{dfs_stats['time_mean']:.2f} ± {dfs_stats['time_std']:.2f} ms"
    a_star_time = f"{a_star_stats['time_mean']:.2f} ± {a_star_stats['time_std']:.2f} ms"
    print("│ {:14} │ {:21} │ {:21} │".format("Time", dfs_time, a_star_time))

    dfs_success = f"{dfs_stats['success_rate']:.2f}%"
    a_star_success = f"{a_star_stats['success_rate']:.2f}%"
    print("│ {:14} │ {:21} │ {:21} │".format("Success Rate", dfs_success, a_star_success))

    dfs_curr = f"{dfs_stats['current_mem_mean']/1024:.2f} ± {dfs_stats['current_mem_std']/1024:.2f} KB"
    a_star_curr = f"{a_star_stats['current_mem_mean']/1024:.2f} ± {a_star_stats['current_mem_std']/1024:.2f} KB"
    print("│ {:14} │ {:21} │ {:21} │".format("Current Memory", dfs_curr, a_star_curr))

    dfs_peak = f"{dfs_stats['peak_mem_mean']/1024:.2f} ± {dfs_stats['peak_mem_std']/1024:.2f} KB"
    a_star_peak = f"{a_star_stats['peak_mem_mean']/1024:.2f} ± {a_star_stats['peak_mem_std']/1024:.2f} KB"
    print("│ {:14} │ {:21} │ {:21} │".format("Peak Memory", dfs_peak, a_star_peak))

    print("└────────────────┴───────────────────────┴───────────────────────┘\n")

def main():
    original_board = [[0 for _ in range(9)] for _ in range(9)]
    current_board = [[0 for _ in range(9)] for _ in range(9)]
    correct_solution = [[0 for _ in range(9)] for _ in range(9)]
    editable = [[False for _ in range(9)] for _ in range(9)]
    solution = [[0 for _ in range(9)] for _ in range(9)]
    running = True
    selected = None
    message = ""
    message_timer = 0
    incorrect_cells = []

    while running:
        screen.fill(WHITE)
        highlight_area(current_board, selected)
        draw_numbers(current_board, solution)
        draw_grid()

        # Vẽ các nút
        pygame.draw.rect(screen, GRAY, solve_button)
        pygame.draw.rect(screen, GRAY, import_button)
        pygame.draw.rect(screen, GRAY, a_star_button)
        pygame.draw.rect(screen, GRAY, reset_button)
        pygame.draw.rect(screen, GRAY, test_button)
        pygame.draw.rect(screen, GRAY, generate_button)
        pygame.draw.rect(screen, GRAY, check_button)  

        # Văn bản trên các nút
        button_text = button_font.render("DFS", True, BLACK)
        screen.blit(button_text, (70, 560))
        import_text = button_font.render("Import", True, BLACK)
        screen.blit(import_text, (270, 560))
        a_star_text = button_font.render("A*", True, BLACK)
        screen.blit(a_star_text, (190, 560))
        reset_text = button_font.render("Reset", True, BLACK)
        screen.blit(reset_text, (425, 560))
        test_text = button_font.render("Test", True, BLACK)
        screen.blit(test_text, (450, 610))
        generate_text = button_font.render("Generate", True, BLACK) 
        screen.blit(generate_text, (25, 610))
        check_text = button_font.render("Check", True, BLACK)  
        screen.blit(check_text, (140, 610))

        # Vẽ các ô sai
        for (row, col) in incorrect_cells:
            pygame.draw.rect(screen, RED, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

        # Hiển thị thông báo
        if message and (time.time() - message_timer < 3):
            msg_surface = button_font.render(message, True, RED)
            screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT - 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if solve_button.collidepoint(x, y):
                    # Giải từ original_board và cập nhật current_board
                    temp_board = [row.copy() for row in original_board]
                    temp_solution = [[0 for _ in range(9)] for _ in range(9)]
                    start_time = time.time()
                    tracemalloc.start()
                    if dfs_solve(temp_board, temp_solution, visualize=True):
                        
                        solution = [row.copy() for row in temp_solution]
                        for i in range(9):
                            for j in range(9):
                                if editable[i][j]:
                                    current_board[i][j] = temp_solution[i][j]
                    current_mem, peak_mem = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    tracemalloc.clear_traces()
                    elapsed_time = time.time() - start_time
                    print(f"DFS - Thời gian: {elapsed_time:.2f}s, Bộ nhớ: {peak_mem / 1024:.2f} KB")
                    incorrect_cells = []
                elif import_button.collidepoint(x, y):
                    new_board = load_sudoku_from_file()
                    if new_board:
                        original_board = [row.copy() for row in new_board]
                        current_board = [row.copy() for row in new_board]
                        editable = [[original_board[i][j] == 0 for j in range(9)] for i in range(9)]
                        # Tính correct_solution
                        temp_board = [row.copy() for row in original_board]
                        temp_solution = [[0 for _ in range(9)] for _ in range(9)]
                        if dfs_solve(temp_board, temp_solution, visualize=False):
                            correct_solution = [row.copy() for row in temp_solution]
                        else:
                            print("Sudoku không hợp lệ!")
                        incorrect_cells = []
                elif a_star_button.collidepoint(x, y):
                    temp_board = [row.copy() for row in original_board]
                    temp_solution = [[0 for _ in range(9)] for _ in range(9)]
                    start_time = time.time()
                    tracemalloc.start()
                    if a_star_solve(temp_board, temp_solution, visualize=True):
                        solution = [row.copy() for row in temp_solution]
    # Don't modify current_board completely, just fill in the editable cells
                        for i in range(9):
                            for j in range(9):
                                if editable[i][j]:
                                    current_board[i][j] = temp_solution[i][j]
                    current_mem, peak_mem = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    tracemalloc.clear_traces()
                    elapsed_time = time.time() - start_time
                    print(f"A* - Thời gian: {elapsed_time:.2f}s, Bộ nhớ: {peak_mem / 1024:.2f} KB")
                    incorrect_cells = []
                elif reset_button.collidepoint(x, y):
                    current_board = [row.copy() for row in original_board]
                    solution = [[0 for _ in range(9)] for _ in range(9)]
                    incorrect_cells = []
                elif test_button.collidepoint(x, y):
                    if any(cell != 0 for row in original_board for cell in row):
                        dfs_stats = run_performance_tests(original_board, "DFS", runs=10)
                        a_star_stats = run_performance_tests(original_board, "A*", runs=10)
                        print_stats(dfs_stats, a_star_stats)
                    else:
                        print("Vui lòng nhập Sudoku trước khi chạy test!")
                elif generate_button.collidepoint(x, y):
                    result = generate_sudoku()
                    if result:
                        new_puzzle, new_solution = result
                        original_board = [row.copy() for row in new_puzzle]
                        current_board = [row.copy() for row in new_puzzle]
                        correct_solution = [row.copy() for row in new_solution]
                        editable = [[original_board[i][j] == 0 for j in range(9)] for i in range(9)]
                        incorrect_cells = []
                    else:
                        print("Không thể tạo đề Sudoku hợp lệ!")
                elif check_button.collidepoint(x, y):
                    # Kiểm tra các ô
                    incorrect_cells = []
                    for i in range(9):
                        for j in range(9):
                            if editable[i][j]:
                                if current_board[i][j] != 0 and current_board[i][j] != correct_solution[i][j]:
                                    incorrect_cells.append((i, j))
                            else:
                                if current_board[i][j] != original_board[i][j]:
                                    incorrect_cells.append((i, j))
                    if not incorrect_cells:
                        message = "Corect."
                    else:
                        message = "Wrong answer."
                    message_timer = time.time()
                else:
                    col, row = x // GRID_SIZE, y // GRID_SIZE
                    selected = (row, col)
            if event.type == pygame.KEYDOWN:
                if selected:
                    row, col = selected
                    if editable[row][col]:
                        if event.unicode.isdigit() and event.unicode != '0':
                            current_board[row][col] = int(event.unicode)
                        elif event.key == pygame.K_BACKSPACE:
                            current_board[row][col] = 0
                        incorrect_cells = []
                    selected = None

    pygame.quit()

if __name__ == "__main__":
    main()