presents = []
with open("./2015/2.txt") as f:
    for line in f:
        presents.append(line.strip().split("x"))

def getWrappingPaper(present):
    l = int(present[0])
    w = int(present[1])
    h = int(present[2])
    lw = l * w
    wh = w * h
    hl = h * l
    return 2 * (lw + wh + hl) + min(lw, wh, hl)

def getRibbon(present):
    l = int(present[0])
    w = int(present[1])
    h = int(present[2])
    lw = l * w
    wh = w * h
    hl = h * l
    return min(2 * (l + w), 2 * (w + h), 2 * (h + l)) + (l * w * h)

print(sum([getWrappingPaper(present) for present in presents]))
print(sum([getRibbon(present) for present in presents]))