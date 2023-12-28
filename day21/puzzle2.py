# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

import fractions, math
from collections import defaultdict

cget2 = lambda iter, cords: iter[cords[0] % len(iter)][cords[1] % len(iter[0])]
cget3 = lambda iter, cords: iter[cords[0]][cords[1]][cords[2]]

def bfs(ev, ms):
    MAX_STEPS = ms
    visited = defaultdict(lambda : defaultdict(lambda : [0, 0]))
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
            if cget2(input, nc) != "#":

                vv = cget3(visited, nc + (((step + 1) % 2),))
                if vv == 0 or step + 1 < vv:
                    # not visited or can be resolved better
                    visited[nc[0]][nc[1]][(step + 1) % 2] = step + 1
                    q.append((nc, step+1))

    ans = 0
    for x in visited.keys():
        for y in visited[x].keys():
            ans += 1 if cget3(visited, (x, y, ev)) else 0
    return ans

# print(bfs(1, 65), bfs(0, 196), bfs(1, 327), bfs(0, 458))
# 3762 33547 93052 182277
# print(bfs(0, 6), bfs(0, 10), bfs(0, 50), bfs(0, 100), bfs(0, 500))

x = [65, 196, 327]
y = [3762, 33547, 93052]
n = 26501365
def poly_lagrange(p):
    a = (
        fractions.Fraction(
            math.prod(p - xj for xj in x if xj != xi),
            math.prod(xi - xj for xj in x if xj != xi),
        )
        for xi in x
    )
    return sum(ai * yi for ai, yi in zip(a, y))

print(poly_lagrange(26501365))
