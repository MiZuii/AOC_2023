# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

def find_intersection_point(p1, v1, p2, v2):
    x1, y1 = p1
    x2, y2 = p2
    dx1, dy1 = v1
    dx2, dy2 = v2

    # Check if the lines are parallel
    det = dx1 * dy2 - dy1 * dx2
    if det == 0:
        return float('inf'), float('inf')

    # Calculate the parameter values for intersection
    t1 = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / det
    t2 = ((x2 - x1) * dy1 - (y2 - y1) * dx1) / det

    if t1 < 0 or t2 < 0:
        return float('inf'), float('inf')

    # Calculate the intersection point
    intersection_x = x1 + t1 * dx1
    intersection_y = y1 + t1 * dy1

    return intersection_x, intersection_y

lines = []
ans = 0
LOWER_BOUND = 200000000000000
UPPER_BOUND = 400000000000000

for line in input:
    point, vector = line.split("@")
    x, y, z = map(int, point.split(","))
    vx, vy, vz = map(int, vector.split(","))

    lines.append(((x, y), (vx, vy)))
    for subline in lines[:-1]:
        ip = find_intersection_point(lines[-1][0], lines[-1][1], subline[0], subline[1])
        if LOWER_BOUND <= ip[0] <= UPPER_BOUND and LOWER_BOUND <= ip[1] <= UPPER_BOUND:
            ans += 1

print(ans)
