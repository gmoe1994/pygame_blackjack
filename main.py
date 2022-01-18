# This is a game of blackjack. it's a simple version and you only goal is to beat the dealer.
# The goal is to get Blackjack or 21, if you go over 21 you bust. Dealer has to draw on 16 and stand on 17 or higher.
import random
import pygame
import json
import time


# Get all pygame funcs and set screen res and window caption
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blackjack: Beat the dealer")

# variables for GUI
font = pygame.font.SysFont("comicsans", 30)
green = (46, 176, 48)
black = (0, 0, 0)
grey = (178, 180, 184)
red = (255, 0, 0)
blue = (0, 128, 255)

# sounds
flip_sound = pygame.mixer.Sound("Card-flip-sound-effect.wav")
win_sound = pygame.mixer.Sound("Game-show-winner-sound-effect.wav")


def score(player):
    """
    :param player: Takes in string of which player to score
    :return: adds score to player
    """
    highscore[player] += 1
    filename = "score.json"
    with open(filename, "w") as file:
        json.dump(highscore, file)


def get_score(player):
    """
    :param player: takes in string of which player to score
    :return: returns score of the chosen player
    """
    filename = "score.json"
    with open(filename) as file:
        score_list = json.load(file)
        return score_list[player]


def draw_screen():
    """
    A function for what will be displayed on screen
    :return: updated screen info
    """
# fills the screen with a green background
    screen.fill(green)

# Sets position for players cards and loads correct cards to screen
    player_x = 0
    player_y = 0
    for card in player1:
        screen.blit(pygame.image.load(card + ".png"), (player_x, player_y))
        player_x += 100

# Sets position for dealers cards and loads correct cards to screen
    dealer_x = 0
    dealer_y = 150
    for card in dealer:
        screen.blit(pygame.image.load(card + ".png"), (dealer_x, dealer_y))
        dealer_x += 100

# Text that is decided in main loop
    text = font.render(the_message, True, black)
    screen.blit(text, (0, 300))

# Buttons for Stand and Draw
    button("Draw", 150, 400, 100, 50, grey, blue)
    button("Stand", 400, 400, 100, 50, grey, red)

# text showing highscore
    text_player = font.render(f"Player score: {highscore['player']}", True, black)
    screen.blit(text_player, (0, 500))


# text showing highscore
    text_player = font.render(f"Dealer score: {highscore['dealer']}", True, black)
    screen.blit(text_player, (0, 550))

# updates display data
    pygame.display.update()


# This function is not my original code, it's inspired from https://pythonprogramming.net/pygame-button-function/
def button(action, x, y, w, h, inactive, active):
    """
    a function for buttons
    :param action: str with buttons action
    :param x: x pos
    :param y: y pos
    :param w: width of button
    :param h: height of button
    :param inactive: inactive color
    :param active: active color
    :return: a display of a button
    """
    mouse_pos = pygame.mouse.get_pos()
# checks if mouse is in same area as button, and changes it color
    if x + w > mouse_pos[0] > x and y + h > mouse_pos[1] > y:
        pygame.draw.rect(screen, active, (x, y, w, h))
    else:
        pygame.draw.rect(screen, inactive, (x, y, w, h))

# text for button
    text_action = font.render(action, True, black)
    screen.blit(text_action, (x + 20, y + 20))


def easy_shuffle():
    """
    adds spades, hearts, cubs and diamonds to every key/item in the list values, stores them in a list: whole_deck
    More explenation about the shuffling in project report.
    :return: Makes a list of 52 cards
    """
    whole_deck.clear()
    for i in values:
        whole_deck.append("s-" + i)
        whole_deck.append("h-" + i)
        whole_deck.append("c-" + i)
        whole_deck.append("d-" + i)


def get_cards(player):
    """
    Draws two cards and removes them from the deck
    :param player: which list to append cards
    :return: appends cards to the players list
    """
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
    """
    :param player: takes in list of players drawn cards
    :param _num: this is the list you want returned values in
    :return: value of the cards drawn into list
    """
    # remove "type" of card to pick out value of card from key in dict
    player = [card[2:] for card in player]
    for cards in player:
        _num.append(values[cards])


def draw(player, player_val):
    """
    Draws a card from deck, and removes that card from the deck,
    :return:
    """
    player.append(random.choice(whole_deck))
    whole_deck.remove(player[len(player) - 1])
    player_val.clear()
    value_cards(player, player_val)
    pygame.mixer.Sound.play(flip_sound)


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

