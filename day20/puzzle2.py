# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from collections import defaultdict
from functools import reduce
import graphviz as gv
from math import gcd


def lcm(*integers):
    a = integers[0]
    for b in integers[1:]:
        a = (a * b) // gcd(a, b)
    return a

FLIP_FLOP = 0
CONJUNCTION = 1
BROADCASTER = 2

LOW = 0
HIGH = 1

nodes = defaultdict(lambda : [0, [], []])

for line in input:
    if line[0] == "%" or line[0] == "&":
        sl = line.split(" ")
        name = sl[0][1:]
        nodes[name][0] = CONJUNCTION if line[0] == "&" else FLIP_FLOP
        for next in sl[2:]:
            if next[-1] == ",":
                next = next[:-1]
            nodes[name][1].append(next)
            nodes[next][2].append(name)
    else:
        sl = line.split(" ")
        name = sl[0]
        nodes[name][0] = BROADCASTER
        for next in sl[2:]:
            if next[-1] == ",":
                next = next[:-1]
            nodes[name][1].append(next)
            nodes[next][2].append(name)


def make_graphvis(nodes, name):
    
    # init
    dot = gv.Digraph(engine="dot")
    dot.attr('graph', ordering="in")

    important_endges = set([("dg", "rx"), ("sp", "dg"), ("xt", "dg"), ("lk", "dg"), ("zv", "dg")])

    # graph creation
    for key in nodes.keys():
        shape = "diamond" if nodes[key][0] == FLIP_FLOP else "oval"
        dot.node(key, shape=shape)

    for key in nodes.keys():
        cont = nodes[key]

        for next_node in cont[1]:
            if (key, next_node) in important_endges:
                dot.edge(key, next_node, weight="30")
            else:
                dot.edge(key, next_node)

    
    # additional properties
    dot.body.append(" { rank = source; \"broadcaster\"; } ")
    dot.body.append(" { rank = sink; \"rx\"; } ")
    dot.body.append(" { rank = same; \"sp\"; \"xt\"; \"lk\"; \"zv\"; } ")
    dot.body.append(" { rank = same; \"xq\"; \"dv\"; \"jc\"; \"vv\"; } ")

    file_name = os.path.dirname(__file__) + f"/{name}"

    # save and return
    if name is not None:
        with open(file_name + ".dot", "w") as f:
            f.write(dot.source)
        dot.render(file_name + ".dot", format="png", cleanup=True)
    return dot.source


# make_graphvis(nodes, "test")

signals = []
state = {key: ( LOW if (item[0] == FLIP_FLOP or item[0] == BROADCASTER) \
                    else {key: LOW for key in item[2]} )
            for key, item in nodes.items()}

bp = 0

# input speicfic
xt, sp, lk, zv = [], [], [], []

while True:

    if len(xt) > 0 and len(sp) > 0 and len(lk) > 0 and len(zv) > 0:
        break

    # signals repr
    # (pulse type [LOW/HIGH], receiver, sender)

    # button push
    signals.append((LOW, 'broadcaster', 'button'))
    bp += 1
    
    # simulate
    while signals:

        signal = signals.pop(0)

        # input specific
        if signal[1] == "dg" and signal[0] == HIGH:
            globals()[signal[2]].append(bp)

        # simulate
        module_type = nodes[signal[1]][0]
        if module_type == FLIP_FLOP:

            # flip flops skip high signals
            if signal[0] == HIGH:
                continue

            ff_state = state[signal[1]]
            new_state = LOW if ff_state == HIGH else HIGH
            state[signal[1]] = new_state
            for next_module in nodes[signal[1]][1]:
                signals.append((new_state, next_module, signal[1]))

        elif module_type == CONJUNCTION:

            # update state first
            state[signal[1]][signal[2]] = signal[0]

            new_sig = LOW if all(state[signal[1]].values()) else HIGH
            for next_module in nodes[signal[1]][1]:
                signals.append((new_sig, next_module, signal[1]))

        else:   # module_type == BROADCASTER
            
            # resend for all
            for next_module in nodes[signal[1]][1]:
                signals.append((signal[0], next_module, signal[1]))

print(lcm(xt[0], sp[0], lk[0], zv[0]))