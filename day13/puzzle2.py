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

    # find the fake tile
    smudgeset = set()
    for i in range(0, len(mm)-1):
        base_row = mm[i]
        for j in range(i+1, len(mm)):
            diff = 0
            ls = 0
            for s in range(len(mm[0])):
                if mm[j][s] != base_row[s]:
                    diff += 1
                    ls = s
            if diff == 1:
                smudgeset.add((j, ls))

    for i in range(0, len(mm[0])-1):
        for j in range(i+1, len(mm[0])):
            diff = 0
            ls = 0
            for s in range(len(mm)):
                if mm[s][j] != mm[s][i]:
                    diff += 1
                    ls = s
            if diff == 1:
                smudgeset.add((ls, j))

    mm = list(map(list, mm))
    tmm = transpose(mm)
    tmm = list(map(list, tmm))
    # for row in mm:
    #     for c in row:
    #         print(c, end="")
    #     print()

    s1, s2, s3, s4 = solve_horizontal(mm), solve_horizontal(mm, reverse=False), solve_horizontal(tmm), solve_horizontal(tmm, reverse=False)

    for smudge in smudgeset:
        chr = mm[smudge[0]][smudge[1]]
        mm[smudge[0]][smudge[1]] = "#" if chr == "." else "."
        tmm[smudge[1]][smudge[0]] = "#" if chr == "." else "."

        sc1, sc2, sc3, sc4 = solve_horizontal(mm), solve_horizontal(mm, reverse=False), solve_horizontal(tmm), solve_horizontal(tmm, reverse=False)

        mm[smudge[0]][smudge[1]] = chr
        tmm[smudge[1]][smudge[0]] = chr
        
        if (sc1 != 0 and sc1 != s1) or (sc2 != 0 and sc2 != s2) or (sc3 != 0 and sc3 != s3) or (sc4 != 0 and sc4 != s4):
            break

    if sc1 == s1:
        sc1 = 0
    if sc2 == s2:
        sc2 = 0
    if sc3 == s3:
        sc3 = 0
    if sc4 == s4:
        sc4 = 0
    
    return 100*(sc1 + sc2 if sc1 != sc2 else sc2) + (sc3 + sc4 if sc3 != sc4 else sc3)
    

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
