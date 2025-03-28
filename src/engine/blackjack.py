import os
import random
import time

from pygame import K_SPACE, K_RETURN, K_r

from src.engine.inputManager import InputManager
from src.engine.state.state import State
from src.engine.ui.textButton import TextButton

card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(suits, card) for suits in card_suits for card in cards_list]

def clear():
    if "TERM" not in os.environ:
        return
    os.system("clear" if os.name != "nt" else "cls")

def card_value(card):
    if card[1] in ['Jack', 'Queen', 'King', "J", "Q", "K"]:
        return 10
    elif card[1] == 'Ace' or card[1] == "A":
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

if __name__ == "__main__":
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


class BlackjackState(State):
    def __init__(self, points: int):
        super().__init__()
        self.background_color = "gray"
        self.buttons = []
        self.points = points
        card_suits = ['hart', 'schop', 'ruit', 'klaver']
        cards_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [(suits, card) for suits in card_suits for card in cards_list]
        random.shuffle(self.deck)
        self.player_cards = [self.deck.pop(), self.deck.pop()]
        self.dealer_cards = [self.deck.pop(), self.deck.pop()]
        self.do_win_checks(True)
        self.show_dealer_second = False

        hit_button = TextButton(
            255,
            500,
            100,
            75,
            "White",
            "Hit",
            "Black"
        )

        hit_button.set_on_click(lambda btn : self.draw_card_speler())

        stand_button = TextButton(
            375,
            500,
            150,
            75,
            "White",
            "Stand",
            "Black"
        )

        stand_button.set_on_click(lambda btn : self.draw_card_dealer())

        self.buttons = [hit_button, stand_button]

        self.dealer_is_pulling = False
        self.dealer_pull_timer = 0
        self.check_win_conditions_after_dealer_pulled = False

        # 0 = speler blackjack
        # 1 = speler busted
        # 2 = speler wint met meer punten
        # 3 = dealer blackjack
        # 5 = dealer busted
        # 6 = dealer wint met meer punten
        # 7 = gelijk spel
        # 8 = wachten voor reset
        self.win_state = -1

        self.player_bet = 1

    def draw_card_speler(self):
        new_card = self.deck.pop()
        self.player_cards.append(new_card)
        print(self.player_cards)

        s = hand_val(self.player_cards)
        if s == 21:
            # TODO speler heeft blackjack
            print("Speler heeft blackjack")
            self.buttons[0].do_render = False
            self.buttons[0].do_clicks = False
            self.buttons[1].do_render = False
            self.do_win_checks()
        elif s > 21:
            # TODO speler busted
            print("Speler busted")
            self.buttons[0].do_render = False
            self.buttons[0].do_clicks = False
            self.buttons[1].do_render = False
            self.do_win_checks()

    def draw_card_dealer(self):
        self.buttons[0].do_render = False
        self.buttons[1].do_render = False
        if not self.show_dealer_second:
            self.show_dealer_second = True
            self.dealer_is_pulling = True
            return
        new_card = self.deck.pop()
        self.dealer_cards.append(new_card)
        print(self.dealer_cards)

    def update(self, inputManager: InputManager, stateMachine):
        if inputManager.is_key_down(K_SPACE):
            self.draw_card_speler()
        if inputManager.is_key_down(K_r):
            stateMachine.start_transitie(BlackjackState(self.points), 0.1)
        if inputManager.is_key_down(K_RETURN):
            if not self.show_dealer_second:
                self.show_dealer_second = True
            else:
                self.draw_card_dealer()
        if self.dealer_is_pulling:
            if hand_val(self.dealer_cards) >= 17:
                self.dealer_is_pulling = False
                self.do_win_checks()
            self.dealer_pull_timer += 1
            if self.dealer_pull_timer >= 60:
                self.draw_card_dealer()
                self.dealer_pull_timer = 0

    def do_win_checks(self, initial_check: bool = False):
        speler_score = hand_val(self.player_cards)
        dealer_score = hand_val(self.dealer_cards)

        if speler_score == 21:
            self.win_state = 0
        elif dealer_score == 21:
            self.win_state = 3
        if not initial_check:
            if speler_score > 21:
                self.win_state = 1
            elif dealer_score > 21:
                self.win_state = 5
            else:
                if speler_score > dealer_score:
                    self.win_state = 2
                elif dealer_score > speler_score:
                    self.win_state = 6
                elif speler_score == dealer_score:
                    self.win_state = 7

        if self.win_state != -1:
            print(self.win_state)

            match self.win_state:
                case 0:
                    print("Speler heeft blackjack (3:2)")
                case 1:
                    print("Speler busted (0:1)")
                case 2:
                    print("Speler wint met meer punten (2:1)")
                case 3:
                    print("Dealer heeft blackjack (0:1)")
                case 5:
                    print("Dealer busted (2:1)")
                case 6:
                    print("Dealer wint met meer punten (0:1)")
                case 7:
                    print("Gelijk spel (1:1)")

            self.win_state = 8

    def draw(self, renderer):
        x = 255

        for card in self.player_cards:
            renderer.draw_image(
                f"assets/cards/{card[0]}/{card[0]}{card[1]}.png", x,
                400, 3)

            x += 100

        renderer.draw_text(str(hand_val(self.player_cards)), 180, 425, centered=False)

        x = 355

        if not self.show_dealer_second:
            renderer.draw_image(f"assets/cards/{self.dealer_cards[0][0]}/{self.dealer_cards[0][0]}{self.dealer_cards[0][1]}.png", x, 100, 3)
            renderer.draw_image(f"assets/cards/empty_card.png", x + 100,  100, 3)
            renderer.draw_text(str(card_value(self.dealer_cards[0])), 280, 125, centered=False)
        else:
            renderer.draw_text(str(hand_val(self.dealer_cards)), 280, 125, centered=False)
            for card in self.dealer_cards:
                renderer.draw_image(
                    f"assets/cards/{card[0]}/{card[0]}{card[1]}.png", x,
                    100, 3)

                x += 100


        # renderer.draw_image("assets/cards/hart/hart5.png", 255, 400,3)
        # renderer.draw_image("assets/cards/hart/hart6.png", 355, 400,3)
        renderer.draw_text(f"Jouw punten: {self.points} points", 10, 10, centered=False, size=48, color="Red")
        # renderer.draw_image("assets/cards/hart/hart7.png", 330, 100,3)
        # renderer.draw_image("assets/cards/empty_card.png", 430, 100, 3)