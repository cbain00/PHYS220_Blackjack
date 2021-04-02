import random
import matplotlib.pyplot as plt

def dealer(hand, deck):
    hand = eval_ace(hand)
    
    while sum(hand) < 17:
        new_card = random.choice(deck)
        deck.remove(new_card)
        hand.append(new_card)
        hand = eval_ace(hand)
    return hand

def eval_ace(hand):
    #if you have any aces in your hand
    if 11 in hand:
        #this loop exists because theoretically every card in your hand could be an ace
        for i in range(len(hand)):
            total = sum(hand)
            if 11 in hand and total > 21:
                # at first position where ace = 11, replace by ace = 1.
                position_ace = hand.index(11)
                hand[position_ace] = 1
    return hand

def game_win(player_hand_sum, dealer_hand_sum):
    if player_hand_sum > 21:
        return 0
    elif dealer_hand_sum > 21:
        return 1
    elif player_hand_sum > dealer_hand_sum:
        return 1
    else: 
        return 0

def main():
    
    sum_combos = [[2,2],[2,3],[2,4],[3,3],[2,5],[3,4],[2,6],[3,5],[4,4],[2,7],[3,6],[4,5],[2,8],[3,7],[4,6],[5,5],[2,9],[3,8],[4,7],[5,6],[2,10],[3,9],[4,8],[5,7],[6,6],[11,11],[3,10],[4,9],[5,8],[6,7],[11,2],[4,10],[5,9],[6,8],[7,7],[11,3],[5,10],[6,9],[7,8],[11,4],[6,10],[7,9],[8,8],[11,5],[7,10],[8,9],[11,6],[8,10],[9,9],[11,7],[9,10],[11,8],[10,10],[11,9],[10,11]]
    hit_list = [0,1,2]
    
    list165 = [[] for x in range(165)]
    
    count = 0
    for i in range(len(sum_combos)):
        for j in range(len(hit_list)):
            wins = []
            list165[count].append(sum(sum_combos[i]))
            list165[count].append(hit_list[j])
            for k in range(101):
                deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11]
                dealer_init_hand = []
    
                #drawing first two cards for dealer
                card1 = random.choice(deck)
                deck.remove(card1)
                dealer_init_hand.append(card1)
                card2 = random.choice(deck)
                deck.remove(card2)
                dealer_init_hand.append(card2)
                
                player_hand_init = sum_combos[i].copy()
                deck.remove(sum_combos[i][0])
                deck.remove(sum_combos[i][1])
                
                if hit_list[j] == 0:
                    player_hand_sum = sum(player_hand_init)
                    
                elif hit_list[j] == 1:
                    new_card = random.choice(deck)
                    deck.remove(new_card)
                    player_hand_init.append(new_card)
                    player_hand = eval_ace(player_hand_init)
                    
                    player_hand_sum = sum(player_hand)
                    
                else:
                    new_card = random.choice(deck)
                    deck.remove(new_card)
                    player_hand_init.append(new_card)
                    new_card = random.choice(deck)
                    deck.remove(new_card)
                    player_hand = eval_ace(player_hand_init)
                    
                    player_hand_sum = sum(player_hand)
                    
    
                #This is where dealer's final hand is determined
                dealer_final_hand = dealer(dealer_init_hand, deck)
                dealer_hand_sum = sum(dealer_final_hand)
                
                outcome = game_win(player_hand_sum, dealer_hand_sum)
                wins.append(outcome)
            
            list165[count].append((sum(wins))/(len(wins)))
            count += 1
    print(list165)
    
    x_0 = []
    y_0 = []
    x_1 = []
    y_1 = []
    x_2 = []
    y_2 = []
    for i in range(len(list165)):
        if list165[i][0] == 22:
            list165[i][0] = 12
        if list165[i][1] == 0:
            x_0.append(list165[i][0])
            y_0.append(list165[i][2])
        elif list165[i][1] == 1:
            x_1.append(list165[i][0])
            y_1.append(list165[i][2]) 
        elif list165[i][1] == 2:
            x_2.append(list165[i][0])
            y_2.append(list165[i][2])
            
    plt.figure()
    plt.scatter(x_0,y_0)
    plt.figure()
    plt.scatter(x_1,y_1)
    plt.figure()
    plt.scatter(x_2,y_2)
    plt.show()
    
main()
