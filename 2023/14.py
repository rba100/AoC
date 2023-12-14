import numpy as np

lines = []

with open("./2023/14.txt", "r") as f:
#with open("./test.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

map = { ".": 0, "O": 1 , "#": 2}
npTable = np.array([[map[c] for c in l] for l in lines])
lineLegnth = len(lines[0])
tableLength = len(lines)

def rotateClockwise2(table: np.array) -> np.array:
    return np.rot90(table, k=1, axes=(1,0))

def getLoad(table: np.array) -> int:
    load = 0
    for row in range(tableLength):
        for col in range(lineLegnth):
            if table[row][col] == 1:
                load += tableLength - row
    return load

def rollUp(table: np.array) -> np.array:
    lineLength = len(table[0])
    rollIndexes = [0 for _ in range(lineLength)]
    for row in range(len(table)):
        line = table[row]
        for col in range(lineLength):
            if line[col] == 0:
                continue
            if line[col] == 1:
                if (rollIndexes[col] == row):
                    rollIndexes[col] = row+1
                else:
                    table[row][col] = 0
                    table[rollIndexes[col]][col] = 1
                    rollIndexes[col] = rollIndexes[col]+1

            else: rollIndexes[col] = row+1
        
    return table

def spinCycle(table: np.array) -> np.array:
    t = table
    for i in range(4):
        t = rollUp(t)
        t = rotateClockwise2(t)
    return t

# part 1
rolled = rollUp(npTable)
load = getLoad(rolled)
print(load)

# part 2
print()
# offset calculations
phase = None
period = None
iterations = 1000000000
npTable = np.array([[map[c] for c in l] for l in lines])
seen = {}
for i in range(iterations):
    npTable = spinCycle(npTable)
    h = hash(npTable.tobytes())
    if h in seen:
        phase = seen[h]
        period = i - phase
        print(f"phase: {phase}, period: {period}")
        break
    seen[h] = i

# fast forward to iteration 1 billion
npTable = np.array([[map[c] for c in l] for l in lines])
remaining = 1000000000 - phase
for i in range(phase + (remaining % period)):
    npTable = spinCycle(npTable)
load = getLoad(npTable)
print(load)