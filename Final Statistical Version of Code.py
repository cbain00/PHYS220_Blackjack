import random
import matplotlib.pyplot as plt
import statistics
import numpy as np
from astropy.table import QTable, Table, Column

# function where the dealer hits until their sum is greater than or equal to 17
def dealer(hand, deck):
    
    # when the function is called, the dealer's hand is equal to the first two cards the dealer was dealt
    hand_updated = eval_ace(hand)
    
    # continue hitting as long as the dealer's hand sum is less than 17
    while sum(hand_updated) < 17:
        # remove the dealt card from the deck and add it to the dealer's hand
        new_card = random.choice(deck)
        deck.remove(new_card)
        hand_updated.append(new_card)
        
        # evaluate the current hand to determine how to handle any aces
        hand_updated = eval_ace(hand_updated)
    return hand_updated

# this function is used to determine the value assigned to an ace (1 or 11) based on the other cards in the hand
def eval_ace(hand):
    
    # aces are initially valued at 11, so this if statement checks if there are any 11s (aces) in the hand
    if 11 in hand:
        # this loop iterates through all cards in the hand to check if each card is an ace
        for i in range(len(hand)):
            total = sum(hand)
            
            # this if statement checks if there is an 11 in the hand AND if the sum exceeds 21 (if so an 11 will be changed to a 1 to try to get the hand sum under 21)
            if 11 in hand and total > 21:
                # if the if statement is met, the value of the first ace is changed from 11 to 1
                position_ace = hand.index(11)
                hand[position_ace] = 1
    return hand

# this function is used to evaluate whether the player won or lost to the dealer
# a win is recorded as a 1 and a loss is recorded as a 0
def game_win(player_hand_sum, dealer_hand_sum):
    
    # first check if the player's hand sum is greater than 21
    if player_hand_sum > 21:
        # if so the player busts and therefore loses
        return 0
    
    # next check if the dealer's hand sum is greater than 21
    elif dealer_hand_sum > 21:
        # since we already checked if the player's hand sum is greater than 21, this case would mean that the dealer busts and the player wins
        return 1
    
    # next check if the player's hand sum is greater than the dealer's hand sum
    elif player_hand_sum > dealer_hand_sum:
        # the two prior cases have already checked if either the player or the dealer busts
        # in this case the player wins
        return 1
    
    # this final case means that the dealer's hand sum is greater than or equal to the player's hand sum
    else: 
        # in this case, the player loses
        return 0

