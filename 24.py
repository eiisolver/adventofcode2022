import math

data = open("24_input.txt", "r").read().splitlines()

N = (0, -1)
E = (1, 0)
S = (0, 1)
W = (-1, 0)
DIRS = [N, E, S, W, (0, 0)]

h = len(data) - 2
w = len(data[0]) - 2
nr_states = (w * h) // math.gcd(w, h)
start = (0, -1)
end = (w - 1, h)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def init():
    """Pre-calculates available empty squares at each minute"""
    bliz_per_dir = [set() for _ in range(4)]  # N/E/S/W blizzards
    all_coords = set((x, y) for x in range(w) for y in range(h))
    for y in range(h):
        for x in range(w):
            dir = "^>v<.".index(data[y + 1][x + 1])
            if dir < 4:
                bliz_per_dir[dir].add((x, y))
    free_coords = [set() for _ in range(nr_states)]
    for s in range(nr_states):
        free_coords[s] = all_coords.copy()
        free_coords[s].add(start)
        free_coords[s].add(end)
        nxt_bliz = []
        for d in range(4):
            free_coords[s] -= bliz_per_dir[d]
            nxt = set()
            for c in bliz_per_dir[d]:
                nxt_c = ((c[0] + DIRS[d][0]) % w, (c[1] + DIRS[d][1]) % h)
                nxt.add(nxt_c)
            nxt_bliz.append(nxt)
        bliz_per_dir = nxt_bliz
    return free_coords


free_coords = init()
# Perform BFS
states = {start}
goals = 0
for r in range(100000000):
    nxt = set()
    curr_empty = free_coords[r % nr_states]
    for s in states:
        for d in DIRS:
            s2 = add(s, d)
            if s2 in curr_empty:
                nxt.add(s2)
        if s == start or s == end:
            nxt.add(s)
    states = nxt
    if end in states:
        if goals == 0:
            print("Part 1:", r)
            goals += 1
            states = {end}
        elif goals == 2:
            print("Part 2:", r)
            break
    if (start in states) and goals == 1:
        print("Back to start!")
        states = {start}
        goals += 1
