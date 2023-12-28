# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from collections import defaultdict
# import graphviz as gv
import networkx as nx

g = defaultdict(set)
G = nx.Graph(strict=True)

for line in input:
    bn, ns = line.split(":")
    nods = filter(lambda x: True if len(x) != 0 else False, ns.split(" "))
    for node in nods:
        if G.has_edge(node, bn):
            pass
        else:
            G.add_edge(bn, node, weight=1)
        g[bn].add(node)
        g[node].add(bn)

cut_value, partition = nx.stoer_wagner(G)
print(len(partition[0])*len(partition[1]))


# def make_graph(g):

#     dot = gv.Graph(strict=True)

#     for key in g.keys():
#         dot.node(key)

#     for key, ks in g.items():
#         for sk in ks:
#             dot.edge(key, sk)
    
#     name = "tmp"
#     file_name = os.path.dirname(__file__) + f"/{name}"

#     # save and return
#     if name is not None:
#         with open(file_name + ".dot", "w") as f:
#             f.write(dot.source)
#         dot.render(file_name + ".dot", format="png", cleanup=True)
#     return dot.source

# make_graph(g)