def main():
    
    # this is the list of all possible starter hand combinations (2 cards)
    initial_hand_combos = [[2,2],[2,3],[2,4],[3,3],[2,5],[3,4],[2,6],[3,5],[4,4],[2,7],[3,6],[4,5],[2,8],[3,7],[4,6],[5,5],[2,9],[3,8],[4,7],[5,6],[2,10],[2,10],[2,10],[2,10],[3,9],[4,8],[5,7],[6,6],[11,11],[3,10],[3,10],[3,10],[3,10],[4,9],[5,8],[6,7],[11,2],[4,10],[4,10],[4,10],[4,10],[5,9],[6,8],[7,7],[11,3],[5,10],[5,10],[5,10],[5,10],[6,9],[7,8],[11,4],[6,10],[6,10],[6,10],[6,10],[7,9],[8,8],[11,5],[7,10],[7,10],[7,10],[7,10],[8,9],[11,6],[8,10],[8,10],[8,10],[8,10],[9,9],[11,7],[9,10],[9,10],[9,10],[9,10],[11,8],[10,10],[10,10],[10,10],[10,10],[10,10],[10,10],[10,10],[10,10],[10,10],[10,10],[11,9],[10,11],[10,11],[10,11],[10,11]]
    
    # the player will hit either 0, 1, or 2 times
    num_hits = [0,1,2]
    
    # number of simulations to run for each case
    N = 50000
    
    # for 91 initial hand combos and 0, 1, or 2 hits for each hand, there are 273 cases to examine (91x3)
    # the results list is a list of 273 lists (one for each case)
    # each inidividual list will be of the following format: [initial hand sum, number of hits, fraction of player wins for 50000 simulations]
    # this information will be appended below in the for loops
    results = [[] for x in range(273)]
    
    # lists to keep track of the number of times a natural blackjack occurs (we are calculating this for the cases of 0,1,2 hits just to have more data, the results aren't dependent on the number of times the player hits)
    natural_blackjack_0 = []
    natural_blackjack_1 = []
    natural_blackjack_2 = []
     
    
    # count is used to keep track of the specific list in the results list that information should be appended to
    # for instance: 
        # results[0] corresponds to the initial hand [2,2] with 0 hits
        # results[1] corresponds to the initial hand [2,2] with 1 hit
        # results[2] corresponds to the initial hand [2,2] with 2 hits
    count = 0
    
    # iterate through each possible initial hand
    for i in range(len(initial_hand_combos)):
        # iterate through each possible number of hits (0, 1, or 2)
        for j in range(len(num_hits)):
            # initialize an empty list that we will append 0's (player loses) or 1's (player wins) to
            num_wins = []
            
            # list to keep track of the number of times a natural blackjack occurs in the 50,000 simulations of a particular case
            blackjack_natural = []
            
            # first append the initial hand sum to the specific list in the results list
            results[count].append(sum(initial_hand_combos[i]))
            # then append the total number of hits to the specific list in the results list
            results[count].append(num_hits[j])
            
            
            # for each initial hand and for each possible number of hits, run 50,000 simulations to determine the probability that the player beats the dealer
            for k in range(N+1):
                # initialize the deck of 52 cards for each simulation
                deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11]
                
                # empty list that the dealer's initial two cards will be appended to
                dealer_initial_hand = []
    
                # randomly draw two cards from the deck for the dealer's initial hand
                card1 = random.choice(deck)
                deck.remove(card1)
                dealer_initial_hand.append(card1)
                card2 = random.choice(deck)
                deck.remove(card2)
                dealer_initial_hand.append(card2)
                
                # sum the dealer's initial hand to check if the dealer was dealt a natual blackjack
                dealer_initial_sum = sum(dealer_initial_hand)
                if dealer_initial_sum == 21:
                    # append a '1' to the blackjack list if the dealer was dealt a natural blackjack
                    blackjack_natural.append('1')
                
                
                # first give the player an initial starter hand from the list of all possible combinations
                player_hand = initial_hand_combos[i].copy()
                # then remove the two cards in the player's initial hand from the deck
                deck.remove(initial_hand_combos[i][0])
                deck.remove(initial_hand_combos[i][1])
                
                # if the player hits 0 times
                if num_hits[j] == 0:
                    # evalute the player's hand to determine what value to assign to aces (1 or 11) if aces are present in the hand
                    player_hand_updated = eval_ace(player_hand)
                    
                    # sum the player's hand to find the player's final hand sum
                    player_final_hand_sum = sum(player_hand_updated)
                    
                # if the player hits 1 time
                elif num_hits[j] == 1:
                    # randomly draw a card from the deck
                    new_card = random.choice(deck)
                    deck.remove(new_card)
                    player_hand.append(new_card)
                    
                    # evalute the player's hand to determine what value to assign to aces (1 or 11) if aces are present in the hand
                    player_hand_updated = eval_ace(player_hand)
                    
                    # sum the player's hand to find the player's final hand sum
                    player_final_hand_sum = sum(player_hand_updated)
                
                # if the player hits 2 times
                else:
                    # randomly draw two cards from the deck
                    new_card = random.choice(deck)
                    deck.remove(new_card)
                    player_hand.append(new_card)
                    new_card = random.choice(deck)
                    deck.remove(new_card)
                    player_hand.append(new_card)
                    
                    # evalute the player's hand to determine what value to assign to aces (1 or 11) if aces are present in the hand
                    player_hand_updated = eval_ace(player_hand)
                    
                    # sum the player's hand to find the player's final hand sum
                    player_final_hand_sum = sum(player_hand_updated)
                    
    
                # now that the player has hit either 0, 1, or 2 times, call the dealer function so the dealer can continue to
                # hit until their sum is greater than or equal to 17
                dealer_final_hand = dealer(dealer_initial_hand, deck)
                dealer_final_hand_sum = sum(dealer_final_hand)
                
                # now check if the player won or lost based on the final sums of the player and dealer
                outcome = game_win(player_final_hand_sum, dealer_final_hand_sum)
                
                # append the outcome (player win: 1, player loss: 0) to the num_wins list
                num_wins.append(outcome)
            
            # after all 50,000 simulations, append the fraction of player wins to the specific list in the results list
            results[count].append((sum(num_wins))/(len(num_wins)))
            
            
            # append the results for the natural blackjack to the list based on what simulation was ran (0, 1, or 2 hits)
            if num_hits[j] == 0:
                natural_blackjack_0.append((len(blackjack_natural)/N))
            elif num_hits[j] == 1:
                natural_blackjack_1.append((len(blackjack_natural)/N))
            elif num_hits[j] == 2:
                natural_blackjack_2.append((len(blackjack_natural)/N))
                
            # increase the count
            count += 1
    
    # take the mean of all the probabilities of being a dealt a natural blackjack
    natural_blackjack_final_0 = statistics.mean(natural_blackjack_0)
    natural_blackjack_final_1 = statistics.mean(natural_blackjack_1)
    natural_blackjack_final_2 = statistics.mean(natural_blackjack_2)
    
    # the following value is the probability of being dealt a natural blackjack
    natural_blackjack = statistics.mean([natural_blackjack_final_0,natural_blackjack_final_1,natural_blackjack_final_2])
    natural_blackjack_percent = natural_blackjack*100
    print('The probability of being dealt a natural blackjack is ' + str(natural_blackjack_percent) + "%.")

