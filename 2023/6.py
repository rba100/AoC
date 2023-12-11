# Time:      7  15   30
# Record:  9  40  200
raceData1=[(7,9),(15,40),(30,200)]

#Time:        48     87     69     81
#Record:   255   1288   1117   1623
raceData2=[(48,255),(87,1288),(69,1117),(81,1623)]

winningChargeTimes = []

for time, record in raceData2:
    winningMoves = 0
    for i in range(1, time - 1):
        distanceTravelled = i * (time-i)
        if(distanceTravelled > record):
            winningMoves += 1
    print(winningMoves)
    winningChargeTimes.append(winningMoves)

product = 1
for time in winningChargeTimes:
    product *= time

print(product)
