# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from z3 import *

p, v = (Int('x'), Int('y'), Int('z')), (Int('vx'), Int('vy'), Int('vz'))
eql = []

def append_equation(eql, pa, va, pb, vb, p, v, s):

    # (dy'-dy) X + (dx-dx') Y + (y-y') DX + (x'-x) DY = x' dy' - y' dx' - x dy + y dx
    eql.append((vb[1+s] - va[1+s])*p[0] + (va[0] - vb[0])*p[1+s] + (pa[1+s] - pb[1+s])*v[0] + (pb[0] - pa[0])*v[1+s] == pb[0]*vb[1+s] - pb[1+s]*vb[0] - pa[0]*va[1+s] + pa[1+s]*va[0])


for i in range(3):
    point_a, vector_a = input[i].split("@")
    pa= tuple(map(int, point_a.split(",")))
    va = tuple(map(int, vector_a.split(",")))
    point_b, vector_b = input[i+1].split("@")
    pb= tuple(map(int, point_b.split(",")))
    vb = tuple(map(int, vector_b.split(",")))
    append_equation(eql, pa, va, pb, vb, p, v, 0)

for i in range(2, 5):
    point_a, vector_a = input[i].split("@")
    pa= tuple(map(int, point_a.split(",")))
    va = tuple(map(int, vector_a.split(",")))
    point_b, vector_b = input[i+1].split("@")
    pb= tuple(map(int, point_b.split(",")))
    vb = tuple(map(int, vector_b.split(",")))
    append_equation(eql, pa, va, pb, vb, p, v, 1)

# sol = solve(eql)
s = Solver()
s.add(eql)
r = s.check()
m = s.model()
print(m.eval(p[0]).as_long() + m.eval(p[1]).as_long() + m.eval(p[2]).as_long())