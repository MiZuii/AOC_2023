# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

pipe_to_cshift = {"|": ((1, 0), (-1, 0)), 
                  "-": ((0, 1), (0, -1)), 
                  "L": ((-1, 0), (0, 1)), 
                  "F": ((1, 0), (0, 1)), 
                  "J": ((-1, 0), (0, -1)), 
                  "7": ((1, 0), (0, -1))}

def get_initial_paths(cords, maze):
    vpaths = []
    for valid_cords, valid_pipes in [((cords[0] + 1, cords[1]), "|LJ"), 
                                     ((cords[0] - 1, cords[1]), "|7F"), 
                                     ((cords[0], cords[1] + 1), "-J7"), 
                                     ((cords[0], cords[1] - 1), "-LF")]:
        if valid_cords[0] >= 0 and valid_cords[0] < len(maze) and valid_cords[1] >= 0 and valid_cords[1] < len(maze[0]) \
                and input[valid_cords[0]][valid_cords[1]] in valid_pipes:
            vpaths.append(valid_cords)
    if len(vpaths) != 2:
        raise RuntimeError("Impossible initial paths calculation!")
    return vpaths


def get_next_path(cords, maze):
    current_pipe = maze[cords[0]][cords[1]]
    shifts = pipe_to_cshift[current_pipe]
    link_cords = [(cords[0] + shift[0], cords[1] + shift[1]) for shift in shifts]
    return link_cords


# get starting point
s_cords = None

for i in range(len(input)):
    s_i = input[i].find("S")
    if s_i != -1:
        s_cords = (i, s_i)
        break


# follow path until finding S again
path = [s_cords]
s_found = False

# perform first step out off loop to establish the initial direction
init_paths = get_initial_paths(s_cords, input)
path.append(init_paths[0])

while not s_found:
    current_cords = path[-1]
    possible_paths = get_next_path(current_cords, input)
    for possible_cords in possible_paths:
        if possible_cords not in path:
            path.append(possible_cords)
        if input[possible_cords[0]][possible_cords[1]] == "S" and len(path) > 3:
            s_found = True

print(len(path)//2)
