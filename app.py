"""
Contains the user interface
Contains the code that sets up each round
Contains the code for each round
"""


from libs.library import *


start_menu = """WELCOME TO....
<<<<<<<RAMEN FURY>>>>>>>

To play a round of Ramen Fury,
please type play

To exit the program,
please type exit

: """
players = "How many players will there be (3-5)? : "







play_or_exit = input(start_menu)
while True:
    if "play" in play_or_exit:
        global how_many_players
        how_many_players = input(players)

        break
    elif "exit" in play_or_exit:
        exit()
    print("Invalid input")
    play_or_exit = input("play? or exit?: ")
    continue

while True:
    if int(how_many_players) >= 3 and int(how_many_players) <= 5:
        player_count = int(how_many_players)
        clearScreen()
        P1_name = input("What is player 1's name?: ")
        P2_name = input("what is player 2's name?: ")
        P3_name = input("What is player 3's name?: ")
        Player1 = Player(P1_name)
        Player2 = Player(P2_name)
        Player3 = Player(P3_name)
        Player4 = False
        Player5 = False
        if player_count == 4 or 5:
            P4_name = input("What is player 4's name?: ")
            Player4 = Player(P4_name)
            Player5 = False
        if player_count == 5:
            P5_name = input("What is player 5's name?: ")
            Player5 = Player(P5_name)
        break
    else:
        print("Invalid input")
        how_many_players = input(players)
        continue


