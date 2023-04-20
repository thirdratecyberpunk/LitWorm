# Python program to print all valid words that
# are possible using character of array
import numpy
from numpy import loadtxt
import string
 
# Alphabet size
# defining our alphabet (probably can modify this to work for non-English letters)
ALPHABET = list(string.ascii_lowercase)
SIZE = len(ALPHABET)

class Trie:
    def __init__(self, filename="assets/words_sanitised.txt"):
        print("Loading dictionary...")
        self.dict = loadtxt(filename, dtype=str,comments="#", delimiter=",", unpack=False)
        print("Dictionary loaded!")
        print("Inserting data")
        self.root = TrieNode()
        
        # insert all words of dictionary into trie
        for word in self.dict:
            self.insert(word)
        print("Data inserted!")
    
    # If not present, inserts key into trie
    # If the key is prefix of trie node, just
    # marks leaf node
    def insert(self, key):
        p_child = self.root
        for i, char in enumerate(key):
            if char not in p_child.children:
                prefix = key[0:i+1]
                p_child.children[char] = TrieNode(prefix)
            p_child = p_child.children[char]
        # make last node as leaf node
        p_child.leaf = True

    def find(self, word):
        """
        Returns if a given word exists in the language trie
        i.e. there is a valid leaf node
        """
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]

        # New code, None returned implicitly if this is False
        if current.leaf:
            return current

    def get_all_words_from_set_of_letters(self, root, letter_set, words=set()):
        """
        Finds all words that can be constructed from a given
        set of letters
        """
        # set the current node to explore to the root given 
        # from the first call
        # let's say you have C,A,T
        # C is the root node
        # then, need to check CA
        # then, need to check CT
        # then, make A the root node
        # then, check AC
        # then, check AT
        # then, need to make T the root node
        # then, need to check TC
        # then, need to check TA
        # finally, need to return the set of words that are valid
        # in this case, it should be C, A, T, TA, AT, CAT and TAC
        current = root
        root.visited = True
        for letter in letter_set:
            other_letters = letter_set.copy()
            other_letters.remove(letter)
            if letter in root.children: 
                current = root.children[letter]
                if current.leaf and current.text not in words:
                    words.add(current.text)
                # if we haven't already explored this node
                if current.visited is False:
                    for other_letter in other_letters:
                        self.get_all_words_from_set_of_letters(current, other_letters, words)
                else:
                    pass
        return words

# trie Node
class TrieNode:
    def __init__(self, text=''):
        # string representing text of node
        self.text = text
        # hashmap of child nodes mapping letter (key) to node (value)
        self.children = {}
        # does node represents end of a word?
        self.leaf = False
        # has this node already BEEN the root node?
        self.visited = False
 
# Driver program to test above function
if __name__ == '__main__':
    trie = Trie()
    # arr = ['y', 'u','o','s','r','p','t','u','a','y','q','b','o','l','p','d']
    arr = ['c', 'a', 't', 'a','o']
    print(f"Checking {arr}")
    print(trie.get_all_words_from_set_of_letters(root=trie.root, letter_set=arr))