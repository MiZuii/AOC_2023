# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #
import math

def binom(n, k):
    if n == 0:
        return 1
    if k == 0 or k == n:
        return 1
    
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def calc_nplus1(n, xv):
    xnplus1 = 0
    for ki in range(n):
        xnplus1 += (-1)**(ki + n + 1) * binom(n, ki) * xv[ki]
    return xnplus1

input = inputf.read().split("\n")
input = [list(map(int, line.split(" "))) for line in input]
ans = sum([calc_nplus1(len(xvector), xvector) for xvector in input])
print(ans)

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()