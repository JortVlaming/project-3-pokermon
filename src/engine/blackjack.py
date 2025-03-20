import random

card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(suits, card) for suits in card_suits for card in cards_list]


def card_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])

random.shuffle(deck)
player_card = [deck.pop(), deck.pop()]
dealer_card = [deck.pop(), deck.pop()]

while True:
    player_score = sum(card_value(player_card) for card in player_card)
    dealer_score = sum(card_value(dealer_card) for card in dealer_card)
    print("Card Player has: ", player_card)
    print("Score of player:", player_score)
    print("\n")
    choice = input('What do you want? ["play" to request another card, "stop" to stop]: ').lower()
    if choice == 'play':
        new_card = deck.pop()
        player_card.append(new_card)
    elif choice == 'stop':
        break
    else:
        print("Invalid input. Please try again.")
        continue

    if player_score > 21:
        print("Cards dealer has:", dealer_card)
        print("Score of dealer:", dealer_score)
        print("Cards player has:", player_card)
        print("Score of player:", player_score)
        print("Dealer (Player loss because player score exceeds 21)")
        break


    while dealer_score < 17:
        new_card = deck.pop()
        dealer_card.append(new_card)
        dealer_score += card_value(new_card)


    print("Cards dealer has:", dealer_card)
    print("Score of dealer:", dealer_score)
    print("\n")


    if dealer_score > 21:
        print("Cards dealer has:", dealer_card)
        print("Score of dealer:", dealer_score)
        print("Cards player has:", player_card)
        print("Score of player:", player_score)
        print("Dealer (Dealer loss because player score exceeds 21)")

    elif player_score > dealer_score:
        print("Cards dealer has:", dealer_card)
        print("Score of dealer:", dealer_score)
        print("Cards player has:", player_card)
        print("Score of player:", player_score)
        print("Player wins (Player has higher score than dealer)")

    elif dealer_score > player_score:
        print("Cards dealer has:", dealer_card)
        print("Score of dealer:", dealer_score)
        print("Cards player has:", player_card)
        print("Score of player:", player_score)
        print("Dealer wins (Dealer has higher score than player)")

    else:
        print("Cards dealer has:", dealer_card)
        print("Score of dealer:", dealer_score)
        print("Cards player has:", player_card)
        print("Score of player:", player_score)
        print("It's a tie.")