import pygame
import pygame_widgets
from pygame_widgets.button import Button, ButtonArray

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
        self.multiplier = 1
        self.letterName = f"assets/vanilla_letters/{self.letter}.png"
        self.grayscaleLetterName = f"assets/grayscale_letters/{self.letter}.png"
        self.sprite = pygame.image.load(self.letterName)

    def update_click_state(self):
        self.clicked = not (self.clicked)
        if self.clicked:
            self.sprite = pygame.image.load(self.grayscaleLetterName)
            clicked_letters.append(self.letter)
        else:
            self.sprite = pygame.image.load(self.letterName)
            clicked_letters.remove(self.letter)

    def set_unclicked(self):
        if self.clicked:
            self.sprite = pygame.image.load(self.letterName)
            clicked_letters.remove(self.letter)
            self.clicked = False

    def set_clicked(self):
        if not self.clicked:
            self.sprite = pygame.image.load(self.grayscaleLetterName)
            clicked_letters.append(self.letter)
            self.clicked = True

# class Board:
#     def __init__(self, grid_x_size, grid_y_size):
#         self.grid_x_size = grid_x_size
#         self.grid_y_size = grid_y_size
#         self.board = [[Cell() for _ in range(self.grid_x_size)] for _ in range(self.grid_y_size)]                     

grid_size = 4
global board
board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

# board = Board(grid_size, grid_size)

pygame.init()
window = pygame.display.set_mode((1000,1200))
my_font = pygame.font.SysFont('monospace', 30)
logo = pygame.image.load("assets/logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("LitWorm")
global clicked_letters
clicked_letters = []
global current_score
current_score = 0
global current_word_score
current_word_score = 0
global current_score_surface
current_score_surface = my_font.render(str(current_score), False, (255, 255, 255))
global current_word_score_surface
current_score_surface = my_font.render(str(current_score), False, (255, 255, 255))
global text_surface
text_surface = my_font.render(''.join(clicked_letters), False, (255, 255, 255))

# loading text file of valid english words into memory
lines = loadtxt("assets/words_alpha.txt", dtype=str,comments="#", delimiter=",", unpack=False)

def unclick_all_tiles():
    """
    Unclicks all tiles and clears selected word
    """
    for iy, rowOfCells in enumerate(board):
        for ix, cell in enumerate(rowOfCells):
            cell.set_unclicked()
    global clicked_letters
    clicked_letters = []
    global current_selected_word
    current_selected_word = ''
    global current_word_score
    current_word_score = 0
    text_surface = my_font.render(''.join(clicked_letters), False, VALID_WORD_COLOUR)

def generate_new_board():
    """
    Generates a new board object and updates the contents
    """
    global board
    board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
    global clicked_letters
    clicked_letters = []

def get_word_score(word):
    score = 0
    if is_valid_word(word):
        for letter in word:
            score += value_list[letter]
    return score

def score_word():
    global current_score
    # check if the currently selected word is a valid word
    # if it is, calculate the score as the base value by the multiplier
    global current_selected_word
    current_score += get_word_score(current_selected_word)
    # remove all clicked tiles and repopulate the grid
    row_count = 0
    for row in board:
        col_count = 0
        for col in row:
            if (col.clicked):
                board[row_count][col_count] = Cell()
            col_count += 1
        row_count += 1
    unclick_all_tiles()


# button to reset grid
unselect_all_button = Button(
    window, # surface
    500, #x-coord of top left
    600, # y-coord of top left
    200,
    120,
    text='Unselect all',
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda:unclick_all_tiles()
)

# button to reset grid
new_grid_button = Button(
    window, # surface
    250, #x-coord of top left
    600, # y-coord of top left
    200,
    120,
    text='New grid',
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda:generate_new_board()
)

# button to score current word
new_grid_button = Button(
    window, # surface
    50, #x-coord of top left
    600, # y-coord of top left
    200,
    120,
    text='Score word',
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda:score_word()
)

"""
Returns whether a given string is found in the list of valid words
"""
def is_valid_word(word):
    return (word in lines and len(word) > 2)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:    
            if event.button == 1:
                row = event.pos[1] // 120
                col = event.pos[0] // 120
                # checking if clicked area is actually in the grid
                # this probably holds up horribly in stuff with an actual UI but it'll do for now
                if (row < grid_size and col < grid_size):
                    board[row][col].update_click_state()
    window.fill((0,0,0))
    for iy, rowOfCells in enumerate(board):
        for ix, cell in enumerate(rowOfCells):
            window.blit(cell.sprite, (ix * 120, iy * 120))
    window.blit(text_surface, (0,480))
    current_score_surface = my_font.render(str(current_score), False, (255, 255, 255))
    # updating label for selected text
    current_selected_word = ''.join(clicked_letters)
    if (is_valid_word(current_selected_word)):
        text_surface = my_font.render(current_selected_word, False, VALID_WORD_COLOUR)
    else:
        text_surface = my_font.render(current_selected_word, False, INVALID_WORD_COLOUR)
    # updating label for selected word score
    current_word_score = get_word_score(current_selected_word)
    current_word_score_surface = my_font.render(f"scores {str(current_word_score)} points", False, (255,255,255))
    window.blit(current_score_surface, (100, 480))
    window.blit(current_word_score_surface, (200, 480))
    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()
exit()