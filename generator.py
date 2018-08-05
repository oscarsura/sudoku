import sys
from time import sleep

meta = open("meta", "r")
output_line = meta.readline().strip()
clues_line = meta.readline().strip()
num_clues = int(clues_line)
output = open(output_line, "w")
meta.close()

grid_array = []

def clear():
    sys.stdout.write("\033[2J")

def hide_cursor():
    sys.stdout.write("\033[?25l")

def show_cursor():
    sys.stdout.write("\033[?25h")

def print_grid(gd):
    clear()
    print("Sudoku Generator v0.0.1\n")
    for array in gd:
        for char in array:
            sys.stdout.write(str(char))
        sys.stdout.write('\n')
    print_status(gd)

def used_in_row(grid_arr, row, num):
    for col in range(9):
        if grid_arr[row][col] == num:
            return True
    return False

def used_in_col(grid_arr, col, num):
    for row in range(9):
        if grid_arr[row][col] == num:
            return True
    return False

def used_in_matrix(grid_arr, row_st, col_st, num):
    for r in range(3):
        for c in range(3):
            if grid_arr[row_st + r][col_st + c] == num:
                return True
    return False

def valid_move(gd, row, col, num):
    return (not used_in_row(gd, row, num) and
            not used_in_col(gd, col, num) and
            not used_in_matrix(gd, row - row % 3, col - col % 3, num))

def get_blank(gd):
    for r in range(9):
        for c in range(9):
            if gd[r][c] == 0:
                return r, c
    return -1, -1

def generate_grid():
    for i in range(num_clues):
        generate_clue()

hide_cursor()
generate_grid()
show_cursor()

output.close()
