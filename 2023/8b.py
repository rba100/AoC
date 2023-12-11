import re

nodes = {}
directionsLr = ""

with open("8.txt", "r") as file:
    lines = file.readlines()
    directionsLr = lines[0].strip()
    for i in range(2, len(lines)):
        nineChars = re.sub('[^0-9A-Z]', '', lines[i])
        nodes[nineChars[0:3]] = (nineChars[3:6], nineChars[6:9])

directions = [0 if d == "L" else 1 for d in directionsLr]
directionCount = len(directions)

journeyStartPoints = [key for key in nodes if key[2] == "A"]
journeyExitPoints = [key for key in nodes if key[2] == "Z"]

journeyCycles = {}
journeyZTimes = []

print("Steps in loop:" + str(directionCount))

for i in range(0, len(journeyStartPoints)):
    stepCount = 0
    start = journeyStartPoints[i]
    visitedNodes = {}
    visitedNodesFirstTouch = {}
    position = start
    while(True):
        directionIndex = stepCount % directionCount
        position = nodes[position][directions[stepCount % directionCount]]
        stepCount += 1

        if position[2] == "Z":
            if not position in visitedNodes:
                visitedNodes[position] = directionIndex
                visitedNodesFirstTouch[position] = stepCount
            elif visitedNodes[position] == directionIndex:
                journeyCycles[start] = (position, stepCount, stepCount % directionCount, int(stepCount / directionCount), visitedNodesFirstTouch[position])
                break

# cycle data
# for i in range(0, len(journeyStartPoints)):
#     start = journeyStartPoints[i]
#     cycle = journeyCycles[start]
#     print (start, cycle)

def quickStep(initialPosition, target):
    cycleData = journeyCycles[initialPosition]    
    position = initialPosition
    start = 0
    cyclesToSkip = int(target / cycleData[1])
    if(cyclesToSkip > 0):
        start = cycleData[1] * cyclesToSkip 
        position = cycleData[0]

    for i in range(start, target):
        position = nodes[position][directions[i % directionCount]]
    return position

def bruteStep(initialPosition, count):
    position = initialPosition
    for i in range(0, count):
        position = nodes[position][directions[i % directionCount]]
    return position

# lowest common multiple for the cycles are 43848348119

count = 43848348119 * 269 # 11795205644011

for start in journeyStartPoints:
    position = quickStep(start, count)
    print(f"{start} after {count}: {position}")
