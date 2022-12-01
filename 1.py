with open('1_input.txt') as f:
    x = 0
    calories = []
    for line in f.readlines():
        line = line.strip()
        if len(line) > 0:
            x += int(line)
        else:
            calories.append(x)
            x = 0
    calories.sort()
    print("highest:", calories[-1])
    print("highest three:", sum(calories[-3:]), "=", calories[-3:])
