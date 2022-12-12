import numpy as np


def calc_t(H, T):
    dist = (H[0] - T[0], H[1] - T[1])
    if max(abs(d) for d in dist) <= 1:
        return T
    return (T[0] + np.sign(dist[0]), T[1] + np.sign(dist[1]))


motions = [(line[0], int(line[2:])) for line in open("9_input.txt", "r").read().splitlines()]
dir_map = {"U": (0, -1), "D": (0, 1), "R": (1, 0), "L": (-1, 0)}


def calc_tail_locations(knots):
    H = [(0, 0) for _ in range(knots)]
    locations = set()
    for dir, count in motions:
        for i in range(count):
            H[0] = (H[0][0] + dir_map[dir][0], H[0][1] + dir_map[dir][1])
            for k in range(1, knots):
                H[k] = calc_t(H[k - 1], H[k])
            locations.add(H[-1])
    return len(locations)


print("Part 1:", calc_tail_locations(2))
print("Part 2:", calc_tail_locations(10))
