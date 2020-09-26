"""
Contains the Objects used in app.py
"""
from random import shuffle
from typing import List
from collections import deque
import pyautogui
import weakref
import subprocess

def clear_screen():
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'k')
    clear = lambda: subprocess.call('cls||clear', shell=True)
    clear()

def escape(func):
    if func == "esc":
        return True
    else:
        return func

class Table:
    game_name = "Solomon's Soup"
    seats = 5
    min_players = 3
    players = []
    turns = 0
    current_player = None

    def add_player(self, player):
        if self.turns == 0:
            self.players.append(player)
        else:
            print("Can't Add Player: Game Started")

    def end_of_game(self):
        # If any Player has all their bowls eaten
        # Is the Deck completely empty
        for obj in self.players:
            if obj.all_bowls_eaten() == True:
                return True
        return False

    def start_game(self):
        if len(self.players) >= self.min_players and len(self.players) <= self.seats:
            self.current_player = self.players[0]
            while not self.end_of_game():
                self.nextTurn()
        else:
            print("Can't Start Game: Too Few Players")

    def nextTurn(self):
        if self.turns == 0:
            self.current_player.turn()
            self.turns += 1
        else:
            self.turns += 1
            #print(self.players[self.players.index(self.current_player)].name)
            self.next_player = self.players.index(self.current_player) + 1
            if  self.next_player == len(self.players):
                self.next_player = 0
            self.current_player = self.players[self.next_player]
            #print(self.current_player.name)
            self.current_player.turn()



