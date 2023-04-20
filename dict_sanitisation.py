import numpy
from numpy import loadtxt
import string

def is_valid_word(word):
    """
    Returns if a word meets the given criteria for it to be included in the dictionary
    Current criteria:
    - word is >2 characters long (i.e. no NO)
    - word has at least 2 unique letters (i.e. no AAA)
    """
    return len(line) > 2 and len(set(word)) > 1

lines = loadtxt("assets/words_alpha.txt", dtype=str,comments="#", delimiter=",", unpack=False)

with open('assets/words_sanitised.txt', 'w') as f:
    for line in lines:
        if is_valid_word(line):
            f.write(f"{line}\n")