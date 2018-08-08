import sys, os
from os import system, listdir

top_left  = u'\u2554'
bot_left  = u'\u255a'
top_right = u'\u2557'
bot_right = u'\u255d'
mid_horiz = u'\u2550' 
mid_verti = u'\u2551'
space_chr = u'\u0020'
path = 'stats'

visual_array = []
unopt_array = []
optim_array = []

runs = 0
data_files = 0
data_file_array = []

num_cols = 81
num_rows = 38
float_len = 14

r,c = 1,1

def clear():
    _ = system('clear')

def hide_cursor():
    sys.stdout.write('\033[?25l')

def show_cursor():
    sys.stdout.write('\033[?25h')

def init():
    build_row(top_left, mid_horiz, top_right)
    for x in range(num_rows):
        build_row(mid_verti, space_chr, mid_verti)
    build_row(bot_left, mid_horiz, bot_right)
    parse_directory()

def build_row(l, m, r):
    row = []
    row += l
    for x in range(num_cols - 2):
        row += m
    row += r
    global visual_array
    visual_array.append(row)

def print_visual():
    clear()
    for row in visual_array:
        for char in row:
            sys.stdout.write(char)
        sys.stdout.write('\n')

def parse_directory():
    global data_file_array
    files = os.listdir(path)
    for name in files:
        fullname = os.path.join(path, name)
        inode = os.stat(fullname)
        data_file_array.append([fullname, inode.st_mtime])
        global data_files
        data_files+=1
    data_file_array = sorted(data_file_array, key = lambda x: x[1])

def print_data_files():
    for file_info in data_file_array:
        filename = file_info[0]
        sys.stdout.write(filename + '\n')
        input_file = open(filename, 'r')
        lines = input_file.readlines()
        opt = False
        for line in lines:
            global runs
            time = float(line)
            arr = optim_array if opt else unopt_array
            arr.append(time)
            opt = not opt
            sys.stdout.write('\t' + line)
            runs+=1

def write_string_buffer(s, char, buflen):
    global visual_array
    global r,c
    write_string(s)
    length = len(s)
    if length < buflen:
        r-=1
        c+=length
        for x in range(buflen - length):
            visual_array[r][c] = char
            c+=1
        r+=1
        c=1

def write_string(s):
    global visual_array
    global r,c
    for char in s:
        visual_array[r][c] = char
        c+=1
    r+=1
    c=1

def print_stats():
    avg_unopt = sum(unopt_array)/len(unopt_array)
    avg_optim = sum(optim_array)/len(optim_array)
    write_string_buffer('avg-unopt=' + str(avg_unopt), '0', float_len)
    write_string_buffer('avg-optim=' + str(avg_optim), '0', float_len)
    write_string('total-runs=' + str(runs))

init()
print_data_files()
print_stats()
print_visual()
