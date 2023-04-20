# Python program to print all valid words that
# are possible using character of array
import numpy
from numpy import loadtxt
import string
 
# Alphabet size
# defining our alphabet (probably can modify this to work for non-English letters)
ALPHABET = list(string.ascii_lowercase)
SIZE = len(ALPHABET)
 
# trie Node
class TrieNode:
    def __init__(self):
        # hashmap of child nodes mapping letter (key) to node (value)
        self.children = {}
        # does node represents end of a word?
        self.leaf = False
 
# Returns new trie node (initialized to NULLs)
def get_node():
    new_node = TrieNode()
    return new_node

# If not present, inserts key into trie
# If the key is prefix of trie node, just
# marks leaf node
def insert_hashmap(root, key):
    n = len(key)
    p_child = root
    for char in key:
        if char not in p_child.children:
            p_child.children[char] = get_node()
        p_child = p_child.children[char]
    # make last node as leaf node
    p_child.leaf = True
 
# A recursive function to print all possible valid
# words present in array
def searchWord(root, hash, string):
    # if this node is the leaf node
    # we have found a valid word
    if root.leaf:
        print(string)
    # otherwise, recursively explore all child nodes
    # of current node

    # for each letter in the alphabet
    for letter in ALPHABET:
        # if this letter IS in our set of letters to explore
        # and there is a child node from this node
        if letter in hash and letter in root.children:
            # recursively search the trie for if there is a sequence with
            # the string + concatenated node
            searchWord(root.children[letter], hash, string + letter)
 
# Prints all words present in dictionary.
def print_all_words(arr, root, n):
    # creates an array storing if each letter in 
    # the alphabet is in the characters to explore
    hash = arr
         
    # temporary node
    p_child = root
     
    # string to hold output words
    string = ""
     
    # Traverse all matrix elements. There are only 26
    # character possible in char array
    for letter in ALPHABET:
        # we start searching for word in dictionary
        # if we found a character which is child
        # of Trie root
        if letter in hash and letter in root.children:
            string = string + letter
            searchWord(p_child.children[letter], hash, string)
            string = ""
 
# Driver program to test above function
if __name__ == '__main__':
    # Let the given dictionary be following
    print("Loading dictionary...")
    dict = loadtxt("assets/words_alpha.txt", dtype=str,comments="#", delimiter=",", unpack=False)
    print("Dictionary loaded!")
    print("Inserting data")
    root = get_node()
     
    # insert all words of dictionary into trie
    n = len(dict)
    for word in dict:
        insert_hashmap(root, word)
    
    print("Data inserted!")
    arr = ['a', 'c', 't', 'o']
    n = len(arr)
    print(f"Checking {arr}")
    print_all_words(arr, root, n)