###############################################################################
    # create a table and plots to display the results
    
    # initialize x and y lists for number of hits = 0
    x_0 = []
    y_0 = []
    
    # initialize x and y lists for number of hits = 1
    x_1 = []
    y_1 = []
    
    # initialize x and y lists for number of hits = 2
    x_2 = []
    y_2 = []
    
    # iterate through the results list
    for i in range(len(results)):
        
        # this first case is for the initial hand sum [11,11] (two aces) for the case where hits = 0
        # in this case, the initial hand sum is appended to the results list as 22, but it is actually evaluated as a 12 by the eval_ace
        # function since a hand of only 2 aces would have to be evaluated as an 11 and a 1 to avoid busting
        if results[i][0] == 22:
            # change the value from 22 to 12
            results[i][0] = 12
            
        # this condition is met if the number of hits = 0 (hits are in the index = 1 spot of each list in the results list) 
        if results[i][1] == 0:
            # append the initial hand sum (in the index = 0 position of each list) to the x-values list
            x_0.append(results[i][0])
            # append the fraction of player wins (in the index = 2 position of each list) to the y-values list
            y_0.append(results[i][2])
            
        # this condition is met if the number of hits = 1 (hits are in the index = 1 spot of each list in the results list) 
        elif results[i][1] == 1:
            # append the initial hand sum (in the index = 0 position of each list) to the x-values list
            x_1.append(results[i][0])
            # append the fraction of player wins (in the index = 2 position of each list) to the y-values list
            y_1.append(results[i][2]) 
            
        # this condition is met if the number of hits = 2 (hits are in the index = 1 spot of each list in the results list) 
        elif results[i][1] == 2:
            # append the initial hand sum (in the index = 0 position of each list) to the x-values list
            x_2.append(results[i][0])
            # append the fraction of player wins (in the index = 2 position of each list) to the y-values list
            y_2.append(results[i][2])
    
    
    # make a table to display the results

    # create a list of possible initial hand sum values (integers 4-21)    
    initial_hand_sum_values = []
    for i in range(4,22):
        initial_hand_sum_values.append(i)
    
    # note that x_0, x_1, x_2 are exactly the same lists
    
    # sort the x_0 values
    x_0_sorted = sorted(x_0)
    
    # determine the order of the indices that sort the x_0 values
    x_0_sorted_indices = np.argsort(x_0)
    
    # re-order the y-values based on the order of the sorted x_0 indices
    y_0_sorted = [y_0[i] for i in x_0_sorted_indices]
    y_1_sorted = [y_1[i] for i in x_0_sorted_indices]
    y_2_sorted = [y_2[i] for i in x_0_sorted_indices]
    

    # initialize empty lists to be used below
    list4 = [[],[],[]]
    list5 = [[],[],[]]
    list6 = [[],[],[]]
    list7 = [[],[],[]]
    list8 = [[],[],[]]
    list9 = [[],[],[]]
    list10 = [[],[],[]]
    list11 = [[],[],[]]
    list12 = [[],[],[]]
    list13 = [[],[],[]]
    list14 = [[],[],[]]
    list15 = [[],[],[]]
    list16 = [[],[],[]]
    list17 = [[],[],[]]
    list18 = [[],[],[]]
    list19 = [[],[],[]]
    list20 = [[],[],[]]
    list21 = [[],[],[]]
    
    for i in range(len(x_0_sorted)):
            if x_0_sorted[i] == 4:
                list4[0].append(y_0_sorted[i])
                list4[1].append(y_1_sorted[i])
                list4[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 5:
                list5[0].append(y_0_sorted[i])
                list5[1].append(y_1_sorted[i])
                list5[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 6:
                list6[0].append(y_0_sorted[i])
                list6[1].append(y_1_sorted[i])
                list6[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 7:
                list7[0].append(y_0_sorted[i])
                list7[1].append(y_1_sorted[i])
                list7[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 8:
                list8[0].append(y_0_sorted[i])
                list8[1].append(y_1_sorted[i])
                list8[2].append(y_2_sorted[i])   
            elif x_0_sorted[i] == 9:
                list9[0].append(y_0_sorted[i])
                list9[1].append(y_1_sorted[i])
                list9[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 10:
                list10[0].append(y_0_sorted[i])
                list10[1].append(y_1_sorted[i])
                list10[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 11:
                list11[0].append(y_0_sorted[i])
                list11[1].append(y_1_sorted[i])
                list11[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 12:
                list12[0].append(y_0_sorted[i])
                list12[1].append(y_1_sorted[i])
                list12[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 13:
                list13[0].append(y_0_sorted[i])
                list13[1].append(y_1_sorted[i])
                list13[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 14:
                list14[0].append(y_0_sorted[i])
                list14[1].append(y_1_sorted[i])
                list14[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 15:
                list15[0].append(y_0_sorted[i])
                list15[1].append(y_1_sorted[i])
                list15[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 16:
                list16[0].append(y_0_sorted[i])
                list16[1].append(y_1_sorted[i])
                list16[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 17:
                list17[0].append(y_0_sorted[i])
                list17[1].append(y_1_sorted[i])
                list17[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 18:
                list18[0].append(y_0_sorted[i])
                list18[1].append(y_1_sorted[i])
                list18[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 19:
                list19[0].append(y_0_sorted[i])
                list19[1].append(y_1_sorted[i])
                list19[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 20:
                list20[0].append(y_0_sorted[i])
                list20[1].append(y_1_sorted[i])
                list20[2].append(y_2_sorted[i])
            elif x_0_sorted[i] == 21:
                list21[0].append(y_0_sorted[i])
                list21[1].append(y_1_sorted[i])
                list21[2].append(y_2_sorted[i])
    
    # take the average of all results
    fraction4 = [statistics.mean(list4[i]) for i in range(0,3)]
    fraction5 = [statistics.mean(list5[i]) for i in range(0,3)]
    fraction6 = [statistics.mean(list6[i]) for i in range(0,3)]
    fraction7 = [statistics.mean(list7[i]) for i in range(0,3)]
    fraction8 = [statistics.mean(list8[i]) for i in range(0,3)]
    fraction9 = [statistics.mean(list9[i]) for i in range(0,3)]
    fraction10 = [statistics.mean(list10[i]) for i in range(0,3)]
    fraction11 = [statistics.mean(list11[i]) for i in range(0,3)]
    fraction12 = [statistics.mean(list12[i]) for i in range(0,3)]
    fraction13 = [statistics.mean(list13[i]) for i in range(0,3)]
    fraction14 = [statistics.mean(list14[i]) for i in range(0,3)]
    fraction15 = [statistics.mean(list15[i]) for i in range(0,3)]
    fraction16 = [statistics.mean(list16[i]) for i in range(0,3)]
    fraction17 = [statistics.mean(list17[i]) for i in range(0,3)]
    fraction18 = [statistics.mean(list18[i]) for i in range(0,3)]
    fraction19 = [statistics.mean(list19[i]) for i in range(0,3)]
    fraction20 = [statistics.mean(list20[i]) for i in range(0,3)]
    fraction21 = [statistics.mean(list21[i]) for i in range(0,3)]
    
    
    fraction_0hits = [fraction4[0],fraction5[0],fraction6[0],fraction7[0],fraction8[0],fraction9[0],fraction10[0],fraction11[0],fraction12[0],fraction13[0],fraction14[0],fraction15[0],fraction16[0],fraction17[0],fraction18[0],fraction19[0],fraction20[0],fraction21[0]]
    fraction_1hits = [fraction4[1],fraction5[1],fraction6[1],fraction7[1],fraction8[1],fraction9[1],fraction10[1],fraction11[1],fraction12[1],fraction13[1],fraction14[1],fraction15[1],fraction16[1],fraction17[1],fraction18[1],fraction19[1],fraction20[1],fraction21[1]]
    fraction_2hits = [fraction4[2],fraction5[2],fraction6[2],fraction7[2],fraction8[2],fraction9[2],fraction10[2],fraction11[2],fraction12[2],fraction13[2],fraction14[2],fraction15[2],fraction16[2],fraction17[2],fraction18[2],fraction19[2],fraction20[2],fraction21[2]]

    # round the results to 4 decimal places
    fraction_0hits = [round(i,4) for i in fraction_0hits]
    fraction_1hits = [round(i,4) for i in fraction_1hits]
    fraction_2hits = [round(i,4) for i in fraction_2hits]

    table_results = Table([initial_hand_sum_values,fraction_0hits,fraction_1hits,fraction_2hits],names=('Initial Hand Sum','0 Hits', '1 Hit', '2 Hit'))
    
    #print(table_results)
    table_results.show_in_browser()
    
    
    # plot for number of hits = 0
    plt.figure()
    plt.scatter(initial_hand_sum_values,fraction_0hits)
    plt.xlabel('Initial Hand Sum of Player')
    plt.ylabel('Fraction of Player Wins')
    plt.title('Fraction of Wins vs Initial Hand Sum of Player (0 Hits)')
    plt.xticks(initial_hand_sum_values)
    plt.grid()
    plt.savefig('0 hits',dpi=600)
    
    # plot for number of hits = 1
    plt.figure()
    plt.scatter(initial_hand_sum_values,fraction_1hits)
    plt.xlabel('Initial Hand Sum of Player')
    plt.ylabel('Fraction of Player Wins')
    plt.title('Fraction of Wins vs Initial Hand Sum of Player (1 Hit)')
    plt.xticks(initial_hand_sum_values)
    plt.grid()
    plt.savefig('1 hits',dpi=600)
    
    # plot for number of hits = 2
    plt.figure()
    plt.scatter(initial_hand_sum_values,fraction_2hits)
    plt.xlabel('Initial Hand Sum of Player')
    plt.ylabel('Fraction of Player Wins')
    plt.title('Fraction of Wins vs Initial Hand Sum of Player (2 Hits)')
    plt.xticks(initial_hand_sum_values)
    plt.grid()
    plt.savefig('2 hits',dpi=600)
    
    plt.show()
    
main()
