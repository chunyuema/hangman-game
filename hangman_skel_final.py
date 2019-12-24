"""
COMP112 Winter Session
Final Project

Name: Chunyue Ma
WesID: 368760

Hangman using a two classes
1 for logic and 1 for GUI
Widgets:root window,labels,Buttons, canvas
"""


import tkinter as tk
import random


# utility functions
# used to see if all chars in a word have been typed
# Thus you WIN when string_minus returns the empty string
def string_minus(s1, s2):
    """
    s1,s2:strings
    return:string consisting of letters in s1 not in s2
    string_minus("automobile","aom") ==> "utbile"
    string_minus("hola","lhaoxy") ==>""
    """
    diff = ""
    for char in s1:
        if not(char in s2):
            diff = diff+char
    return diff


def make_display_word(word, letters_used):
    """
    word:str
    letters_used:str
    return:str - word, with underscores for letters
    that have not been used yet
    make_display_word ("automobile","aom") ==> "a __ __ o m o __ __ __ __"
    """
    display_word = ""
    for char in word:
        if char in letters_used:
            display_word += char+"  "
        else:
            display_word += "__  "
    return display_word


# logic part of game
# there should be NO GRAPHICS here.
class Hangman_game:

    def __init__(self):

        vocab = open("words.txt")
        self.words = list(vocab)

        """
        The file words.txt should be in the
        same folder as this program for everything to work
        Download the file from
        """
        self.start()

    def start(self):

        self.game_over = False
        self.body_parts_remaining = ["head", "body", "leftarm",
                                     "rightarm", "leftleg", "rightleg"]
        self.body_parts_used = []
        self.word = random.choice(self.words).strip()
        self.letters_used = ""
        self.message_string = ""  # this string reports WIN/LOSS to player

    def __str__(self):
        """
        this defines the way to print game
        which allows checking of the progress of the game in shell
        """
        return "words={},bodypartsremaining={},bodypartsused={},lettersused={},"\
               "messagestring={}". format(self.word, self.body_parts_remaining,
                                          self.body_parts_used, self.letters_used,
                                          self.message_string)

    def make_display(self):
        """
        creates word with underscores for missing letters
        uses make_display_word, defined at top
        make_display_word ("automobile","aom") ==> "a __ __ o m o __ __ __"
        """
        return make_display_word(self.word, self.letters_used)

    def update_game(self, char):
        """
        THIS IS THE MOST IMPORTANT METHOD
        char:str - a single letter
        result:update letters_used,
        If char not in word update body_parts_used and
        body_parts_remaining (using the update_body_parts method)
        """

        # DO NOTHING if letter has already been typed or if the game is over
        if char in self.letters_used or self.game_over or not(char.isalpha()):
            pass

        else:
            """
            update letters_used, also body parts information
            if necessary
            and check for the end of the game (win or loss)
            """
            self.letters_used = self.letters_used + char
            self.update_body_parts(char)

            if string_minus(self.word, self.letters_used) == "":
                self.win_game()

            elif self.body_parts_remaining == []:
                self.lose_game()

        # to test and follow the progress of the game in shell
        print(self)

    def update_body_parts(self, char):
        """
        add the next body part to body_parts_used and remove it from
        body_parts_remaining
        """

        if char in self.word or string_minus(self.word, self.letters_used) == "":
            # do not update the body parts if the char:
            # if the player guesses correctly
            # or if the player has already won the game
            pass

        else:
            body_part = self.body_parts_remaining.pop(0)
            self.body_parts_used.append(body_part)

    def win_game(self):
        """
        result:notify player of win (on label2)
        and update the game_over attribute
        """

        self.message_string = "YOU WON THE ULTIMATE HANGMAN GAME!:)"
        self.game_over = False

    def lose_game(self):
        """
        result:notify player of loss
        and display the word they failed to guess
        and update the game_over attribute
        """

        self.message_string = "YOU LOST THE ULTIMATE HANGMAN GAME!:("
        self.game_over = True


