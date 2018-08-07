import sys, copy
from os import system

grid_array = []
cand_array = []
lines = []

def clear():
    _ = system('clear')

def init():
    data_file = open('meta', 'r')
    grid_file = data_file.readline().strip()
    istream = open(grid_file, 'r')
    global lines
    lines = istream.readlines()
    istream.close()
    data_file.close()

def used_in_row(grid, row, num):
    for col in range(9):
        if grid[row][col] == num:
            return True
    return False

def used_in_col(grid, col, num):
    for row in range(9):
        if grid[row][col] == num:
            return True
    return False

def used_in_subgrid(grid, r_start, c_start, num):
    for r in range(3):
        for c in range(3):
            if grid[r_start + r][c_start + c] == num:
                return True
    return False

def valid_move(grid, row, col, num):
    return (not used_in_row(grid, row, num) and
            not used_in_col(grid, col, num) and
            not used_in_subgrid(grid, row - (row % 3), col - (col % 3), num))

def print_lines():
    for line in lines:
        sys.stdout.write(line)

def parse_lines():
    for line in lines:
        if line.strip() in ['']:
            continue
        num_string = line.strip().split()
        int_row = []
        for trio in num_string:
            for num in trio:
                if num in ['_']:
                    num = 0
                int_row.append(int(num))
        global grid_array
        grid_array.append(int_row)

def fill_cand_array():
    global cand_array
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    temp = []
    for x in range(9):
        temp.append(copy.deepcopy(nums))
    for x in range(9):
        cand_array.append(copy.deepcopy(temp))

def print_status():
    return

def print_grid():
    print('Sudoku Solver v2.0.1\n')
    for row in grid_array:
        for num in row:
            sys.stdout.write(str(num))
        sys.stdout.write('\n')
    print_status()

def trim_cand_tree():
    for r in range(9):
        for c in range(9):
            val = grid_array[r][c]
            if not val == 0:
                for x in range(1, 10, 1):
                    if not val == x:
                        cand_array[r][c].remove(x)

def elim_cand_tree():
    for r in range(9):
        for c in range(9):
            val = grid_array[r][c]
            if val == 0:
                for x in range(1, 10, 1):
                    if not valid_move(grid_array, r, c, x) and x in cand_array[r][c]:
                        cand_array[r][c].remove(x)

init()
parse_lines()
print_grid()
fill_cand_array()

trim_cand_tree()
elim_cand_tree()
print(cand_array)
