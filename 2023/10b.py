import math
import time
from colorama import Fore, Back, Style

start_time = time.time()

def debug(stng):
    debug = False
    if(debug): print(stng)

class Symbol:
    def __init__(self, symbol, isPipe, connectsEast=False, connectsWest=False, connectsNorth=False, connectsSouth=False, isStart=False, unicodePipeSymbol=None):
        self.symbol = symbol
        self.isPipe = isPipe
        self.connectsEast = connectsEast
        self.connectsWest = connectsWest
        self.connectsNorth = connectsNorth
        self.connectsSouth = connectsSouth
        self.isStart = isStart
        self.direction = "?"
        self.unicodePipeSymbol = unicodePipeSymbol if unicodePipeSymbol != None else symbol

        self.claimed = False
        self.enclosed = None
        self.x = None
        self.y = None
    
    def copy(self, x , y):
        s = Symbol(self.symbol, self.isPipe, self.connectsEast, self.connectsWest, self.connectsNorth, self.connectsSouth, self.isStart, self.unicodePipeSymbol)
        s.x = x
        s.y = y
        s.coords = (x, y)
        return s
    
    def __str__(self):
        return self.symbol
    def __repr__(self) -> str:
        return self.symbol

symbols = {
    "|"  : Symbol("|", isPipe=True, connectsNorth=True, connectsSouth=True, unicodePipeSymbol="│"),
    "-"  : Symbol("-", isPipe=True, connectsEast=True,  connectsWest=True,  unicodePipeSymbol="─"),
    "L"  : Symbol("L", isPipe=True, connectsNorth=True, connectsEast=True,  unicodePipeSymbol="└"),
    "J"  : Symbol("J", isPipe=True, connectsNorth=True, connectsWest=True,  unicodePipeSymbol="┘"),
    "7"  : Symbol("7", isPipe=True, connectsSouth=True, connectsWest=True,  unicodePipeSymbol="┐"),
    "F"  : Symbol("F", isPipe=True, connectsSouth=True, connectsEast=True,  unicodePipeSymbol="┌"),
    "."  : Symbol(".", isPipe=False),
    "S"  : Symbol("S", isPipe=True, isStart=True, connectsEast=True, connectsWest=True, connectsNorth=True, connectsSouth=True),
}

class Pipe:
    def __init__(self, parts, containsAnimal):
        self.parts = parts.copy()
        self.containsAnimal = containsAnimal

    def maxSteps(self):
        return math.ceil(len(self.parts)/2)
    
    def markEnclosed(self, map, maxX, maxY):
        if(not any([p for p in self.parts if p.isStart])):
            return None
        
        rightHandCount = 0
        rightHandCells = set()
        leftHandCells = set()
        
        # get an ordering with S at the end
        startIndex = self.parts.index([p for p in self.parts if p.isStart][0]) + 1
        if(startIndex >= len(self.parts)):
            startIndex = 0
        path = self.parts[startIndex:] + self.parts[:startIndex]

        # check if the path is left or right handed by counting turns
        dir = GetInitialDirection(path[0], path[1])

        for i in range(0, len(path) - 1):
            current = path[i]
            next = path[i+1]
            
            if(dir == "N"):
                rightHandCells.add((current.x+1, current.y))
                rightHandCells.add((current.x+1, current.y-1))
                leftHandCells.add((current.x-1, current.y))
                leftHandCells.add((current.x-1, current.y-1))
                if(next.connectsEast):
                    rightHandCount += 1
                    dir = "E"
                elif(next.connectsWest):
                    rightHandCount -= 1
                    dir = "W"
            elif(dir == "S"):
                rightHandCells.add((current.x-1, current.y))
                rightHandCells.add((current.x-1, current.y+1))
                leftHandCells.add((current.x+1, current.y))
                leftHandCells.add((current.x+1, current.y+1))
                if(next.connectsEast):
                    rightHandCount -= 1
                    dir = "E"
                elif(next.connectsWest):
                    rightHandCount += 1
                    dir = "W"
            elif(dir == "E"):
                rightHandCells.add((current.x, current.y+1))
                rightHandCells.add((current.x+1, current.y+1))
                leftHandCells.add((current.x, current.y-1))
                leftHandCells.add((current.x+1, current.y-1))
                if(next.connectsNorth):
                    rightHandCount -= 1
                    dir = "N"
                elif(next.connectsSouth):
                    rightHandCount += 1
                    dir = "S"
            elif(dir == "W"):
                rightHandCells.add((current.x, current.y-1))
                rightHandCells.add((current.x-1, current.y-1))
                leftHandCells.add((current.x, current.y+1))
                leftHandCells.add((current.x-1, current.y+1))
                if(next.connectsNorth):
                    rightHandCount += 1
                    dir = "N"
                elif(next.connectsSouth):
                    rightHandCount -= 1
                    dir = "S"
        
        # assertion - check that we've got 4 or -4 more right turns than left for a complete path with right angle turns.
        #             Bug: because we don't count S the count can be off by one, so ±3:5
        if(abs(rightHandCount) not in [3,4,5]): raise Exception(f"Path is not closed (rightHandCount: {rightHandCount})")
        isRightHanded = rightHandCount > 0

        insideCells = rightHandCells if isRightHanded else leftHandCells
        outsideCells = leftHandCells if isRightHanded else rightHandCells

        # remove cells with coordinates outside the map or are part of the pipe
        pipeCords = set([(p.x, p.y) for p in self.parts])
        insideCells = [cell for cell in insideCells if cell[0] >= 0 and cell[0] < maxX and cell[1] >= 0 and cell[1] < maxY and cell not in pipeCords]
        outsideCells = [cell for cell in outsideCells if cell[0] >= 0 and cell[0] < maxX and cell[1] >= 0 and cell[1] < maxY and cell not in pipeCords]

        # assertion - check that no cells are marked both left and right
        #             After all, the path-following algo is pretty shonky.
        for cell in insideCells:
            if cell in outsideCells:
                raise Exception("Cell is both right and left handed")

        # mark cells as enclosed
        for cell in insideCells:
            map[cell[1]][cell[0]].enclosed = True
        for cell in outsideCells:
            map[cell[1]][cell[0]].enclosed = False

        # iterate over the remaining cells until all are marked by checking with neighbours
        # This could be simplified but I wanted to detect possible errors in previous logic
        remainingCells = [cell for row in map for cell in row if cell.coords not in pipeCords and cell.enclosed == None]
        remainingCellCount = len(remainingCells)
        while(remainingCellCount > 0):
            for cell in remainingCells:
                surroundingCells = []
                if(cell.x+1 < maxX):
                    surroundingCells.append(map[cell.y][cell.x+1])
                if(cell.x-1 >= 0):
                    surroundingCells.append(map[cell.y][cell.x-1])
                if(cell.y+1 < maxY):
                    surroundingCells.append(map[cell.y+1][cell.x])
                if(cell.y-1 >= 0):
                    surroundingCells.append(map[cell.y-1][cell.x])
                closureStates = set([c.enclosed for c in surroundingCells if c.enclosed != None])
                if(True in closureStates and False in closureStates):
                    raise Exception("Cell has conflicting neighbours")
                if(True in closureStates):
                    cell.enclosed = True
                if(False in closureStates):
                    cell.enclosed = False
            remainingCells = [cell for cell in remainingCells if cell.enclosed == None]
            if(len(remainingCells) == remainingCellCount):
                raise Exception(f"No progress made in cell closure, remaining cells: {remainingCellCount}")
            remainingCellCount = len(remainingCells)

        return isRightHanded

