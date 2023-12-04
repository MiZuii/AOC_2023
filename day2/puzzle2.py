# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
input = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

ans = 0

line = input.readline()
while len(line):
    sline = line.split(":")
    gameid = sline[0][5:]
    ssline = sline[1].split(";")

    # max numbers of cubes to make game possible
    mr = 0
    mg = 0
    mb = 0

    for sub_game_line in ssline:
        # analyze game colors of each subgame
        colors = sub_game_line.split(",")
        for color in colors:
            r = color.find('red')
            g = color.find('green')
            b = color.find('blue')
            if r != -1:
                rn = int(color[1:r-1])
                mr = max(mr, rn)
            if g != -1:
                gn = int(color[1:g-1])
                mg = max(mg, gn)
            if b != -1:
                bn = int(color[1:b-1])
                mb = max(mb, bn)
    
    set_power = mr*mg*mb
    ans += set_power

    line = input.readline()

print(ans)

# -------------------------------- FILE CLOSE -------------------------------- #
input.close()