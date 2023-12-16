# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

visited = None
# 1000 - 8 - ^
# 0100 - 4 - >
# 0010 - 2 - v
# 0001 - 1 - <
UP = 8
RIGHT = 4
DOWN = 2
LEFT = 1

DIRECTION_MAP = {UP: {".": (UP,), "-": (LEFT, RIGHT), "|": (UP,), "/": (RIGHT,), "\\": (LEFT,)},
                 RIGHT: {".": (RIGHT,), "-": (RIGHT,), "|": (UP, DOWN), "/": (UP,), "\\": (DOWN,)},
                 DOWN: {".": (DOWN,), "-": (LEFT, RIGHT), "|": (DOWN,), "/": (LEFT,), "\\": (RIGHT,)},
                 LEFT: {".": (LEFT,), "-": (LEFT,), "|": (UP, DOWN), "/": (DOWN,), "\\": (UP,)}}

def mark_visited(beam):
    visited[beam[0]][beam[1]] |= beam[2]


def get_energized(start_beam):

    global visited
    visited = [[0 for _ in range(len(input[0]))] for _ in range(len(input))]
    beams = [start_beam]

    while True:

        if len(beams) == 0:
            break

        next_beams = []

        for beam in beams:

            beams.remove(beam)

            if beam[2] == UP:
                next_char_cords = (beam[0] - 1, beam[1])
            elif beam[2] == RIGHT:
                next_char_cords = (beam[0], beam[1] + 1)
            elif beam[2] == DOWN:
                next_char_cords = (beam[0] + 1, beam[1])
            elif beam[2] == LEFT:
                next_char_cords = (beam[0], beam[1] - 1)
            else:
                raise RuntimeError("Why?")

            if 0 <= next_char_cords[0] < len(input) and 0 <= next_char_cords[1] < len(input[0]):
                # if the beams doesn't go outside the grid than calculate it

                next_beam_char = input[next_char_cords[0]][next_char_cords[1]]
                next_directions = DIRECTION_MAP[beam[2]][next_beam_char]

                if len(next_directions) == 1:
                    if not (visited[next_char_cords[0]][next_char_cords[1]] & next_directions[0]):
                        next_beam = (next_char_cords[0], next_char_cords[1], next_directions[0])
                        next_beams.append(next_beam)
                        mark_visited(next_beam)
                else:
                    if not (visited[next_char_cords[0]][next_char_cords[1]] & next_directions[0]):
                        next_beam_1 = (next_char_cords[0], next_char_cords[1], next_directions[0])
                        next_beams.append(next_beam_1)
                        mark_visited(next_beam_1)

                    if not (visited[next_char_cords[0]][next_char_cords[1]] & next_directions[1]):
                        next_beam_2 = (next_char_cords[0], next_char_cords[1], next_directions[1])
                        next_beams.append(next_beam_2)
                        mark_visited(next_beam_2)

        beams.extend(next_beams)

    return len(visited)*len(visited[0]) - sum([row.count(0) for row in visited])


def solve():
    best_solve = 0
    for i in range(len(input)):
        sb1 = (i, -1, 4)
        sb2 = (i, len(input), 1)

        sb1s = get_energized(sb1)
        sb2s = get_energized(sb2)

        best_solve = max(best_solve, sb1s, sb2s)

    for j in range(len(input[0])):
        sb1 = (-1, j, DOWN)
        sb2 = (len(input[0]), j, UP)

        sb1s = get_energized(sb1)
        sb2s = get_energized(sb2)

        best_solve = max(best_solve, sb1s, sb2s)
    
    return best_solve


print(solve())
