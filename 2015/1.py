line = None
with open("./2015/1.txt") as f:
    line = f.readline()
floorMaps = {}
count = 0
for i, c in enumerate(line):
    if c == "(":
        count += 1
    elif c == ")":
        count -= 1
    if count not in floorMaps:
        floorMaps[count] = i+1

print(count)
for k, v in floorMaps.items():
    if k == -1:
        print(v)
        break