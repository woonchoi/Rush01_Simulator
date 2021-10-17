from os import popen
from time import time
from random import shuffle


### GLOBALS ###
SIZE = 0
TAB = []
NUMS = []
COND = []


### UTILITY FUNCTIONS ###
def is_valid(idx: int, val: int) -> bool:
    for i in range(1, idx % SIZE + 1):
        if val == TAB[idx - i]:
            return False
    for i in range(1, idx // SIZE + 1):
        if val == TAB[idx - SIZE * i]:
            return False
    return True

def count_views(line: list) -> int:
    max = 0
    view = 0
    for n in line:
        if n > max:
            max = n
            view += 1
    return view

def get_row(nr: int) -> list:
    row = []
    for i in range(nr*SIZE, (nr + 1)*SIZE):
        row.append(TAB[i])
    return row

def get_col(nc: int) -> list:
    col = []
    for i in range(SIZE):
        col.append(TAB[nc%SIZE + i*SIZE])
    return col

def blue(text: str) -> str:
    beg = '\033[94m'
    end = '\033[0m'
    return f"{beg}{text}{end}"

def red(text: str) -> str:
    beg = '\033[91m'
    end = '\033[0m'
    return f"{beg}{text}{end}"

def green(text: str) -> str:
    beg = '\033[92m'
    end = '\033[0m'
    return f"{beg}{text}{end}"


### MAIN FUNCTIONS ###
def solve(idx: int) -> bool:
    if idx == SIZE ** 2:
        return True

    shuffle(NUMS)
    nums = NUMS.copy()
    for val in nums:
        if is_valid(idx, val):
            TAB[idx] = val
            if solve(idx + 1):
                return True
    else:
        return False

def gen_cond() -> None:
    global COND
    COND = [[0 for _ in range(SIZE)] for _ in range(4)]
    for c in range(SIZE):
        col = get_col(c)
        COND[0][c] = count_views(col)
        COND[1][c] = count_views(reversed(col))
    for r in range(SIZE):
        row = get_row(r)
        COND[2][r] = count_views(row)
        COND[3][r] = count_views(reversed(row))

def print_puzzle() -> None:
    cu, cd, rl, rr = COND
    print(blue(f"  {' '.join(map(str, cu))}"))
    for r in range(SIZE):
        print(blue(f"{rl[r]}"), end=' ')
        print(red(' '.join(map(str, get_row(r)))), end=' ')
        print(blue(f"{rr[r]}"))
    print(blue(f"  {' '.join(map(str, cd))}\n"))

def print_ans(output) -> None:
    cu, cd, rl, rr = COND
    print(blue(f"  {' '.join(map(str, cu))}"))
    for r in range(SIZE):
        print(blue(f"{rl[r]}"), end=' ')
        print(green(output[r]), end=' ')
        print(blue(f"{rr[r]}"))
    print(blue(f"  {' '.join(map(str, cd))}"))

def print_args(bin_name) -> None:
    print(green(f"./{bin_name} "), end=red('"'))
    for i, line in enumerate(COND):
        end = ' ' if i < len(COND) - 1 else ''
        print(red(' '.join(map(str, line))), end=end)
    print(red('"\n'))

def print_execute_results(bin_name) -> None:
    dest = []
    for element in COND:
        dest += element
    numlist = ' '.join(map(str, dest))
    script = "./" + bin_name + ' "' + numlist + '"'
    start = time()
    stream = popen(script)
    output = stream.read()
    output = output.split('\n')
    print(green(f"=================== YOUR ANSWER ===================\n"))
    print_ans(output)
    end = time()
    print(green(f"\nruntime : {end - start:.5f} sec\n"))

### PROGRAM ###
if (__name__ == '__main__'):
    exename = input(blue("input your executable's name: "))
    exename = exename
    itercount = int(input(blue("input number of repetitions: ")))

    print(red("\nThe execution result may be different from the example above."))
    print(red("There's no big problem. Don't panic!\n"))

    for i in range(0, itercount):
        while True:
            sz = int(input(blue("input valid size(3 to 9): ")))
            if 2 < sz < 10:
                SIZE = sz
                break
        NUMS = [i for i in range(1, SIZE + 1)]

        while True:
            TAB = [0 for _ in range(SIZE ** 2)]
            if solve(0):
                break
        print(green(f"==================== EXAMPLE {i + 1} ====================\n"))
        gen_cond()
        print_puzzle()
        print(green(f"================= EXECUTE COMMAND =================\n"))
        print_args(exename)
        print_execute_results(exename)
