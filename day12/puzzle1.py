# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from itertools import permutations


def gen_perms(noh, nod, l, pref=""):
    
    # recursion depth
    if noh == 0 and nod == 0:
        l.append(pref)
    
    if noh != 0:
        gen_perms(noh-1, nod, l, pref + "#")
    if nod != 0:
        gen_perms(noh, nod-1, l, pref + ".")

    return l


def validate(s, fill, data):
    
    # iteration indexes
    di = -1
    dcouter = 0
    counting = False

    # helper functions
    def iter_s():
        filli = 0
        for chr in s:
            if chr != "?":
                yield chr
            else:
                yield fill[filli]
                filli += 1
    
    # iteration
    for chr in iter_s():
        if chr == "#" and counting is True:
            dcouter += 1
        elif chr == "#" and counting is False:
            counting = True
            dcouter = 1
            di += 1
        elif chr == "." and counting is True:
            counting = False
            if data[di] != dcouter:
                return 0
            
    # edge (last char = #) case
    if data[di] != dcouter:
        return 0
    return 1


ans = 0
en = 0
for springs, data in [zip(line.split(" ")) for line in input]:
    springs = springs[0]
    data = list(map(int, data[0].split(",")))
    
    noh = sum(data) - springs.count("#")
    nod = springs.count("?")-noh
    
    combination_strings = gen_perms(noh, nod, [])
    ans += sum([validate(springs, comb, data) for comb in combination_strings])

print(ans)
