import pygame
import random
import numpy
from numpy import loadtxt

global value_list 
value_list = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 
            'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 
            'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 
            'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

global VALID_WORD_COLOUR 
VALID_WORD_COLOUR = (124,252,0)
global INVALID_WORD_COLOUR 
INVALID_WORD_COLOUR = (255,0,0)

class Cell:
    def __init__(self):
        self.clicked = False
        self.letter  = random.choice(list(value_list.keys()))
        self.value = value_list[self.letter]
        self.letterName = f"assets/letters/{self.letter}.png"
        self.sprite = pygame.image.load(self.letterName)

grid_size = 4
board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

pygame.init()
window = pygame.display.set_mode((500, 510))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('monospace', 30)
logo = pygame.image.load("assets/logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("LitWorm")
clicked_letters = []
text_surface = my_font.render(''.join(clicked_letters), False, (255, 255, 255))

# loading text file of valid english words into memory
lines = loadtxt("assets/words_alpha.txt", dtype=str,comments="#", delimiter=",", unpack=False)
print(lines)

"""
Returns whether a given string is found in the list of valid words
"""
def is_valid_word(word):
    return (word in lines and len(word) > 2)

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:    
            if event.button == 1:
                row = event.pos[1] // 120
                col = event.pos[0] // 120
                print(f"{board[row][col].clicked}")
                board[row][col].clicked = not (board[row][col].clicked)
                if(board[row][col].clicked):
                    clicked_letters.append(board[row][col].letter)
                else:
                    clicked_letters.remove(board[row][col].letter)
                print(f"clicked {row}-{col}, letter {board[row][col].letter} with value {board[row][col].value}")
                print(f"{clicked_letters}")
                # updating label for selected text
                current_selected_word = ''.join(clicked_letters)
                if (is_valid_word(current_selected_word)):
                    text_surface = my_font.render(current_selected_word, False, VALID_WORD_COLOUR)
                else:
                    text_surface = my_font.render(current_selected_word, False, INVALID_WORD_COLOUR)
    window.fill(0)
    for iy, rowOfCells in enumerate(board):
        for ix, cell in enumerate(rowOfCells):
            color = (64, 64, 64) if cell.clicked else (164, 164, 164)
            # pygame.draw.rect(window, color, (ix*20+1, iy*20+1, 18, 18))
            window.blit(cell.sprite, (ix * 120, iy * 120))
            window.blit(text_surface, (0,480))
    pygame.display.flip()

pygame.quit()
exit()