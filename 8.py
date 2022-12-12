import itertools
import numpy as np

data = open("8_input.txt", "r").read().splitlines()
w = len(data[0])
h = len(data)


def part1():
    visible = [[False] * w for _ in range(h)]
    for x in range(w):
        for y in range(h):
            visible[y][x] = False
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                vis = True
                for n in range(1, w * h):
                    a = x + n * dx
                    b = y + n * dy
                    if 0 <= a < w and 0 <= b < h:
                        if data[y][x] <= data[b][a]:
                            vis = False
                            break
                    else:
                        break
                if vis:
                    visible[y][x] = True
                    break
    return np.sum(visible)


def part2():
    max_score = 0
    for x in range(w):
        for y in range(h):
            score = 1
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                vis = 0
                for n in range(1, w * h):
                    a = x + n * dx
                    b = y + n * dy
                    if 0 <= a < w and 0 <= b < h:
                        vis += 1
                        if data[y][x] <= data[b][a]:
                            break
                    else:
                        break
                score *= vis
            max_score = max(score, max_score)
    return max_score


print("Part 1:", part1())
print("Part 2:", part2())
