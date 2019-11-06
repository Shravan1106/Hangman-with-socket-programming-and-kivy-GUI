#!/usr/bin/env python3

# Hangman
# By Bisola Bruno solaocodes@gmail.com

import os
from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.anchorlayout import AnchorLayout

FPS = 1 / 60  # frames per second
WINDOWWIDTH = 500  # size of window's with in pixels
WINDOWHEIGHT = 600  # size of window's height in pixels
NUM_OF_GUESSES = 4  # number of guesses before game over
INNER_MARGIN = 15  # distance of inner border from window edge in pixels
OUTER_MARGIN = 10  # distance of outer border from window edge in pixels
LINE_LENGTH = 13  # length of single line of a capital letter.

#           R    G    B    A
SALMON = (0.58, 0.24, 0.28, 1.00)
GOLD = (1.00, 0.84, 0.00, 1.00)
WHITE = (1.00, 1.00, 1.00, 1.00)
FADED_WHITE = (1.00, 1.00, 1.00, 0.30)
LIGHT_RED = (1.00, 0.00, 0.00, 0.50)
LIGHT_GREEN = (0.00, 1.00, 0.00, 0.50)
NO_COLOR = (0.00, 0.00, 0.00, 0.00)


def start_conditions():
    # Sets the starting conditions for a new game.

    # open up a text file with a category and words.
    files = list(filter(lambda x: x.endswith('.txt'), os.listdir()))
    file_in = files[randint(0, len(files) - 1)]
    with open(file_in, 'r') as f:
        words = f. readlines()

    words = [i.strip() for i in words]
    category = words[0].upper()
    word = words[randint(1, len(words) - 1)]
    hidden_word = ['_' if i.isalpha() else i for i in word]
    misses = 0

    # Properly aligns word/phrase longer than a single line.
    if len(word) > LINE_LENGTH and ' ' in word[LINE_LENGTH - 1:]:
        space = word[LINE_LENGTH - 1:].index(' ') + (LINE_LENGTH - 1)
        hidden_word[space] = '\n'
    elif len(word) > LINE_LENGTH:
        space = word[:LINE_LENGTH].rfind(' ')
        hidden_word[space] = '\n'

    return category, word, hidden_word, misses


class HangmanBoard(AnchorLayout):
    # Class that contains the Hangman game

    category, word, hidden_word, misses = start_conditions()

    def update(self, dt):
        # renders updates of guesses and hidden word, and checks if the game is
        # won or not

        self.ids['category'].text = self.category
        self.ids['hidden'].text = ' '.join(self.hidden_word)

        self.hangman_body()
        self.win_or_lose()

    def win_or_lose(self):
        # checks if the game is won or not

        list1 = [i for i in self.word if i.isalpha()]
        list2 = [i for i in ''.join(self.hidden_word) if i.isalpha()]
        if list1 == list2:
            self.disable_letters()
        elif NUM_OF_GUESSES == self.misses:
            self.disable_letters()

    def hangman_body(self):
        # draws/reveals the hangman body

        body = self.ids['gallows'].canvas.get_group('body')
        if self.misses == 1:
            body[0].rgba = WHITE  # the head
        elif self.misses == 2:
            body[1].rgba = WHITE  # the body
        elif self.misses == 3:
            body[2].rgba = WHITE  # the arms
        elif self.misses == 4:
            body[3].rgba = WHITE  # the legs

    def letter_click(self, letter):
        # Checks if clicked letter is in the word or not

        letter.disabled = True
        letter.disabled_color = WHITE

        guess = letter.text.lower()
        answer = self.word.lower()

        # sets letter background to red
        letter.background_color = LIGHT_RED

        # checks for match, and turns letter background green if correct
        if guess in answer:
            for i in range(len(answer)):
                if guess == answer[i]:
                    self.hidden_word[i] = self.word[i]
                    letter.background_color = LIGHT_GREEN
        else:
            self.misses += 1

    def disable_letters(self):
        # disables all remaining letter buttons right after game is won or lost

        for k, v in self.ids.items():
            if k[0:6] == 'letter' and v.disabled is False:
                v.disabled = True
                v.disabled_color = FADED_WHITE

    def enable_letters(self):
        # enables letter buttons

        for k, v in self.ids.items():
            if k[0:6] == 'letter':
                v.disabled = False
                v.background_color = SALMON

    def new_game(self):
        # refreshes game board with new game.

        t = start_conditions()
        self.category, self.word, self.hidden_word, self.misses = t

        self.enable_letters()

        body = self.ids['gallows'].canvas.get_group('body')
        for parts in body:
            parts.rgba = NO_COLOR


class HangmanApp(App):
    # App that runs Hangman game.

    # Configuration Settings
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('graphics', 'resizable', 0)
    Config.set('graphics', 'width', WINDOWWIDTH)
    Config.set('graphics', 'height', WINDOWHEIGHT)

    # Makes constant variables avaiable to hangman.kv file
    IM = INNER_MARGIN
    OM = OUTER_MARGIN
    BACKGROUND_COLOR = SALMON
    BORDER_LINE_COLOR = GOLD
    BODY_COLOR = NO_COLOR
    GALLOW_COLLOR = GOLD

    def build(self):
        game = HangmanBoard()
        Clock.schedule_interval(game.update, FPS)
        return game


if __name__ == '__main__':
    HangmanApp().run()
