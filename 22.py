import re
from typing import NamedTuple

Pos = NamedTuple("Pos", [("x", int), ("y", int), ("dir", int)])
# Position on cube, x, y < plane_size, direction: direction on map
CubePos = NamedTuple("CubePos", [("plane", str), ("pos", Pos)])

TEST = False
if TEST:
    f = "22_test_input.txt"
    planes = ["  U", "BLF", "  DR"]
    plane_size = 4
    neighbours = {"U": "R2F0L3B2", "F": "R1D0L0U0", "R": "U2B3D0F3", "B": "L0D2R1U2", "L": "F0D3B0U1", "D": "R0B2L1F0"}
else:
    f = "22_input.txt"
    planes = [" UR", " F", "LD", "B"]
    plane_size = 50
    neighbours = {"U": "R0F0L2B1", "F": "R3D0L3U0", "R": "D2F1U0B0", "B": "D3R0U3L0", "L": "D0B0U2F1", "D": "R2B1L0F0"}

plane_pos = dict()
for y in range(len(planes)):
    for x in range(len(planes[y])):
        plane_pos[planes[y][x]] = Pos(plane_size * x, plane_size * y, 0)

data = open(f, "r").read().splitlines()
b = data[:-2]  # the map
instr_str = data[-1]

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
TURNS = {"R": 1, "L": -1}


def turn(pos: Pos, dir: str) -> Pos:
    """Turns L or R on current pos"""
    return Pos(pos.x, pos.y, (pos.dir + TURNS[dir]) % 4)


def next_pos(pos: Pos) -> Pos:
    """Moves to next position on map"""
    return Pos(pos.x + DIRS[pos.dir][0], pos.y + DIRS[pos.dir][1], pos.dir)


def board_pos(pos: Pos) -> str:
    """Gets content of map at position"""
    if pos.x < 0 or pos.y < 0 or pos.y >= len(b) or pos.x >= len(b[pos.y]):
        return " "
    return b[pos.y][pos.x]


def wrap(pos: Pos) -> Pos:
    """Part1 wrapping"""
    p2 = Pos(pos.x, pos.y, (pos.dir + 2) % 4)
    nxt = next_pos(p2)
    while board_pos(nxt) != " ":
        p2 = nxt
        nxt = next_pos(nxt)
    return Pos(p2.x, p2.y, pos.dir)


def rot90(pos: Pos, n: int):
    result = pos
    for _ in range(n):
        result = Pos(plane_size - 1 - result.y, result.x, (result.dir + 1) % 4)
    return result


def get_plane(pos: Pos) -> str:
    return planes[pos.y // plane_size][pos.x // plane_size]


def cube_pos_to_pos(c: CubePos) -> Pos:
    p0 = plane_pos[c.plane]
    return Pos(p0.x + c.pos.x, p0.y + c.pos.y, c.pos.dir)


def wrap_on_cube(pos: Pos) -> Pos:
    """Part 2 wrapping"""
    curr_plane = get_plane(pos)
    plane = neighbours[curr_plane][2 * pos.dir]
    rotations = int(neighbours[curr_plane][2 * pos.dir + 1])
    pos = next_pos(pos)
    cube_pos = Pos(pos.x % plane_size, pos.y % plane_size, pos.dir)
    cube_pos = rot90(cube_pos, rotations)
    new_c = CubePos(plane, cube_pos)
    r = cube_pos_to_pos(new_c)
    return r


instructions = re.findall("(\d+|[A-Za-z]+)", instr_str)


def part(part, wrap_fn):
    pos = Pos(0, 0, 0)
    while board_pos(pos) == " ":
        pos = next_pos(pos)
    for instr in instructions:
        if instr in ("L", "R"):
            pos = turn(pos, instr)
        else:
            for _ in range(int(instr)):
                nxt = next_pos(pos)
                v = board_pos(nxt)
                if v == " ":
                    nxt = wrap_fn(pos)
                    v = board_pos(nxt)
                if v == "#":
                    break
                pos = nxt
    print(f"Part {part}: {pos} ->", 1000 * (pos.y + 1) + 4 * (pos.x + 1) + pos.dir)


def validate_cube():
    for y in range(len(b)):
        for x in range(len(b[y])):
            if b[y][x] == " ":
                continue
            for d in range(4):
                p = Pos(x, y, d)
                p2 = next_pos(p)
                v = board_pos(p2)
                if v == " ":
                    print("Test ", p)
                    nxt = wrap_on_cube(p)
                    v = board_pos(nxt)
                    t2 = turn(turn(nxt, "L"), "L")
                    p3 = next_pos(t2)
                    v = board_pos(p3)
                    if v != " ":
                        print("ERROR: v:", v, "pos:", p, " -> p2", p2, ", p3:", p3)
                        print(
                            "cube pos p:",
                        )
                        raise Exception("error")
                    p4 = wrap_on_cube(t2)
                    p4_turned = Pos(p4.x, p4.y, (p4.dir + 2) % 4)
                    if p4_turned != p:
                        print(f"ERROR: p: {p}, nxt: {nxt}, p4: {p4}, turned:  {p4_turned}")
                        raise Exception("error")
                    else:
                        print("SUCCESS!!!")


part(1, wrap)
part(2, wrap_on_cube)
