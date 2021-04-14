import random

# Constants
USER_BALANCE = 1000 # Initial player balance
NUM_OF_DECKS = 1 # Number of decks in use for play

def deal(deck):
    """
    Deals card to a single hand

    Parameters
    ----------
    deck : 
        The deck in use

    Returns
    -------
    hand : 
        The player's (or dealer's) hand

    """
    hand = []
    card1 = random.choice(deck)
    deck.remove(card1)
    hand.append(card1)
    card2 = random.choice(deck)
    deck.remove(card2)
    hand.append(card2)
    return hand

def hit(hand, deck):
    """
    A function that recreates the "hit" move in blackjack

    Parameters
    ----------
    hand : 
        The player's (or dealer's) hand
    deck : 
        The deck in use

    Returns
    -------
    hand : 
        Updated player's (or dealer's) hand

    """
    card = random.choice(deck)
    deck.remove(card)
    hand.append(card)
    return hand

def double_down(hand, deck, bet):
    """
    A function that recreates the "double down" move in blackjack

    Parameters
    ----------
    hand : 
        The player's hand
        The deck in use
    bet : 
        The player's original bet

    Returns
    -------
    hand : 
        The player's updated hand
    bet : 
        The player's updated bet

    """
    bet += bet
    hand = hit(hand, deck)
    return hand, bet

def hand_total(hand):
    """
    Determines the sum of the hand passed

    Parameters
    ----------
    hand : 
        The player's (or dealer's) hand

    Returns
    -------
    hand_total : 
        The sum of the hand passed

    """
    hand_total = 0
    
    # Adds each card value to hand_total
    for card in hand:
        # Adds 10 if card is a face card
        if card == "J" or card == "Q" or card == "K":
            hand_total += 10
        # Adds 11 or 1 if card is an Ace (depends on which is most beneficial)
        elif card == "A":
            if hand_total < 11:
                hand_total += 11
            else:
                hand_total += 1
        # Adds face value of card otherwise
        else:
            hand_total += card
    return hand_total

def choose(hand):
    """
    Function that executes what move the player wants to make

    Parameters
    ----------
    hand : 
        The player's hand

    Returns
    -------
    choice : 
        The player's choice

    """
    choice = ""
    can_double_down = False
    inputString = "Do you want to Hit[H], Stand[S]"
    
    # Adds double down option if player's hand allows for such a move
    if (9 <= hand_total(hand) <= 11 and len(hand) == 2):
        inputString += ", Double Down[D]"
        can_double_down = True
    inputString += ": "
    
    # Asks player what move they want to make 
    
    # Includes double down move if applicable
    if can_double_down:
        choice = input(inputString).lower()
        while choice != "h" and choice != "s" and choice != "d":
            print("Please enter a valid choice")
            choice = input(inputString).lower()
    
    # Just includes the hit and stand moves
    else:
        choice = input(inputString).lower()
        while choice != "h" and choice != "s":
            print("Please enter a valid choice")
            choice = input(inputString).lower()
    
    return choice
    
def set_bet(balance):
    """
    Sets bet by asking player how much they want to bet

    Parameters
    ----------
    balance : 
        The player's current balance

    Returns
    -------
    bet : 
        The player's bet

    """
    print("You have a total balance of $" + str(balance))
    bet = int(input("How much do you want to bet? "))
    
    # Reasks player if their bet value is invalid
    while bet < 0 or bet > balance:
        print("Please enter a valid bet")
        print("You have a total balance of $" + str(balance))
        bet = int(input("How much do you want to bet? "))
        
    return bet
        
def game_win(player_hand_sum, dealer_hand_sum):
    """
    Determines whether the player or dealer won the game (round)

    Parameters
    ----------
    player_hand_sum : 
        The sum of the player's hand
    dealer_hand_sum : 
        The sum of the dealers' hand

    Returns
    -------
    bool
        True if player wins, False if the player loses (and dealer wins)

    """
    if player_hand_sum > 21:
        return False
    elif dealer_hand_sum > 21:
        return True
    elif player_hand_sum > dealer_hand_sum:
        return True
    else: 
        return False

    
def game(balance):
    """
    Function that actually runs a game/round of blackjack

    Parameters
    ----------
    balance : 
        The player's balance at the start of the game

    Returns
    -------
    balance : 
        The player's balance after the game

    """
    bet = set_bet(balance)
    player_choice = ""
    
    deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,
            10,10,10,10,"J","J","J","J","Q","Q","Q","Q","K","K","K","K","A",
            "A","A","A"] * NUM_OF_DECKS
    
    # Dealing initial hands
    player_hand = deal(deck)
    dealer_hand = deal(deck)  
    
    # Allows the player to make moves until they or the dealer wins (or if the 
    # player decides to stand or double down)
    while (hand_total(player_hand) < 21 and hand_total(dealer_hand) < 21) and player_choice != "s" and player_choice != "d":
        print("The dealer is showing a " + str(dealer_hand[0]))
        print("You have a " + str(player_hand) + " for a total of " + 
              str(hand_total(player_hand)))
        player_choice = choose(player_hand)
        
        # The case if the player decides to hit
        if player_choice == "h":
            player_hand = hit(player_hand, deck)
            if hand_total(dealer_hand) < 17 and hand_total(player_hand) <= 21:
                dealer_hand = hit(dealer_hand, deck)
        
        # The case if the player decides to stand
        elif player_choice == "s":
            while hand_total(dealer_hand) < 17 and hand_total(player_hand) <= 21:
                dealer_hand = hit(dealer_hand, deck)
        
        # The case if the player decides to double down
        elif player_choice == "d":
            player_hand, bet = double_down(player_hand, deck, bet)
            while hand_total(dealer_hand) < 17 and hand_total(player_hand) <= 21:
                dealer_hand = hit(dealer_hand, deck)
    
    # The case if the player wins the game/round (their bet is added to their balance)
    if (game_win(hand_total(player_hand), hand_total(dealer_hand))):
        print("The dealer has a " + str(dealer_hand) + " for a total of " + 
              str(hand_total(dealer_hand)))
        print("You have a " + str(player_hand) + " for a total of " + 
              str(hand_total(player_hand)))
        print("You win $" + str(bet) + "!")
        balance += bet
    
    # the case if the dealer wins the game/round (the player's bet is deducted from their balance)
    else:
        print("The dealer has a " + str(dealer_hand) + " for a total of " + 
              str(hand_total(dealer_hand)))
        print("You have a " + str(player_hand) + " for a total of " + 
              str(hand_total(player_hand)))
        print("You lost $" + str(bet) + "!")
        balance -= bet
        
    return balance


def main():
    """
    Function that runs the entire blackjack game (until the player loses their
    balance or they decide to quit)

    Returns
    -------
    None.

    """
    balance = USER_BALANCE
    choice = input("Welcome to Blackjack!\nWould you like to play? [Y] or [N]: ").lower()
    
    # Player plays new games/rounds if they decide to play and if they can enough 
    # money in their balance
    while (choice == "y" and balance > 0):
        balance = game(balance)
        print("\nYour current balance is $" + str(balance))
        
        if (balance <= 0):
            print("You ran out of money!")

        elif balance > 0:
            choice = input("Would you like to play again? [Y] or [N]: ").lower()
    
    print("You ended with a balance of $" + str(balance))

            
if __name__ == "__main__":
    main()