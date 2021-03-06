# another quality program
# debug mode only shows number of bot cards and the change detector. turn off to reduce clutter.
debug = True
color_toggle = True

# heckin-doggo github has the issues instead of here
import random
from time import sleep
try:
    from colorama import init
    init()
except:
    print("ERROR: Colorama failed to load!")


def main():
    active = True

    while active:
        print_header()
        print("\nWelcome to Uno! Type your choice.")
        print("NOTE: if the title looks like garbled mess, turn off colors in OPTIONS")
        choice = input("[PLAY] [QUIT] [OPTIONS]\n>>>").strip().lower()
        # Play
        if choice == "play":
            game()
            # After the game
            choice = input("\nWould you like to play again? (y/n)\n>>>").strip().lower()
            if choice == "no" or choice == "n":
                print("Goodbye!")
                active = False
            elif choice == "yes" or choice == "y":
                print("")
        elif choice == "quit":
            print("Goodbye!")
            active = False
        elif choice == "options":
            options()

        else:
            print("'{}' not recognized. Please try again.".format(choice))


def game():
    deck = get_deck()

    player_count = input("How many players? (2-5) ")
    try:
        if int(player_count) <= 5 and int(player_count) >= 2:  
            player_count = int(player_count)
            print("Valid!")
        else:
            print("Invalid, you get 2.")
            player_count = 2
    except:
        print("Invalid. Setting Players to 2")
        player_count = 2
    # TODO: give each player (for player_count) 7 cards from deck

    bots = [[],[]]
    bot_names = bots[0]
    bot_decks = bots[1]
    # Setting Bot Decks
    for p in range(player_count):
        cards = []  # start with empty hand
        for i in range(7):
            card = deck.pop(0)
            cards.append(card)  # add card to hand
        # bots["Bot {}".format(p+1)] = cards  # adds new cards for bot
        bot_names.append("Bot {}".format(p+1))
        bot_decks.append(cards)

    # Setting User Deck
    cards = []
    for i in range(7):
        card = deck.pop(0)
        cards.append(card)  # add card to hand
    # cards.append("WILDCARD")
    # cards.append("RED REVERSE")  #TODO: remove lines adding reverse and wild
    player = Player(cards)  # initialize with cards as deck, player+1 as number

    discard = []
    discard.append(deck.pop(0))
    # Anti Wildcard for the start card.
    check = True
    while check:
        if discard[-1] == "WILDCARD" or discard[-1] == "WILD +4":
            discard.append(deck.pop(0))
        else:
            check = False

    # game variables initialized
    active = True
    card_choice = None
    wild = False
    wild_color = None
    valid = False
    reverse = False
    skip = False
    draw_2 = False
    draw_4 = False

    # start on reversed order check
    if discard[0].find("REVERSE") != -1:
        reverse = True

    # game
    while active:
        # note: color_card(card) returns the card with attached color codes. invalid when color_toggle is False
        print("\nThe current card is {}".format(color_card(discard[-1])))  # discard[-1] is the last added card.
        split = discard[-1].find(" ")
        current_color = discard[-1][:split]  # grabs color
        current_number = discard[-1][split + 1:]  # grabs number
        sleep(1)

        if not skip and not draw_2 and not draw_4:
            if wild_color is not None:
                # wild = False
                current_color = wild_color
                print("The Wild Card's color is {}".format(colorize(current_color, current_color)))

            print("You have {} cards. They are:".format(len(player.hand)))
            for card in player.hand:
                print(color_card(card))

            check = True
            while check:
                card_choice = input("Which card will you deploy? (type 'draw' to get a new card) \n>>>").strip().upper()
                if card_choice in player.hand or card_choice == "DRAW":
                    check = False
                else:
                    if card_choice == "DATA DUMP":
                        data_dump(bots, player, wild_color, reverse, wild, draw_2, draw_4, skip)
                    print("That's not a real card! Try again, or draw a card.")

            # CARD CHECK
            if card_choice == "DRAW":
                if deck:
                    new_card = deck.pop(0)
                    player.hand.append(new_card)  # grab top card from deck
                    print("Drew a {}.".format(color_card(new_card)))

                else:
                    print("No more cards! Shuffling...")
                    deck = discard[:-2]  # all but top card
                    random.shuffle(deck)
                    new_card = deck.pop(0)
                    player.hand.append(new_card)

            elif card_choice in player.hand:  # duh, gotta see if the card actually exists

                # Wildcard
                if card_choice == "WILDCARD" or card_choice == "WILD +4":
                    print("Wild Card! What is the new Color?")
                    wild = True
                    check = True
                    valid = True
                    while check:
                        wild_color = input("\033[0;34;0m[BLUE]\033[0;33;0m[YELLOW]\033[0;31;0m[RED]\033[0;32;0m[GREEN]\033[0;0;0m\n>>>").lower().strip()

                        # set wild color
                        if wild_color == "blue" or wild_color == "red" or wild_color == "green" or wild_color == "yellow":
                            wild_color = wild_color.upper()
                            check = False
                        else:
                            print("That's not a color! Try again.")

                    if card_choice == "WILD +4":
                        print("The next player also draws 4 cards!")
                        draw_4 = True
                # Other Cards
                else:
                    split = card_choice.find(" ")
                    card_color = card_choice[:split]
                    card_number = card_choice[split + 1:]

                    if card_number == "SKIP" and (card_color == current_color or card_number == current_number):
                        print("Skipped next player.")
                        skip = True
                        valid = True
                    # TODO: the below isnt working.
                    elif card_number == "REVERSE" and (card_color == current_color or card_number == current_number):
                        print("The order is reversed!")
                        if reverse:
                            reverse = False
                        else:
                            reverse = True
                        valid = True
                    elif card_number == "DRAW 2" and (card_color == current_color or card_number == current_number):
                        print("The next player draws 2 cards!")
                        draw_2 = True
                        valid = True
                    elif card_color == current_color:
                        print("Valid!")
                        valid = True
                    elif card_number == current_number:
                        print("Valid!")
                        valid = True
                    elif card_choice == "DRAW":
                        pass  # this is to avoid the below
                    else:
                        print("{} don't work. gonna need a different card bub.".format(card_choice))
                        # TODO: make this draw a card.
        elif skip:
            print("You have been skipped!")
            skip = False
        # TODO: theres a way to simplify the below but honestly i really dont care.
        elif draw_4:
            print("...which doesn't matter since you just got hit by a WILD +4.")
            for i in range(4):
                if deck:
                    player.hand.append(deck.pop(0))
                else:
                    reshuffle(discard, deck)
                    player.hand.append(deck.pop(0))
                draw_4 = False
        elif draw_2:
            print("...which doesn't matter since you just got hit by a DRAW 2.")
            for i in range(2):
                if deck:
                    player.hand.append(deck.pop(0))
                else:
                    reshuffle(discard, deck)
                    player.hand.append(deck.pop(0))
                    draw_2 = False
        else:
            print("Hmm.... you really aren't ever supposed to see this text. If you do, say something to the dev."
                  "@Heckin-Doggo on GitHub. The only way you can see it is if you had a skip and it revoked itself.")

        if valid:
            valid = False
            c_spot = player.hand.index(card_choice)
            used_card = player.hand.pop(c_spot)
            discard.append(used_card)

        if len(player.hand) == 0:
            active = False
            print("You win! Congratulations!")
            print(discard) # prints out entire game
            break
        elif len(player.hand) == 1:
            print("Uno!")

        # TODO: put this in the bot loop
        if reverse:
            bot_names = list(reversed(bot_names))
            bot_decks = list(reversed(bot_decks))
            reverse = False

        for bot in range(len(bot_names)):

            current_card = discard[-1]
            if wild_color:
                current_card = "WILDCARD"
            bot_cards = bot_decks[bot]
            bot_name = bot_names[bot]
            print("\nThe Card is {}".format(color_card(current_card)))
            if debug:
                error_print("CARD COUNT: {}".format(len(bot_cards)))

            if not skip and not draw_2 and not draw_4:
                print("{}, what do you do?".format(bot_name))
                sleep(2)
                if len(bot_cards) > 0:
                    if len(bot_cards) == 1:
                        print("{} says: 'Uno!'".format(bot_name))

                    if wild_color:
                        bot_card, status, wild_color= use_card(current_card, bot_cards, discard, wild_color)
                        # wild = False # broken maybe
                    else:
                        bot_card, status, wild_color = use_card(current_card, bot_cards, discard)
                    if bot_card is not None:
                        print("{} used {}.".format(bot_name, color_card(bot_card)))
                        if status == "reverse":
                            reverse = True
                        elif status == "skip":
                            skip = True
                        elif status.find("wild") != -1:
                            wild = True
                        elif status == "draw 2":
                            draw_2 = True
                        if status == "wild draw 4":
                            draw_4 = True

                        if len(bot_cards) == 0:  # if the bot has no cards left it wins
                            print("{} has won the game!".format(bot_name))
                            break
                    else:  # if nothing happens, draw a card
                        print("{} drew a card.".format(bot_name))
                        bot_cards.append(deck.pop(0))
                elif len(bot_cards) == 0:  # This shouldn't happen but if it does heres a solution
                    print("{} has won the game... but this text should never show up!".format(bot))
                    active = False
                    break
            elif skip:
                skip = False
                print("{} was skipped!".format(bot_name))
            elif draw_4:
                print("{} got straight up yeeted by a WILD +4".format(bot_name))
                for i in range(4):
                    if deck:
                        bot_cards.append(deck.pop(0))
                    else:
                        reshuffle(discard, deck)
                        bot_cards.append(deck.pop(0))
                    draw_4 = False
            elif draw_2:
                print("{} was hit by a draw 2.".format(bot_name))
                for i in range(2):
                    if deck:
                        bot_cards.append(deck.pop(0))
                    else:
                        reshuffle(discard, deck)
                        bot_cards.append(deck.pop(0))
                    draw_2 = False
            sleep(1)

            # debug check to see if card was actually placed in discard
            if discard[-1] != current_card and debug:  # "and debug" = debug mode is on
                error_print("Card changed!!")


