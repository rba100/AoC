from functools import cmp_to_key

cardRankings = [ "J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A" ]

class Hand:
    def __init__(self, cards, bid=None):
        if(len(cards) != 5):
            raise Exception("Hands must have 5 cards. input: " + str(cards))
        self.cards = cards
        self.bid = int(bid) if bid != None else None
        self.unique = set(cards)
        self.uniqueWithoutJoker = set([c for c in cards if c != "J"])
        self.jokerCount = len([c for c in cards if c == "J"])
        self.hasJoker = self.jokerCount > 0
        self.shortestNonJokerRun = 5
        self.longestNonJokerRun = 0
        for u in self.uniqueWithoutJoker:
            run = 0
            for c in [c for c in cards if c != "J"]:
                if(c == u):
                    run += 1
            if(run > self.longestNonJokerRun):
                self.longestNonJokerRun = run
            if(run < self.shortestNonJokerRun):
                self.shortestNonJokerRun = run

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
    
    # These methods only work if checked in order

    def isFiveOfAKind(self):
        return len(self.unique) == 1 or (self.hasJoker and len(self.uniqueWithoutJoker) == 1)
    
    def isFourOfAKind(self):
        longestRunRequired = 4 - self.jokerCount
        return self.shortestNonJokerRun == 1 and self.longestNonJokerRun == longestRunRequired
    
    def isFullHouse(self):
        if(self.jokerCount > 2): # assert assumption
            raise Exception("isFullHouse: Too many jokers, methods called in wrong order or bug, hand: " + str(self.cards))
        uniqueRequired = 3 if self.hasJoker else 2
        longestRunRequired = 3 - self.jokerCount
        return len(self.unique) == uniqueRequired and self.longestNonJokerRun == longestRunRequired
    
    def isThreeOfAKind(self):
        if(self.jokerCount > 2): # assert assumption
            raise Exception("isThreeOfAKind: Too many jokers, methods called in wrong order or bug, hand: " + str(self.cards))
        uniqueRequired = 4 if self.hasJoker else 3
        runRequired = 3 - self.jokerCount
        return len(self.unique) == uniqueRequired and self.longestNonJokerRun == runRequired
    
    def isTwoPairs(self):
        if(self.jokerCount > 0): return False
        return len(self.unique) == 3 and self.longestNonJokerRun == 2
    
    def isPair(self):
        if(self.jokerCount > 1): raise Exception("isPair: Too many jokers, methods called in wrong order or bug, hand: " + str(self.cards))
        uniqueRequired = 5 if self.hasJoker else 4
        return len(self.unique) == uniqueRequired

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

#for hand in hands: print(hand.cards, hand.jokerCount, hand.shortestNonJokerRun, hand.longestNonJokerRun)

sorted_hands = sorted(hands, key=cmp_to_key(card_comparator), reverse=True)

results = [h.bid * (i+1) for i, h in enumerate(sorted_hands)]

print(sum(results))