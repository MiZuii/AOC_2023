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
start_point = ?

queue = [start_point]
while queue:
    pass
    