# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #
from sortedcontainers import SortedKeyList
from itertools import combinations

def tcm(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))

horizontal_spaces = []
for i in range(len(input[0])):
    if input[i] == len(input[i]) * input[i][0]:
        horizontal_spaces.append(i)

galaxies = []
shift_col = 0
MIL = 10**6 - 1
for col in range(len(input[0])):

    shift_row = 0
    no_galaxies = True

    for row in range(len(input)):
        
        if row in horizontal_spaces:
            shift_row += MIL
        
        if input[row][col] == "#":
            no_galaxies = False
            galaxies.append((row + shift_row, col + shift_col))

    if no_galaxies:
        shift_col += MIL

ans = sum([tcm(g1, g2) for g1, g2 in combinations(galaxies, 2)])
print(ans)
