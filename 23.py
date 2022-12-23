from collections import Counter

data = open("23_input.txt", "r").read().splitlines()

elves = set((x, y) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == "#")

N = (0, -1)
E = (1, 0)
S = (0, 1)
W = (-1, 0)
NE = (1, -1)
SE = (1, 1)
SW = (-1, 1)
NW = (-1, -1)
DIRS8 = (N, E, S, W, NE, SE, SW, NW)
PROPOSED_DIRS = [(N, NE, NW), (S, SE, SW), (W, NW, SW), (E, NE, SE)]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def is_empty(elves, e, dirs):
    adj = set(add(e, d) for d in dirs)
    return not (elves & adj)


def calc_empty(elves):
    min_x = min(e[0] for e in elves)
    max_x = max(e[0] for e in elves)
    min_y = min(e[1] for e in elves)
    max_y = max(e[1] for e in elves)
    empty = 0
    print("range: x:", min_x, max_x, ", y:", min_y, max_y)
    for y in range(min_y, max_y + 1):
        s = ""
        for x in range(min_x, max_x + 1):
            if not (x, y) in elves:
                empty += 1
                s += "."
            else:
                s += "#"
        print(s)
    print("nr empty:", empty)
    return empty


def perform_round(elves, r):
    moves = []
    move_count = 0
    for e in elves:
        dest = e
        if not is_empty(elves, e, DIRS8):
            move_count += 1
            for i in range(len(PROPOSED_DIRS)):
                dirs = PROPOSED_DIRS[(r + i) % len(PROPOSED_DIRS)]
                if is_empty(elves, e, dirs):
                    dest = add(e, dirs[0])
                    break
        moves.append((e, dest))
    counter = Counter([m[1] for m in moves])
    new_elves = set()
    for m in moves:
        e2 = m[1] if counter[m[1]] <= 1 else m[0]
        assert e2 not in new_elves
        new_elves.add(e2)
    assert len(elves) == len(new_elves)
    return move_count, new_elves


for r in range(100000000):
    move_count, elves = perform_round(elves, r)
    if r == 9:
        print("Part 1:", calc_empty(elves))
    if move_count == 0:
        print("Part 2:", r + 1)
        break
