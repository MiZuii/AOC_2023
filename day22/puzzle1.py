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
no_del = set()

def gprint():
    global g
    print("-==-=--=-==-=")
    for row in g:
        print(row)

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
        no_del.add(g[bsx][bsy][1])

        # update grid
        g[bsx][bsy][0] += abs(bez-bsz) + 1
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
        if len(ts) == 1:
            no_del.add(ts.pop())

no_del.remove("Base")
print(len(input)-len(no_del))
