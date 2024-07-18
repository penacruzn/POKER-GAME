from tkinter import messagebox

class Player:
    def __init__(self, name, wallet):
        self.name = name  # Player's name
        self.wallet = wallet  # Player's wallet amount
        self.hand = []  # List to hold the player's hand

    def add_card_to_hand(self, card):
        self.hand.append(card)  # Add a card to the player's hand

    def display_hand(self):
        return "\n".join(str(card) for card in self.hand)  # Display the player's hand

    def sort_hand(self):
        self.hand.sort(key=lambda card: card.value)  # Sort the hand by card value

    def display_updated_hand(self):
        # Display the updated hand after discarding
        messagebox.showinfo("Updated Hand", f"Your updated hand after discarding:\n{self.display_hand()}")
