# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split(",")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

ans = 0
for code in input:
    base = 0
    for c in code:
        base = ((base + ord(c))*17) % 256
    ans += base

print(ans)
