'''
File to contain all of human and bot players
Inspo taken from: https://github.com/Kinkelin/WordleCompetition/blob/main/WordleAI.py#L12
'''
from abc import ABC, abstractmethod
import random
import config
import math
from helper_funcs import *

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


class InfoPlayer(Player):
    def guess(self, guess_history):
        '''
        Pick the guess that maximizes the expected information gained
        '''


    def get_info_dict(self, guess_history):
        '''
        Loops through each word and then through each possible
        combination to get the expected information from 
        each combination and sums to get the expectation.
        '''
        info_dict = {}
        available_words = remaining_options(self.words, guess_history)
        n = len(available_words)  # amount of info we have now
        for word in self.words:
            combo_probs = get_combo_probs(available_words, word)
            expected_bits = 0
            for combo, prob in combo_probs.items():
                new_guess_history = guess_history.copy()
                # if we guess this word and get this combo,
                # how much does that reduce the number of available words
                new_guess_history.append((word, combo))
                # print(new_guess_history)
                new_available_words = remaining_options(available_words, new_guess_history)
                m = len(new_available_words)
                # print('m', m)
                # print('n', n)
                if m > 0:
                    bits = - math.log2(m / n)
                    # print('bits', bits)
                    expected_bits += prob * bits
            info_dict[word] = expected_bits
        return info_dict
    

def main():
    words = txt_to_set('official_word_bank.txt')
    player = InfoPlayer(words, 'info')
    guess_history = []
    info_dict = player.get_info_dict(guess_history)
    print(info_dict)

if __name__ == "__main__":
    main()