# HEY: THIS LOOKS TERRIBLE IN EDITOR SOMETIMES BUT IT WORKS IN TERMINAL. DO NOT MESS WITH print_header().
def print_header():
    print("----------------------------------")
    print(colorize(" ■■   ■■    ■■    ■■    ■■■■■■■■", "RED"))
    print(colorize(" ■■   ■■    ■■■   ■■    ■■    ■■", "BLUE"))
    print(colorize(" ■■   ■■    ■■■■  ■■    ■■    ■■", "GREEN"))
    print(colorize(" ■■   ■■    ■■ ■■ ■■    ■■    ■■", "YELLOW"))
    print(colorize(" ■■   ■■    ■■  ■■■■    ■■    ■■", "RED"))
    print(colorize(" ■■   ■■    ■■    ■■    ■■    ■■", "BLUE"))
    print(colorize(" ■■■■■■■    ■■    ■■    ■■■■■■■■", "GREEN"))
    print("----------------------------------")

    #print(colorize("test red","RED"))
    #print(colorize("test blue","BLUE"))
    #print(colorize("test green","GREEN"))
    #print(colorize("test yellow","YELLOW"))
    #color_test()


# Deck Generation + Shuffling
def get_deck():
    deck = []
    # The below just creates the deck.
    for color in ["RED", "GREEN", "BLUE", "YELLOW"]:
        # Cards 0-9
        for i in range(10):
            deck.append(color + " " + str(i))
        # Another set of 1-9
        for i in range(1, 10):
            deck.append(color + " " + str(i))
        # Action Cards
        deck.append(color + " REVERSE")
        deck.append(color + " REVERSE")
        deck.append(color + " SKIP")
        deck.append(color + " SKIP")
        deck.append(color + " DRAW 2")
        deck.append(color + " DRAW 2")

    # Wild Cards
    for i in range(4):
        deck.append("WILDCARD")
        deck.append("WILD +4")

    random.shuffle(deck)
    return deck


