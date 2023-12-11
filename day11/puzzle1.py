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

shift = 0
for hs_index in horizontal_spaces:
    input.insert(hs_index+shift, input[hs_index+shift])
    shift += 1

galaxies = []
shift = 0
for col in range(len(input[0])):

    no_galaxies = True

    for row in range(len(input)):
        if input[row][col] == "#":
            no_galaxies = False
            galaxies.append((row, col + shift))

    if no_galaxies:
        shift += 1

ans = sum([tcm(g1, g2) for g1, g2 in combinations(galaxies, 2)])
print(ans)
