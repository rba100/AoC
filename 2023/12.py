from functools import cache 
import time

start = time.time()

def parseLine(line: str, isPart2=False) -> (str, [int]):
    parts = line.split(" ")
    pattern = parts[0]
    runs = [int(r) for r in parts[1].split(",")]
    if(isPart2):
        pattern = ((pattern + "?") * 5)[:-1]
        runs = runs * 5
    return (pattern, [int(r) for r in runs])

def getValidOffsets(pattern: str, run: int) -> ([int]):
    validOffsets = []
    for offset in range(len(pattern) - run + 1):
        segment = pattern[offset:offset+run]
        if len([c for c in segment if c == "."]): continue
        beforeSegment = pattern[:offset]
        afterSegment = pattern[offset+run:]
        if "#" in str(beforeSegment): break
        if "#" in str(afterSegment[:1]): continue        
        validOffsets.append(offset)
    return validOffsets

#@cache
def countArrangementsRecursively(pattern: str, runs: [int]):
    validArrangements = 0
    run = runs[0]
    remainingRuns = runs[1:]
    validOffsets = getValidOffsets(pattern, run)
    for offset in validOffsets:
        remainingPattern = pattern[offset+run:][1:]
        if(len(remainingRuns) == 0):
            if not "#" in remainingPattern:
                validArrangements += 1
            continue
        validArrangements += countArrangementsRecursively(remainingPattern, remainingRuns)
    return validArrangements

with open("./2023/12.txt") as file:
    lines = []
    for line in file:
        lines.append(parseLine(line.strip(), True))
    print(sum([countArrangementsRecursively(line[0], tuple(line[1])) for line in lines]))

print("time:", time.time() - start)