import sys, copy
from os import system

grid_array = []
cand_array = []
lines = []

pbars = 27
num_clues = 81
pchar = 0x2588

def clear():
    _ = system('clear')

def hide_cursor():
    sys.stdout.write('\033[?25l')

def show_cursor():
    sys.stdout.write('\033[?25h')

def init():
    hide_cursor()
    data_file = open('meta', 'r')
    grid_file = data_file.readline().strip()
    istream = open(grid_file, 'r')
    global lines
    lines = istream.readlines()
    istream.close()
    data_file.close()

def dest():
    show_cursor()

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
    print('')
    full_count = 0
    for r in range(9):
        for c in range(9):
            if not grid_array[r][c] == 0:
                full_count+=1
    pbar_num = (full_count+0.00)/num_clues
    pbar = int(pbar_num*pbars)

    status = '['
    for x in range(pbar):
        status += unichr(pchar)
    for x in range(pbars - pbar):
        status += ' '
    status += '] '
    status += str(full_count) + '/' + str(num_clues)
    print(status)

def print_grid():
    clear()
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

def get_blank():
    for r in range(9):
        for c in range(9):
            if grid_array[r][c] == 0:
                return r, c
    return -1,-1

def board_full():
    for r in range(9):
        for c in range(9):
            if grid_array[r][c] == 0:
                return False
    return True

def find_solution():
    print_grid()
    if board_full():
        return True
    r, c = get_blank()
    if r == -1 or c == -1:
        return False

    num_cand = len(cand_array[r][c])
    for x in range(num_cand):
        move = cand_array[r][c][x]
        if valid_move(grid_array, r, c, move):
            global grid_array
            grid_array[r][c] = move
            if find_solution():
                return True
            grid_array[r][c] = 0
    return False

def print_solution():
    print('Found a solution?: ' + str(find_solution()))
    
init()
parse_lines()
fill_cand_array()

trim_cand_tree()
elim_cand_tree()

print_solution()
dest()
