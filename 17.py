from typing import List, NamedTuple, Tuple
from unittest.util import _MAX_LENGTH

W = 7
Rock = NamedTuple("Rock", [("width", int), ("bitmap", List[int])])
Pos = NamedTuple("Pos", [("x", int), ("y", int)])

ROCKS = [Rock(4, [15]), Rock(3, [2, 7, 2]), Rock(3, [7, 4, 4]), Rock(1, [1, 1, 1, 1]), Rock(2, [3, 3])]
MAX_LEN = 500


class Chamber:
    def __init__(self, jet: str) -> None:
        self.jet = jet
        self.chamber: List[int] = []  # list of bitmaps
        self.jet_index: int = 0
        self.rock_index: int = 0
        self.clipped: int = 0

    def drop_next_rock(self) -> None:
        pos: Pos = Pos(2, 3 + len(self.chamber))
        rock = ROCKS[self.rock_index]
        self.rock_index = (self.rock_index + 1) % len(ROCKS)
        while True:
            # Jet push
            dir: int = 1 if self.jet[self.jet_index] == ">" else -1
            self.jet_index = (self.jet_index + 1) % len(self.jet)
            if pos.x + dir >= 0 and pos.x + dir + rock.width <= W:
                next_pos = Pos(pos.x + dir, pos.y)
                if self._fits(next_pos, rock):
                    pos = next_pos
            # Fall 1 down
            next_pos = Pos(pos.x, pos.y - 1)
            if self._fits(next_pos, rock):
                pos = next_pos
            else:
                self._drop(pos, rock)
                return

    def clip(self) -> None:
        """Keeps the chamber small"""
        l = len(self.chamber)
        if l > MAX_LEN:
            self.clipped += l - MAX_LEN
            self.chamber = self.chamber[-MAX_LEN:]

    def height(self) -> int:
        return len(self.chamber) + self.clipped

    def _fits(self, pos: Pos, rock: Rock) -> bool:
        if pos.y < 0:
            return False
        for y in range(len(rock.bitmap)):
            if pos.y + y >= len(self.chamber):
                return True
            if self.chamber[pos.y + y] & (rock.bitmap[y] << pos.x) != 0:
                return False
        return True

    def _drop(self, pos: Pos, rock: Rock) -> None:
        for y in range(len(rock.bitmap)):
            if pos.y + y >= len(self.chamber):
                self.chamber.append(0)
            self.chamber[pos.y + y] += rock.bitmap[y] << pos.x

    def draw(self):
        for y in range(len(self.chamber) - 1, len(self.chamber) - 10, -1):
            print("{:07b}".format(self.chamber[y])[::-1].replace("0", "."))
        print("Height:", self.height())


jet = open("17_input.txt", "r").read().strip()


def part1():
    chamber = Chamber(jet)
    for _ in range(2022):
        chamber.drop_next_rock()
    print("Part 1:", chamber.height())


def part2():
    N = 1000000000000

    chamber = Chamber(jet)
    key0 = None
    height0 = 0
    period0 = len(jet) * len(ROCKS)
    for i in range(N):
        for _ in range(period0):
            chamber.drop_next_rock()
        chamber.clip()
        curr_height = chamber.height()
        key = tuple(chamber.chamber[-1 - a] for a in range(30))
        print("Iteration", i, " -> ", period0 * (i + 1), "rocks, height:", chamber.height())
        if i == 0:
            key0 = key
            height0 = curr_height
        elif key == key0:
            print("Periodicity found! height0:", height0, "curr height", curr_height)
            height_delta = curr_height - height0
            rounds_left = (N - period0) % (i * period0)
            big_periods_left = (N - period0) // (i * period0) - 1
            print("Left rounds: ", rounds_left)
            for _ in range(rounds_left):
                chamber.drop_next_rock()
                chamber.clip()
            chamber.draw()
            print("Part 2:", chamber.height() + big_periods_left * height_delta)
            break


part1()
part2()
