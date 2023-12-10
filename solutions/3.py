def isSymbol(symbol):
    if symbol.isdigit():
        return False
    if symbol == ".":
        return False
    return True

with open("3.txt", "r") as file:
    lines = file.readlines()
    blankLine = "." * len(lines[0])
    lines.insert(0, blankLine)
    lines.append(blankLine)

    numbers = []
    symbolPoints = []

    # extract coordinates of all symbols
    for i in range(1, len(lines) - 1):
        line = lines[i]
        for j in range(0, len(line) - 1):
            if(isSymbol(line[j])):
                symbolPoints.append((j, i))

    def isNearSymbol(number, i, j):
        left = j - len(number)
        right = j - 1
        for symbolPoint in symbolPoints:
            if((abs(symbolPoint[1]- i)) <= 1 and ((left - 1) <= symbolPoint[0] <= (right + 1))):
                return True
        return False

    # extract all numbers
    for i in range(1, len(lines) - 1):
        line = lines[i]
        currentPartalNumber = ""
        for j in range(0, len(line) - 1):
            if(line[j].isdigit()):
               currentPartalNumber += line[j]
            elif (currentPartalNumber != ""):
                if(isNearSymbol(currentPartalNumber, i, j)):
                    numbers.append(int(currentPartalNumber))
                currentPartalNumber = ""
        if(currentPartalNumber != ""):
            if(isNearSymbol(currentPartalNumber, i, j)):
                    numbers.append(int(currentPartalNumber))
            currentPartalNumber = ""

    print(sum(numbers))



