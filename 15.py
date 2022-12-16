data = open("15_input.txt", "r").read().splitlines()

min_x = 0
min_y = 0
max_x = 0
max_y = 0
row_nr = 2000000
row = []


def dist(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)


def fill_ix(x, v):
    row[x - min_x] = v


def fill(x, y, dist):
    if abs(y - row_nr) > dist:
        return
    for i in range(min_x, max_x + 1):
        d = abs(x - i) + abs(y - row_nr)
        if d <= dist:
            fill_ix(i, 1)


def x_range(x, y, dist, row):
    dx = dist - abs(y - row)
    if dx < 0:
        return (0, 0)
    return (x - dx, x + dx + 1)


# Read input
sensors = []
for line in data:
    v = line.split("=")
    x = int(v[1].split(",")[0])
    y = int(v[2].split(":")[0])
    bx = int(v[3].split(",")[0])
    by = int(v[4])
    d = dist(x, y, bx, by)
    max_x = max(max_x, x + d)
    max_y = max(max_y, y + d)
    min_x = min(min_x, x - d)
    min_y = min(min_y, y - d)
    sensors.append([x, y, bx, by, d])

# Part 1: fill row with all sensors' ranges
row = (1 + max_x - min_x) * [0]
for (x, y, _, _, d) in sensors:
    fill(x, y, d)
# Substract all known beacons
for (_, _, bx, by, _) in sensors:
    if by == row_nr:
        fill_ix(bx, 0)
print("Part 1:", sum(row))

# Part 2
n = 4000000
found = False

for row in range(n + 1):
    if found:
        break
    col = 0
    while col <= n:
        next_col = col
        for (x, y, _, _, d) in sensors:
            r = x_range(x, y, d, row)
            if r == (0, 0) or r[0] > col or r[1] <= col:
                continue
            # Jump x (hopefully a lot) to next x that is not in this sensor's range
            next_col = r[1]
            break
        if col == next_col:
            print("FOUND at x=", col, "y=", row)
            print("Part 2:", col * n + row)
            found = True
            break
        else:
            col = next_col