def GetNextPoint(map, x, y, maxX, maxY):
    current = map[y][x]
    if(current.isPipe == False):
        raise Exception("Something went wrong, navigated off pipe")
    east = map[y][x+1] if x+1 < maxX and map[y][x+1].claimed == False else None
    west = map[y][x-1] if x-1 >= 0 and map[y][x-1].claimed == False else None
    north = map[y-1][x] if y-1 >= 0 and map[y-1][x].claimed == False else None
    south = map[y+1][x] if y+1 < maxY and map[y+1][x].claimed == False else None

    if(east != None and current.connectsEast and east.connectsWest):
        return east
    if(west != None and current.connectsWest and west.connectsEast):
        return west
    if(north != None and current.connectsNorth and north.connectsSouth):
        return north
    if(south != None and current.connectsSouth and south.connectsNorth):
        return south
    return None

def GetInitialDirection(start, next):
    if(start.x == next.x):
        if(start.y < next.y):
            return "S"
        else:
            return "N"
    if(start.x < next.x):
        return "E"
    else:
        return "W"

def GetPipe(map, x, y, maxX, maxY):
    containsAnimal = False
    segments = []
    currentSegment = map[y][x]
    start = currentSegment

    def followPipe(segment, containsAnimal):
        segment.claimed = True
        if(segment.isStart):
            containsAnimal = True
        segments.append(segment)
        return GetNextPoint(map, segment.x, segment.y, maxX, maxY), containsAnimal
    
    currentSegment, containsAnimal = followPipe(currentSegment, containsAnimal)
    while(currentSegment != None and currentSegment != start):   
        currentSegment, containsAnimal = followPipe(currentSegment, containsAnimal)

    return Pipe(segments, containsAnimal)

lines = []
pipes = []
map = []

with open("10.txt", "r") as file:
    lines = file.readlines()
maxX = len(lines[0]) - 1
maxY = len(lines)

for y in range(maxY):
    mapLine = []
    for x in range(maxX):
        mapLine.append(symbols[lines[y][x]].copy(x, y))
    map.append(mapLine)        

for y in range(maxY):
    for x in range(maxX):
        sym = map[y][x]
        if(sym.isPipe and sym.claimed == False):
            pipes.append(GetPipe(map, x, y, maxX, maxY))

pipeWithAnimal = [pipes[i] for i in range(len(pipes)) if pipes[i].containsAnimal][0]

if(pipeWithAnimal == None):
    raise Exception("No pipe with animal found")    
else:
    pipeWithAnimal.markEnclosed(map, maxX, maxY)
ownPartCoords = set([(p.x, p.y) for p in pipeWithAnimal.parts])

for row in map:
    for cell in row:
        if(cell.enclosed == None):
            if(cell.coords in ownPartCoords):
                if(cell.isStart):
                    print(Fore.WHITE + Back.MAGENTA + "S" + Back.BLACK, end="")
                else:
                    print(Fore.WHITE + cell.unicodePipeSymbol, end="")
            else:
                print(Fore.RED + cell.symbol, end="")
        elif(cell.enclosed):
            print(Fore.LIGHTGREEN_EX + "I", end="")
        else:
            print(Fore.BLUE + "O", end="")
    print(Style.RESET_ALL)

enclosedCells = [cell for row in map for cell in row if cell.enclosed == True]
unenclosedCells = [cell for row in map for cell in row if cell.enclosed == False]
errorCells = [cell for row in map for cell in row if cell.enclosed == None and cell.coords not in ownPartCoords]
print(f"Steps to half way point: {pipeWithAnimal.maxSteps()}")
print(f"Enclosed cells: {len(enclosedCells)}")

print("--- %s seconds ---" % (time.time() - start_time))