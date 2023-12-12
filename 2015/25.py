def getNextCode(code):
    return (code * 252533) % 33554393

def getNthCode(n):
    code = 20151125
    for i in range(1, n):
        code = getNextCode(code)
    return code

def coordsToN(row, col):
    return sum(range(row + col - 1)) + col

def coordsToN2(row, col):
    return (row + col - 1) * (row + col) // 2 - row + 1

# Part 1
n = coordsToN2(2947, 3029)
print(getNthCode(n))
