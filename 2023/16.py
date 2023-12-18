RIGHT = 0x1
LEFT = 0x2
UP = 0x4
DOWN = 0x8

class Tile:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        # 0x1 = right, 0x2 = left, 0x4 = up, 0x8 = down
        self.energy = 0

    def isEngergised(self):
        return self.energy != 0

    def __str__(self):
        return f"{self.x},{self.y} {self.type}"

class Contraption:
    def __init__(self, input: str):
        self.tiles: [Tile] = []
        self.processInput(input)
        self.width = len(input.split("\n")[0])
        self.height = len(input.split("\n"))

    def reset(self):
        for t in self.tiles:
            t.energy = 0

    def processInput(self, input: str):
        lines = input.split("\n")
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                self.tiles.append(Tile(x, y, c))

    def sumEnergised(self):
        return sum([1 for t in self.tiles if t.isEngergised()])

    def __getitem__(self, key):
        if isinstance(key, tuple):            
            x, y = key
            offset = y * self.height + x
            return self.tiles[offset]
        raise Exception("Invalid key type")
    
    def beamTrace(self, x, y, direction):
        while(not (x < 0 or x >= self.width or y < 0 or y >= self.height)):
            tile = self[x, y]
            if(tile.energy & direction != 0):
                return
            tile.energy |= direction

            if(tile.type == "-" and direction in [UP, DOWN]):
                self.beamTrace(x-1, y, LEFT)
                self.beamTrace(x+1, y, RIGHT)
                return
            
            if(tile.type == "|" and direction in [LEFT, RIGHT]):
                self.beamTrace(x, y-1, UP)
                self.beamTrace(x, y+1, DOWN)
                return
            
            if(tile.type == "/"):
                if(direction == UP):
                    x += 1
                    direction = RIGHT
                    continue
                if(direction == DOWN):
                    x -= 1
                    direction = LEFT
                    continue
                if(direction == LEFT):
                    y += 1
                    direction = DOWN
                    continue
                if(direction == RIGHT):
                    y -= 1
                    direction = UP
                    continue

            if(tile.type == "\\"):
                if(direction == UP):
                    x -= 1
                    direction = LEFT
                    continue
                if(direction == DOWN):
                    x += 1
                    direction = RIGHT
                    continue
                if(direction == LEFT):
                    y -= 1
                    direction = UP
                    continue
                if(direction == RIGHT):
                    y += 1
                    direction = DOWN
                    continue
            
            if(direction == UP):
                y -= 1
                continue
            if(direction == DOWN):
                y += 1
                continue
            if(direction == LEFT):
                x -= 1
                continue
            if(direction == RIGHT):
                x += 1
                continue

contraption = None
with open("./2023/16.txt", "r") as file:
    input = file.read()
    contraption = Contraption(input)

# Part 1
contraption.beamTrace(0, 0, RIGHT)
print(contraption.sumEnergised())

# Part 2
contraption.reset()
maxEnergised = 0
BestX = 0
BestY = 0
BestDirection = 0

# RIGHT
for x in [0, contraption.width-1]:
    for y in range(0, contraption.height):
            direction = RIGHT if x == 0 else LEFT
            contraption.beamTrace(0, y, direction)
            energised = contraption.sumEnergised()
            if(energised > maxEnergised):
                maxEnergised = energised
                BestX = x
                BestY = y
                BestDirection = direction
            contraption.reset()

for y in [0, contraption.height-1]:
    for x in range(0, contraption.width):
            direction = DOWN if y == 0 else UP
            contraption.beamTrace(x, 0, direction)
            energised = contraption.sumEnergised()
            if(energised > maxEnergised):
                maxEnergised = energised
                BestX = x
                BestY = y
                BestDirection = direction
            contraption.reset()

print(f"Best: {BestX},{BestY} {BestDirection}: {maxEnergised}")