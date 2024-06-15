'''
File to contain all of human and bot players
Inspo taken from: https://github.com/Kinkelin/WordleCompetition/blob/main/WordleAI.py#L12
'''
from abc import ABC, abstractmethod
import random
import config


def remaining_options(words, guess_history):
    '''
    Guesses is a list of tuples (word, result)
    Returns the subset of words that fit the parameters
    '''
    in_word = set()  # set of characters
    right_place = set()  # set of tuples (char, index)
    wrong_place = set()  # set of tuples (char, index)
    not_in_word = set()  # set of characters

    for word, result in guess_history:
        for i, letter in enumerate(word):
            if result[i] == config.GREEN:
                in_word.add(letter)
                right_place.add((letter, i))
            elif result[i] == config.YELLOW:
                in_word.add(letter)
                wrong_place.add((letter, i))
            else:
                not_in_word.add(letter)
    # in case there were multiple occurrences of a letter
    not_in_word = not_in_word.difference(in_word)

    # filter words
    for c in in_word:
        words = [w for w in words if c in w]
    for c in not_in_word:
        words = [w for w in words if c not in w]
    for c in right_place:
        words = [w for w in words if c[0] == w[c[1]]]
    for c in wrong_place:
        words = [w for w in words if c[0] != w[c[1]]]

    return set(words)

class Player:
    def __init__(self, words: set[str], name: str):
        '''
        Takes in a WordBank object wb and a name to identify the player
        '''
        self.words = words
        self.name = name
    
    @abstractmethod
    def guess(self, guess_history):
        """
        Returns a 5 letter word trying to guess the wordle.

        Parameters
        ----------
        guess_history : list of tuples (guess, result)
            A list of tuples (word, result) with result consisting of config.{color} for each letter on their
            position specifically, for example one previous guess with the guess 'steer' for the word 'tiger':
            [('steer',[config.GRAY, config.YELLOW, config.YELLOW, config.GREEN, config.GREEN])]
        """
        pass

class RandomPlayer(Player):
    def guess(self, guess_history):
        available_words = list(remaining_options(self.words, guess_history))
        return random.choice(available_words)
    
class HumanPlayer(Player):
    def guess(self, guess_history):
        while True:
            try:
                guess = input("Enter a word: ")
                guess = guess.lower()
                if guess == 'q':
                    return False
                if guess in self.words:
                    return guess
                else:
                    print("That is not a valid word. Try again...")
            except:
                print("Invalid input. Try again...")