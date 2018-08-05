import sys
from os import system

grid = open("grid-1.data", "r")
lines = grid.readlines()
grid.close()

grid_array = []

def clear():
    _ = system('clear')

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

def valid_board(g):
    return check_rows(g) and check_cols(g) and check_matrices(g)

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
clear()

for array in grid_array:
    for char in array:
        sys.stdout.write(str(char))
    sys.stdout.write('\n')

print("The result was: " + str(valid_board(grid_array)))
