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
            dg[parent_node][f"{cords[0]}x{cords[1]}"] = edge_len
        else:
            dg[parent_node][f"{cords[0]}x{cords[1]}"] = max(tmp, edge_len)
    else:
        try:
            tmp = dg[parent_node]["E"]
        except KeyError:
            dg[parent_node]["E"] = edge_len
        else:
            dg[parent_node]["E"] = max(tmp, edge_len)
        return
    
    # run next scans
    if f"{cords[0]}x{cords[1]}" in scanned:
        return
    
    scanned.add(parent_node)
    for chr, nc in zip("v^><", [(cords[0]+1, cords[1]), (cords[0]-1, cords[1]), (cords[0], cords[1]+1), (cords[0], cords[1]-1)]):
        if cget(input, nc) == chr:
            scan(nc, f"{cords[0]}x{cords[1]}", cords)

scan((0, 1), "S", (0, 0))

# perform shortest path search but on negative numbers
# length vector
d = defaultdict(lambda : float('inf'))

q = [(0, "S")]
d["S"] = 0


while q:

    u = hq.heappop(q)
    u = u[1]

    for v, wei in dg[u].items():
        if d[v] > d[u] - dg[u][v]:
            d[v] = d[u] - dg[u][v]

            hq.heappush(q, (d[v], v))

print(abs(d["E"])-1)


# PUZZLE VIZUALIZATION
def make_graph(dg, name):

    dot = gv.Digraph()

    for key in dg.keys():
        dot.node(key)

    for key in dg.keys():
        for end, wei in dg[key].items():
            dot.edge(key, end, label=str(wei))

    file_name = os.path.dirname(__file__) + f"/{name}"

    # save and return
    if name is not None:
        with open(file_name + ".dot", "w") as f:
            f.write(dot.source)
        dot.render(file_name + ".dot", format="png", cleanup=True)
    return dot.source

# make_graph(dg, "t")
