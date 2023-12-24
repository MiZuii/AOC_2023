# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #
from collections import defaultdict

cords = (0, 0)
CHAR_TO_SHIFT = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
cords_add = lambda x, y : (x[0] + y[0], x[1] + y[1])

path = defaultdict(lambda : '.')
path[cords] = "#"

for ins_i, instruction in enumerate(input):
    inss = instruction.split(" ")
    shift = CHAR_TO_SHIFT[inss[0]]
    
    for _ in range(int(inss[1])):
        cords = cords_add(cords, shift)
        path[cords] = "#"

# find start cords
# iterate rows from the top. find the first point inside 
# (with o side borders!). This fill be the first point
# for the flood fill algorithm
# IMPORTANT
# worst case this can not return a valid value (loop forever)
# but the case is very very unlikely
top = min(map(lambda x: x[0], path.keys()))
bottom = max(map(lambda x: x[0], path.keys()))
left = min(map(lambda x: x[1], path.keys()))
right = max(map(lambda x: x[1], path.keys()))
y = top - 1
stop_flag = False
while not stop_flag:

    found = 0
    if y > bottom:
        raise RuntimeError("FUCK")
    
    for x in range(left-1, right + 1):
        cc = (y, x)
        cchr = path[cc]

        if cchr == '.' and found == 1:
            start_point = cc
            stop_flag = True
            break

        if cchr == '.' and found == 0:
            continue

        if cchr == '.' and found > 1:
            break

        if cchr == '#':
            found += 1
    y += 1

queue = [start_point]
while queue:
    p = queue.pop()

    for v in [(p[0]+1, p[1]), (p[0]-1, p[1]), (p[0], p[1]+1), (p[0], p[1]-1)]:
        if path[v] == '.':
            path[v] = '#'
            queue.append(v)

print(list(path.values()).count("#"))
