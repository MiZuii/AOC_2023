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

    # flag if game is valid
    valid = True

    for sub_game_line in ssline:
        # analyze game colors of each subgame
        colors = sub_game_line.split(",")
        for color in colors:
            r = color.find('red')
            g = color.find('green')
            b = color.find('blue')
            if r != -1:
                rn = int(color[1:r-1])
                if rn > 12:
                    valid = False
            if g != -1:
                gn = int(color[1:g-1])
                if gn > 13:
                    valid = False
            if b != -1:
                bn = int(color[1:b-1])
                if bn > 14:
                    valid = False
    
    if valid:
        ans += int(gameid)


    line = input.readline()

print(ans)

# -------------------------------- FILE CLOSE -------------------------------- #
input.close()