with open("input1.txt", "r") as f:
    sum = 0
    line = f.readline()
    while len(line):
        digits = [d for d in line if d.isdigit()]
        sum += int(digits[0])*10 + int(digits[-1])
        line = f.readline()
print(sum)