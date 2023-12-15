# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split(",")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

def hash(s):
    base = 0
    for c in s:
        base = ((base + ord(c))*17) % 256
    return base


HASHMAP = {i:([], {}) for i in range(256)}


def print_hashmap():
    print("--==-=--==--=-==--==---=-")
    for i, box in HASHMAP.items():
        if len(box[0]):
            print(i, ":", box)


def solve():
    for code in input:
        code_op = code[-2]

        if code_op == "=":
            code_label = code[:-2]
            code_hash = hash(code_label)
            if code_label not in HASHMAP[code_hash][0]:
                HASHMAP[code_hash][0].append(code_label)
            HASHMAP[code_hash][1][code_label] = int(code[-1])

        else:
            code_label = code[:-1]
            code_hash = hash(code_label)
            try:
                HASHMAP[code_hash][1].pop(code_label)
                HASHMAP[code_hash][0].remove(code_label)
            except KeyError:
                pass

    # sum the result
    ans = 0
    for box_id, val in HASHMAP.items():
        for i, label in enumerate(val[0]):
            ans += (box_id+1)*(i+1)*val[1][label]
    return ans


print(solve())
