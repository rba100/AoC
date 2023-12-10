from functools import reduce

#example line:
#Game 1: 9 red, 2 green, 13 blue; 10 blue, 2 green, 13 red; 8 blue, 3 red, 6 green; 5 green, 2 red, 1 blue

def parseLine(line) -> {}:
    gameId = int(line.split(':')[0].split(' ')[1])
    maxCubes = {"red": 0, "green": 0, "blue": 0}
    drawsRaw =line.split(':')[1].split(';')
    for drawRaw in drawsRaw:
        draw = {"red": 0, "green": 0, "blue": 0}
        drawRaw = drawRaw.strip()
        colours = drawRaw.split(',')
        for colour in colours:
            colour = colour.strip()
            colour = colour.split(' ')
            draw[colour[1]] = int(colour[0])
        for colour, count in draw.items():
            if(count > maxCubes[colour]):
                maxCubes[colour] = count
        
    return {"gameId": gameId, "maxCubes": maxCubes, "power": reduce(lambda x, y: x * y, maxCubes.values())}


with open('./2.txt', 'r') as file:
    lines = file.readlines()
    games = []
    for line in lines:
        data = parseLine(line)
        games.append(data)
    powers = [game["power"] for game in games]
    print(sum(powers))