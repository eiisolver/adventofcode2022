class Elem:
    def __init__(self, v) -> None:
        self.value = v
        self.prev = self
        self.next = self

    def move(self, steps):
        self.next.prev = self.prev
        self.prev.next = self.next
        e = self.next
        for _ in range(steps):
            e = e.next
        self.next = e
        self.prev = e.prev
        e.prev = self
        self.prev.next = self

    def to_list(self):
        result = []
        e = self
        while True:
            result.append(e.value)
            e = e.next
            if e == self:
                break
        return result


data = open("20_input.txt", "r").read().splitlines()
nrs = [*map(int, data)]


def init(nrs):
    elems = [Elem(v) for v in nrs]
    for ix, e in enumerate(elems):
        e.next = elems[(ix + 1) % len(elems)]
        e.prev = elems[ix - 1]
    return elems


def sum3(elems):
    lst = elems[0].to_list()
    ix = lst.index(0)
    return sum(lst[(ix + a) % len(lst)] for a in (1000, 2000, 3000))


def part1():
    elems = init(nrs)
    for e in elems:
        e.move(e.value % (len(elems) - 1))
    print("Part 1:", sum3(elems))


def part2():
    elems = init(nrs)
    F = 811589153
    for e in elems:
        e.value *= F
    for _ in range(10):
        for e in elems:
            e.move(e.value % (len(elems) - 1))
    print("Part 2:", sum3(elems))


part1()
part2()
