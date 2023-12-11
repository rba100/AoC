lines = None
with open('./2015/5.txt') as f:
    lines = [l.strip() for l in f.readlines()]

vowels = ['a', 'e', 'i', 'o', 'u']

def part1():
    nice = 0
    for line in lines:
        vowelCount = 0
        doubleLetter = False
        badString = False
        for i in range(len(line)):
            if line[i] in vowels:
                vowelCount += 1
            if i > 0 and line[i] == line[i - 1]:
                doubleLetter = True
            if i > 0 and (line[i - 1] + line[i]) in ['ab', 'cd', 'pq', 'xy']:
                badString = True
        if vowelCount >= 3 and doubleLetter and not badString:
            nice += 1
    print(nice)

def part2():
    nice = 0
    for line in lines:
        pair = False
        repeat = False
        for i in range(len(line) - 1):
            if line[i:i + 2] in line[i + 2:]:
                pair = True
            if i > 0 and line[i - 1] == line[i + 1]:
                repeat = True
        if pair and repeat:
            nice += 1
    print(nice)

part1()
part2()