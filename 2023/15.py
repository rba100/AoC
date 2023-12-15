def holidayHash(input: str) -> int:
    result = 0
    for c in input:
        ci = ord(c)
        result += ci
        result *= 17
        result %= 256
    return result

def hashSequence(input: str) -> int:
    parts = input.split(",")
    result = 0
    for p in parts:
        result += holidayHash(p)
    return result

class Lens:
    def __init__(self, label: str, focalLength: int):
        self.label = label
        self.focalLength = focalLength
    
    def __str__(self):
        return self.label + "  " + str(self.focalLength)
    def __repr__(self):
        return str(self)

class Box:
    def __init__(self, id: int):
        self.id = id
        self.lenses: [Lens] = []

    def power(self) -> int:
        if(len(self.lenses) == 0): return 0
        s = sum([(i+1) * l.focalLength for i, l in enumerate(self.lenses)])
        power = s * (self.id + 1)
        return power
    
    def __str__(self):
        return str(self.lenses)
    def __repr__(self):
        return str(self)
        
def processLensArray(input: str) -> [Lens]:
    boxes = [Box(i) for i in range(0, 256)]
    parts = input.split(",")
    for p in parts:
        isRemove = p[-1] == "-"
        lensLabel = p[:-1] if isRemove else p.split("=")[0]
        boxCode = holidayHash(lensLabel)
        box = boxes[boxCode]
        
        existingLens = next((l for l in box.lenses if l.label == lensLabel), None)

        if(isRemove):
            if(existingLens != None):
                box.lenses.remove(existingLens)
        else:
            focalLength = int(p.split("=")[1])
            existingLens = next((l for l in box.lenses if l.label == lensLabel), None)
            if(existingLens == None):
                box.lenses.append(Lens(lensLabel, focalLength))
            else:
                existingLens.focalLength = focalLength
        
    return boxes

input = None
with open("./2023/15.txt") as file:
    input = file.read().strip()

print(holidayHash("HASH"))
print(hashSequence("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"))

# part 1
print("\nPart 1")
print(hashSequence(input))

# part 2
print("\nPart 2")
#boxes = processLensArray("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7")
boxes = processLensArray(input)
print(sum([b.power() for b in boxes]))