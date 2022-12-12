games = [(ord(line[0]) - ord("A"), ord(line[2]) - ord("X")) for line in open("2_input.txt", "r")]

part1 = sum(1 + game[1] + [3, 6, 0, 6, 0][game[1] - game[0]] for game in games)
part2 = sum((2 + game[0] + game[1]) % 3 + 1 + 3 * game[1] for game in games)

print("part 1:", part1)
print("part 2:", part2)
