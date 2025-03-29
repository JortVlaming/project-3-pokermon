import os
import random
import time
from typing import List, Tuple

from pygame import K_r, K_UP, K_DOWN

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


def generate_deck() -> List[Tuple[str, int]]:
    card_suits = ['hart', 'schop', 'ruit', 'klaver']
    cards_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [(suits, card) for suits in card_suits for card in cards_list]
    random.shuffle(deck)
    return deck


class BlackjackState(State):
    def __init__(self, points: int):
        super().__init__()
        self.show_dealer_second = False
        self.player_cards = None
        self.dealer_cards = None
        self.background_color = "gray"
        self.buttons = []
        self.points = points
        self.deck = generate_deck()
        self.win_state = -2
        self.player_bet = 0
        self.restart_timer = -1

        hit_button = TextButton(255, 500, 100, 75, "White", "Hit", "Black")
        hit_button.set_on_click(lambda btn: self.draw_card_speler())

        stand_button = TextButton(375, 500, 150, 75, "White", "Stand", "Black")
        stand_button.set_on_click(lambda btn: self.draw_card_dealer())

        start_button = TextButton(350, 400, 200, 75, "White", "Start", "Black")
        start_button.set_on_click(lambda btn: self.start())

        quit_button = TextButton(350, 500, 200, 75, "White", "Quit", "Black")
        quit_button.set_on_click(lambda btn: self.quit())

        hit_button.do_render = False
        stand_button.do_render = False

        self.buttons = [hit_button, stand_button, start_button, quit_button]

        self.dealer_is_pulling = False
        self.dealer_pull_timer = 0
        self.check_win_conditions_after_dealer_pulled = False
        self.feedback_message = ""

    def start(self):
        if self.player_bet <= 0:
            return
        if self.player_bet > self.points:
            self.player_bet = self.points

        self.points -= self.player_bet
        self.win_state = -1

        self.player_cards = [self.deck.pop(), self.deck.pop()]
        self.dealer_cards = [self.deck.pop(), self.deck.pop()]

        self.buttons[2].do_render = False
        self.buttons[3].do_render = False

        self.do_win_checks(True)

        if self.win_state == -1:  # Only enable hit and stand if no instant win/loss
            self.buttons[0].do_render = True
            self.buttons[1].do_render = True
            self.buttons[2].do_render = False
            self.buttons[3].do_render = False

        self.show_dealer_second = False

    def draw_card_speler(self):
        new_card = self.deck.pop()
        self.player_cards.append(new_card)
        print(self.player_cards)

        s = hand_val(self.player_cards)
        if s == 21:
            print("Speler heeft blackjack")
            self.buttons[0].do_render = False
            self.buttons[0].do_clicks = False
            self.buttons[1].do_render = False
            self.do_win_checks()
        elif s > 21:
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

    def quit(self):
        from src.states.chooseState import ChooseState
        self.stateMachine.start_transitie(ChooseState.from_blackjack(self.points), 1)

    def do_win_checks(self, initial_check: bool = False):
        speler_score = hand_val(self.player_cards)
        dealer_score = hand_val(self.dealer_cards)

        if speler_score == 21:
            self.win_state = 0
            self.feedback_message = "Blackjack! You win!"
        elif dealer_score == 21:
            self.win_state = 3
            self.feedback_message = "Dealer got Blackjack! You lose."

        if not initial_check:
            if speler_score > 21:
                self.win_state = 1
                self.feedback_message = "You busted! Game over."
            elif dealer_score > 21:
                self.win_state = 5
                self.feedback_message = "Dealer busted! You win!"
            else:
                if speler_score > dealer_score:
                    self.win_state = 2
                    self.feedback_message = "You win! Higher score than dealer."
                elif dealer_score > speler_score:
                    self.win_state = 6
                    self.feedback_message = "Dealer wins! Higher score."
                elif speler_score == dealer_score:
                    self.win_state = 7
                    self.feedback_message = "It's a tie! Bet returned."

        if self.win_state >= 0:
            self.handle_payout()
            self.restart_timer = 180

    def handle_payout(self):
        payout = 0
        match self.win_state:
            case 0:  # Player blackjack (3:2)
                payout = int(self.player_bet * 1.5)
            case 1:  # Player busted (lose bet)
                payout = 0
            case 2:  # Player wins with more points (1:1)
                payout = self.player_bet * 2
            case 3:  # Dealer blackjack (lose bet)
                payout = 0
            case 5:  # Dealer busted (1:1)
                payout = self.player_bet * 2
            case 6:  # Dealer wins with more points (lose bet)
                payout = 0
            case 7:  # Tie (bet returned)
                payout = self.player_bet

        self.points += payout
        print(f"Payout: {payout}, New points: {self.points}")

    def update(self, inputManager: InputManager, stateMachine):
        self.stateMachine = stateMachine

        if self.restart_timer > 0:
            self.restart_timer -= 1
            if self.restart_timer == 0:
                self.stateMachine.start_transitie(BlackjackState(self.points), 1)

        if inputManager.is_key_down(K_r):
            stateMachine.start_transitie(BlackjackState(self.points), 0.1)
        if inputManager.is_key_down(K_UP):
            self.player_bet = min(self.player_bet + 1, self.points)
        if inputManager.is_key_down(K_DOWN):
            self.player_bet = max(self.player_bet - 1, 0)
        if self.dealer_is_pulling:
            if hand_val(self.dealer_cards) >= 17:
                self.dealer_is_pulling = False
                self.do_win_checks()
            self.dealer_pull_timer += 1
            if self.dealer_pull_timer >= 60:
                self.draw_card_dealer()
                self.dealer_pull_timer = 0

    def draw(self, renderer):
        if self.win_state == -2:
            renderer.draw_text_x_centered("Welcome to blackjack!", 40)
            renderer.draw_text_x_centered(f"Your bet: {self.player_bet}/{self.points}", 80)
            return
        elif self.win_state >= 0:
            renderer.draw_text_x_centered(self.feedback_message, 300, size=48)


        x = 255

        for card in self.player_cards:
            renderer.draw_image(
                f"assets/cards/{card[0]}/{card[0]}{card[1]}.png", x,
                350, 3)

            x += 100

        renderer.draw_text(str(hand_val(self.player_cards)), 180, 375, centered=False)

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

        renderer.draw_text(f"Jouw punten: {self.points} points", 10, 10, centered=False, size=48)