lights = [[0 for _ in range(1000)] for _ in range(1000)]

def turn_on(x1, y1, x2, y2):
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            lights[i][j] += 1

def turn_off(x1, y1, x2, y2):
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            if lights[i][j] > 0:
                lights[i][j] -= 1

def toggle(x1, y1, x2, y2):
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            lights[i][j] += 2

def count():
    return sum([sum(l) for l in lights])


with open('./2015/6.txt') as f:
    for line in f.readlines():
        line = line.strip()
        #turn off 464,858 through 833,915
        if line.startswith('turn off'):
            line = line.replace('turn off ', '')
            x1, y1 = line.split(' through ')[0].split(',')
            x2, y2 = line.split(' through ')[1].split(',')
            turn_off(int(x1), int(y1), int(x2), int(y2))
        #turn on 226,196 through 599,390
        elif line.startswith('turn on'):
            line = line.replace('turn on ', '')
            x1, y1 = line.split(' through ')[0].split(',')
            x2, y2 = line.split(' through ')[1].split(',')
            turn_on(int(x1), int(y1), int(x2), int(y2))
        #toggle 577,43 through 683,54
        elif line.startswith('toggle'):
            line = line.replace('toggle ', '')
            x1, y1 = line.split(' through ')[0].split(',')
            x2, y2 = line.split(' through ')[1].split(',')
            toggle(int(x1), int(y1), int(x2), int(y2))

print(count())
