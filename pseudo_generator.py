import sys
from time import sleep
from random import randint
from os import system

meta = open("meta", "r")
meta.readline()
output_line = meta.readline().strip()
clues_line = meta.readline().strip()
num_clues = int(clues_line)
output = open(output_line, "w+")
meta.close()

status_bars = 27

grid_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]
 
def clear():
    _ = system('clear')

def hide_cursor():
    sys.stdout.write("\033[?25l")

def show_cursor():
    sys.stdout.write("\033[?25h")

def print_status(gd):
    print("")
    full_count = 0
    for r in range(9):
        for c in range(9):
            if gd[r][c] not in [0]:
                full_count = full_count+1
    pbar_num = (full_count+0.00)/num_clues
    pbar = int(pbar_num*status_bars)

    bar = "["
    for i in range(pbar):
        bar += unichr(0x2588)
    for i in range(status_bars - pbar):
        bar += " "
    bar += "] "
    bar += str(full_count) + "/" + str(num_clues)
    print(bar)

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
    if num == -1: return False
    return (not used_in_row(gd, row, num) and
            not used_in_col(gd, col, num) and
            not used_in_matrix(gd, row - row % 3, col - col % 3, num))

def get_blank(gd):
    for r in range(9):
        for c in range(9):
            if gd[r][c] == 0:
                return r, c
    return -1, -1

def is_blank(gd, row, col):
    if row == -1 or col == -1:
        return False
    return gd[row][col] == 0

def random_loc():
    return randint(0, 8), randint(0, 8)

def random_num():
    return randint(1, 9)

def generate_clue(grid_arr):
    row, col = -1, -1
    num = -1
    while not is_blank(grid_arr, row, col):
        row, col = random_loc()

    while not valid_move(grid_arr, row, col, num):
        num = random_num()
    grid_arr[row][col] = num
    print_grid(grid_arr)
    sleep(.100)

def generate_grid():
    for i in range(num_clues):
        generate_clue(grid_array)

def write_grid(grid_arr):
    array_count = 0
    for array in grid_arr:
        if array_count == 3:
            output.write('\n')
            array_count = 0

        int_count = 0
        for num in array:
            if int_count == 3:
                output.write(' ')
                int_count = 0
            char = num
            if num == 0:
                char = '_'
            output.write(str(char))
            int_count = int_count+1
        output.write('\n')
        array_count = array_count+1

hide_cursor()
generate_grid()
write_grid(grid_array)
show_cursor()

output.close()
