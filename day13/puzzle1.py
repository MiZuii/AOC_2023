# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #


def solve_horizontal(mm, reverse = True):
    # reverse accualy means no reverse but it this algorithm context this doesn't matter

    i = 0 if reverse else len(mm) - 1     # main iterator
    prev_i = 0 if reverse else len(mm) - 1
    mi = 0 if not reverse else len(mm) - 1  # iterator going from the back
    refi = 0
    sym_start = False
    while True:

        # iteration stop conditions
        if i == (len(mm) if reverse else -1) or (mi <= i if reverse else i <= mi):
            if sym_start:
                refi = i if reverse else mi
            break

        if not sym_start and mm[i] == mm[mi] and i != mi and (abs(i - mi) % 2) != 0:
            # and (abs(i - mi) % 2) != 0 -> detects if the symetry will end inbetween the rows
            sym_start = True
            i += 1 if reverse else -1
            mi -=1 if reverse else -1
            prev_i = i
        elif not sym_start:
            # not sym_start and mi[i] != mm[mi]
            i += 1 if reverse else -1
        elif sym_start and (mm[i] != mm[mi]):
            # symetry broken start from prev i
            i = prev_i
            mi = 0 if not reverse else len(mm) - 1
            sym_start = False
        else:
            # sym_start and mm[i] == mm[mi]
            i += 1 if reverse else -1
            mi -=1 if reverse else -1
    
    return refi


def transpose(mm):
    res = []
    for coli in range(len(mm[0])):
        s = ""
        for rowi in range(len(mm)):
            s += mm[rowi][coli]
        res.append(s)
    return res


def solve(mm):
    tmm = transpose(mm)
    s1, s2, s3, s4 = solve_horizontal(mm), solve_horizontal(mm, reverse=False), solve_horizontal(tmm), solve_horizontal(tmm, reverse=False)
    return 100*(s1 + s2 if s1 != s2 else s2) + (s3 + s4 if s3 != s4 else s3)
    

input.append([])
ans = 0
mirrors_map = []
for row in input:
    if len(row):
        mirrors_map.append(row)
    else:
        ans += solve(mirrors_map)
        mirrors_map = []
print(ans)
