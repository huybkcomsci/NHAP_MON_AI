import heapq
import time
from config import *
from gui import *

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

def is_valid(board, num, pos):
    row, col = pos
    for i in range(9):
        if board[row][i] == num and i != col:
            return False
        if board[i][col] == num and i != row:
            return False
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def heuristic(board):
    empty_cells = 0
    for row in board:
        empty_cells += row.count(0)
    return empty_cells

def a_star_solve(board, solution):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (heuristic(board), board, []))
    
    while open_list:
        _, current_board, path = heapq.heappop(open_list)
        
        if all(cell != 0 for row in current_board for cell in row):
            for row, col, num in path:
                solution[row][col] = num
            return True
        
        closed_list.add(tuple(tuple(row) for row in current_board))
        
        empty = find_empty(current_board)
        if not empty:
            continue
        row, col = empty
        
        for num in range(1, 10):
            if is_valid(current_board, num, (row, col)):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                if tuple(tuple(row) for row in new_board) not in closed_list:
                    new_path = path + [(row, col, num)]
                    heapq.heappush(open_list, (len(new_path) + heuristic(new_board), new_board, new_path))
                    
                    screen.fill(WHITE)
                    highlight_area(new_board, (row, col))
                    draw_numbers(new_board, solution)
                    draw_grid()
                    pygame.display.update()
                    time.sleep(0.1)
    return False

def dfs_solve(board, solution):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            solution[row][col] = num
            screen.fill(WHITE)
            highlight_area(board, (row, col))
            draw_numbers(board, solution)
            draw_grid()
            pygame.display.update()
            time.sleep(0.1)
            
            if dfs_solve(board, solution):
                return True
            
            board[row][col] = 0
            solution[row][col] = 0
            screen.fill(WHITE)
            highlight_area(board, (row, col))
            draw_numbers(board, solution)
            draw_grid()
            pygame.display.update()
            time.sleep(0.1)
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None
