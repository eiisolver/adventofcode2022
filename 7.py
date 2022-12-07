class File:
    def __init__(self, sz) -> None:
        self.size = sz
        self.parent = None
        self.files = dict()

    def total_size(self):
        return self.size + sum(f.total_size() for _, f in self.files.items())


lines = open("7_input.txt", "r").read().splitlines()

root = File(0)
curr = root
dirs = []
for line in lines:
    tok = line.split()
    if tok[0] == "$":
        if tok[1] == "ls":
            pass
        elif tok[2] == "/":
            curr = root
        elif tok[2] == "..":
            curr = curr.parent
        else:
            curr = curr.files[tok[2]]
    else:
        if tok[0] == "dir":
            f = File(0)
            dirs.append(f)
        else:
            f = File(int(tok[0]))
        f.parent = curr
        curr.files[tok[1]] = f

print("Part 1:", sum(f.total_size() for f in dirs if f.total_size() <= 100000))
required_size = root.total_size() - (70000000 - 30000000)
print("Part 2:", min(f.total_size() for f in dirs if f.total_size() >= required_size))
