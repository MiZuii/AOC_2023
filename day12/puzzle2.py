# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from functools import lru_cache

@lru_cache(maxsize=None)
def calc(si, di, hlen):

    global springs
    global data

    # recursion depth limit
    if si == len(springs):
        if di == len(data) and hlen == 0:
            return 1    # this means a valid configuration has been reached
        elif di == len(data) - 1 and hlen == data[di]:
            return 1    # this also means a valid configuration has been reached
        return 0
    
    # create ret variable which sums the propagated answer from lower calls
    ret = 0

    # there are 3 cases:
    # 1. currently viewed char is "#"
    # 2. currently viewed char is "."
    # 3. currently viewed char is "?"

    if springs[si] == "#":
        # this just continues counting the #tags block (checks are after 
        #   block finishes soo here is just a simple recursion call)
        ret += calc(si+1, di, hlen+1)
    elif springs[si] == ".":
        # 2 subcases:
        # 1. A block is currently being counted ( hlen != 0 )
        # 2. No block is counted -> simple recursion
        if hlen != 0:
            # check if the created block is valid (if not don't deepen the recursion)
            if di < len(data) and data[di] == hlen:
                ret += calc(si+1, di+1, 0)
        else:
            ret += calc(si+1, di, hlen,)
    else:
        # for the "?" just run both above cases as if the springs[si] was this character
        ret += calc(si+1, di, hlen+1)
        if hlen != 0:
            if di < len(data) and data[di] == hlen:
                ret += calc(si+1, di+1, 0)
        else:
            ret += calc(si+1, di, hlen)
    
    return ret

ans = 0
for springs, data in [line.split(" ") for line in input]:
    springs = (springs + "?")*4 + springs
    data = ",".join([data, data, data, data, data])
    data = list(map(int, data.split(",")))

    ans += calc(0, 0, 0)
    calc.cache_clear()

print(ans)
