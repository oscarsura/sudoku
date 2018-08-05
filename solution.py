import sys
from os import system

grid = open("grid-2.data", "r")
lines = grid.readlines()
grid.close()

grid_array = []

def clear():
    _ = system('clear')

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

def used_in_matrix(grid_arr, row_start, col_start, num):
    for r in range(3):
        for c in range(3):
            if grid_arr[row_start + r][col_start + c] == num:
                return True
    return False

def check_rows(grid_arr):
    for row in grid_arr:
        int_set = set()
        for char in row:
            if char == 0: continue
            if char in int_set:
                return False
            else:
                int_set.add(char)
    return True

def check_cols(grid_arr):
    for col in range(9):
        int_set = set()
        for row in range(9):
            char = grid_arr[row][col]
            if char == 0: continue
            if char in int_set:
                return False
            else: 
                int_set.add(char)
    return True

def check_matrix(grid_arr, r, c):
    int_set = set()
    for row in range(3):
        for col in range(3):
            val = grid_arr[r + row][c + col]
            if val == 0: continue
            if val in int_set:
                return False
            else:
                int_set.add(val)
    return True

def check_matrices(grid_arr):
    retval = True
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            retval = check_matrix(grid_arr, row, col)
    return retval

def valid_move(garr, row, col, num):
    return (not used_in_row(garr, row, num) and 
           not used_in_col(garr, col, num) and 
           not used_in_matrix(garr, row - row % 3, col - col % 3, num)) 

def get_blank(garr):
    for r in range(9):
        for c in range(9):
            if garr[r][c] == 0:
                return r, c
    return -1, -1

def is_valid(g):
    return check_rows(g) and check_cols(g) and check_matrices(g)

def parse_file():
    for line in lines:
        if line.strip() == '':
            continue
        else:
            num_string = line.strip().split()
            nums_int = []
            for trio in num_string:
                for x in range(3):
                    num = 0
                    if (trio[x] not in ['_']):
                        num = int(trio[x])
                    nums_int.append(num)
            grid_array.append(nums_int)

def print_grid(g):
    clear()
    for array in g:
        for char in array:
            sys.stdout.write(str(char))
        sys.stdout.write('\n')

def board_full(g):
    for r in range(9):
        for c in range(9):
            if g[r][c] == 0:
                return False
    return True

def find_solution(grid_arr):
    print_grid(grid_arr)
    if board_full(grid_arr):
        return is_valid(grid_arr)
   
    r, c = get_blank(grid_arr)
    if r == -1 or c == -1:
        return False
    
    for i in range(10):
        if (valid_move(grid_arr, r, c, i)):
            grid_arr[r][c] = i
            if find_solution(grid_arr):
                return True
            grid_arr[r][c] = 0
    return False

parse_file()
print("Found a solution?: " + str(find_solution(grid_array)))