# creates player that has multiple actions
class Player:

    _instances = set()

    def __init__(self, name, bowls: List):
        self.name = name
        self.bowls = bowls
        self.hand = []
        self.spoons = 2
        self.actions = 0
        self._instances.add(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def print_hand(self):
        names = [card.name for card in self.hand]
        print(*names, sep=", ")

    def all_bowls_eaten(self):
        i = 0
        for bowl in self.bowls:
            if bowl.eaten == True:
                i += 1
        if i == 3:
            return True
        else:
            return False

    def turn(self):

        print("Player Moves")
        self.actions =2

        while self.actions > 0:
            clear_screen()
            action_num = input(f"""{self.name} has {self.actions} moves left. 
Available Moves:

    1. Place Card
    2. Use Special
    3. Draw Card Pantry
    4. Draw Card Deck
    5. Wipe Pantry
    6. Use Spoon
    7. Eat Bowl

What action would you like to perform: 
    """)
            if len(action_num) != 1:
                print("Invalid Input")
                continue

            if "1" in action_num:
                pass
            if "2" in action_num:
                pass
            if "3" in action_num:
                pass
            if "4" in action_num:
                pass
            if "5" in action_num:
                pass
            if "6" in action_num:
                self.use_spoon()
            elif "7" in action_num:
                while True:
                    bowl = escape(input("Which bowl: "))
                    if bowl == True:
                        break
                    else:
                        bowl = int(bowl)
                    try:
                        if self.bowls[bowl - 1].eaten == False:
                            self.eat(self.bowls[bowl - 1])
                            break
                        else:
                            print("Bowl already eaten")
                            continue
                    except IndexError:
                        print("No bowl found")
                        continue

    def discard(self):
        self.names = [card.name for card in self.hand]
        while True:
            card_to_discard = escape(input("Which card do you want to discard?: "))
            if card_to_discard == True:
                break
            if card_to_discard in self.names:
                for card in self.hand:
                    if card.name == card_to_discard:
                        self.hand.remove(card)
                        return
            print("Invalid input")

    def draw_card_deck(self):
        if len(self.hand) == 5:
            confirmation = input("""You have 5 cards in your hand. 
            If you pick up another card, then you will have to use it immediately (if you have an action left) 
            or discard the card. Do you still want to draw the card? y/n: """).lower()
            while True:
                if "yes" in confirmation:
                    self.hand.append(deck.pop())
                    self.print_hand()
                    self.actions -= 1
                    if self.actions != 0:
                        while True:
                            confirmation2 = input("""
                            Would you like to place a card or discard one?: """)
                            if "place" in confirmation2:
                                self.place_card()
                            elif "discard" in confirmation2:
                                self.discard()
                            else:
                                continue
                    else:
                        self.discard()
                elif "no" in confirmation:
                    return
                print("Invalid input")
                confirmation = input("Do you still want to draw the card? y/n: ").lower()
        self.actions -= 1
        self.hand.append(deck.pop())

    def draw_card_pantry(self):
        card = input("which card do you want to draw?")
        for i in pantry:
            if i.name == card:
                self.actions -= 1
                self.hand.append(i)
                pantry[pantry.index(i)] = deck.pop()

    def select_player(self):
        while True:
            player = input("Which player do you want to use this on?: ")
            for obj in Player.get_instances():
                if obj.name.lower() == player.lower():
                    return obj
                else:
                    continue;

    def use_special(self, card):
        player = self.select_player()
        while True:
            bowl = input("Which bowl would you like to take a card from?: ")
            if '1' in bowl and len(player.bowls[0]) > 0:
                if '1' in bowl and len(player.bowls[0]) < 5:
                    player.bowls[0].bowl.append(card)
                    self.hand.remove(card)
                    return
                elif '1' in bowl and len(player.bowls[0]) == 5:
                    print("Bowl full")
                    continue
                elif '2' in bowl and len(player.bowls[1]) < 5:
                    player.bowls[1].bowl.append(card)
                    self.hand.remove(card)
                    return
                elif '2' in bowl and len(player.bowls[1]) == 5:
                    print("Bowl full")
                    continue
                elif '3' in bowl and len(player.bowls[2]) < 5:
                    player.bowls[2].bowl.append(card)
                    self.hand.remove(card)
                    return
                elif '3' in bowl and len(player.bowls[2]) == 5:
                    print("Bowl full")
                    continue

            else:
                print("Invalid player name")
                continue

    def place_card(self):
        self.names = [card.name for card in self.hand]
        while True:
            card_to_place = input("Which card would you like to place into a bowl?: ")
            if card_to_place in self.names:
                for card in self.hand:
                    if card.name == card_to_place:
                        if card.kind == "chili" or card.kind == "nori":
                            self.use_special(card)
                        obj = self.select_player()
                        while True:
                            bowl = input("Which bowl would you like to place a card into?: ")
                            if '1' in bowl and len(obj.bowls[0]) < 5:
                                self.bowls[0].bowl.append(card)
                                self.hand.remove(card)
                                self.actions -= 1
                                return
                            elif '1' in bowl and len(obj.bowls[0]) == 5:
                                print("Bowl full")
                                continue
                            elif '2' in bowl and len(obj.bowls[1]) < 5:
                                self.bowls[1].bowl.append(card)
                                self.hand.remove(card)
                                self.actions -= 1
                                return
                            elif '2' in bowl and len(obj.bowls[1]) == 5:
                                print("Bowl full")
                                continue
                            elif '3' in bowl and len(obj.bowls[2]) < 5:
                                self.bowls[2].bowl.append(card)
                                self.hand.remove(card)
                                self.actions -= 1
                                return
                            elif '3' in bowl and len(obj.bowls[2]) == 5:
                                print("Bowl full")
                                continue

    def eat(self, bowl):
        for card in bowl.bowl:
            if card.kind == "tofu":
                while True:
                    tofu_card = input("""You have a tofu in your bowl
                    How do you want it to be used, as a meat, or a veggie?: """)
                    if "meat" in tofu_card:
                        card.kind = "meat"
                        break
                    elif "veggie" in tofu_card:
                        card.kind = "veggie"
                        break
                    print("Invalid input")
        bowl.eaten = True
        self.actions -= 1


    def use_spoon(self):
        if self.spoons == 0:
            print("You don't have any spoons left")
            return
        while True:
                player = self.select_player()
                try:
                    prompt = ""
                    for bowl in player.bowls:
                        if bowl.eaten == True:
                            prompt = prompt + f"\n{player.bowls.index(bowl)+1}. Bowl {player.bowls.index(bowl)+1} is already eaten."
                        elif len(bowl.bowl) == 0:
                            prompt = prompt + f"\n{player.bowls.index(bowl)+1}. Bowl {player.bowls.index(bowl)+1} is empty."
                        else:
                            prompt = prompt + f"\n{player.bowls.index(bowl)+1}. Bowl {player.bowls.index(bowl)+1} with top card {bowl.bowl[len(bowl.bowl)-1].name}"
                    prompt = prompt + "\nor\n 'back' to go back: "
                    prompt = prompt + "\nWhich bowl would you like to take a card from?: "
                    bowl_response = input(prompt)
                    if bowl_response == "back":
                        return
                    bowl = int(bowl_response) - 1
                    if player.bowls[bowl].eaten == False and len(player.bowls[bowl].bowl) > 0:
                        while True:
                            card = player.bowls[bowl].bowl[len(player.bowls[bowl].bowl)-1]
                            self.hand.append(card)
                            player.bowls[bowl].bowl.pop(-1)
                            self.actions -= 1
                            while True:
                                if len(self.hand) > 5 and self.actions==0:
                                    print("You have 6 cards in your hand you must discard a card.")
                                    self.discard()
                                else:
                                    place_or_no = input("Do you want to place the card on a bowl?: ").lower
                                    if "yes" in place_or_no:
                                        pass
                                    #TODO
                    else:
                        if player.bowls[bowl].eaten == True:
                            print("Bowl is Eaten")
                        elif len(player.bowls[bowl].bowl) == 0 :
                            print("Bowl empty")
                        else:
                            pass
                        continue
                except IndexError:
                    print("Bowl not found")
                    continue
                except ValueError:
                    print("Invalid Bowl")
                    continue


# Defines ingredient with name, kind and verifier
class Card:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind


class Bowl:
    def __init__(self):
        self.bowl = []
        self.eaten = False

    def count_name(self, name):
        i = 0
        for card in self.bowl:
            if card.name == name:
                i += 1
        return i

    @property
    def score(self):
        number = 0
        score_num = 0
        broth_card = ""
        duplicate = []
        for card in self.bowl:
            if card.kind == "broth":
                broth_card = card.name

        if broth_card == "":
            for card in self.bowl:
                if card.kind == "nori":
                    score_num += 1
                elif card.kind == "chili":
                    score_num = score_num - 2
            return  score_num

        if broth_card == "Beef Flavor":
            for card in self.bowl:
                if card.kind == "meat" and card.name not in duplicate:
                    duplicate.append(card.name)
                    number += 1
                elif card.kind == "nori":
                    score_num += 1
                elif card.kind == "chili":
                    score_num = score_num - 2
            if number == 1:
                score_num += 2
                return score_num
            elif number == 2:
                score_num += 5
                return score_num
            elif number == 3:
                score_num += 9
                return score_num
            elif number == 4:
                score_num += 14
                return score_num

        elif broth_card == "Soy Flavor":
            for card in self.bowl:
                if card.kind == "veggie" and card.name not in duplicate:
                    duplicate.append(card.name)
                    number += 1
                elif card.kind == "nori":
                    score_num += 1
                elif card.kind == "chili":
                    score_num = score_num - 2
            if number == 1:
                score_num += 2
                return score_num
            elif number == 2:
                score_num += 5
                return score_num
            elif number == 3:
                score_num += 9
                return score_num
            elif number == 4:
                score_num += 14
                return score_num

        elif broth_card == "Chicken Flavor":
            for card in self.bowl:
                if card.kind != "chili" or card.kind != "nori":
                    if self.count_name(card.name) == 2:
                        number += 1
                    if self.count_name(card.name) == 3 or self.count_name(card.name) == 4:
                        number = 3
                elif card.kind == "nori":
                    score_num += 1
                elif card.kind == "chili":
                    score_num = score_num - 2
            if number == 2:
                score_num += 6
                return score_num
            elif number == 4:
                score_num += 12
                return score_num
            elif number == 3:
                score_num += 10
                return score_num

        elif broth_card == "Shrimp Flavor":
            veggies = []
            meats = []
            for card in self.bowl:
                if card.kind == "veggie":
                    veggies.append(card.name)
                if card.kind == "meat":
                    meats.append(card.name)
                elif card.kind == "nori":
                    score_num += 1
                elif card.kind == "chili":
                    score_num = score_num - 2
            veggies_num = len(veggies)
            meats_num = len(meats)
            if meats_num == 1 and (veggies_num == 1 or veggies_num == 2):
                score_num += 4
                return score_num
            if veggies_num == 1 and (meats_num == 1 or meats_num == 2):
                score_num += 4
                return score_num
            if veggies_num == 2 and meats_num == 2:
                score_num += 8
                return  score_num


        elif broth_card == "Fury Flavor":
            for card in self.bowl:
                if card.kind == "chili" and card.name not in duplicate:
                    duplicate.append(card.name)
                    number += 1
                elif card.kind == "nori":
                    score_num += 1
            if number == 1:
                score_num += 2
                return score_num
            elif number == 2:
                score_num += 4
                return score_num
            elif number == 3:
                score_num += 6
                return score_num
            elif number == 4:
                score_num += 8
                return score_num

class Deck:
    def give_hand(self, player):
        player.hand = []
        player.hand.append(deck.pop())
        player.hand.append(deck.pop())
        player.hand.append(deck.pop())

    def wipe_pantry(self):
        pantry.clear()
        pantry.append(deck.pop())
        pantry.append(deck.pop())
        pantry.append(deck.pop())
        pantry.append(deck.pop())

    def print_pantry(self):
        names = [card.name for card in pantry]
        print(*names, sep=", ")


eggs1 = Card("Eggs", "meat")
eggs2 = Card("Eggs", "meat")
eggs3 = Card("Eggs", "meat")
eggs4 = Card("Eggs", "meat")
eggs5 = Card("Eggs", "meat")
eggs6 = Card("Eggs", "meat")
naruto1 = Card("Naruto", "meat")
naruto2 = Card("Naruto", "meat")
naruto3 = Card("Naruto", "meat")
naruto4 = Card("Naruto", "meat")
naruto5 = Card("Naruto", "meat")
naruto6 = Card("Naruto", "meat")
chashu1 = Card("Chashu", "meat")
chashu2 = Card("Chashu", "meat")
chashu3 = Card("Chashu", "meat")
chashu4 = Card("Chashu", "meat")
chashu5 = Card("Chashu", "meat")
chashu6 = Card("Chashu", "meat")
tofu1 = Card("Tofu", "tofu")
tofu2 = Card("Tofu", "tofu")
tofu3 = Card("Tofu", "tofu")
tofu4 = Card("Tofu", "tofu")
tofu5 = Card("Tofu", "tofu")
tofu6 = Card("Tofu", "tofu")
scallions1 = Card("Scallions", "veggie")
scallions2 = Card("Scallions", "veggie")
scallions3 = Card("Scallions", "veggie")
scallions4 = Card("Scallions", "veggie")
scallions5 = Card("Scallions", "veggie")
scallions6 = Card("Scallions", "veggie")
mushroom1 = Card("Mushroom", "veggie")
mushroom2 = Card("Mushroom", "veggie")
mushroom3 = Card("Mushroom", "veggie")
mushroom4 = Card("Mushroom", "veggie")
mushroom5 = Card("Mushroom", "veggie")
mushroom6 = Card("Mushroom", "veggie")
corn1 = Card("Corn", "veggie")
corn2 = Card("Corn", "veggie")
corn3 = Card("Corn", "veggie")
corn4 = Card("Corn", "veggie")
corn5 = Card("Corn", "veggie")
corn6 = Card("Corn", "veggie")
beef1 = Card("Beef Flavor", "broth")
beef2 = Card("Beef Flavor", "broth")
beef3 = Card("Beef Flavor", "broth")
beef4 = Card("Beef Flavor", "broth")
beef5 = Card("Beef Flavor", "broth")
beef6 = Card("Beef Flavor", "broth")
soy1 = Card("Soy Flavor", "broth")
soy2 = Card("Soy Flavor", "broth")
soy3 = Card("Soy Flavor", "broth")
soy4 = Card("Soy Flavor", "broth")
soy5 = Card("Soy Flavor", "broth")
soy6 = Card("Soy Flavor", "broth")
chicken1 = Card("Chicken Flavor", "broth")
chicken2 = Card("Chicken Flavor", "broth")
chicken3 = Card("Chicken Flavor", "broth")
chicken4 = Card("Chicken Flavor", "broth")
chicken5 = Card("Chicken Flavor", "broth")
chicken6 = Card("Chicken Flavor", "broth")
shrimp1 = Card("Shrimp Flavor", "broth")
shrimp2 = Card("Shrimp Flavor", "broth")
shrimp3 = Card("Shrimp Flavor", "broth")
shrimp4 = Card("Shrimp Flavor", "broth")
shrimp5 = Card("Shrimp Flavor", "broth")
shrimp6 = Card("Shrimp Flavor", "broth")
fury1 = Card("Fury Flavor", "broth")
fury2 = Card("Fury Flavor", "broth")
fury3 = Card("Fury Flavor", "broth")
chili1 = Card("Chili Peppers", "chili")
chili2 = Card("Chili Peppers", "chili")
chili3 = Card("Chili Peppers", "chili")
chili4 = Card("Chili Peppers", "chili")
chili5 = Card("Chili Peppers", "chili")
chili6 = Card("Chili Peppers", "chili")
chili7 = Card("Chili Peppers", "chili")
chili8 = Card("Chili Peppers", "chili")
chili9 = Card("Chili Peppers", "chili")
chili10 = Card("Chili Peppers", "chili")
chili11 = Card("Chili Peppers", "chili")
chili12 = Card("Chili Peppers", "chili")
nori1 = Card("Nori Garnish", "nori")
nori2 = Card("Nori Garnish", "nori")
nori3 = Card("Nori Garnish", "nori")
nori4 = Card("Nori Garnish", "nori")
nori5 = Card("Nori Garnish", "nori")
nori6 = Card("Nori Garnish", "nori")
nori7 = Card("Nori Garnish", "nori")
nori8 = Card("Nori Garnish", "nori")
deck = deque(
    [
        eggs1, eggs2, eggs3, eggs4, eggs5, eggs6,
        naruto1, naruto2, naruto2, naruto3, naruto4, naruto5, naruto6,
        chashu1, chashu2, chashu3, chashu4, chashu5, chashu6,
        tofu1, tofu2, tofu3, tofu4, tofu5, tofu6,
        scallions1, scallions2, scallions3, scallions4, scallions5, scallions6,
        mushroom1, mushroom2, mushroom3, mushroom4, mushroom5, mushroom6,
        corn1, corn2, corn3, corn4, corn5, corn6,
        beef1, beef2, beef3, beef4, beef5, beef6,
        soy1, soy2, soy3, soy4, soy5, soy6,
        chicken1, chicken2, chicken3, chicken4, chicken5, chicken6,
        shrimp1, shrimp2, shrimp3, shrimp4, shrimp5, shrimp6,
        fury1, fury2, fury3,
        chili1, chili2, chili3, chili4, chili5, chili6, chili7, chili8, chili9, chili10, chili11, chili12,
        nori1, nori2, nori3, nori3, nori4, nori5, nori6, nori7, nori8
    ]
)
pantry = []

shuffle(deck)
Deck = Deck()
Deck.wipe_pantry()


P1bowl1 = Bowl()
P1bowl2 = Bowl()
P1bowl3 = Bowl()

P2bowl1 = Bowl()
P2bowl2 = Bowl()
P2bowl3 = Bowl()

P3bowl1 = Bowl()
P3bowl2 = Bowl()
P3bowl3 = Bowl()

P3bowl1.eaten = True
P3bowl2.bowl.append(eggs1)
table1 = Table()

solomon = Player("solomon",[P1bowl1,P1bowl2,P1bowl3])
something = Player("something", [P2bowl1, P2bowl2, P2bowl3])
mom = Player("mom", [P3bowl1, P3bowl2, P3bowl3])

Deck.give_hand(solomon)
Deck.give_hand(something)
Deck.give_hand(mom)

table1.add_player(solomon)
table1.add_player(something)
table1.add_player(mom)

solomon.hand += [chashu1, chashu2]

table1.start_game()