# Program doesn't come with highscore file, therefore get_score funcs cannot run.
# Until a round of blackjack is finished, no highscore files will exist and score is set to 0
try:
    highscore = {"player": get_score("player"), "dealer": get_score("dealer")}
except FileNotFoundError:
    highscore = {"player": 0, "dealer": 0}


play = True
# while play loop is needed to shuffle the deck and get new cards, for every new round of the game
while play:

    # list with all cards in the deck
    whole_deck = []

    easy_shuffle()

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

    the_message = f"Player has: {sum(player1_num)}, Dealer has: {sum(dealer_num)}"
    game_runs = True
    # The main game loop.
    # Breaks every time there's a winner, to shuffle the deck and get new cards, for every new round of the game
    while game_runs:

        # checks for blackjack or 21, before user can interfere with buttons.
        if sum(player1_num) == 21:
            pygame.mixer.Sound.play(win_sound)
            if len(player1) == 2:
                the_message = "Blackjack! you win"
            else:
                the_message = "21! you win!"
            score("player")
            game_runs = False
        elif sum(dealer_num) == 21:
            if len(dealer) == 2:
                the_message = "Blackjack for the dealer, you lost"
            else:
                the_message = "21! dealer wins!"
            score("dealer")
            game_runs = False

        # Draws the cards and other data to the display
        draw_screen()
        right_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # executes an event based on user interference
        for event in pygame.event.get():

            # quits the game
            if event.type == pygame.QUIT:
                play = False
                game_runs = False

            # draws a new card if mouse is over draw button and right clicked
            elif 150 + 100 > mouse_pos[0] > 150 and 400 + 50 > mouse_pos[1] > 400:
                if right_click[0] == 1:
                    draw(player1, player1_num)
                    the_message = f"Player has: {sum(player1_num)}, Dealer has: {sum(dealer_num)}"

            # draws card/s for dealer if mouse is over stand button and right clicked, or if player has over 21
            elif (400 + 100 > mouse_pos[0] > 400 and 400 + 50 > mouse_pos[1] > 400) or sum(player1_num) > 21:
                if right_click[0] == 1 or sum(player1_num) > 21:
                    the_message = f"the dealer has: {sum(dealer_num)}"

                    # Draws card/s for dealer while it's sum under 17
                    # if sum of dealer cards is over 16, it checks if player or dealer is closer to 21
                    # 1 point will be added to the winner and the game is started over
                    while sum(dealer_num) <= 21:
                        if sum(dealer_num) <= 16:
                            draw(dealer, dealer_num)
                            the_message = f"the dealer has: {sum(dealer_num)}"
                            if sum(dealer_num) > 21:
                                if sum(player1_num) <= 21:
                                    pygame.mixer.Sound.play(win_sound)
                                    the_message = "You win!"
                                    score("player")
                                    game_runs = False
                                    break
                                else:
                                    the_message = "you both busted"
                                    game_runs = False
                                    break
                            elif 21 >= sum(dealer_num) > 16:
                                if sum(dealer_num) > sum(player1_num):
                                    the_message = "Dealer wins"
                                    score("dealer")
                                    game_runs = False
                                    break
                                elif sum(dealer_num) < sum(player1_num) <= 21:
                                    pygame.mixer.Sound.play(win_sound)
                                    the_message = "You win!"
                                    score("player")
                                    game_runs = False
                                    break
                                elif sum(dealer_num) == sum(player1_num):
                                    the_message = "You draw the same, play again and show us who's the boss"
                                    game_runs = False
                                    break
                            else:
                                continue
                        else:
                            if sum(dealer_num) > sum(player1_num) or sum(player1_num) >= 22:
                                the_message = "Dealer wins"
                                score("dealer")
                                game_runs = False
                                break
                            elif sum(dealer_num) < sum(player1_num) < 22:
                                pygame.mixer.Sound.play(win_sound)
                                the_message = "You win!"
                                score("player")
                                game_runs = False
                                break
                            elif sum(dealer_num) == sum(player1_num):
                                the_message = "You draw the same, play again and show us who's the boss"
                                game_runs = False
                                break
        draw_screen()
        # waits 2 seconds, for the user to see who wins before it starts over again
        if not game_runs:
            time.sleep(2)
pygame.quit()
