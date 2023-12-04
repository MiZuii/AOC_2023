# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

def num_idxs(line: str):
    idxs = []
    num = False
    for i, chr in enumerate(line):
        if chr.isdigit() and not num:
            num = True
            idxs.append(i)
        if not chr.isdigit() and num:
            idxs.append(i)
            num = False
    if num:
        idxs.append(len(line))
    return idxs

ans = 0
input = inputf.read().split("\n")
number_indexes = [num_idxs(line) for line in input]
gears_arr = [[[] for _ in range(len(input[0]))] for _ in range(len(input))]

def fill_gear(input, lineno, start_idx, end_idx):
    num = int(input[lineno][start_idx:end_idx])
    xss = max(start_idx - 1, 0)
    xse = min(end_idx + 1, len(input[0]))
    yss = max(lineno - 1, 0)
    yse = min(lineno + 2, len(input))
    for y, line in enumerate(input[yss:yse]):
        for x, chr in enumerate(line[xss:xse]):
            if chr == '*':
                gears_arr[yss+y][xss+x].append(num)

for lineno in range(len(input)):
    for ni in range(0, len(number_indexes[lineno]), 2):
        fill_gear(input, lineno, number_indexes[lineno][ni], number_indexes[lineno][ni+1])

for gear_line in gears_arr:
    for gear in gear_line:
        if len(gear) == 2:
            ans += gear[0]*gear[1]

print(ans)

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()