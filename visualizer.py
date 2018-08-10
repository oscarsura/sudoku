import sys, os
from os import system, listdir

dated = True

top_left  = u'\u2554'
bot_left  = u'\u255a'
top_right = u'\u2557'
bot_right = u'\u255d'
mid_horiz = u'\u2550' 
mid_verti = u'\u2551'
space_chr = u'\u0020'
path = 'stats'

visual_array = [] #visual array is the screen output
unopt_array = [] #unoptimized contains all, regardless of file
optim_array = [] #optimized contains all, regardless of file

runs = 0
data_files = 0
entries_per_file = 0
data_file_array = [] #contains [datafile, inode_info] pairs
data_entry_array = [] #contains [datafile, [times]] pairs

num_cols = 81
num_rows = 38
float_len = 14

default_row = 1
default_col_left = 1
default_col_right = num_cols-2

r,c = default_row, default_col_left
rev_r, rev_c = default_row, default_col_right
command_c = 42

index_datafile = 0 #index within the file
index_dataentry = 0 #index within all entries

def clear():
    _ = system('clear')

def l_clear():
    _ = d_clear_line() if dated else clear_line(command_c-1,0)

def d_clear_line():
    sys.stdout.write('\033[F')
    sys.stdout.write('\033[K') 

def clear_line(r,c):
    clearstr = '\033[' + str(r) + ';' + str(c) + 'H'
    delstr = '\033[K'
    sys.stdout.write(clearstr)
    sys.stdout.write(delstr)	

def hide_cursor():
    sys.stdout.write('\033[?25l')

def show_cursor():
    sys.stdout.write('\033[?25h')

def init():
    hide_cursor()
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
        file_entry_pair = [filename, lines]
        global data_entry_array
        data_entry_array.append(file_entry_pair)
        opt = False
        for line in lines:
            global runs
            time = float(line)
            arr = optim_array if opt else unopt_array
            arr.append(time)
            opt = not opt
            sys.stdout.write('\t' + line)
            runs+=1
        global entries_per_file
        entries_per_file = int(data_files/runs)

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

def r_write_string(s):
    global visual_array
    global rev_r, rev_c
    length = len(s)
    for x in range(length):
        visual_array[rev_r][rev_c] = s[length-1-x]
        rev_c-=1
    rev_r+=1
    rev_c = default_col_right

def write_string(s):
    global visual_array
    global r,c
    for char in s:
        visual_array[r][c] = char
        c+=1
    r+=1
    c=1

def write_string_set(s, row_num, col_num):
    global visual_array
    row, col = row_num, col_num
    for char in s:
        visual_array[row][col] = char
        col+=1

def print_stats():
    avg_unopt = sum(unopt_array)/len(unopt_array)
    avg_optim = sum(optim_array)/len(optim_array)
    write_string_buffer('avg-unopt=' + str(avg_unopt), '0', float_len)
    write_string_buffer('avg-optim=' + str(avg_optim), '0', float_len)
    write_string('total-runs=' + str(runs))

def get_input():
    line = raw_input('command-line: ')
    l_clear()
    return line

def move_entry(direction):
    print(data_entry_array)

def next_entry():
    move_entry(1)

def prev_entry():
    move_entry(-1)

def switch_command(arg):
    switch = {
        'next' : next_entry,
        'prev' : prev_entry,
        'break' : exit,
        'exit' : exit
    }
    func = switch.get(arg, lambda: l_clear)
    func()

def trunc(string, i):
    return string[:i]

def display_datafile():
    filename = data_file_array[index_datafile][0]
    filename = trunc(filename, 11)
    r_write_string('file: ' + filename)

def display_indices():
    entries = int(runs/2)
    files = data_files
    entry_index_str = ''
    file_index_str = ''
    if index_dataentry < 10 and entries > 9:
        entry_index_str += '0'
    entry_index_str += str(index_dataentry)
    if index_datafile < 10 and files > 9:
       file_index_str += '0'
    file_index_str += str(index_datafile)
    entry_arr = '[' + entry_index_str + '/' + str(entries) + ']'
    file_arr = '[' + file_index_str + '/' + str(files) + ']'
    
    index_line_nospace = entry_arr + '   ' + file_arr
    right_space = int((num_cols - 2 - len(index_line_nospace))/2)
    index_line = ''
    for x in range(right_space):
        index_line += ' '
    index_line += index_line_nospace
    write_string_set(index_line, num_rows, 1)

def display_results():
    print_visual()
    line = get_input()
    while True:
        switch_command(line)
        line = get_input()
        print_visual()

def dest():
    show_cursor()

init()
print_data_files()
print_stats() #this should be in a handler that updates before while looping
display_datafile() #this should also be in a handler that updates
display_indices() #this should also be in a handler that updates
display_results()
dest()
