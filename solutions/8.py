import re

nodes = {}
directions = ""

with open("8.txt", "r") as file:
    lines = file.readlines()
    directions = lines[0].strip()
    for i in range(2, len(lines)):
        nineChars = re.sub('[^A-Z]', '', lines[i])
        nodes[nineChars[0:3]] = (nineChars[3:6], nineChars[6:9])

stepCount = 0
currentNode = "AAA"

while(currentNode != "ZZZ"):
    directionIndex = stepCount % len(directions)
    nodeIndex = 0 if directions[directionIndex] == "L" else 1
    nextNode = nodes[currentNode][nodeIndex]
    currentNode = nextNode
    stepCount += 1
    if(stepCount > 1000000000):
        raise Exception("Too many steps")

print(stepCount)