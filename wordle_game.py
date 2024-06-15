'''
Host games and manage the board in the Game class
'''
import config
from players import Player
import matplotlib.pyplot as plt
from helper_funcs import *

def guess_is_legal(words, guess):
    return len(guess) == 5 and guess in words
    
def play_game(words, word, player: Player, verbose=True):
    '''
    Runs a game with the given player, legal_words (words), and target word (word)
    Returns (success, words_guessed) where success iff game won
    and guesses is a list of the words guessed
    '''
    # inspo from https://github.com/Kinkelin/WordleCompetition/blob/main/Competition.py#L36
    guess_history = []
    words_guessed = []
    for i in range(6):  # six guesses
        guess = player.guess(guess_history)
        if not guess_is_legal(words, guess):
            if verbose:
                print(f'Illegal guess!')
                print(f'{player.name} cannot guess {guess}.')
            return False, words_guessed
        
        result = get_result(word, guess)
        words_guessed.append(guess)
        guess_history.append((guess, result))

        if guess == word:
            if verbose:
                print("Good Job!")
                print(f"{player.name} correctly guessed {word} in {i+1} guesses!")
            return True, words_guessed
    return False, words_guessed


def main():
    word = 'grace'
    filename = 'test_words.txt'
    words = txt_to_set(filename)

    combo_probs = get_combo_probs(words, word)
    sorted_probs = {k: v for k, v in sorted(combo_probs.items(), key=lambda item: item[1])}
    print(sorted_probs)


    

if __name__ == "__main__":
    main()