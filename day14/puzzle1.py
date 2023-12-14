# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

def discharge(index, quantity):
    return quantity*((2*index - quantity + 1)/2)

ans = 0
rock_vector = [0 for i in range(len(input[0]))]
for ri, row in enumerate(input[::-1]):
    # if O -> accomulate, add 1 to rock vector
    # if # -> discharge the accomulation
    for i, c in enumerate(row):
        if c == "O":
            rock_vector[i] += 1
        if c == "#":
            # print(ri, i, discharge(ri, rock_vector[i]))
            ans += discharge(ri, rock_vector[i])
            rock_vector[i] = 0

# accomulate the ones directly on the boarder
for i in range(len(input[0])):
    ans += discharge(len(input), rock_vector[i])

print(int(ans))