# "reshuffle" probably will break and be sad for anyone in a long game :(
# edit: probably not tbh hasnt failed me yet.
def reshuffle(discard, deck):
    for card in discard:
        if discard.index(card) != discard.index(discard[-1]):
            card = discard.pop(card)
            deck.append(card)


# TODO: make Player not be a class, but with the bots list, then rename bots to players.
# TODO: make sure player is only accessable by player.
class Player:
    def __init__(self, hand):
        self.hand = hand
        self.number = 1  # abosolutely redundant code.


def use_card(current_card, hand, pile, wild_color=None):  # TODO: see if this wild_color = None is breaking things
    # set up for card check
    split = current_card.find(" ")
    current_color = current_card[:split]
    current_number = current_card[split + 1:]
    status = "default"
    if wild_color:
        current_color = wild_color

    # card check
    for card in hand:
        split = card.find(" ")
        card_color = card[:split]
        card_number = card[split + 1:]

        if card == "WILDCARD" or card == "WILD +4":
            for color in ["BLUE", "RED", "GREEN", "YELLOW"]:
                if color in hand:  # TODO: make an "ai" for this? count cards before choosing? right now its just based on first card seen
                    card_color = color
                    wild_color = card_color
                else:
                    card_color = random.choice(["BLUE", "RED", "GREEN", "YELLOW"])  # rare occurance but still
                    wild_color = card_color
            print("Wildcard! New color is {}".format(colorize(card_color, card_color)))
            status = "wild"
            if card == "WILD +4":
                print("The next player will ALSO draw 4 cards! Rekt!")
                status = "wild draw 4"
                
            pile.append(hand.pop(hand.index(card)))
            return card, status, wild_color

        # the following just tell the event handler what happens in this function
        elif card_number == "SKIP" and (card_color == current_color or card_number == current_number):
            print("Skipped next player.")
            status = "skip"
            break
        elif card_number == "REVERSE" and (card_color == current_color or card_number == current_number):
            print("The order is reversed!")
            status = "reverse"
            break
        elif card_number == "DRAW 2" and (card_color == current_color or card_number == current_number):
            print("The next player draws 2 cards!")
            status = "draw 2"
            break
        elif card_color == current_color:
            break
        elif card_number == current_number:
            break
        elif card == hand[-1]:
            return None, status, wild_color # THIS PREVENTS THE BELOW FROM FIRING IF NO CARD REPLACES THE WILD

    wild_color = None  # THIS ONE SHOULD ONLY WORK IF THEY DREW A CARD TO REPLACE THE WILD
    pile.append(hand.pop(hand.index(card)))
    return card, status, wild_color

