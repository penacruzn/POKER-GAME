import random  # For shuffling the deck of cards
import os  # For handling file paths
import sqlite3  # For database operations
import tkinter as tk  # For creating the GUI
from tkinter import messagebox, simpledialog  # For dialog boxes in the GUI
from PIL import Image, ImageTk  # For handling images of cards (Make sure to install the Pillow library)
from deck import Deck
from player import Player
from card import card_name_mapping
from datetime import datetime

DATABASE_PATH = "CasinoDB.db"  # Path to the SQLite database

class PokerGame:
    def __init__(self):
        print("Initializing PokerGame")
        self.connect_to_database()  # Connect to the database first
        self.create_tables()  # Create necessary tables if they don't exist
        self.deck = Deck()  # Create a deck of cards
        self.players = [Player(f"Player {i+1}", 150) for i in range(3)]  # Create 3 players with initial wallet amount
        self.pot = 0  # Initialize the pot
        self.player_winnings = {}  # Dictionary to track player winnings
        self.root = tk.Tk()  # Create the main window
        self.root.title("Poker Game")  # Set the title of the main window
        self.card_images = self.load_card_images()  # Load card images
        self.hand_windows = []  # List to keep track of hand windows
        self.create_menu()  # Create the menu

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect(DATABASE_PATH)
            self.cursor = self.conn.cursor()
            print("Database connection established")
        except sqlite3.Error as e:
            print(f"Database connection failed: {e}")

    def create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS HISTORY (
                                   TIMESTAMP TEXT,
                                   GAMEID INTEGER,
                                   USERID TEXT,
                                   RESULT TEXT,
                                   AMOUNT INTEGER
                                   )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS USER (
                                   USERID TEXT PRIMARY KEY,
                                   PASSWORD TEXT,
                                   NETGAIN INTEGER,
                                   BALANCE INTEGER,
                                   HASCHEATED BOOLEAN
                                   )''')
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Table creation failed: {e}")

    def save_game_result(self, game_id, user_id, result, amount):
        try:
            print(f"Saving game result for user {user_id}")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("INSERT INTO HISTORY (TIMESTAMP, GAMEID, USERID, RESULT, AMOUNT) VALUES (?, ?, ?, ?, ?)",
                                (timestamp, game_id, user_id, result, amount))
            self.conn.commit()
            print(f"Game result saved for user {user_id}: {result} with amount {amount}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def update_user_balance_and_netgain(self, user_id, netgain, balance):
        try:
            print(f"Updating user balance and net gain for user {user_id}")
            self.cursor.execute("UPDATE USER SET NETGAIN = NETGAIN + ?, BALANCE = BALANCE + ? WHERE USERID = ?",
                                (netgain, balance, user_id))
            self.conn.commit()
            print(f"User balance and net gain updated for user {user_id}: Net Gain {netgain}, Balance {balance}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def load_card_images(self):
        card_images = {}
        # Path to the directory containing card images
        image_dir = r"C:\Users\penacruzn\OneDrive - Wentworth Institute of Technology\Desktop\DECK OF CARDS"
        for suit in ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]:
            for name in ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING"]:
                filename = f"{card_name_mapping[name]}_of_{suit.lower()}.png"
                path = os.path.join(image_dir, filename)
                if os.path.exists(path):
                    image = Image.open(path)
                    image = image.resize((100, 150), Image.LANCZOS)  # Resize the image
                    card_images[f"{name} of {suit}"] = ImageTk.PhotoImage(image)
                else:
                    print(f"Image not found: {path}")
        return card_images

    def create_menu(self):
        self.root.geometry("600x400")  # Set the window size
        menu_frame = tk.Frame(self.root, bg="green")  # Create a frame for the menu
        menu_frame.pack(expand=True, fill="both")  # Pack the frame to fill the window

        # Create and pack the welcome label
        welcome_label = tk.Label(menu_frame, text="Welcome to Poker", font=("Comic Sans MS", 24, "bold"), bg="green", fg="white")
        welcome_label.pack(pady=20)

        # Create and pack the "Go to Table" button
        btn_go_to_table = tk.Button(menu_frame, text="Go to Table", command=self.start_game, bg="blue", fg="white", font=("Arial", 16))
        btn_go_to_table.pack(pady=10)

        # Create and pack the "See Rules" button
        btn_see_rules = tk.Button(menu_frame, text="See Rules", command=self.display_rules, bg="blue", fg="white", font=("Arial", 16))
        btn_see_rules.pack(pady=10)

        # Create and pack the "See Poker Hands and Rules" button
        btn_see_hands_rules = tk.Button(menu_frame, text="See Poker Hands and Rules", command=self.display_hands_and_rules, bg="blue", fg="white", font=("Arial", 16))
        btn_see_hands_rules.pack(pady=10)

        # Create and pack the "Quit Game" button
        btn_quit = tk.Button(menu_frame, text="Quit Game", command=self.root.quit, bg="blue", fg="white", font=("Arial", 16))
        btn_quit.pack(pady=10)

        self.root.mainloop()  # Start the Tkinter main loop

    def start_game(self):
        ante = 10  # Ante amount for each player
        for player in self.players:
            player.wallet -= ante  # Deduct ante from each player's wallet
            self.pot += ante  # Add ante to the pot
        self.deck.shuffle_deck()  # Shuffle the deck before dealing new cards
        self.deal_cards()  # Deal cards to players
        self.betting_cycle()  # Start the first betting cycle
        self.discard_phase()  # Allow players to discard and draw new cards
        self.betting_cycle()  # Start the second betting cycle
        self.determine_winner()  # Determine the winner of the game
        self.print_wallets()  # Display the updated wallets

    def deal_cards(self):
        self.close_all_hand_windows()  # Close all open hand windows
        for player in self.players:
            player.hand.clear()  # Clear the player's hand before dealing new cards
        for _ in range(5):
            for player in self.players:
                card = self.deck.deal_card()  # Deal a card to the player
                player.add_card_to_hand(card)  # Add the card to the player's hand
                card.image = card.get_image(self.card_images)  # Assign the image to the card

        for player in self.players:
            player.sort_hand()  # Sort the player's hand
            self.display_hand(player)  # Display the player's hand

    def display_hand(self, player):
        hand_window = tk.Toplevel(self.root)  # Create a new window for the player's hand
        self.hand_windows.append(hand_window)  # Keep track of the hand window
        hand_window.title(f"{player.name}'s Hand")  # Set the title of the hand window
        
        hand_frame = tk.Frame(hand_window)  # Create a frame for the hand
        hand_frame.pack(pady=20)  # Pack the frame

        # Display each card in the player's hand
        for card in player.hand:
            card_label = tk.Label(hand_frame, image=card.image, padx=10, pady=5)
            card_label.pack(side="left")

    def update_hand_display(self, player, window):
        for widget in window.winfo_children():  # Clear existing widgets in the window
            widget.destroy()
        # Display each card in the player's hand
        for card in player.hand:
            card_label = tk.Label(window, image=card.image, padx=10, pady=5)
            card_label.pack(side="left")

    def close_all_hand_windows(self):
        for window in self.hand_windows:  # Close all hand windows
            window.destroy()
        self.hand_windows.clear()  # Clear the list of hand windows

    def betting_cycle(self):
        current_bet = 0  # Initialize the current bet
        for player in self.players:
            if player.hand:  # If the player has not folded
                bet = simpledialog.askinteger("Betting", f"{player.name}'s turn. Current bet is {current_bet}. Your wallet: {player.wallet}\nEnter your bet (0 to fold): ")
                if bet == 0:
                    player.hand.clear()  # Clear the player's hand if they fold
                else:
                    current_bet = max(current_bet, bet)  # Update the current bet
                    player.wallet -= bet  # Deduct the bet from the player's wallet
                    self.pot += bet  # Add the bet to the pot

    def discard_phase(self):
        for player in self.players:
            if player.hand:  # If the player has not folded
                self.close_all_hand_windows()  # Close all hand windows before showing the current player's hand
                hand_window = tk.Toplevel(self.root)  # Create a new window for the player's hand
                self.hand_windows.append(hand_window)  # Keep track of the hand window
                hand_window.title(f"{player.name}'s Hand")

                hand_frame = tk.Frame(hand_window)  # Create a frame for the hand
                hand_frame.pack(pady=20)

                self.update_hand_display(player, hand_frame)  # Display the player's hand

                # Prompt the player to choose cards to discard
                discard_indexes = simpledialog.askstring("Discard Phase", f"{player.name}, choose the cards to discard (enter indexes separated by spaces):\n{player.display_hand()}")
                discard_indexes = [int(x)-1 for x in discard_indexes.split() if x.isdigit()]

                for idx in sorted(discard_indexes, reverse=True):
                    if 0 <= idx < len(player.hand):
                        player.hand.pop(idx)  # Remove the discarded card from the player's hand
                        card = self.deck.deal_card()  # Deal a new card to the player
                        card.image = card.get_image(self.card_images)  # Assign the image to the card
                        player.add_card_to_hand(card)  # Add the card to the player's hand

                player.sort_hand()  # Sort the player's hand
                self.update_hand_display(player, hand_frame)  # Update the display of the player's hand
    
                # Close the current player's hand window after they finish discarding
                hand_window.destroy()

    def determine_winner(self):
        player_hands = []
        player_cards = {}

        for player in self.players:
            if player.hand:
                hand_type = self.evaluate_hand(player.hand)  # Evaluate the player's hand
                player_hands.append((player.name, hand_type))  # Add the player's hand type to the list
                player_cards[player.name] = player.hand  # Store the player's hand

        if not player_hands:  # If all players folded
            messagebox.showinfo("Result", "All players folded. No winner.")
            return

        # Rank the hands and determine the winner
        hand_rank = {
            "High Card": 1, "One Pair": 2, "Two Pair": 3,
            "Three of a Kind": 4, "Straight": 5, "Flush": 6,
            "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9, "Royal Flush": 10
        }

        player_hands.sort(key=lambda pair: hand_rank[pair[1]], reverse=True)

        winner_name = player_hands[0][0]
        winner_hand_type = player_hands[0][1]
        messagebox.showinfo("Winner", f"Congratulations {winner_name} wins with a {winner_hand_type}!")
        winning_hand = ", ".join([f"{card.name} of {card.suit}" for card in player_cards[winner_name]])
        messagebox.showinfo("Winning Hand", f"Winning hand: {winning_hand}")

        # Update the player's winnings
        self.player_winnings[winner_name] = self.player_winnings.get(winner_name, 0) + self.pot

        # Save game result to database
        user_id = winner_name.split()[-1]
        result = 'WIN'
        amount = self.player_winnings[winner_name]
        print("Attempting to save game result to database")
        if hasattr(self, 'cursor'):
            self.save_game_result(1, user_id, result, amount)
            self.update_user_balance_and_netgain(user_id, amount, self.players[int(user_id) - 1].wallet)
        else:
            print("Cursor attribute is not initialized")

        self.pot = 0

    def print_wallets(self):
        wallets_display = ""
        for player in self.players:
            wallets_display += f"{player.name}'s Wallet: {player.wallet + self.player_winnings.get(player.name, 0)}\n"
        messagebox.showinfo("Wallets", wallets_display)

    def evaluate_hand(self, hand):
        # Evaluate the hand and return the hand type
        if self.is_royal_flush(hand):
            return "Royal Flush"
        if self.is_straight_flush(hand):
            return "Straight Flush"
        if self.is_four_of_a_kind(hand):
            return "Four of a Kind"
        if self.is_full_house(hand):
            return "Full House"
        if self.is_flush(hand):
            return "Flush"
        if self.is_straight(hand):
            return "Straight"
        if self.is_three_of_a_kind(hand):
            return "Three of a Kind"
        if self.is_two_pair(hand):
            return "Two Pair"
        if self.is_one_pair(hand):
            return "One Pair"
        return "High Card"

    def is_royal_flush(self, hand):
        return self.is_straight_flush(hand) and hand[0].value == 10

    def is_straight_flush(self, hand):
        return self.is_straight(hand) and self.is_flush(hand)

    def is_four_of_a_kind(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 4 in counts.values()

    def is_full_house(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 3 in counts.values() and 2 in counts.values()

    def is_flush(self, hand):
        return all(card.suit == hand[0].suit for card in hand)

    def is_straight(self, hand):
        return all(hand[i].value == hand[i - 1].value + 1 for i in range(1, len(hand)))

    def is_three_of_a_kind(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 3 in counts.values()

    def is_two_pair(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return list(counts.values()).count(2) == 2

    def is_one_pair(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 2 in counts.values()

    def display_rules(self):
        # Display the rules of the poker game
        rules = (
            "Poker Rules:\n"
            "1. The game is 5-card draw poker.\n"
            "2. Each player is dealt 5 cards.\n"
            "3. Players bet, discard, and draw new cards.\n"
            "4. Best hand wins the pot.\n"
            "5. $10 to play each round.\n\n"
            "Betting Rules:\n"
            "During each betting cycle, players have three options:\n"
            "  a. Fold (Enter 0): If you think your hand is weak, you can fold by entering 0.\n"
            "     This means you will not participate further in this round, and your cards will be discarded.\n"
            "  b. Call (Enter the current bet amount): If you want to match the current highest bet placed by other players,\n"
            "     you enter an amount equal to the current bet. This means you are staying in the game by matching the current bet.\n"
            "  c. Raise (Enter an amount greater than the current bet): If you believe your hand is strong or you want to bluff,\n"
            "     you can enter an amount greater than the current bet to raise. This forces other players to either match your new bet or fold.\n\n"
            "Example:\n"
            "  - Assume the current bet is 10.\n"
            "  - If you think your hand is weak and you don't want to continue, enter 0 to fold.\n"
            "  - If you think your hand is decent and you want to stay in the game without raising the stakes, enter 10 to call the current bet.\n"
            "  - If you think your hand is strong or want to bluff, enter 20 or any higher amount to raise the bet.\n"
            "    This means other players will now have to match 20 to stay in the game.\n"
        )
        messagebox.showinfo("Poker Rules", rules)

    def display_hands_and_rules(self):
        # Display the poker hands and rules
        hands_rules = (
            "Poker Hands and Rules:\n"
            "1. Royal Flush: A, K, Q, J, 10, all the same suit.\n"
            "2. Straight Flush: Five cards in a sequence, all the same suit.\n"
            "3. Four of a Kind: All four cards of the same rank.\n"
            "4. Full House: Three of a kind with a pair.\n"
            "5. Flush: Any five cards of the same suit, but not in a sequence.\n"
            "6. Straight: Five cards in a sequence, but not of the same suit.\n"
            "7. Three of a Kind: Three cards of the same rank.\n"
            "8. Two Pair: Two different pairs.\n"
            "9. One Pair: Two cards of the same rank.\n"
            "10. High Card: When you haven't made any of the hands above, the highest card plays.\n"
        )
        messagebox.showinfo("Poker Hands and Rules", hands_rules)

# To start the game, create an instance of PokerGame and call display_menu.
if __name__ == "__main__":
    game = PokerGame()

