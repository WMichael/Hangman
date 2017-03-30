"""
A Simple implementation of Hangman. At the begining of each game, a random word is taken from the words.txt file.
The player has 8 chances to guess what the word is, after the game ends then the player can decide if they want to continue.
A text art representation is shown to represent lives left.
"""
from random import randint
import os

# Used to clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Holding current score
class Score:
    def __init__(self):
        self.wins = 0
        self.losses = 0

    def win(self):
        self.wins += 1

    def lose(self):
        self.losses += 1

    def score(self):
        print("- Wins: {0} Losses: {1}".format(self.wins,self.losses))
# Holds game state, guess function and representation of game function.
class Game:
    def __init__(self,word):
        self.actual_word = list() #hidden word
        self.display_word = list() #word to be displayed
        self.finished = False
        self.remaining_chances = 8
        self.guessed_chars = list()

        for x in range(0, len(word)): #put word into a list
            self.actual_word.append(word[x].lower())

        self.chars_left_to_guess = len(self.actual_word)

        for x in range(0, len(word)): #put word into a list with *'s
            self.display_word.append("*")

    def guess(self,char):
        clear()
        print("Hangman - Created by Michael.W")
        print("----------------------")
        if len(char) != 1: # Checks that only one character has been inputted.
            print("- Please enter only one character!")
        else:
            already_guessed = False # Checks whether char given has already been guessed.
            for x in range(0, len(self.guessed_chars)):
                if char.lower() == self.guessed_chars[x]:
                    already_guessed = True
                    print("- {} has already been guessed.".format(char.lower()))

            if already_guessed == False:
                no_of_char_in_word = 0 # Used to check how many times the char appears in the word
                for x in range(0, len(self.actual_word)): # Checks whether char is in word, if so then replaces corresponding * with char.
                    if char.lower() == self.actual_word[x]:
                        self.display_word[x] = char.lower()
                        self.chars_left_to_guess -= 1
                        no_of_char_in_word += 1

                if no_of_char_in_word == 0: # If char doesn't appear in word then one chance is taken away.
                    self.remaining_chances -= 1

                self.guessed_chars.append(char.lower())

    def displayed_word(self):
        dword = ""
        return dword.join(self.display_word)

# Prints a text art represention of hangman.
def representation(chances):
    lapp = "/"
    rapp = "\ "

    print("""\
    ______________
    | /          {0}
    |/           {1}
    |            {2}
    |           {4}{3}{5}
    |            {3}
    |           {6} {7}
    |
    |
    |____________|
    """.format("|" if chances <= 7 else " ","|" if chances <= 6 else " ", "0" if chances <= 5 else " ","|" if chances <= 4 else " ",lapp if chances <= 3 else " ",rapp if chances <= 2 else " ",lapp if chances <= 1 else " ",rapp if chances == 0 else " "))

# The Game
repeat = True
score = Score()

# Whilst game is running
while repeat is True:
    clear()
    print("Hangman - Created by Michael.W")
    print("----------------------")
    with open("words.txt", "r") as w: # opens word file.
        words = w.read().splitlines()

    #Creates a new game with random word.
    game = Game(words[randint(0,len(words))])
    representation(game.remaining_chances)
    print("- {}".format(game.displayed_word()))
    print("----------------------")

    # When player is currently guessing a word
    while game.finished == False:
        game.guess(input("What's your Guess? ")) #Inputs guess
        representation(game.remaining_chances)

        if game.remaining_chances == 0: # If remaining chances is 0, then finish game.
            game.finished = True
            score.lose()
            print("- Sorry, You Lost!")
            print("- The word was {}".format("".join(game.actual_word)))
            score.score()
            print("----------------------")
            break

        print("- {}".format(game.displayed_word())) # print display word

        if game.chars_left_to_guess == 0: # If every char is guessed, then finish game.
            score.win()
            print("- You Won!")
            score.score()
            game.finished = True
        else:
            print("- {} chances remaining".format(game.remaining_chances)) # print remaining chances
        print("----------------------")

    if input("Press 'y' to play again ") != "y": # To continue the game
        repeat = False
