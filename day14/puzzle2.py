# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #
from copy import deepcopy
# IDEA: simulate first few cycles until finding a reapeting pattern

input = list(map(list, input))

def draw_input(input):
    for row in input:
        for c in row:
            print(c, end="")
        print()


def back_draw_N(input, i, j, q):
    for qi in range(q):
        input[i + qi + 1][j] = "O"


def back_draw_S(input, i, j, q):
    for qi in range(q):
        input[i - qi - 1][j] = "O"


def back_draw_E(input, i, j, q):
    for qi in range(q):
        input[i][j - qi - 1] = "O"


def back_draw_W(input, i, j, q):
    for qi in range(q):
        input[i][j + qi + 1] = "O"


def input_to_string(input):
    return "".join(map("".join, input))


rock_vector_SN = [0 for i in range(len(input[0]))]
rock_vector_WE = [0 for i in range(len(input))]


def tilt_N():
    for i in range(len(input)-1, -1, -1):
        # if O -> accomulate, add 1 to rock vector
        # if # -> discharge the accomulation
        # if i=-2 final discharge
        for j, c in enumerate(input[i]):
            if c == "O":
                rock_vector_SN[j] += 1
                input[i][j] = "."
            if c == "#":
                back_draw_N(input, i, j, rock_vector_SN[j])
                rock_vector_SN[j] = 0
    # final discharge
    for j in range(len(input[0])):
        back_draw_N(input, -1, j, rock_vector_SN[j])
        rock_vector_SN[j] = 0


def tilt_S():
    for i in range(len(input)):
        for j, c in enumerate(input[i]):
            if c == "O":
                rock_vector_SN[j] += 1
                input[i][j] = "."
            if c == "#":
                back_draw_S(input, i, j, rock_vector_SN[j])
                rock_vector_SN[j] = 0
    # final discharge
    for j in range(len(input[0])):
        back_draw_S(input, len(input), j, rock_vector_SN[j])
        rock_vector_SN[j] = 0


def tilt_E():
    for j in range(len(input[0])):
        for i in range(len(input)):
            if input[i][j] == "O":
                rock_vector_WE[i] += 1
                input[i][j] = "."
            if input[i][j] == "#":
                back_draw_E(input, i, j, rock_vector_WE[i])
                rock_vector_WE[i] = 0
    # final discharge
    for i in range(len(input)):
        back_draw_E(input, i, len(input[0]), rock_vector_WE[i])
        rock_vector_WE[i] = 0


def tilt_E():
    for j in range(len(input[0])):
        for i in range(len(input)):
            if input[i][j] == "O":
                rock_vector_WE[i] += 1
                input[i][j] = "."
            if input[i][j] == "#":
                back_draw_E(input, i, j, rock_vector_WE[i])
                rock_vector_WE[i] = 0
    # final discharge
    for i in range(len(input)):
        back_draw_E(input, i, len(input[0]), rock_vector_WE[i])
        rock_vector_WE[i] = 0


def tilt_W():
    for j in range(len(input[0])-1, -1, -1):
        for i in range(len(input)):
            if input[i][j] == "O":
                rock_vector_WE[i] += 1
                input[i][j] = "."
            if input[i][j] == "#":
                back_draw_W(input, i, j, rock_vector_WE[i])
                rock_vector_WE[i] = 0
    # final discharge
    for i in range(len(input)):
        back_draw_W(input, i, -1, rock_vector_WE[i])
        rock_vector_WE[i] = 0


def calc_load():
    ans = 0
    for i, row in enumerate(input):
        oc = row.count("O")
        ans += oc*(len(input) - i)
    return ans


def solve():
    cyclei=0
    insf=-1
    ins = []
    while True:
        cyclei += 1
        tilt_N()
        tilt_W()
        tilt_S()
        tilt_E()
        input_s = input_to_string(input)
        try:
            insf = ins.index(input_s)
            break
        except ValueError:
            ins.append(input_s)

    cycle_len = cyclei - insf - 1
    cycles_left = (1000000000 - cyclei) % cycle_len
    for _ in range(cycles_left):
        tilt_N()
        tilt_W()
        tilt_S()
        tilt_E()

    return calc_load()

print(solve())
