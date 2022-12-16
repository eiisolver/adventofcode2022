import numpy as np
from typing import List, NamedTuple, Set

Valve = NamedTuple("Valve", [("name", str), ("rate", int), ("neighbours", List[str])])
State = NamedTuple("State", [("released", int), ("at", List[str]), ("opened", Set[str])])

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


def gen_next_states(s: State, i: int) -> List[State]:
    next_states = []
    v = s.at[i]
    valve = valves[v]
    # Go to neighbour valves without opening current
    for nb in valve.neighbours:
        next_at = s.at[:]
        next_at[i] = nb
        nxt = State(s.released, next_at, s.opened)
        next_states.append(nxt)
    if v not in s.opened and valve.rate > 0:
        # Open current valve
        rel = (T - t) * valve.rate
        nxt = State(s.released + rel, s.at, set(s.opened))
        nxt.opened.add(v)
        next_states.append(nxt)
    return next_states


states = [State(0, ["AA", "AA"], set())]
T = 26
# Perform a beam search
MAX_STATES = 10000
limit = 0  # cutoff limit
for t in range(1, T):
    next_states = []
    for s in states:
        if s.released < limit:
            continue
        # Generate next states using all combinations for me and the elephant
        states1 = gen_next_states(s, 0)
        for s2 in states1:
            next_states.extend(gen_next_states(s2, 1))

    states = next_states
    if len(states) > MAX_STATES:
        # Get the kth largest value and use it as cutoff in next iteration
        p = np.partition([-s.released for s in states], kth=MAX_STATES)
        limit = -p[MAX_STATES]
    print("T", t, ", cutoff limit:", limit, ", nr states:", len(states))


print("Part 2:", max(s.released for s in states))
