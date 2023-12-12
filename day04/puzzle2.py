# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
input = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

inp = input.read()
inp = inp.split('\n')
copies = [0 for _ in range(len(inp))]
for i, raw_line in enumerate(inp):
    line = raw_line.split(":")[1]
    winning = line.split("|")[0].split(" ")
    yours = line.split("|")[1].split(" ")
    
    wset = set()
    for wnum in winning:
        if len(wnum):
            wset.add(int(wnum))

    yset = set()
    for ynum in yours:
        if len(ynum):
            yset.add(int(ynum))

    resset = wset.intersection(yset)
    for j in range(copies[i] + 1):
        # repeat as much times as this card has copies (+ original)
        for ci in range(len(resset)):
            copies[i+ci+1] += 1

print(sum(copies) + len(copies))

# -------------------------------- FILE CLOSE -------------------------------- #
input.close()