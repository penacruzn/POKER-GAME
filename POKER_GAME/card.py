import os
from PIL import Image, ImageTk

# Mapping suits to symbols
suit_symbols = {
    "HEARTS": "♥",
    "DIAMONDS": "♦",
    "CLUBS": "♣",
    "SPADES": "♠"
}
# Mapping card names to file name prefixes
card_name_mapping = {
    "ACE": "ace",
    "TWO": "2",
    "THREE": "3",
    "FOUR": "4",
    "FIVE": "5",
    "SIX": "6",
    "SEVEN": "7",
    "EIGHT": "8",
    "NINE": "9",
    "TEN": "10",
    "JACK": "jack",
    "QUEEN": "queen",
    "KING": "king"
}

class Card:
    def __init__(self, suit, name, value):
        self.suit = suit  # Suit of the card
        self.name = name  # Name of the card (e.g., ACE, TWO, etc.)
        self.value = value  # Value of the card for game logic
        self.image = None  # Placeholder for the card image

    def __str__(self):
        return f"{self.name} of {suit_symbols[self.suit]}"  # String representation of the card

    def get_image(self, card_images):
        key = f"{self.name} of {self.suit}"  # Key to retrieve the image from card_images
        return card_images.get(key, None)  # Return the image if it exists

