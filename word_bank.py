"""
File to handle the WordBank class which makes WordBank objects consisting of
all possible legal words and has functions to get legal moves
"""

import csv

ALPHABET = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

class WordBank:
  def __init__(self, filename=''):
    self.filename=filename
    self.word_set = set()

    # load the file into the word set
    with open(self.filename, mode='r') as f:
      the_file = csv.reader(f)
      for lines in the_file:
        self.word_set.add(lines[0].lower())


def main():
  test_bank = WordBank(filename='test_word_bank.csv')
  print(test_bank.word_set)


if __name__ == "__main__":
  main()
