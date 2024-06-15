'''
Config file for global variables
'''

GREEN = 'G' # in correct spot
YELLOW = 'Y' # present in word but wrong spot
GRAY = '-' # not in word
BLACK = ' ' # not guessed yet

ALPHABET = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

l = [GREEN, YELLOW, GRAY]
COLOR_COMBOS = [a + b + c + d + e for a in l for b in l for c in l for d in l for e in l]