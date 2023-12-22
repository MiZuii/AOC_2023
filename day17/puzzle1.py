# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #
import heapq as hq
from collections import defaultdict

# length vector
d = defaultdict(lambda : float('inf'))
p = {}

# visited vector
visited = defaultdict(lambda : False)

# DIRECTIONS ENUM
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4
DIRECTION_TO_CORDS_SHIFT = {UP: (-1, 0), DOWN: (1, 0), RIGHT: (0, 1), LEFT: (0, -1)}
BACK_STEP = {UP: DOWN, DOWN: UP, RIGHT: LEFT, LEFT: RIGHT}

def get_neighbors(u):
    for DIR in [UP, DOWN, RIGHT, LEFT]:
        # If the neighbor is not a step back
        if DIR != BACK_STEP[u[2]]:
            shift = DIRECTION_TO_CORDS_SHIFT[DIR]
            new_blocks_count = 1 if DIR != u[2] else u[3] + 1
            cords_x = u[0] + shift[0]
            cords_y = u[1] + shift[1]
            if 0 <= cords_x < len(input) and 0 <= cords_y < len(input[0]) and new_blocks_count <= 3:
                yield (cords_x, cords_y, DIR, new_blocks_count)

def find_index_by_values_filter(lst, target_values):
    filtered_tuples = filter(lambda tpl: tpl[1:5] == target_values, lst)
    try:
        index = lst.index(next(filtered_tuples))
    except StopIteration:
        index = -1
    return index

def get_ans():
    res = []
    for i in range(1, 5):
        for j in range(3):
            ans = d[(len(input)-1, len(input[0])-1, i, j)]
            if ans != float('inf'):
                res.append(ans)
    return res

def print_lens():
    for x in range(len(input)):
        for y in range(len(input[0])):
            res = []
            for i in range(1, 5):
                for j in range(3):
                    ans = d[(x, y, i, j)]
                    if ans != float('inf'):
                        res.append(ans)
            print(min(res), end=" ")
        print()

def print_path():

    DIR_TO_CHAR = {UP: "^", DOWN: "v", RIGHT: ">", LEFT: "<"}

    best = float('inf')
    bc = None
    for i in range(1, 5):
        for j in range(3):
            ans = d[(len(input)-1, len(input[0])-1, i, j)]
            if ans < best:
                bc = (len(input)-1, len(input[0])-1, i, j)
                best = ans
    
    node = bc
    ic = input.copy()
    ic = list(map(list, ic))
    while True:
        ic[node[0]][node[1]] = DIR_TO_CHAR[node[2]]
        node = p[node]
        if node[0] == 0 and node[1] == 0:
            break
    for row in ic:
        for c in row:
            print(c, end="")
        print()

# key struct
# tuple(x coordinate, y coordinate, direction, blocks count)
start_key_arr = [(0, 0, RIGHT, 0), (0, 0, DOWN, 0)]

# set the starting vertices
d[start_key_arr[0]] = 0
d[start_key_arr[1]] = 0

# init the heapq
q = [(0,) + start_key_arr[0], (0,) + start_key_arr[1]]

while q:

    u = hq.heappop(q)
    cost, *key = u
    u = tuple(key)

    if visited[u] is True:
        continue

    # for every neighbor of u
    for v in get_neighbors(u):
        
        # check if visited
        if visited[v] is True:
            continue

        if d[v] > d[u] + int(input[v[0]][v[1]]):
            d[v] = d[u] + int(input[v[0]][v[1]])
            p[v] = u

        # push to queue
        i = find_index_by_values_filter(q, v[:4])
        if i == -1:
            hq.heappush(q, (d[v],) + v)

    visited[u] = True

print(min(get_ans()))
