import numpy as np
from typing import List, NamedTuple, Set

Valve = NamedTuple("Valve", [("name", str), ("rate", int), ("neighbours", List[str])])
State = NamedTuple("State", [("released", int), ("at", str), ("opened", Set[str])])

data = open("16_input.txt", "r").read().splitlines()
valves = dict()
for line in data:
    name = line[6:8]
    rate = int(line[line.find("=") + 1 : line.find(";")])
    for s in ("to valves", "to valve"):
        if line.find(s) >= 0:
            nb = line[line.find(s) + len(s) + 1 :].split(", ")
            break
    valves[name] = Valve(name, rate, nb)

states = [State(0, "AA", set())]
T = 30
# Perform a beam search
MAX_STATES = 500
limit = 0  # cutoff limit
for t in range(1, T):
    next_states = []
    for s in states:
        if s.released < limit:
            continue
        valve = valves[s.at]
        # Go to neighbour valves without opening current
        for nb in valve.neighbours:
            nxt = State(s.released, nb, s.opened)
            next_states.append(nxt)
        if s.at not in s.opened and valve.rate > 0:
            # Open current valve
            rel = (T - t) * valve.rate
            nxt = State(s.released + rel, s.at, set(s.opened))
            nxt.opened.add(s.at)
            next_states.append(nxt)

    states = next_states
    if len(states) > MAX_STATES:
        # Get the kth largest value and use it as cutoff in next iteration
        p = np.partition([-s.released for s in states], kth=MAX_STATES)
        limit = -p[MAX_STATES]


print("Part 1:", max(s.released for s in states))
