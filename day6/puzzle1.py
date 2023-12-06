# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

from math import sqrt, floor, ceil

input = inputf.read().split("\n")
times = list(map(lambda x: int(x), filter(lambda x: len(x) > 0, input[0][9:].split(" "))))
distances = list(map(lambda x: int(x), filter(lambda x: len(x) > 0, input[1][9:].split(" "))))
ans = 1

for time, distance in zip(times, distances):

    ts = (time - sqrt(time**2 - 4*distance))/2
    te = (time + sqrt(time**2 - 4*distance))/2

    if ts.is_integer():
        ts += 0.5
    if te.is_integer():
        te -= 0.5

    ans *= (floor(te) - ceil(ts) + 1)

print(ans)

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()