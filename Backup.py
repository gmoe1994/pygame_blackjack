# This is a game of blackjack. it's a simple version and you only goal is to beat the dealer.
import random


def get_cards(player):
    while len(player) < 2:
        player.append(random.choice(whole_deck))
        if len(player) == 2:
            if player[0] == player[1]:
                del player[-1]
                break
            else:
                whole_deck.remove(player[0])
                whole_deck.remove(player[1])
                break
        else:
            continue


def value_cards(player, _num):
    player = [e[2:] for e in player]
    for card in player:
        if "ace" in player[2:]:
            values["ace"] = 1
        _num.append(values[card])


def draw():
    player1.append(random.choice(whole_deck))
    whole_deck.remove(player1[len(player1) - 1])
    player1_num.clear()
    value_cards(player1, player1_num)


def stand():
    dealer.append(random.choice(whole_deck))
    whole_deck.remove(dealer[len(dealer) - 1])
    dealer_num.clear()
    value_cards(dealer, dealer_num)


def dealer_draws():
    print(f"the dealer has {dealer}, this amounts to: {sum(dealer_num)}\n")
    while sum(dealer_num) <= 21:
        if sum(dealer_num) <= 16:
            stand()
            print(f"the dealer draw {dealer}, this amounts to: {sum(dealer_num)}\n")
            if sum(dealer_num) > 21:
                if sum(player1_num) <= 21:
                    print("Dealer bust, you win!\n")
                else:
                    print("you both busted\n")
            elif 21 >= sum(dealer_num) > 16:
                if sum(dealer_num) > sum(player1_num):
                    print("Dealer wins\n")
                    break
                elif sum(dealer_num) < sum(player1_num) < 22:
                    print("You win!\n")
                    break
                elif sum(dealer_num) == sum(player1_num):
                    print("You draw the same, play again and show us who's the boss\n")
                    break
            else:
                continue
        else:
            if sum(dealer_num) > sum(player1_num) or sum(player1_num) >= 22:
                print("Dealer wins\n")
                break
            elif sum(dealer_num) < sum(player1_num) < 22:
                print("You win!\n")
                break
            elif sum(dealer_num) == sum(player1_num):
                print("You draw the same, play again and show us who's the boss\n")
                break


# value of the cards
values = {
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "jack": 10,
    "queen": 10,
    "king": 10,
    "ace": 11
}

whole_deck = []
play = []
while play != "quit":
    play = input("If you wish to quit write quit, else press enter: ")
    whole_deck.clear()

    # a loop to create a deck of 52 cards
    for i in values:
        whole_deck.append("s-" + i)
        whole_deck.append("h-" + i)
        whole_deck.append("c-" + i)
        whole_deck.append("d-" + i)

    # Which card was drawn?
    player1 = []
    dealer = []

    # whats the num of the cards?
    player1_num = []
    dealer_num = []

    # draw the cards
    get_cards(player1)
    get_cards(dealer)


    # get the value of the cards drawn
    value_cards(player1, player1_num)
    value_cards(dealer, dealer_num)

    if play == "quit":
        break

    elif sum(player1_num) == 21:
        print("Blackjack! you won\n")

    elif sum(dealer_num) == 21:
        print("Blackjack for the dealer, you lost\n")

    else:
        print(f"you draw {player1} this amounts to: {sum(player1_num)}\n")
        while sum(player1_num) < 21:
            action = input("stand or draw?: ")
            if action == "draw":
                draw()
                print(f"you draw {player1} this amounts to: {sum(player1_num)}\n")
                if sum(player1_num) > 21:
                    print("BUST!\n")
                    dealer_draws()
                    break
                elif sum(player1_num) == 21:
                    print("You draw 21!\n")
                    dealer_draws()
                    break
                else:
                    continue
            elif action == "stand":
                dealer_draws()
                break
