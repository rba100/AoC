#example line:
#Game 1: 9 red, 2 green, 13 blue; 10 blue, 2 green, 13 red; 8 blue, 3 red, 6 green; 5 green, 2 red, 1 blue

def parseLine(line) -> {}:
    gameId = int(line.split(':')[0].split(' ')[1])
    draws = []
    drawsRaw =line.split(':')[1].split(';')
    for drawRaw in drawsRaw:
        draw = {"red": 0, "green": 0, "blue": 0}
        drawRaw = drawRaw.strip()
        colours = drawRaw.split(',')
        for colour in colours:
            colour = colour.strip()
            colour = colour.split(' ')
            draw[colour[1]] = int(colour[0])
        draws.append(draw)
    return {"gameId": gameId, "draws": draws}


with open('./2.txt', 'r') as file:
    lines = file.readlines()
    maxCubes = {
        "red" : 12,
        "green" : 13,
        "blue" : 14
    }
    validGames = []
    for line in lines:
        data = parseLine(line)
        valid = True
        for draw in data["draws"]:
            for colour, count in draw.items():
                if(count > maxCubes[colour]):
                    valid = False
        if(valid):
            validGames.append(data)
    gameIds = [game["gameId"] for game in validGames]
    print(sum(gameIds))