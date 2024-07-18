import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.make_deck()

    def make_deck(self):
        suits = ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]
        names = ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING"]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        # Create a list of Card objects for each suit and name
        self.cards = [Card(suit, names[i], values[i]) for suit in suits for i in range(13)]
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
