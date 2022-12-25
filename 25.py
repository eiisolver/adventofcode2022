import re

data = open("25_input.txt", "r").read().splitlines()

def from_snafu(x: str) -> int:
    a = int(re.sub("[-=]", "0", x), 5)
    b = int(re.sub("[12]", "0", x).replace("=", "2").replace("-", "1"), 5)
    return a - b

def to_snafu(x: int) -> str:
    d = x % 5
    p = x // 5
    s = "012=-"[d]
    if d >= 3:
        p += 1
    return s if p == 0 else to_snafu(p) + s

print("Part 1:", to_snafu(sum(map(from_snafu, data))))
