directions = []

with open("./2015/3.txt") as f:
    for line in f:
        for c in line.strip():
            directions.append(c)

houses = {}
startingHouse = (0, 0)
def visitHouse(house):
    if house in houses:
        houses[house] += 1
    else:
        houses[house] = 1


def part1():
    currentHouse = startingHouse
    visitHouse(currentHouse)
    for direction in directions:
        if direction == "^":
            currentHouse = (currentHouse[0], currentHouse[1] + 1)
        elif direction == "v":
            currentHouse = (currentHouse[0], currentHouse[1] - 1)
        elif direction == ">":
            currentHouse = (currentHouse[0] + 1, currentHouse[1])
        elif direction == "<":
            currentHouse = (currentHouse[0] - 1, currentHouse[1])
        visitHouse(currentHouse)
    print(len(houses))

def part2():
    santaHouse = startingHouse
    robotHouse = startingHouse
    visitHouse(santaHouse)
    visitHouse(robotHouse)
    for i in range(len(directions)):
        direction = directions[i]
        if i % 2 == 0:
            if direction == "^":
                santaHouse = (santaHouse[0], santaHouse[1] + 1)
            elif direction == "v":
                santaHouse = (santaHouse[0], santaHouse[1] - 1)
            elif direction == ">":
                santaHouse = (santaHouse[0] + 1, santaHouse[1])
            elif direction == "<":
                santaHouse = (santaHouse[0] - 1, santaHouse[1])
            visitHouse(santaHouse)
        else:
            if direction == "^":
                robotHouse = (robotHouse[0], robotHouse[1] + 1)
            elif direction == "v":
                robotHouse = (robotHouse[0], robotHouse[1] - 1)
            elif direction == ">":
                robotHouse = (robotHouse[0] + 1, robotHouse[1])
            elif direction == "<":
                robotHouse = (robotHouse[0] - 1, robotHouse[1])
            visitHouse(robotHouse)
    print(len(houses))

part1()
houses = {}
part2()