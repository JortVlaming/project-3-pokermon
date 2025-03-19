import random

# symbolen die gerolt kunnen worden
symbols = ["cherry", "lemon", "grapes", "watermelon","seven"]

# het rollen van de drie symbolen die mogelijk zijn
def rolling():
    slot_1 = random.choice(symbols)
    slot_2 = random.choice(symbols)
    slot_3 = random.choice(symbols)
    return slot_1, slot_2, slot_3

# bepaald of de symbolen hetzelfde zijn
def checker(rolling):
    return rolling[0] == rolling[1] == rolling[2], 0

def main():
    print("Welcome to the Slots Game!")
    input("press enter to spin the slots")
    while True:
        rols = rolling()
        print(f"slot 1: {rols[0]}, slot 2: {rols[1]}, slot 3: {rols[2]}")
        gewonnen, payout = checker(rols)
        if gewonnen:
            print(f"You win! {payout}")
        else:
            print("You lose!")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing! Goodbye!")
            break



main()