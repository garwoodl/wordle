'''
Host games and manage the board in the Game class
'''
from word_bank import WordBank
import config
from players import *

class Game:
    def __init__(self, wb: WordBank, word: str):
        '''
        guesses is a list of tuples (word, result)
        where each word is a string and each result is a string of chars
        representing the colored squares
        '''
        self.word_set = wb.word_set
        self.word = word
        self.words_guessed = []  # list of words guessed
        self.guess_history = []  # list of tuples of (word, result)
        self.success = False

    def guess_is_legal(self, guess):
        return len(guess) == 5 and guess in self.word_set
    
    def play_game(self, player: Player, verbose=True):
        '''
        Runs a game with the given player
        Returns (success, guesses) where success iff game won
        and guesses is a list of the words guessed
        '''


def get_result(true_word: str, guess_word: str) -> str:
    '''
    Returns a string of color characters for the given guessed word
    Assumes true_word and guess_word are same length
    '''
    result = ''
    for i, letter in enumerate(guess_word):
        if letter == true_word[i]:
            result += config.GREEN
        elif letter in true_word:
            result += config.YELLOW
        else:
            result += config.GRAY
    return result


def main():
    true_word = 'smell'
    wb = WordBank('official_word_bank.txt')
    G = Game(wb, true_word)
    
    guessed_words = ['soare', 'elend', 'gecko']
    guesses = [(w, get_result(true_word, w)) for w in guessed_words]
    available_words = G.word_bank.remaining_options(guesses)
    print(f'The word to guess is {G.word}')
    for word in guessed_words:
        print(f'{word}\t\t{get_result(G.word, word)}')
    print(available_words)


    

if __name__ == "__main__":
    main()