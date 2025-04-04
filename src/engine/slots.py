import random

from src.utils.input import int_input
from pygame import K_SPACE, K_UP, K_DOWN, K_r, K_a, K_ESCAPE
from src.engine.ui.textButton import TextButton
from src.engine.logger import info
from src.engine.state.state import State
from src.engine.inputManager import InputManager

balance = 10
winning = 0
bet = 0
total = 0


# symbolen die gerolt kunnen worden
symbols = ["cherry","cherry","lemon","grapes","watermelon","seven"]

# het rollen van de drie symbolen die mogelijk zijn
def rolling():
    slot_1 = random.choice(symbols)
    slot_2 = random.choice(symbols)
    slot_3 = random.choice(symbols)
    return slot_1, slot_2, slot_3

#bepaald of je wint en hoeveel je dan wint
def win_amount(rolling, balance, winning, bet, total):
    if rolling[0] == "cherry" and rolling[1] == "cherry" or rolling[1] == "cherry" and rolling[2] == "cherry" or rolling[0] == "cherry" and rolling[2] == "cherry" :
        winning = bet * 2
        balance += winning
        total += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning, total
    if rolling[0] == "cherry" and rolling[1] == "cherry" and rolling[2] == "cherry":
        winning = bet * 5
        balance += winning
        total += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning, total
    if rolling[0] == "lemon" and rolling[1] == "lemon" and rolling[2] == "lemon":
        winning = bet * 10
        balance += winning
        total += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning, total
    if rolling[0] == "grapes" and rolling[1] == "grapes" and rolling[2] == "grapes":
        winning = bet * 15
        balance += winning
        total += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning, total
    if rolling[0] == "watermelon" and rolling[1] == "watermelon" and rolling[2] == "watermelon":
        winning = bet * 20
        balance += winning
        total += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning, total
    if rolling[0] == "seven" and rolling[1] == "seven" and rolling[2] == "seven":
        winning = bet * 30
        balance += winning
        total += winning
        return balance, winning, total
    else:
        balance -= bet
        print(f"You lost: {bet} and your balance is now: {balance}")
        return balance, 0, total

def main():
    global bet, balance
    print("Welcome to the Slots Game!")
    print(f"Youre balance is now: {balance}")
    #checkt of je nog wel kan inzetten of niet meer inzet dan dat je kan
    while balance > 0:
        bet = int_input("Enter bet: ")
        if bet <= 0:
            print("You cant bet nothing.")
            continue
        if bet > balance:
            print("Sorry, you don't have enough money!")
            continue
        #spint de slots en en roept de checker aan
        input("press enter to spin the slots")
        rols = rolling()
        print(f"slot 1: {rols[0]}, slot 2: {rols[1]}, slot 3: {rols[2]}")
        win_amount(rolling(), balance, winning, bet, total)
        #vraagt of je opnieuw wilt of niet en of dat wel kan
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing! Goodbye!")
            break
        elif play_again == "yes" and balance == 0:
            print("Sorry, you don't have enough money left")
            break
# op deze manier start de code niet via de commandline
if __name__ == "__main__":
    main()
#bepaald de status van het spel
class SlotsState(State):
    def __init__(self):
        super().__init__()

        self.background_color = "Black"

        self.buttons = []

        self.balance = 10
        self.winning = 0
        self.bet = 0
        self.total = 0

        self.roll_results = None
        self.win_results = None

# hier wordt aangeroepen wat nodig is om het spel te starten
    def transition_cue(self):
        self.roll_results = rolling()
        self.win_results = win_amount(self.roll_results, self.balance, self.winning, self.bet, self.total)
        info(self.roll_results)

# dit zorgt ervoor dat keyboard inputs iets doen
    def update(self, inputManager: InputManager, stateMachine):
        if inputManager.is_key_held(K_r):
            s = SlotsState()
            s.balance = 5
            stateMachine.start_transitie(s, .25)
        if inputManager.is_key_held(K_a):
            self.bet = self.balance
        if inputManager.is_key_down(K_ESCAPE):
            from src.states.chooseState import ChooseState
            stateMachine.start_transitie(ChooseState.from_slots(self.balance), 1)
        if inputManager.is_key_down(K_SPACE) and self.bet > 0:
            self.roll_results = rolling()
            self.win_results = win_amount(self.roll_results, self.balance, self.winning, self.bet, self.total)
            info(self.roll_results)
        if inputManager.is_key_down(K_UP):
            self.bet += 1
        elif inputManager.is_key_down(K_DOWN):
            self.bet -= 1
        if self.bet > self.balance:
            self.bet = self.balance
        if self.bet < 0:
            self.bet = 0


    def draw(self, renderer):
        #dit tekent 3 vierkanten zodat de icoontjes beter in het midden van de slot machine
        renderer.draw_rect((20, 230, 190), 0, 0, 2000, 1000)
        s1 = renderer.draw_rect("hotpink", 302, 290, 88, 192)
        s2 = renderer.draw_rect("hotpink", 398, 290, 88, 192)
        s3 = renderer.draw_rect("hotpink", 494, 290, 88, 192)
        renderer.draw_image("assets/slotsmachine.png", 190, 100, 8)
        #hier tekent de machine de resultaten van het rollen zodat de goede icoontjes op het beeld komen
        if self.roll_results is not None:
            if self.roll_results[0] != "nothing":
                renderer.draw_image_centered(f"assets/{self.roll_results[0]}.png", s1, 1.6)
            if self.roll_results[1] != "nothing":
                renderer.draw_image_centered(f"assets/{self.roll_results[1]}.png", s2, 1.6)
            if self.roll_results[2] != "nothing":
                renderer.draw_image_centered(f"assets/{self.roll_results[2]}.png", s3, 1.6)
        #hier laat het zien hoeveel balance je hebt en hoeveel je wint en totaal gewonnen hebt
        s = f"Balance: {self.balance}{f", Won: {self.win_results[1]}, Total Winnings: {self.win_results[2]}" if self.win_results else ""}"
        if self.win_results:
            self.balance = self.win_results[0]
            self.winning = self.win_results[1]
            self.total = self.win_results[2]
        #hier is de tekst die de uitleg geeft
        renderer.draw_text_x_centered(s, 30, size=30)
        renderer.draw_text_x_centered(f"Bet: {str(self.bet)}", 80, size=30)
        renderer.draw_text("a = all in.", 50, 80, size=30,)
        renderer.draw_text("arrows = higher/lower bet.", 133, 100, size=30)
        renderer.draw_text("space = spin.", 70, 120, size=30)
        renderer.draw_text("r = reset.", 50, 140, size=30)
        renderer.draw_text("esc = cash out.", 80, 160, size=30)
