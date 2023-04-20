import numpy
from numpy import loadtxt
import string

def is_valid_word(word):
    """
    Returns if a word meets the given criteria for it to be included in the dictionary
    """
    return len(line) > 2

lines = loadtxt("assets/words_alpha.txt", dtype=str,comments="#", delimiter=",", unpack=False)

with open('assets/words_sanitised.txt', 'w') as f:
    for line in lines:
        if is_valid_word(line):
            f.write(f"{line}\n")