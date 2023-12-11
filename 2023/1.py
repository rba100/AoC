symbolMap = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven":"7",
    "eight":"8",
    "nine":"9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7":"7",
    "8":"8",
    "9":"9",
    "0":"0"
}

def getSymbols(line) -> []:
    position = 0
    digits = []
    while position < len(line):
        possibleSymbols = {symbol:mapped for symbol, mapped in symbolMap.items() if line[position:].startswith(symbol)}
        if(len(possibleSymbols) == 0):
            position += 1
        else:
            if(len(possibleSymbols) > 1):
                raise Exception("Ambiguous symbol")
            digit = possibleSymbols.popitem()[1]
            digits.append(digit)
            position += len(digit)
    return digits

with open('./Done/1.txt', 'r') as file:
    lines = file.readlines()
    nums = []
    for line in lines:
        symbols = getSymbols(line)
        first = symbols[0]
        last = symbols[-1]
        num = int(first + last)
        #print(num)
        nums.append(num)
    print(sum(nums))