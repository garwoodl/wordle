'''
File to contain all of human and bot players
Inspo taken from: https://github.com/Kinkelin/WordleCompetition/blob/main/WordleAI.py#L12
'''
from abc import ABC, abstractmethod
from word_bank import WordBank
import random

class Player:
    def __init__(self, wb: WordBank, name: str):
        '''
        Takes in a WordBank object wb and a name to identify the player
        '''
        self.wb = wb
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
        return random.choice(self.wb.word_set)