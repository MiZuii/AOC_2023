# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from functools import reduce

def printi(p):
    print("-==-=--=--=--=-==-")
    print(f"step: {p}")
    ic = list(map(list, input))
    for i in range(len(input)):
        for j in range(len(input[0])):
            if cget(visited, (i, j, p % 2)):
                ic[i][j] = "O"

    for row in ic:
        for c in row:
            print(c, end="")
        print()

cget = lambda iter, cords: reduce(lambda val, idx : val[idx], cords, iter)

MAX_STEPS = 64

visited = [[[0, 0] for _ in range(len(input[0]))] for _ in range(len(input))]
s = (len(input)//2, len(input[0])//2)
q = [(s, 0)]

while q:

    # pop next step cords
    node = q.pop()
    cords, step = node

    # check if in steps
    if step > MAX_STEPS:
        continue

    for nc in [(cords[0]+1, cords[1]), (cords[0]-1, cords[1]), (cords[0], cords[1]+1), (cords[0], cords[1]-1)]:
        if 0 <= nc[0] < len(input) and 0 <= nc[1] < len(input[0]) and cget(input, nc) != "#":
            vv = cget(visited, nc + (((step + 1) % 2),))
            if vv == 0 or step + 1 < vv:
                # not visited or can be resolved better
                visited[nc[0]][nc[1]][(step + 1) % 2] = step + 1
                q.append((nc, step+1))


ans = 0
for i in range(len(input)):
    for j in range(len(input[0])):
        ans += 1 if cget(visited, (i, j, 0)) else 0
print(ans)
