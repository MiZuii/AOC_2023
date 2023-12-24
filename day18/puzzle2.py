# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #
import heapq as hq
from sortedcontainers import SortedListWithKey
from functools import reduce
from operator import getitem

# cords repr
# (x, y)
# 0\0 -----> x
# |
# |
# V
# y

# lines repr
# (sorting val, (start point), (end point))

# help functions
cords_add =     lambda x, y: (x[0] + y[0], x[1] + y[1])
cords_mul =     lambda x, mul: (x[0] * mul, x[1] * mul)
none_to_inf =   lambda x, idx: float('inf') if len(x) == 0 else reduce(getitem, idx, x)

# init structs
ans = 0
prev_cords = (0, 0)
DIR_TO_SHIFT = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
h_stamps = []
v_lines = []

# parse input into lines
for instruction in input:
    inss = instruction.split(" ")
    distance = inss[2][2:7]
    direction = int(inss[2][7])
    cords = cords_add(prev_cords, cords_mul(DIR_TO_SHIFT[direction], int(distance, 16)))
    if cords[0] == prev_cords[0]:
        # new vline
        hq.heappush(v_lines, (min(prev_cords[1], cords[1]), prev_cords if prev_cords[1] <= cords[1] else cords, prev_cords if cords[1] < prev_cords[1] else cords))
    elif cords[1] == prev_cords[1]:
        # new hline
        hq.heappush(h_stamps, cords[1])
    else:
        raise RuntimeError('U stupid')
    prev_cords = cords

# create initial structures
stamp = hq.heappop(h_stamps)
prev_stamp = None
upper_v_lines = SortedListWithKey(key=lambda x: x[0][0])
lower_v_lines = SortedListWithKey(key=lambda x: x[0][0])

# fill the initial lower lines
while len(v_lines) > 0 and v_lines[0][0] == stamp:
    new_lower_line = hq.heappop(v_lines)
    lower_v_lines.add((new_lower_line[1], new_lower_line[2]))

# start algorithm
while h_stamps:

    # get new stamps
    prev_stamp = stamp
    stamp = hq.heappop(h_stamps)

    # push old lower lines to upper lines with updates
    upper_v_lines.clear()
    tmplines = SortedListWithKey(key=lambda x: x[0][0])
    for line in lower_v_lines:

        # if lower point of the line is now on the new stamp -> the line can just be pushed up
        if line[1][1] == stamp:
            upper_v_lines.add(line)
        # else the line needs to be split into parts and lower cut stays in the lower lines
        else:
            new_upper_line = (line[0], (line[0][0], stamp))
            new_lower_line = ((line[0][0], stamp), line[1])
            upper_v_lines.add(new_upper_line)
            tmplines.add(new_lower_line)
    lower_v_lines = tmplines

        
    # push new lines to lower_v_lines
    while len(v_lines) > 0 and v_lines[0][0] == stamp:
        new_lower_line = hq.heappop(v_lines)
        lower_v_lines.add((new_lower_line[1], new_lower_line[2]))

    llc = lower_v_lines.copy()  # copy of lower lines
    # now the structures are updated soo the calculation step can be performed
        
    # init(reset) variables
    ul = None       # last popped upper line
    pul = None      # previous ul
    ll = None       # last popped lower line
    llin = False    # lower part is in box indicator
    ulin = False    # upper part is in box indicator
    cflg = False    # flag written to True if the ulin got changed from True -> False in this step (indicates the end of a box to calculate)
    lll = []        # list of loser lines in the range of claculated upper box

    while True:

        # perform step ( move to the next X value in both lower and upper lines )
        # lines[0][0][0] -> gets the x value of the line with the lowest x in the list
        # if the structure is correct the none_to_inf function prevents the algorithm from popping from empty list
        # none_to_inf(list, (0, 0, 0)) -> list[0][0][0] # but with the none check
        minx = min(none_to_inf(upper_v_lines, (0, 0, 0)), none_to_inf(lower_v_lines, (0, 0, 0)))

        # due to none_to_inf function the stop condition is
        if minx == float('inf'):
            break

        # update vars
        if minx == none_to_inf(upper_v_lines, (0, 0, 0)) and minx == none_to_inf(lower_v_lines, (0, 0, 0)):
            pul = ul
            ul = upper_v_lines.pop(0)
            ll = lower_v_lines.pop(0)

            if ulin is False:
                lll = [ll]
            else:
                cflg = True
                lll.append(ll)

            ulin = not ulin
            llin = not llin

        elif minx == none_to_inf(upper_v_lines, (0, 0, 0)):
            pul = ul
            ul = upper_v_lines.pop(0)

            # ul is pushed to lll here because only the x values matter (saves time for changing it to a real ll)
            if ulin is False:
                if llin is True:
                    lll = [ul]
                else:
                    lll = []
            else:
                cflg = True
                if llin is True:
                    lll.append(ul)
                else:
                    pass
                

            ulin = not ulin

        elif minx == none_to_inf(lower_v_lines, (0, 0, 0)):
            ll = lower_v_lines.pop(0)

            if ulin:
                lll.append(ll)

            llin = not llin

        else:
            raise RuntimeError('Why are you here?')
        
        # calculate box volume and add to ans
        if cflg:
            cflg = False

            # main squre calc
            h = stamp - prev_stamp + 1
            w = ul[0][0] - pul[0][0] + 1
            ans += h*w

            # overlap removal
            if len(lll) > 0:
                overlap_sum = sum([lll[i+1][0][0] - lll[i][0][0] + 1 for i in range(0, len(lll), 2)])
            else:
                overlap_sum = 0
            ans -= overlap_sum

    # retrive the lower lines
    lower_v_lines = llc

print(ans)
        