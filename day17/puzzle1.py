# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #
import heapq as hq
from collections import defaultdict

# DIRECTIONS ENUM
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4
DIRECTION_TO_CORDS_SHIFT = {UP: (-1, 0), DOWN: (1, 0), RIGHT: (0, 1), LEFT: (0, -1)}


# LENGTH VECTOR DEFINITION
d = defaultdict(lambda : float('inf'))

# VISITED VECTOR INIT
V = defaultdict(lambda : False)

def get_key(coordinates, direction, blocks_in_line):
    return coordinates[0], coordinates[1], direction, blocks_in_line

def key_to_val(key):
    return (key[0], key[1]), key[2], key[3]

def dput(key, new_d):
    d[key] = new_d

def dget(key):
    return d[key]

def vput(key):
    V[key] = True

def vget(key):
    return V[key]

def d_get_all(coordinates):
    ret = []
    for DIR in [UP, DOWN, LEFT, RIGHT]:
        for i in range(3):
            dd = dget(get_key(coordinates, DIR, i))
            if dd != float('inf'):
                ret.append(dd)
    return ret

def v_get_all(coordinates):
    ret = []
    for DIR in [UP, DOWN, LEFT, RIGHT]:
        for i in range(3):
            dd = vget(get_key(coordinates, DIR, i))
            if dd != False:
                ret.append(dd)
    return ret

# set the starting vertex
s = get_key((0, 0), RIGHT, 0)
sp = get_key((0, 0), DOWN, 0)
dput(s, 0)

q = [(0,) + s, (0,) + sp]

while q:
    u = hq.heappop(q)
    x, *xxxx = u
    u = tuple(xxxx)
    u_cords, u_direct, u_blinl = key_to_val(u)

    if vget(u):
        continue

    # for every neighbor of u
    for v in [((u_cords[0] + DIRECTION_TO_CORDS_SHIFT[DIR][0], u_cords[1] + DIRECTION_TO_CORDS_SHIFT[DIR][1]), DIR, 1 if DIR != u_direct else u_blinl + 1) for DIR in [UP, DOWN, LEFT, RIGHT]]:
        v_cords, v_direct, v_blinl = v
        v = get_key(v_cords, v_direct, v_blinl)

        # check if is valid and not visited
        if 0 <= v_cords[0] < len(input) and 0 <= v_cords[1] < len(input[0]) and vget(v) is False and v_blinl <= 3:
            
            # check if better way is possible, if yes then write new distance
            if dget(v) > dget(u) + int(input[v_cords[0]][v_cords[1]]):
                dput(v, dget(u) + int(input[v_cords[0]][v_cords[1]]))
            
            if ((dget(v),) + v) not in q:
                hq.heappush(q, (dget(v),) + v)

    vput(u)

print(d_get_all((len(input)-1, len(input[0])-1)))
