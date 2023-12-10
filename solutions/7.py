from functools import cmp_to_key

cardRankings = [ "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A" ]

class Hand:
    def __init__(self, cards, bid=None):
        if(len(cards) != 5):
            raise Exception("Hands must have 5 cards. input: " + str(cards))
        self.cards = cards
        self.bid = int(bid) if bid != None else None
        self.unique = set(cards)
        self.longestRun = 0
        for u in self.unique:
            run = 0
            for c in cards:
                if(c == u):
                    run += 1
            if(run > self.longestRun):
                self.longestRun = run

    def score(self):
        if(self.isFiveOfAKind()):
            return 7
        if(self.isFourOfAKind()):
            return 6
        if(self.isFullHouse()):
            return 5
        if(self.isThreeOfAKind()):
            return 4
        if(self.isTwoPairs()):
            return 3
        if(self.isPair()):
            return 2
        return 1
    
    def isFiveOfAKind(self):
        return len(self.unique) == 1
    
    def isFourOfAKind(self):
        return len(self.unique) == 2 and self.longestRun == 4
    
    def isFullHouse(self):
        return len(self.unique) == 2 and self.longestRun == 3
    
    def isThreeOfAKind(self):
        return len(self.unique) == 3 and self.longestRun == 3
    
    def isTwoPairs(self):
        return len(self.unique) == 3 and self.longestRun == 2
    
    def isPair(self):
        return len(self.unique) == 4

    def beats(self, otherHand: 'Hand'):
        if(self.score() == otherHand.score()):
            for i in range(0, 5):
                ownCardRanking = cardRankings.index(self.cards[i])
                otherCardRanking = cardRankings.index(otherHand.cards[i])
                if(ownCardRanking > otherCardRanking):
                    return True
                elif(ownCardRanking < otherCardRanking):
                    return False
            raise Exception("Hands are equal")
        return self.score() > otherHand.score()
    
def card_comparator(card1, card2):
    return -1 if card1.beats(card2) else 1
    
hands = []

with open("7.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        parts = line.split()
        hands.append(Hand(parts[0].strip(), parts[1].strip()))

sorted_hands = sorted(hands, key=cmp_to_key(card_comparator), reverse=True)

#for i, hand in enumerate(sorted_hands): print(hand.cards, hand.bid, (i+1) * hand.bid)

results = [h.bid * (i+1) for i, h in enumerate(sorted_hands)]

print(sum(results))