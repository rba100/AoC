def getGalaxies(map):
    lastId = 0
    galaxies = []
    for y in range(0, len(map)):
        for x in range(0, len(map[0])):
            if map[y][x] == "#":
                lastId += 1
                galaxies.append(Galaxy(lastId, x, y))
    return galaxies

class Galaxy:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Galaxy(id={self.id}, x={self.x}, y={self.y})"
    def __str__(self):
        return self.__repr__()

class Space:
    def __init__(self, map, expansionCoefficient):
        self.map = map
        blankLine = str.join("", ["."] * len(map[0]))
        self.rowSizes = [expansionCoefficient if line == blankLine else 1 for line in map]
        self.columnSizes = [expansionCoefficient if all([line[i] == "." for line in map]) else 1 for i in range(len(map[0]))]
    
    def sumShortestDistances(self, galaxies):
        distances = []
        for i in range(len(galaxies)):
            for j in range(i + 1, len(galaxies)):
                d = self.distanceBetween(galaxies[i], galaxies[j])
                distances.append(d)
        return sum(distances)

    def distanceBetween(self, a, b):
        lx = min(a.x, b.x)
        hx = max(a.x, b.x)
        ly = min(a.y, b.y)
        hy = max(a.y, b.y)
        colDistances = self.columnSizes[lx:hx]
        rowDistances = self.rowSizes[ly:hy]
        return sum(colDistances) + sum(rowDistances)


map = None
fileName = "11.txt"
with open(fileName, "r") as file:
    map = [line.strip() for line in file.readlines()]

galaxies = getGalaxies(map)

# Part 1
space = Space(map, 2)
print(space.sumShortestDistances(galaxies))
# Part 2
space = Space(map, 1000000)
print(space.sumShortestDistances(galaxies))

