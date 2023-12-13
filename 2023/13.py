inputs = []

with open("./2023/13.txt", "r") as file:
    currentBatch = []
    for line in file:
        l = line.strip()
        if(l == ''):
            inputs.append(currentBatch)
            currentBatch = []
        else:
            currentBatch.append(l)
    if(len(currentBatch) > 0):
        inputs.append(currentBatch)

def rotate(frame: [str]) -> [str]:
    return ["".join([frame[j][i] for j in range(len(frame)-1,-1,-1)]) for i in range(len(frame[0]))]

def getReflectionsWithSmudge(frame: [str]) -> (int,int):
    vf = rotate(frame)
    v = getReflectionWithSmudgeH(vf)
    h = getReflectionWithSmudgeH(frame)
    if(not v == None and not h == None):
        for l in frame:
            print(l)
        raise Exception("ERROR: Both reflections found: " + str(v) + " " + str(h))
    if(not v == None): return v, 0
    if (not h == None): return 0, h
    for l in frame:
        print(l)
    raise Exception("ERROR: No reflection found")

def getReflectionWithSmudgeH(frame: [str]) -> int | None:
    for i in range(0, len(frame) - 1):
        accumulatedDifferences = 0
        for offset in range(0, len(frame)):
            a = i - offset
            b = i + offset + 1
            if(a<0 or b>=len(frame)): break
            for j in range(0, len(frame[0])):
                if(frame[a][j] != frame[b][j]):
                    accumulatedDifferences += 1
            if(accumulatedDifferences>1):
                break
        if(accumulatedDifferences == 1): return i + 1
    return None

def getReflectionIndex(frame: [str]) -> (int,int):    
    vf = rotate(frame)
    v = getReflectionIndexH(vf)
    h = getReflectionIndexH(frame)
    if(not v == None and not h == None):
        for l in frame:
            print(l)
        raise Exception("ERROR: Both reflections found: " + str(v) + " " + str(h))
    if(not v == None): return v, 0
    if (not h == None): return 0, h
    for l in frame:
        print(l)
    raise Exception("ERROR: No reflection found")


def getReflectionIndexH(frame: [str]) -> int | None:
    for i in range(0, len(frame) - 1):
        failed = False
        for offset in range(0, len(frame)):
            a = i-offset
            b = i + offset + 1
            if(a<0 or b>=len(frame)): break
            if(frame[a] != frame[b]):
                failed = True
                break
        if(not failed): return i + 1
    return None

part1Results = []
for frame in inputs:
    r = getReflectionIndex(frame)
    part1Results.append(r)

part1 = sum([v + 100*h for v,h in part1Results])
print(f"Part 1: {part1}")

part2Results = []
for frame in inputs:
    r = getReflectionsWithSmudge(frame)
    check = getReflectionIndex(frame)
    if(r == check):
        raise Exception("ERROR: Failed to find a different reflection")
    part2Results.append(r)
part2 = sum([v + 100*h for v,h in part2Results])
print(f"Part 2: {part2}")