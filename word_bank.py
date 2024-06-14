"""
File to handle the WordBank class which makes WordBank objects consisting of
all possible legal words and has functions to get legal moves
"""
import copy
import config

class WordBank:
  def __init__(self, filename=''):
    self.filename=filename
    self.word_set = set()

    # load the file into the word set
    with open(self.filename, mode='r') as file:
      for line in file:
        self.word_set.add(line.strip().lower())
  
  def __str__(self):
    s = f'{len(self.word_set)} words\n'
    for w in self.word_set:
      s += f'{w}, '
    s = s[:-2]  # remove last ,
    return s
  
  def __eq__(self, wb2):
    return self.word_set == wb2.word_set

  def __copy__(self):
    return copy.deepcopy(self)
  
  def remaining_options(self, guesses):
    '''
    Guesses is a list of tuples (word, result)
    Returns the set of words from the word_bank
    that fit the parameters
    '''
    words = self.word_set

    # find which letters are allowed
    in_word = set()  # set of characters
    right_place = set()  # set of tuples (char, index)
    wrong_place = set()  # set of tuples (char, index)
    not_in_word = set()  # set of characters

    for word, result in guesses:
      for i, letter in enumerate(word):
        if result[i] == config.GREEN:
          in_word.add(letter)
          right_place.add((letter, i))
        elif result[i] == config.YELLOW:
          in_word.add(letter)
          wrong_place.add((letter, i))
        else:
          not_in_word.add(letter)

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
    

def main():
  test_bank = WordBank(filename='test_words.txt')
  print(test_bank)



if __name__ == "__main__":
  main()
