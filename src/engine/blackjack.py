import os
import random
import time

card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(suits, card) for suits in card_suits for card in cards_list]

def clear():
    if "TERM" not in os.environ:
        return
    os.system("clear" if os.name != "nt" else "cls")

def card_value(card):
    if card[1] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[1] == 'Ace':
        return 11
    else:
        return int(card[1])

def hand_str(hand):
    r = ""

    for card in hand:
        r = r + card[1] + " of " + card[0] + ", "

    r = r[:-2]

    return r

def card_str(card):
    return card[1] + " of " + card[0]

def hand_val(hand):
    return sum(card_value(card) for card in hand)

random.shuffle(deck)
player_card = [deck.pop(), deck.pop()]
dealer_card = [deck.pop(), deck.pop()]

while True:
    clear()
    player_score = hand_val(player_card)
    print("Player has:", hand_str(player_card))
    print("Score of player:", player_score)
    print("")
    print("Dealer has:", card_str(dealer_card[0]) + ", ?")
    print("Score of dealer:", card_value(dealer_card[0]))
    if player_score == 21:
        print("Player wins (Player has blackjack)")
        break
    elif player_score > 21:
        print("Dealer wins (Player exceeds 21)")
        break
    dealer_score = hand_val(dealer_card)
    print("\n")
    choice = ""
    stop_game = False
    while choice != "stop" and choice != "stand" and not stop_game:
        choice = input('What do you want? ["hit" to request another card, "stand" to continue to dealer, "stop" to stop]: ').lower()
        if choice == 'hit':
            new_card = deck.pop()
            player_card.append(new_card)
            player_score = hand_val(player_card)
            clear()
            print("Player has:", hand_str(player_card))
            print("Score of player:", player_score)
            print("")
            print("Dealer has:", card_str(dealer_card[0]) + ", ?")
            print("Score of dealer:", card_value(dealer_card[0]))
            if player_score == 21:
                print("Player wins (Player has blackjack)")
                stop_game = True
                break
            elif player_score > 21:
                print("Dealer wins (Player exceeded 21)")
                stop_game = True
                break
        elif choice == 'stop':
            stop_game = True
            break
        elif choice == "stand":
            break
        else:
            print("Invalid input. Please try again.")
            time.sleep(1)
            continue

    if stop_game:
        break

    if player_score > 21:
        print("Cards dealer has:", hand_str(dealer_card))
        print("Score of dealer:", dealer_score)
        print("Cards player has:", hand_str(player_card))
        print("Score of player:", player_score)
        print("Dealer (Player loss because player score exceeds 21)")
        break


    while dealer_score < 17:
        new_card = deck.pop()
        dealer_card.append(new_card)
        dealer_score += card_value(new_card)
        print("Dealer pulls", card_str(new_card))
        print("Dealer has:", hand_str(dealer_card))
        print("Dealer score:", hand_val(dealer_card))
        print("")
        time.sleep(1)


    if dealer_score > 21:
        print("Cards dealer has:", hand_str(dealer_card))
        print("Score of dealer:", dealer_score)
        print("Cards player has:", hand_str(player_card))
        print("Score of player:", player_score)
        print("Dealer (Dealer loss because score exceeds 21)")
    elif player_score > dealer_score:
        print("Cards dealer has:", hand_str(dealer_card))
        print("Score of dealer:", dealer_score)
        print("Cards player has:", hand_str(player_card))
        print("Score of player:", player_score)
        print("Player wins (Player has higher score than dealer)")
    elif dealer_score > player_score:
        print("Cards dealer has:", hand_str(dealer_card))
        print("Score of dealer:", dealer_score)
        print("Cards player has:", hand_str(player_card))
        print("Score of player:", player_score)
        print("Dealer wins (Dealer has higher score than player)")
    else:
        print("Cards dealer has:", hand_str(dealer_card))
        print("Score of dealer:", dealer_score)
        print("Cards player has:", hand_str(player_card))
        print("Score of player:", player_score)
        print("It's a tie.")

    break