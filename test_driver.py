import sys, time
import hashlib
from os import system

output_dir = 'stats/'
unop = 'python solution.py'
reop = 'python optimized_solution.py'
rounds = 10

unopt_array = []
optim_array = []

console = False
raw = True
dump = True

def clear():
    _ = system('clear')

def init():
    for x in range(3):
        clear()
        print('Starting algorithm testing in ' + str(3-x))
        time.sleep(1)

def test(s):
    for x in range(rounds):
        start = time.time()
        _ = system(s)
        end = time.time()
        diff = end - start
        arr = unopt_array
        if 'opt' in s:
            arr = optim_array
        arr.append(diff)

def print_results():
    clear()
    if not console:
        return
    if raw:
        for x in range(rounds):
            sys.stdout.write(str(unopt_array[x]) + '\n')
            sys.stdout.write(str(optim_array[x]) + '\n')
        return
    print('Sudoku Algorithm Test Driver v0.0.1\n')
    for x in range(rounds):
        sys.stdout.write('unoptimized-time ' + str(x) + ': ' + str(unopt_array[x]) + '\n')
        sys.stdout.write('  optimized-time ' + str(x) + ': ' + str(optim_array[x]) + '\n')
        sys.stdout.write('algorithmadvantage ' + str(optim_array[x] - unopt_array[x]) + '\n')
        sys.stdout.write('----------------------------------\n')

def dump():
    if not dump:
        return
    curr_time = str(time.time())
    filename_md5 = hashlib.md5(bytes(curr_time))
    filename = output_dir + filename_md5.hexdigest()
    out = open(filename, 'w+')
    for x in range(rounds):
        out.write(str(unopt_array[x]) + '\n')
        out.write(str(optim_array[x]) + '\n')

init()
test(unop)
test(reop)
print_results()
dump()
