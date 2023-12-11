class EnginePartCode:
    def __init__(self, number, i, jLeft, jRight):
        self.number = number
        self.i = i
        self.jLeft = jLeft
        self.jRight = jRight

    def __str__(self):
        return "number: " + str(self.number) + ", i: " + str(self.i) + ", jLeft: " + str(self.jLeft) + ", jRight: " + str(self.jRight)

    def __repr__(self):
        return self.__str__()


def isGear(symbol):
    return symbol == "*"

with open("3.txt", "r") as file:
    lines = file.readlines()
    blankLine = "." * len(lines[0])
    lines.insert(0, blankLine)
    lines.append(blankLine)

    numbers = []
    possibleGears = []

    # extract coordinates of all symbols
    for i in range(1, len(lines) - 1):
        line = lines[i]
        for j in range(0, len(line) - 1):
            if(isGear(line[j])):
                possibleGears.append((j, i))

    # extract all numbers
    for i in range(1, len(lines) - 1):
        line = lines[i]
        currentPartalNumber = ""
        for j in range(0, len(line) - 1):
            if(line[j].isdigit()):
               currentPartalNumber += line[j]
            elif (currentPartalNumber != ""):
                left = j - len(currentPartalNumber)
                right = j - 1
                numbers.append(EnginePartCode(int(currentPartalNumber), i, left, right))
                currentPartalNumber = ""
        if(currentPartalNumber != ""):
            left = j - len(currentPartalNumber)
            right = j - 1
            numbers.append(EnginePartCode(int(currentPartalNumber), i, left, right))
            currentPartalNumber = ""

    validGearNumbers = []

    for gear in possibleGears:
        nearbyNumbers = []
        for number in numbers:
            if(abs(number.i - gear[1]) <= 1):
                if(number.jLeft - 1 <= gear[0] <= number.jRight + 1):
                    nearbyNumbers.append(number)
        if(len(nearbyNumbers) == 2):
            validGearNumbers.append(nearbyNumbers[0].number * nearbyNumbers[1].number)


    print(sum(validGearNumbers))

