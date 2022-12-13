from functools import cmp_to_key


def compare(p1, ix1, p2, ix2):
    """
    Returns 0 if both are equal, 1 if not equal but in right order, -1 if in wrong order
    """
    if ix1 == len(p1):
        return 0 if ix2 == len(p2) else 1
    if ix2 >= len(p2):
        return -1
    a = p1[ix1]
    b = p2[ix2]
    is_list1 = isinstance(a, list)
    is_list2 = isinstance(b, list)
    if not is_list1 and not is_list2:
        # integer comparison
        if a != b:
            return 1 if a < b else -1
        return compare(p1, ix1 + 1, p2, ix2 + 1)
    else:
        # list comparison
        a = [a] if not is_list1 else a
        b = [b] if not is_list2 else b
        result = compare(a, 0, b, 0)
        if result != 0:
            return result
        return compare(p1, ix1 + 1, p2, ix2 + 1)


def compare_packets(p1, p2):
    return compare(p1, 0, p2, 0)


def part1(packets):
    sum = 0
    for i in range(0, len(packets), 2):
        p1 = packets[i]
        p2 = packets[i + 1]
        r = compare_packets(p1, p2)
        if r >= 0:
            sum += i // 2 + 1
    print("Part 1:", sum)


def part2(packets):
    div1 = [[2]]
    div2 = [[6]]
    p = packets[:]
    p.append(div1)
    p.append(div2)
    p.sort(key=cmp_to_key(compare_packets), reverse=True)
    print("Part 2:", (1 + p.index(div1)) * (1 + p.index(div2)))


data = open("13_input.txt", "r").read().splitlines()
packets = [eval(line) for line in data if line]

part1(packets)
part2(packets)
