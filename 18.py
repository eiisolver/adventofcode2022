data = open("18_input.txt", "r").read().splitlines()
DIRS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]

# Part 1
cubes = set()
for line in data:
    cube = tuple(int(x) for x in line.split(","))
    cubes.add(cube)

area = 0
for c in cubes:
    for d in DIRS:
        if tuple(c[i] + d[i] for i in range(3)) not in cubes:
            area += 1
print("Part 1:", area)

# Part 2
# Calculate all surface air with BFS
size = 1 + max(v for c in cubes for v in c)
surface_air = set()
added = set()
added.add(
    (
        -1,
        -1,
        -1,
    )
)
while added:
    surface_air.update(added)
    new_added = set()
    for c in added:
        for d in DIRS:
            c2 = tuple(c[i] + d[i] for i in range(3))
            if min(x for x in c2) >= -1 and max(x for x in c2) <= size and c2 not in surface_air and c2 not in cubes:
                new_added.add(c2)
    added = new_added

# Calculate cube/surface air intersection
area2 = 0
for c in cubes:
    for d in DIRS:
        c2 = tuple(c[i] + d[i] for i in range(3))
        if c2 in surface_air:
            area2 += 1
print("Part 2:", area2)
