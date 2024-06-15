'''
Stores miscellaneous helpful functions
'''
import config

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