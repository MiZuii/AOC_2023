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

# setter for path matrix
def path_update(cords, path_matrix):
    path_matrix[cords[0]][cords[1]] = 1


# getter for path matrix
def path_get(cords, path_matrix):
    return path_matrix[cords[0]][cords[1]]


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


# create matrix for tracking path
path_matrix = [[0 for _ in range(len(input[0]))] for _ in range(len(input))]
path_update(s_cords, path_matrix)
s_found = False
path_len = 1


# perform first step out off loop to establish the initial direction
init_paths = get_initial_paths(s_cords, input)
path_update(init_paths[0], path_matrix)
current_cords = init_paths[0]

# fill the whole path
while not s_found:
    path_len += 1
    possible_paths = get_next_path(current_cords, input)
    for possible_cords in possible_paths:
        if not path_get(possible_cords, path_matrix):
            path_update(possible_cords, path_matrix)
            current_cords = possible_cords
        # PATH GET IS USED AS UNIVERSAL MATRIX GETTER
        if path_get(possible_cords, input) == "S" and path_len > 3:
            s_found = True

# raytrace every line automaticly updating the ans
ans = 0
for y, line in enumerate(input):

    in_loop = False
    on_border = False
    border_start = ""
    border_end = ""

    # iterate trhough line checking which elements are inside
    # there are three possible cases
    # 1. the char is "|" => Change the in_loop indicator
    # 2. the cords are not loop included => increment the ans by 1 if the in_loop is True
    # 3. the char is not "|" and cords are in loop => indicates the vertical boarder. =>
    #   ship the boarder counting if indicator should change or not

    for x, pipe in enumerate(line):

        # seccond case
        if not path_get((y, x), path_matrix) and in_loop:
            ans += 1

        # first case
        elif path_get((y, x), path_matrix) and pipe == "|":
            in_loop = not in_loop

        # third case
        elif path_get((y, x), path_matrix):
            if not on_border:
                border_start = pipe
                on_border = True

            elif on_border and pipe != "-":
                border_end = pipe
                on_border = False

                # calculate at the end of pipe if the indicator changes
                pipe_type = border_start + border_end
                if pipe_type == "FJ" or pipe_type == "L7":
                    in_loop = not in_loop

                # else      empty because it just continues without changeing the in_loop

            # else      no else because else just skips the pipe

print(ans)
