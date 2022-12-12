def prio(item):
    c = ord("A") - 26 if "A" <= item <= "Z" else ord("a")
    return 1 + ord(item) - c


lines = open("3_input.txt").read().splitlines()
rucksacks = [(set(line[: len(line) // 2]), set(line[len(line) // 2 :])) for line in lines]
intersects = [r[0].intersection(r[1]) for r in rucksacks]
print("part 1:", sum([prio(x.pop()) for x in intersects]))

groups = [(set(lines[i]), set(lines[i + 1]), set(lines[i + 2])) for i in range(0, len(lines), 3)]
badges = [set.intersection(*g) for g in groups]
print("part 2:", sum(prio(b.pop()) for b in badges))
