#Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

class Card:
    def __init__(self, line):
        parts = line.split(':')
        self.id = int(parts[0].split(' ')[-1].strip())
        numberParts = parts[1].split('|')
        self.winningNumbers = [int(n.strip()) for n in numberParts[0].split(' ') if n != '']
        self.numbersHeld = [int(n.strip()) for n in numberParts[1].split(' ') if n != '']

    def score(self):
        matches = 0
        for number in self.winningNumbers:
            if(number in self.numbersHeld):
                matches += 1
        if matches == 0:
            return 0
        return 1 * (2 ** (matches - 1))

with open("4.txt", "r") as file:
    lines = file.readlines()
    cards = [Card(line) for line in lines]
    scores = [card.score() for card in cards]
    print(sum(scores))


