#Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

class Card:
    def __init__(self, line):
        parts = line.split(':')
        self.id = int(parts[0].split(' ')[-1].strip())
        numberParts = parts[1].split('|')
        self.winningNumbers = [int(n.strip()) for n in numberParts[0].split(' ') if n != '']
        self.numbersHeld = [int(n.strip()) for n in numberParts[1].split(' ') if n != '']
        self.copies = 1

    def score(self):
        matches = 0
        for number in self.winningNumbers:
            if(number in self.numbersHeld):
                matches += 1
        return matches

with open("4.txt", "r") as file:
    lines = file.readlines()
    cards = [Card(line) for line in lines]
    for i in range(0, len(cards)):
        card = cards[i]
        score = card.score()
        if(score > 0):
            cardsToCopy = cards[i+1:][:score]
            for cardToCopy in cardsToCopy:
                cardToCopy.copies += card.copies
    
    totalCards = sum([card.copies for card in cards])
    print(totalCards)


