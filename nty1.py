import random

#nty before using aima games.py

class Hand:
    def __init__(self, cards = {}, counters = 11):
        self.cards = cards
        self.counters = counters

    def __repr__(self):
        return 'Cards: ' + str(self.cards) + \
               '\nCounters: ' + str(self.counters) + \
               '\nValue: ' + str(self.value()) + '\n'

    def value(self):
        total = 0
        previous = 0
        for card in sorted(self.cards):
            if card > previous + 1:
                total += card
            previous = card
            
        total -= self.counters
        return total

    def takeCard(self, game):
        

class Deck:
    def __init__(self, deck = random.sample(range(3,36),24)):
        self.deck = deck

    def __repr__(self):
        return str(len(self.deck)) +  ' cards: ' + str(self.deck)

    def draw(self):
        return self.deck.pop(0)

class Game:
    def __init__(self, deck = Deck(), card = 0, counters = 0):
        self.deck = deck
        self.card = self.deck.draw() if not card else card
        self.counters = counters

    def __repr__(self):
        return str(Deck()) + \
               '\nDrawn card: ' + str(self.card) + \
               '\nCounters: ' + str(self.counters) + '\n'

    def draw(self):
        return self.deck.draw()
        

print(Game())
#print(Hand())
#print(Hand({3,4,5,11}))
