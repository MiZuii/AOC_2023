# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #
from math import gcd

input = inputf.read().split("\n")
instructions = input[0]
nodes_strings = input[2:]
nodes = {}
nodev = []
for line in nodes_strings:
    nodes[line[0:3]] = (line[7:10], line[12:15])
    if line[2] == "A":
        nodev.append(line[0:3])
instructions_01 = [0 if ins == "L" else 1 for ins in instructions]
cycles = []

# perform floyds tortoise and hare algorithm
for node in nodev:
    ins_is = 0
    ins_len = len(instructions)
    steps = 0
    snode = node
    zcount = 0
    s = []

    while zcount != 2:
        
        if snode[2] == "Z":
            zcount += 1
            s.append(steps)

        snode = nodes[snode][instructions_01[ins_is]]
        ins_is += 1
        ins_is %= ins_len
        steps += 1

    cycles.append(s[1] - s[0])

def lcm(*integers):
    a = integers[0]
    for b in integers[1:]:
        a = (a * b) // gcd(a, b)
    return a

print(lcm(*cycles))

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()