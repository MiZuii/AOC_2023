# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

input = inputf.read().split("\n")
instructions = input[0]
nodes_strings = input[2:]
nodes = {}
for line in nodes_strings:
    nodes[line[0:3]] = (line[7:10], line[12:15])

node = "AAA"
ins_i = 0
steps = 0
ins_len = len(instructions)
while node != "ZZZ":
    node = nodes[node][0 if instructions[ins_i] == "L" else 1]
    ins_i += 1
    ins_i %= ins_len
    steps += 1

print(steps)

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()