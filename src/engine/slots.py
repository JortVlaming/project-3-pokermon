import random
balance = 10
winning = 0


# symbolen die gerolt kunnen worden
symbols = ["nothing", "cherry", "nothing", "lemon", "nothing", "grapes", "nothing", "watermelon", "nothing", "seven", "nothing"]

# het rollen van de drie symbolen die mogelijk zijn
def rolling():
    slot_1 = random.choice(symbols)
    slot_2 = random.choice(symbols)
    slot_3 = random.choice(symbols)
    return slot_1, slot_2, slot_3

# bepaald of de symbolen hetzelfde zijn
def checker(rolling):
    return rolling[0] == rolling[1] == rolling[2]

#bepaald of je wint en hoeveel je dan wint
def win_amount(rolling):
    global balance
    global winning
    global bet
    if rolling[0] == "cherry" or rolling[1] == "cherry" or rolling[2] == "cherry":
        winning = bet * 1
        balance += winning
        print(f"You get: {winning} back and your balance is still : {balance}")
        return balance, winning
    if rolling[0] == "cherry" and rolling[1] == "cherry" or rolling[2] == "cherry" and rolling[3] == "cherry" or rolling[0] == "cherry" and rolling[2] == "cherry" :
        winning = bet * 3
        balance += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning
    if rolling[0] == "cherry" and rolling[1] == "cherry" and rolling[2] == "cherry":
        winning = bet * 4
        balance += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning
    if rolling[0] == "lemon" and rolling[1] == "lemon" and rolling[2] == "lemon":
        winning = bet * 5
        balance += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning
    if rolling[0] == "grapes" and rolling[1] == "grapes" and rolling[2] == "grapes":
        winning = bet * 6
        balance += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning
    if rolling[0] == "watermelon" and rolling[1] == "watermelon" and rolling[2] == "watermelon":
        winning = bet * 7
        balance += winning
        print(f"You won: {winning} and your balance is now: {balance}")
        return balance, winning
    if rolling[0] == "seven" and rolling[1] == "seven" and rolling[2] == "seven":
        winning = bet * 8
        balance += winning
        return balance, winning
    else:
        balance -= bet
        print(f"You lost: {bet} and your balance is now: {balance}")
        return balance, winning

def main():
    global bet
    print("Welcome to the Slots Game!")
    while balance >= 0:
        try:
            bet = int(input("Enter bet: "))
            break
        except:
            print("Sorry, that's not a valid number.")

        if bet <= 0:
            print("Sorry, you cant bet nothing")

        elif bet > balance:
            print("Sorry, you don't have enough money!")
        else:
            input("press enter to spin the slots")
            rols = rolling()
            print(f"slot 1: {rols[0]}, slot 2: {rols[1]}, slot 3: {rols[2]}")
            win = win_amount(rols)

            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again != "yes":
                print("Thanks for playing! Goodbye!")
                break
main()