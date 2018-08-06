import sys
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

def used_in_col(grid, row, num):
    for row in range(9):
        if grid[row][col] == num:
            return True
    return False

def used_in_subgrid(grid, r_start, c_start, num):
    for r in range(9):
        for c in range(9):
            if grid[r_start + r][c_start + c] == num:
                return True
    return False

def valid_move(grid, row, col, num):
    return (not used_in_row(grid, row, num) and
            not used_in_col(grid, col, num) and
            not used_in_subgrid(grid, row - row % 3, col - col % 3, num))

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
    for i in range(9):
        cand_array.append([[], [], [], [], [], [], [], [], []])

    for r in range(9):
        for c in range(9):
            cand_array[r][c].append(nums)

def print_status():
    return

def print_grid():
    clear()
    print('Sudoku Solver v2.0.1\n')
    for row in grid_array:
        for num in row:
            sys.stdout.write(str(num))
        sys.stdout.write('\n')
    print_status()

init()
parse_lines()
print_grid()
fill_cand_array()

#print("print(cand_array):")
#print(cand_array)
#print("")

#print("print(cand_array[0]):")
#print(cand_array[0])
#print("")

#print("print(cand_array[0][0]):")
#print(cand_array[0][0])
#print("")

#print("print(cand_array[0][0][0]):")
#print(cand_array[0][0][0])
#print("")
