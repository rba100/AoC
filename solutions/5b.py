from typing import List

class IdRangeSet:
    def __init__(self, idRanges: List['IdRange']):
        if not isinstance(idRanges, List):
            raise Exception("Cannot create IdRangeSet from non list")
        for idRange in idRanges:
            if not isinstance(idRange, IdRange):
                type = idRange.__class__.__name__
                raise Exception(f"Cannot create IdRangeSet from list containing non IdRange: {type}")
        self.idRanges = idRanges

    def minValue(self):
        startValues = [idRange.start for idRange in self.idRanges]  
        return min(startValues)

    def getOverlaps(self, otherIdRange):
        if not isinstance(otherIdRange, IdRange):
            raise Exception("Cannot get overlap with non IdRange")
        overlaps = []
        nonOverlaps = []
        for ownIdRange in self.idRanges:
            if ownIdRange.start > otherIdRange.end or ownIdRange.end < otherIdRange.start:
                nonOverlaps.append(ownIdRange)
                continue
            if ownIdRange in otherIdRange:
                overlaps.append(ownIdRange)
                continue
            early = IdRange(ownIdRange.start, otherIdRange.start - ownIdRange.start)
            overlap = IdRange(start=max(ownIdRange.start, otherIdRange.start),
                              length=min(ownIdRange.end, otherIdRange.end) - max(ownIdRange.start, otherIdRange.start))
            late = IdRange(otherIdRange.end, ownIdRange.end - otherIdRange.end)
            if(early.length > 0):
                nonOverlaps.append(early)
            if(late.length > 0):
                nonOverlaps.append(late)
            overlaps.append(overlap)

        return overlaps, nonOverlaps

class IdRange:
    def __init__(self, start, length):
        self.start = start
        self.length = length
        self.end = start + length
    
    def __contains__(self, other):
        if isinstance(other, IdRange):
            return other.start >= self.start and other.end <= self.end
        else:
            return other >= self.start and other < self.end

class MappingDefinition:
    def __init__(self, line):
        parts = line.split(' ')
        self.destinationRangeStart = int(parts[0])
        self.idRange = IdRange(int(parts[1]), int(parts[2]))
        
class DataMap:
    def __init__(self, lines):
        headerLine = lines[0].split(' ')[0]
        self.source = headerLine.split('-')[0]
        self.destination  = headerLine.split('-')[2]
        self.mappings = [MappingDefinition(line) for line in lines[1:] if line.strip() != '']

    def getMappedIdRanges(self, idRangeSet):
        handledRanges = []
        unhandledRanges = idRangeSet
        for mapping in self.mappings:
            overlaps, nonOverLaps = unhandledRanges.getOverlaps(mapping.idRange)

            for overlap in overlaps:
                mappedRange = IdRange(mapping.destinationRangeStart + (overlap.start - mapping.idRange.start),
                                      overlap.length)
                handledRanges.append(mappedRange)
            unhandledRanges = IdRangeSet(nonOverLaps)
        return IdRangeSet(handledRanges + unhandledRanges.idRanges)

def getSeedIds(idParings):
    idRanges = []
    for i in range(0, len(idParings), 2):
        start = idParings[i]
        length = idParings[i+1]
        idRanges.append(IdRange(start, length))
    return idRanges

with open("5.txt", "r") as file:
    lines = file.readlines()
    seedIdParings = [int(n.strip()) for n in lines[0].split(':')[1].split(' ') if n.strip() != '']
    seedIdRanges = getSeedIds(seedIdParings)
    rangeSet = IdRangeSet(seedIdRanges)

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

    for dataMap in maps:
        rangeSet = dataMap.getMappedIdRanges(rangeSet)        

    print(rangeSet.minValue())