# WARNING: the code below starts to get pretty messy

# should really be called "debug_print" but whatever. too much work to change it now and im too lazy
def error_print(text):
    print("\033[0;35;0m{}\033[0;0;0m".format(text))


def colorize(text, color):
    color = color.upper()
    new_text = text
    if color_toggle:
        if color == "BLUE":
            new_text = "\033[0;34;0m{}\033[0;0;0m".format(text)
        elif color == "RED":
            new_text = "\033[0;31;0m{}\033[0;0;0m".format(text)
        elif color == "YELLOW":
            new_text = "\033[0;33;0m{}\033[0;0;0m".format(text)
        elif color == "GREEN":
            new_text = "\033[0;32;0m{}\033[0;0;0m".format(text)
        elif color == "WHITE" or color == "WILD":
            new_text = "\033[0;30;0m{}\033[0;0;0m".format(text)
    return new_text


def color_test():
    # color codes are also at http://ozzmaker.com/add-colour-to-text-in-python/
    for i in range(108):
        print("\033[0;{};0m{}\033[0;0;0m".format(i,i))


def options():
    global color_toggle
    global debug
    print("Colors? (turn off if you see garbage/glitch text) (on/off)")
    choice = input(">>>").lower().strip()
    if choice == "on":
        color_toggle = True
        print("Setting Saved!")
    elif choice == "off":
        color_toggle = False
        print("Setting Saved! (COLORS OFF)")
    else:
        print("'{}' not recognized. Setting Colors to Off")
        color_toggle = False

    print("\nDebug mode? (turn on only if things seem broken) (on/off)")
    choice = input(">>>").lower().strip()
    if choice == "on":
        debug = True
        print("Setting Saved!")
    elif choice == "off":
        debug = False
        print("Setting Saved! (COLORS OFF)")
    else:
        print("'{}' not recognized. Setting Colors to Off")
        debug = False


def color_card(card):
    split = card.find(" ")
    color = card[:split]
    if split != -1:
        return colorize(card, color)
    else:
        return colorize(card, "WHITE")


def data_dump(bots, player, wild_color, reverse, wild, draw_2, draw_4, skip):
    print("\033[0;35;0m")
    print(bots)
    print("PLAYER:{}".format(player.hand))
    print("WILD_COLOR: {}".format(wild_color))
    print("WILD: {}".format(wild))
    print("REVERSE: {}".format(reverse))
    print("DRAW_2: {}".format(draw_2))
    print("DRAW_4: {}".format(draw_4))
    print("SKIP: {}".format(skip))
    print("\033[0;0;0m")


if __name__ == "__main__":
    main()
