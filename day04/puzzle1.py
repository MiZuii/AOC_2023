# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
input = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

ans = 0
inp = input.read()
inp = inp.split('\n')
for raw_line in inp:
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
    # print(len(resset))
    ans += 2**(len(resset) - 1) if len(resset) != 0 else 0

print(ans)

# -------------------------------- FILE CLOSE -------------------------------- #
input.close()