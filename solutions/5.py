
class RangeDef:
    def __init__(self, line):
        parts = line.split(' ')

        self.destinationRangeStart = int(parts[0])
        self.sourceRangeStart = int(parts[1])
        self.length = int(parts[2])

    def getMappedValue(self, source):
        if(source >= self.sourceRangeStart and source < self.sourceRangeStart + self.length):
            return self.destinationRangeStart + (source - self.sourceRangeStart)
        else:
            return None
        
class DataMap:
    def __init__(self, lines):
        headerLine = lines[0].split(' ')[0]
        self.source = headerLine.split('-')[0]
        self.destination  = headerLine.split('-')[2]
        self.rangeDefs = [RangeDef(line) for line in lines[1:] if line.strip() != '']

with open("5.txt", "r") as file:
    lines = file.readlines()
    seedIds = [int(n.strip()) for n in lines[0].split(':')[1].split(' ') if n.strip() != '']
    lowestLocation = None
    seeds = []
    maps = []
    currentLines = []

    for i in range(2, len(lines)):
        if(lines[i].strip() == ''):
            maps.append(DataMap(currentLines))
            currentLines = []
        else:
            currentLines.append(lines[i])
        
    if len(currentLines) > 0:
        maps.append(DataMap(currentLines))
    
    for seedId in seedIds:
        seed = {"seed": seedId}
        seeds.append(seed)
        key = "seed"
        currentMap = None
        currentId = seedId
        while(key != "location"):
            currentMap = [m for m in maps if m.source == key][0]
            for rangeDef in currentMap.rangeDefs:
                mappedValue = rangeDef.getMappedValue(currentId)
                if(mappedValue != None):
                    currentId = mappedValue
                    break;
            key = currentMap.destination
            seed[key] = currentId

        if(lowestLocation == None or currentId < lowestLocation):
            lowestLocation = currentId

    print(lowestLocation)    