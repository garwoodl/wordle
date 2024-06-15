'''
Host games and manage the board in the Game class
'''
import config
from players import Player

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

def txt_to_set(filename):
    word_set = set()
    with open(filename, mode='r') as file:
      for line in file:
        word_set.add(line.strip().lower())
    return word_set

def get_result(true_word: str, guess_word: str) -> str:
    '''
    Returns a string of color characters for the given guessed word
    Assumes true_word and guess_word are same length
    '''
    result = [config.GRAY] * 5
    # make a dict to keep track of multiple letter occurrences
    true_counts = {}
    for c in true_word:
        if c in true_counts:
            true_counts[c] += 1
        else:
            true_counts[c] = 1

    # iterate once to get all greens
    for i, letter in enumerate(guess_word):
        if letter == true_word[i]:
            result[i] = config.GREEN
            true_counts[letter] -= 1
    # iterate again to get the yellows
    for i, letter in enumerate(guess_word):
        if ((letter in true_word) and (result[i] == config.GRAY) and 
            (true_counts[letter] > 0)):
            result[i] = config.YELLOW
            true_counts[letter] -= 1  # make sure not to overdisplay yellows
        
    return ''.join(result)

def get_combo_probs(possible_words, guess):
    '''
    Given a list of possible words (for example by using remaining options) this
    function returns a dictionary of all result combinations and their respective
    probability of happening
    '''
    n = len(possible_words)
    combo_probs = {combo: 0 for combo in config.COLOR_COMBOS}
    
    for w in possible_words:
        result = get_result(w, guess)
        combo_probs[result] += 1 / n
    return combo_probs


def main():
    word = 'grace'
    filename = 'test_words.txt'
    words = txt_to_set(filename)

    combo_probs = get_combo_probs(words, 'aaaaa')
    sorted_probs = {k: v for k, v in sorted(combo_probs.items(), key=lambda item: item[1])}
    print(sorted_probs)


    

if __name__ == "__main__":
    main()