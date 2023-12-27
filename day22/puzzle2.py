# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from collections import defaultdict

# make 2d grid with tuples (A, num) which mean what block is the highest there and the hight
# go through all blocks updating the 2d grid and constructing support dict. Dict contains
# for all blocks a set of blocks that is rellies on. finally while checking if you can delete
# a block. Remove it from all dict sets and check if all the sets have at least one element
# if yes the block can be desintegrated else it cannot

# based on the input the grid is 10x10
g = [[[0, "Base"] for _ in range(10)] for _ in range(10)]
d = defaultdict(lambda : [set(), set()])
# first set is for nodes the current node relies on and the seccond set
# is for nodes that relly on current node

ref = []

for block in input:

    bs, be = block.split("~")
    bsx, bsy, bsz = map(int, bs.split(","))
    bex, bey, bez = map(int, be.split(","))
    ref.append((bsx, bsy, bsz, bex, bey, bez))

ref.sort(key=lambda b: b[2])

for i, block in enumerate(ref):
    bsx, bsy, bsz, bex, bey, bez = block
    
    # vertical block
    if bsx == bex and bsy == bey:

        # update reliance dict
        d[str(i)][0].add(g[bsx][bsy][1])
        d[g[bsx][bsy][1]][1].add(str(i))

        # update grid
        g[bsx][bsy][0] += bez-bsz + 1
        g[bsx][bsy][1] = str(i)

    # horizontal block
    else:

        highs = None    # for typing
        highest = -1

        for x in range(bsx, bex+1):
            for y in range(bsy, bey+1):
                if g[x][y][0] > highest:
                    highs = [g[x][y][1]]
                    highest = g[x][y][0]
                elif g[x][y][0] == highest:
                    highs.append(g[x][y][1])
        
        for x in range(bsx, bex+1):
            for y in range(bsy, bey+1):
                g[x][y][0] = highest + 1
                g[x][y][1] = str(i)

        ts = set(highs)
        d[str(i)][0] = ts
        for h in ts:
            d[h][1].add(str(i))

ans = 0
for key in d.keys():
    
    if key == "Base":
        continue

    fall_set = set([key])

    q = [k for k in d[key][1]]
    while q:
        ck = q.pop(0)
        cs = d[ck][0]
        if cs.issubset(fall_set):
            # this means all the supports of the new ck already fell
            fall_set.add(ck)
            for add_el in d[ck][1]:
                q.append(add_el)

    ans += len(fall_set)-1

print(ans)
