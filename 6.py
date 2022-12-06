data = open("6_input.txt").read()
for n in (4, 14):
    print(min(i for i in range(n, len(data)) if len(set(data[i-n:i])) == n))
