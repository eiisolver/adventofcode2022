import numpy as np

data = open("14_input.txt", "r").read().splitlines()
occupied = set()


def add_segment(fr, to):
    occupied.add(fr)
    while fr != to:
        fr = tuple(fr[i] + np.sign(to[i] - fr[i]) for i in range(2))
        occupied.add(fr)


max_y = 0
for line in data:
    segments = [tuple(int(x) for x in seg.split(",")) for seg in line.split(" -> ")]
    max_y = max(max_y, max(seg[1] for seg in segments))
    for i in range(len(segments) - 1):
        add_segment(segments[i], segments[i + 1])

stack = [(500, 0)]  # Contains the path along which the sand falls
count = 0
part1_completed = False
while True:
    c = stack[-1]
    rest = True
    for delta in [(0, 1), (-1, 1), (1, 1)]:
        c2 = tuple(c[i] + delta[i] for i in range(2))
        if not c2 in occupied:
            stack.append(c2)
            rest = False
            c = c2
            break
    if c[1] > max_y and not part1_completed:
        part1_completed = True
        print("Part 1:", count)
    if rest or c[1] == max_y + 1:
        # The sand came to a rest, or to the bottom
        occupied.add(c)
        count += 1
        stack.pop()
        if not stack:
            print("Part 2:", count)
            break
