
time = 48876981
record = 255128811171623

winningMoveStart = time
winningMoveEnd = 0

# Could binary chop but CPU is fast enough

for i in range(1, time - 1):
    distanceTravelled = i * (time-i)
    if(distanceTravelled > record):
        winningMoveStart = i
        break

for i in range(time - 1, 1, -1):
    distanceTravelled = i * (time-i)
    if(distanceTravelled > record):
        winningMoveEnd = i
        break

winningMoves = winningMoveEnd - winningMoveStart + 1

print(winningMoves)
