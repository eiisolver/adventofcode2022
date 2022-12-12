instructions = [line.split() for line in open("10_input.txt", "r").read().splitlines()]
x = [1]
for inst in instructions:
    x.append(x[-1])
    if inst[0] == "addx":
        x.append(x[-1] + int(inst[1]))

print(x)
interesting_x = [i * x[i - 1] for i in range(20, 221, 40)]
print("Part 1", sum(interesting_x))

crt = ""
for i in range(240):
    diff = abs(x[i] - i % 40)
    c = "#" if diff <= 1 else "."
    crt += c

for i in range(0, 240, 40):
    print(crt[i : i + 40])
