from dataclasses import dataclass
import dataclasses
import math
from typing import List


@dataclass
class Monkey:
    items: List
    op: str
    p1: str
    p2: str
    divide_by: int
    if_true: int
    if_false: int
    inspections: int = 0

    def calc_new(self, old_level: int) -> int:
        par1 = old_level if self.p1 == "old" else int(self.p1)
        par2 = old_level if self.p2 == "old" else int(self.p2)
        return par1 + par2 if self.op == "+" else par1 * par2

    def throws_to(self, level: int):
        return self.if_true if level % self.divide_by == 0 else self.if_false


input = open("11_input.txt", "r").read().splitlines()
monkeys = []
for i in range(0, len(input), 7):
    m = [line.split() for line in input[i : i + 7]]
    items = [int(x.replace(",", "")) for x in m[1][2:]]
    monkey = Monkey(
        items=items,
        op=m[2][-2],
        p1=m[2][-3],
        p2=m[2][-1],
        divide_by=int(m[3][-1]),
        if_true=int(m[4][-1]),
        if_false=int(m[5][-1]),
    )
    monkeys.append(monkey)


def calc_monkey_business(monkeys_orig, rounds, divisor):
    # Make copy of the monkeys
    monkeys = []
    for m in monkeys_orig:
        cpy = dataclasses.replace(m)
        cpy.items = m.items[:]
        monkeys.append(cpy)
    product = math.prod(m.divide_by for m in monkeys)
    for _ in range(rounds):
        for m in monkeys:
            for item in m.items:
                level = (m.calc_new(item) // divisor) % product
                monkeys[m.throws_to(level)].items.append(level)
            m.inspections += len(m.items)
            m.items = []
    inspections = sorted([m.inspections for m in monkeys])
    return inspections[-1] * inspections[-2]


print("Part 1:", calc_monkey_business(monkeys, 20, 3))
print("Part 2:", calc_monkey_business(monkeys, 10000, 1))
