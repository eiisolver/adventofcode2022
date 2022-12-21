from functools import lru_cache
import numpy as np
import re
from typing import NamedTuple

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

Robot = NamedTuple("Robot", [("id", int), ("cost", list[int])])
BluePrint = NamedTuple("BluePrint", [("id", int), ("robots", list[Robot])])
State = NamedTuple("State", [("robots", tuple[int]), ("produced", tuple[int]), ("value", int)])

# Used to look for dominating states, to reduce the search space
class LookupTree:
    def __init__(self) -> None:
        self.lookup = {}
        self.produced_list = []
        self.size = 0

    def add(self, s: State, ix: int = 0):
        self.size += 1
        if ix >= 4:
            self.produced_list.append(s.produced)
        else:
            next = self.lookup.get(s.robots[ix])
            if not next:
                next = LookupTree()
            self.lookup[s.robots[ix]] = next
            next.add(s, ix + 1)

    def contains_dominating_state(self, s: State, ix: int = 0, bigger: bool = False) -> bool:
        """
        Checks if the lookup tree contains a state that dominates the given state
        """
        if ix >= 4:
            for prod in self.produced_list:
                # print("check produced list", prod)
                if all(s.produced[i] <= prod[i] for i in range(4)):
                    if bigger or any(s.produced[i] < prod[i] for i in range(4)):
                        return True
            return False
        for (k, v) in self.lookup.items():
            if k >= s.robots[ix]:
                if v.contains_dominating_state(s, ix + 1, bigger or k > s.robots[ix]):
                    return True
        return False


data = open("19_input.txt", "r").read().splitlines()
bps = dict()  # dict(int -> BluePrint)
for line in data:
    a = [*map(int, re.sub(r"[a-zA-Z\.:]+", r" ", line).strip().split())]
    print(a)
    bp = BluePrint(
        a[0], [Robot(0, [a[1], 0, 0]), Robot(1, [a[2], 0, 0]), Robot(2, [a[3], a[4], 0]), Robot(3, [a[5], 0, a[6]])]
    )
    print(bp)
    bps[bp.id] = bp


def state_value(robots, produced):
    f = [1, 10, 100, 1000]
    return sum(100 * f[i] * robots[i] + 10 * f[i] * produced[i] for i in range(4)) + 10000000 * produced[GEODE]


def can_produce(resources: tuple[int], r: Robot):
    return all(resources[i] >= r.cost[i] for i in range(len(r.cost)))


@lru_cache(maxsize=100000)
def calc_produceable_robots(id: int, resources: tuple[int], max_robot_id: int) -> list[list[int]]:
    result1: list[int] = []
    robots = bps[id].robots
    if can_produce(resources, robots[GEODE]):
        result1.append(GEODE)  # Must produce geode if possible
    elif can_produce(resources, robots[OBSIDIAN]):
        result1.append(OBSIDIAN)  # Otherwise must produce obsidian if possible
    else:
        for r_id in (CLAY, ORE):
            if r_id > max_robot_id:
                continue
            if can_produce(resources, robots[r_id]):
                result1.append(r_id)
    return [[r] for r in result1]


def calc_next_states(bp: BluePrint, s: State, is_last_minute) -> list[State]:
    produceable_robots = calc_produceable_robots(bp.id, s.produced, GEODE)
    produced0 = list(s.produced)
    for i, r in enumerate(s.robots):
        produced0[i] += r
    nxt = []
    if not is_last_minute:  # at last minute there is no need to produce new robots
        for p in produceable_robots:
            produced = list(produced0)
            robots = list(s.robots)
            for r in p:
                robots[r] += 1
                robot = bp.robots[r]
                for i in range(3):
                    produced[i] -= robot.cost[i]
                    if produced[i] < 0:
                        print("ERROR!, state", s, "p:", p, ", produced0:", produced0, ", produced:", produced)
                        raise Exception("Production error")
            nxt.append(State(tuple(robots), tuple(produced), state_value(robots, produced)))
    must_produce = produceable_robots and produceable_robots[0][0] >= OBSIDIAN or len(produceable_robots) > 2
    if is_last_minute or not must_produce:
        # Add next state where no new robots are produced
        nxt.append(State(s.robots, tuple(produced0), state_value(s.robots, produced0)))
    return nxt


def calc_geodes(bp: BluePrint, T: int) -> int:
    states = [State((1, 0, 0, 0), (0, 0, 0, 0), 0)]
    # Perform a beam search
    MAX_STATES = 100000
    limit = 0  # cutoff limit
    for t in range(0, T):
        print("ID: ", bp.id, "T:", t + 1, ", states:", len(states), ", limit:", limit)
        next_states = []
        next_set = set()
        lookup = LookupTree()
        for s in states:
            if s.value < limit:
                continue
            nxt = calc_next_states(bp, s, t == T - 1)
            for s2 in nxt:
                if s2 in next_set:
                    continue
                if lookup.contains_dominating_state(s2):
                    continue
                if lookup.size <= 100000:
                    lookup.add(s2)
                next_set.add(s2)
                next_states.append(s2)

        states = next_states
        if len(states) > MAX_STATES:
            # Get the kth largest value and use it as cutoff in next iteration
            p = np.partition([-s.value for s in states], kth=MAX_STATES)
            limit = -p[MAX_STATES]
        m = max(s.value for s in states)
        for s in states:
            if s.value == m:
                print("  TOP STATE", s, " of", len(states))
                break

        if len(states) < 100000:
            states2 = []
            for s in states:
                dominated = lookup.contains_dominating_state(s)
                if not dominated:
                    states2.append(s)
            states = states2

    m = max(s.produced[GEODE] for s in states)
    for s in states:
        if s.produced[GEODE] == m:
            print("RESULT STATE", s)
            break
    return m


q = 0
for _, bp in bps.items():
    q += bp.id * calc_geodes(bp, 24)
print("Part 1:", q)

prod = 1
for id in (1, 2, 3):
    prod *= calc_geodes(bps[id], 32)
print("Part 2:", prod)
