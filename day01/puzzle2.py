nsm = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
rsm = {'eno': 1, 'owt': 2, 'eerht': 3, 'ruof': 4, 'evif': 5, 'xis': 6, 'neves': 7, 'thgie': 8, 'enin': 9}

def first_digit(line: str, rev):
    vsm = rsm if rev else nsm
    digits = [d for d in line if d.isdigit()]
    if len(digits) > 0:
        first_digit = digits[0]
    else:
        first_digit = str(-1)
    ss_line = line[0:line.find(first_digit)]
    fs = list(filter(lambda x: x[1] != -1, sorted([(vsm[numstr], ss_line.find(numstr)) for numstr in vsm.keys()], key=lambda x: x[1])))
    if len(fs) > 0:
        return fs[0][0]
    else:
        return int(first_digit)

with open("day1/input2.txt", "r") as f:
    sum = 0
    line = f.readline()
    while len(line):
        fd = first_digit(line, False)
        ld = first_digit(line[::-1], True)
        sum += fd*10 + ld
        line = f.readline()

print(sum)