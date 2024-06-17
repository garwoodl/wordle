'''
File to contain all of human and bot players
Inspo taken from: https://github.com/Kinkelin/WordleCompetition/blob/main/WordleAI.py#L12
'''
from abc import ABC, abstractmethod
import random
import config
import math
from helper_funcs import *
from operator import itemgetter
import json
import os

class Player:
    def __init__(self, words: set[str], name: str):
        '''
        Takes in a WordBank object wb and a name to identify the player
        '''
        self.words = words
        self.name = name
    
    @abstractmethod
    def guess(self, guess_history, verbose=False):
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
    def __init__(self, words: set[str], name: str, starting_dict_filename='info_dict.json'):
        '''
        Load the precomputed info
        '''
        self.words = words
        self.name = name
        if os.path.isfile(starting_dict_filename):
            with open(starting_dict_filename, 'r') as json_file:
                self.loaded_combo_probs = json.load(json_file)
        else:
            print(f"{starting_dict_filename} does not exist yet. Creating it now...")
            self.loaded_combo_probs = self.get_info_dict([], verbose=True)
            print(f"{starting_dict_filename} created.")
            with open(starting_dict_filename, 'w') as json_file:
                json.dump(self.loaded_combo_probs, json_file)

    def guess(self, guess_history, verbose=False):
        '''
        Pick the guess that maximizes the expected information gained
        '''
        options = remaining_options(self.words, guess_history)
        if len(options) == 1:
            return list(options)[0]

        if len(guess_history) == 0:
            info_dict = self.loaded_combo_probs
        else:
            info_dict = self.get_info_dict(guess_history, verbose=verbose)
        argmax = max(info_dict, key=info_dict.get)
        if verbose:
            print(f"{self.name} chooses {argmax} for guess number {len(guess_history) + 1}.")
        return argmax

    def get_info_dict(self, guess_history, verbose=False):
        '''
        Loops through each word and then through each possible
        combination to get the expected information from 
        each combination and sums to get the expectation.
        '''
        info_dict = {}
        available_words = remaining_options(self.words, guess_history)
        n = len(available_words)  # amount of info we have now
        for i, word in enumerate(self.words):
            if verbose and i % 2000 == 0:
                print(f"{round(i / len(self.words), 4)*100}% done...")
                headline = dict(sorted(info_dict.items(), key=itemgetter(1), reverse=True)[:10])
                print(headline)
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
        if verbose:
            print('Done.')
        return info_dict

class InfoPlayerAnswerSet(InfoPlayer):
    def __init__(self, words: set[str], answer_words: set[str], name: str, starting_dict_filename='info_dict.json'):
        '''
        Load the precomputed info
        '''
        self.words = words
        self.answer_words = answer_words
        self.name = name
        if os.path.isfile(starting_dict_filename):
            with open(starting_dict_filename, 'r') as json_file:
                self.loaded_combo_probs = json.load(json_file)
        else:
            print(f"{starting_dict_filename} does not exist yet. Creating it now...")
            self.loaded_combo_probs = self.get_info_dict([], verbose=True)
            print(f"{starting_dict_filename} created.")
            with open(starting_dict_filename, 'w') as json_file:
                json.dump(self.loaded_combo_probs, json_file)

    def guess(self, guess_history, verbose=False):
        '''
        Pick the guess that maximizes the expected information gained
        '''
        options = remaining_options(self.answer_words, guess_history)
        if len(options) == 1:
            return list(options)[0]

        if len(guess_history) == 0:
            info_dict = self.loaded_combo_probs
        else:
            info_dict = self.get_info_dict(guess_history, verbose=verbose)
        argmax = max(info_dict, key=info_dict.get)
        if verbose:
            print(f"{self.name} chooses {argmax} for guess number {len(guess_history) + 1}.")
        return argmax

    def get_info_dict(self, guess_history, verbose=False):
        '''
        Loops through each word and then through each possible
        combination to get the expected information from 
        each combination and sums to get the expectation.
        '''
        info_dict = {}
        available_words = remaining_options(self.answer_words, guess_history)
        n = len(available_words)  # amount of info we have now
        for i, word in enumerate(self.words):
            if verbose and i % 2000 == 0:
                print(f"{round(i / len(self.words), 4)*100}% done...")
                headline = dict(sorted(info_dict.items(), key=itemgetter(1), reverse=True)[:10])
                print(headline)
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
        if verbose:
            print('Done.')
        return info_dict

def main():
    words = txt_to_set('official_word_bank.txt')
    player = InfoPlayer(words, 'info')
    guess_history = []
    info_dict = player.get_info_dict(guess_history)
    print(info_dict)

if __name__ == "__main__":
    main()