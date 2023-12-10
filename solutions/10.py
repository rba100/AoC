import math

class Symbol:
    def __init__(self, symbol, isPipe, connectsEast=False, connectsWest=False, connectsNorth=False, connectsSouth=False, isStart=False):
        self.symbol = symbol
        self.isPipe = isPipe
        self.connectsEast = connectsEast
        self.connectsWest = connectsWest
        self.connectsNorth = connectsNorth
        self.connectsSouth = connectsSouth
        self.isStart = isStart

        self.claimed = False
        self.x = None
        self.y = None
    
    def copy(self, x , y):
        s = Symbol(self.symbol, self.isPipe, self.connectsEast, self.connectsWest, self.connectsNorth, self.connectsSouth, self.isStart)
        s.x = x
        s.y = y
        return s
    
    def __str__(self):
        return self.symbol
    def __repr__(self) -> str:
        return self.symbol

symbols = {
    "|"  : Symbol("|", True, connectsNorth=True, connectsSouth=True),
    "-"  : Symbol("-", True, connectsEast=True, connectsWest=True),
    "L"  : Symbol("L", True, connectsNorth=True, connectsEast=True),
    "J"  : Symbol("J", True, connectsNorth=True, connectsWest=True),
    "7"  : Symbol("7", True, connectsSouth=True, connectsWest=True),
    "F"  : Symbol("F", True, connectsSouth=True, connectsEast=True),
    "."  : Symbol(".", False),
    "S"  : Symbol("S", True, isStart=True, connectsEast=True, connectsWest=True, connectsNorth=True, connectsSouth=True),
}

class Pipe:
    def __init__(self, parts, containsAnimal=False):
        self.parts = parts.copy()
        self.containsAnimal = containsAnimal

    def maxSteps(self):
        return math.ceil(len(self.parts)/2)

def GetNextPoint(map, x, y, maxX, maxY):
    current = map[y][x]
    if(current.isPipe == False):
        raise Exception("Tried to navigate dry ground")
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

def GetPipe(map, x, y, maxX, maxY):
    containsAnimal = False
    segments = []
    currentSegment = map[y][x]
    start = currentSegment
    
    currentSegment.claimed = True
    if(currentSegment.isStart):
        containsAnimal = True
    segments.append(currentSegment)
    next = GetNextPoint(map, x, y, maxX, maxY)

    while(next != None and next != start):        
        next.claimed = True
        if(next.isStart):
            containsAnimal = True
        segments.append(next)
        currentSegment = next
        next = GetNextPoint(map, currentSegment.x, currentSegment.y, maxX, maxY)

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
    print("No animal found")
else:
    print(pipeWithAnimal.maxSteps())

#for pipe in pipes: print(pipe.parts)