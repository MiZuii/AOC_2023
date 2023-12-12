# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

def issymbol(chr: str):
    return not(chr.isdigit() or chr == '.')

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

def is_valid_number(input, lineno, start_idx, end_idx):
    xss = max(start_idx - 1, 0)
    xse = min(end_idx + 1, len(input[0]))
    yss = max(lineno - 1, 0)
    yse = min(lineno + 2, len(input))
    for line in input[yss:yse]:
        for chr in line[xss:xse]:
            if issymbol(chr):
                return True
    return False

ans = 0
input = inputf.read().split("\n")
number_indexes = [num_idxs(line) for line in input]
for lineno in range(len(input)):
    for ni in range(0, len(number_indexes[lineno]), 2):
        num = input[lineno][number_indexes[lineno][ni]:number_indexes[lineno][ni+1]]
        if is_valid_number(input, lineno, number_indexes[lineno][ni], number_indexes[lineno][ni+1]):
            ans += int(num)

print(ans)

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()