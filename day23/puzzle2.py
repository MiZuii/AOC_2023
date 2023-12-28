# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from collections import defaultdict
import heapq as hq
import graphviz as gv

# digraph dict. nodes are crossroads coordinates like "12x5"
# start node is "S" and end node is "E"
# content of dg is 'node : {edge_end_node: edge_len}'

cget = lambda list, cords: list[cords[0]][cords[1]]
def cset(list, cords, val):
    list[cords[0]][cords[1]] = val

dg = defaultdict(dict)
scanned = set()

ets = []    # list of edge_start coordinates to scan

# recursiv function scanning the whole graph
def scan(edge_start, parent_node, prev_cords):
    edge_len = 1
    prev_v = False
    cords = edge_start
    pcords = prev_cords

    while True:

        # choose next cords from possible cords
        tcords = None
        for nc_pos in [(cords[0]+1, cords[1]), (cords[0]-1, cords[1]), (cords[0], cords[1]+1), (cords[0], cords[1]-1)]:
            if nc_pos != edge_start and nc_pos != pcords and 0 <= nc_pos[0] < len(input) and 0 <= nc_pos[1] < len(input[0]) and cget(input, nc_pos) != "#":
                tcords = nc_pos
        pcords = cords
        cords = tcords

        if cords is None:
            break

        # new step made
        edge_len += 1

        if prev_v:
            # end of path
            break

        if cget(input, cords) != "." and pcords != None:
            prev_v = True

    if prev_v:
        try:
            tmp = dg[parent_node][f"{cords[0]}x{cords[1]}"]
        except KeyError:
            dg[parent_node][f"{cords[0]}x{cords[1]}"] = edge_len-1
            dg[f"{cords[0]}x{cords[1]}"][parent_node]= edge_len-1
        else:
            dg[parent_node][f"{cords[0]}x{cords[1]}"] = max(tmp, edge_len-1)
            dg[f"{cords[0]}x{cords[1]}"][parent_node] = max(tmp, edge_len-1)
    else:
        try:
            tmp = dg[parent_node]["E"]
        except KeyError:
            dg[parent_node]["E"] = edge_len-1
            dg["E"][parent_node] = edge_len-1
        else:
            dg[parent_node]["E"] = max(tmp, edge_len-1)
            dg["E"][parent_node] = max(tmp, edge_len-1)
        return
    
    # run next scans
    if f"{cords[0]}x{cords[1]}" in scanned:
        return
    
    scanned.add(parent_node)
    for chr, nc in zip("v^><", [(cords[0]+1, cords[1]), (cords[0]-1, cords[1]), (cords[0], cords[1]+1), (cords[0], cords[1]-1)]):
        if cget(input, nc) == chr:
            scan(nc, f"{cords[0]}x{cords[1]}", cords)

scan((0, 1), "S", (0, 0))

v = defaultdict(lambda : 0)
v["S"] = 1

def dfs(dg, v, node, summ):

    if node == "E":
        return summ + sum(v.values()) - 1
    
    ret = []
    for neighbor in dg[node].keys():
        if v[neighbor] == 0:
            v[neighbor] = 1
            ret.append(dfs(dg, v, neighbor, summ + dg[node][neighbor]))
            v[neighbor] = 0
    if len(ret) == 0:
        return 0
    return max(ret)

print(dfs(dg, v, "S", 0)-1)