# graphical layer
class Hangman_gui:
    """
    The graphical display part of
    Hangman
    """

    def __init__(self):
        """
        hangman_gui attributes:
        a root window, two labels, a button
        and a canvas
        label 1 will dislay the word
        label 2 displays "you won" or "you lost"
        """

        self.tkroot = tk.Tk()  # The frame holding all the components
        self.tkroot.title("The Ultimate Hangman Game")
        self.tkroot.geometry("700x700+5+5")
        self.tkroot.focus()

        labelfont = ('helvetica', 12, 'bold')
        self.label1 = tk.Label(self.tkroot)
        self.label2 = tk.Label(self.tkroot)
        self.label3 = tk.Label(self.tkroot)
        self.make_labels(labelfont)

        button = tk.Button(self.tkroot, text="Restart")
        self.make_buttons(button)

        self.canvas = tk.Canvas(self.tkroot)
        self.make_canvas()

        self.tkroot.bind('<KeyPress>', self.onkeypress)

        # create a list with names of methods
        # each draws a corresponding body part
        self.draw_action = [self.make_head, self.make_body, self.make_larm,
                            self.make_rarm, self.make_lleg, self.make_rleg]

        # create a hangman game object
        self.game = Hangman_game()
        self.start()

    def start(self):

        self.draw_scaffold()
        # draws the scaffold so players see it everytime they start the game

        self.game.start()
        # call this to set the game back to starting stage

        self.label1['text'] = make_display_word(self.game.word, "")
        self.label2['text'] = "START BY GUESSING A LETTER!"
        self.label3['text'] = "WELCOME TO THE ULTIMATE HANGMAN GAME!"

        self.tkroot.mainloop()

    def make_buttons(self, button):
        """
        configure restart button and pack it
        set its command function to self.restart
        """

        button.config(command=self.restart)
        button.pack()

    def make_canvas(self):
        """
        configure and pack canvas
        """

        self.canvas.config(height=150, width=50)
        self.canvas.pack(expand=True, fill='both')

    def draw_scaffold(self):  # draw the scaffold

        self.canvas.create_line(150, 100, 350, 100, fill='brown', width=5)
        self.canvas.create_line(175, 100, 175, 325, fill='brown', width=5)
        self.canvas.create_line(250, 100, 250, 125, fill='brown', width=5)
        self.canvas.create_polygon(175, 325, 125, 425, 400, 425, fill='brown',
                                   outline="brown", width=5)

    def make_head(self):
        self.canvas.create_oval(225, 125, 275, 175, fill='red')

    def make_body(self):
        self.canvas.create_rectangle(225, 175, 275, 250, fill='red')

    def make_larm(self):
        self.canvas.create_line(225, 175, 200, 200, fill='red')

    def make_rarm(self):
        self.canvas.create_line(275, 175, 300, 200, fill='red')

    def make_lleg(self):
        self.canvas.create_line(235, 250, 225, 300, fill='red')

    def make_rleg(self):
        self.canvas.create_line(265, 250, 275, 300, fill='red')

    def draw_body_parts(self):
        """
        retrives the functions defined above and call them accordingy
        based on the body parts added into the list of body_parts_used
        """

        for x in range(len(self.game.body_parts_used)):
            self.draw_action[x]()

    def make_labels(self, fnt):
        """
        configure the necessary labels
        and pack them
        """

        self.label1.config(font=("Courier", 20))

        self.label2['text'] = "START BY GUESSING A LETTER!"
        self.label2.config(bg='lightblue')

        self.label3.config(bg='yellow')

        self.label1.pack()
        self.label2.pack()
        self.label3.pack()

    def onkeypress(self, event):
        """
        define action carried out when user types a character
        it will be called self.onkeypress
        --grab the character typed by the user
        --update the logic game with the character typed by the user
        --update the texts on labels 1 and 2
        display the word (by updating the text on label1)
        """

        ch = event.char  # get the character typed by the user
        self.game.update_game(ch)
        self.draw_body_parts()

        if self.game.game_over == False:

            # This is the case when the player wins the game
            if string_minus(self.game.word, self.game.letters_used) == "":
                self.label1['text'] = self.game.message_string
                self.label2['text'] = "Correct Word: " + self.game.word
                self.label3['text'] = "Click Restart to Try Again"
                self.canvas.create_text(475, 150, text="I'm saved!!(*♥ω♥*)", anchor="se",
                                        font=("Comic Sans MS", 20, "bold"),
                                        fill="orange")

            # This is the case when the player is still playing
            else:
                updatelabel1 = make_display_word(self.game.word, self.game.letters_used)
                self.label1['text'] = updatelabel1

                self.label2['text'] = "Your Letter: " + ch

                updatelabel3 = ""
                for letter in self.game.letters_used:
                    updatelabel3 = updatelabel3 + letter + " "
                    # putting a space in between each letter to
                    # make the game more user friendly

                self.label3['text'] = "Your Trails: " + updatelabel3

        # This is the case when the player loses
        else:
            self.label1['text'] = self.game.message_string
            self.label2['text'] = "Correct Word: " + self.game.word
            self.label3['text'] = "Click Restart to Try Again"
            self.canvas.create_text(430, 150, text="ahhh~(;´༎ຶД༎ຶ`)", anchor="se",
                                    font=("Comic Sans MS", 20, "bold"),
                                    fill="orange")

    def restart(self):
        """
        restart the game
        change text displayed on labels
        clear the canvas
        using  self.canvas.delete("all")
        """

        self.canvas.delete("all")
        self.start()


# This starts everything.
Hangman_gui()
