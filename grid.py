import pygame
import pygame_widgets
from pygame_widgets.button import Button

import random
import numpy
from numpy import loadtxt

import pickle

from trie import Trie

from enemies.enemy_factory import EnemyFactory
from enemies.enemy import Enemy
from enemies.roman_soldier import RomanSoldier
from enemies.persian_soldier import PersianSoldier
from enemies.minotaur import Minotaur

from players.player import Player

factory = EnemyFactory()
factory.register_enemy_type('ROMANSOLDIER', RomanSoldier)
factory.register_enemy_type('PERSIANSOLDIER', PersianSoldier)
factory.register_enemy_type('MINOTAUR', Minotaur)

global value_list 
value_list = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 
            'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 
            'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 
            'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

global VALID_WORD_COLOUR 
VALID_WORD_COLOUR = (124,252,0)
global INVALID_WORD_COLOUR 
INVALID_WORD_COLOUR = (255,0,0)
global ENEMY_STATS_COLOUR 
ENEMY_STATS_COLOUR = (255,255,0)
global PLAYER_STATS_COLOUR 
PLAYER_STATS_COLOUR = (0,255,0)

trie = Trie()
# loading dictionary trie from pickle
# with open('assets/english_dictionary.txt', 'rb+') as file:
#     trie = pickle.load(file)

class Cell:
    """
    Class representing a Tile the player can select to assemble words
    """
    def __init__(self, x, y):
        self.clicked = False
        self.letter = random.choice(list(value_list.keys()))
        self.value = value_list[self.letter]
        self.multiplier = 1
        self.letterName = f"assets/vanilla_letters/{self.letter}.png"
        self.grayscaleLetterName = f"assets/grayscale_letters/{self.letter}.png"
        self.sprite = pygame.image.load(self.letterName)
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_click_state(self):
        self.clicked = not (self.clicked)
        if self.clicked:
            self.sprite = pygame.image.load(self.grayscaleLetterName)
            # TODO: move logic tracking clicked letters to Board
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

    def check_click(self, mouse_position):
        """
        Returns whether the current mouse position is colliding with hitbox
        """
        return pygame.Rect.collidepoint(self.rect, mouse_position)

    def __str__(self):
        return str(self.letter)

class Board:
    """
    Class representing a collection of Cell objects
    grid_x_size -- number of columns of Cell objects
    grid_y_size -- number of rows of Cell objects
    start_x_pos -- x position on the screen where the Cells should start drawing from
    start_y_pos -- y position on the screen where the Cells should start drawing from
    """
    def __init__(self,
                grid_x_size=4,
                grid_y_size=4, 
                start_x_pos=250, 
                start_y_pos=600):
        self.grid_x_size = grid_x_size
        self.grid_y_size = grid_y_size
        self.start_x_pos = start_x_pos
        self.start_y_pos = start_y_pos
        self.board = [[Cell(self.start_x_pos + (120 * x), start_y_pos + (120 * y)) for x in range(self.grid_x_size)] for y in range(self.grid_y_size)]

    def get_all_letters(self):
        """
        Returns a list of all letters for cells in the current board
        """
        letters = []
        for row in board.board:
            for column in row:
                letters.append(column.letter)
        return letters

    def get_all_possible_words(self):
        """
        Gets all possible accepted words for this grid
        """
        return trie.get_all_words_from_set_of_letters(root=trie.root,letter_set=self.get_all_letters())

    def get_new_hints(self, num_hints=1):
        """
        Gets a random possible word given the board's current set of letters
        """
        return random.sample(sorted(self.get_all_possible_words()),num_hints)
    
    def get_new_clicked_cells(self):
        """
        Replaces any clicked cells with new cells
        """
        row_count = 0
        for row in self.board:
            col_count = 0
            for col in row:
                if (col.clicked):
                    self.board[row_count][col_count] = Cell(self.start_x_pos + (120 * col_count), self.start_y_pos + (120 * row_count))
                col_count += 1
            row_count += 1

    def __str__(self):
        """
        Stringified representation of the board
        """
        return str(self.get_all_letters())

grid_size = 4
global board
board = Board()
enemy = factory.create()
player = Player()

pygame.init()
window = pygame.display.set_mode((1000,1200))
my_font = pygame.font.SysFont('monospace', 30)
logo = pygame.image.load("assets/logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("LitWorm")

# player information display
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
global chosen_word_surface
chosen_word_surface = my_font.render(''.join(clicked_letters), False, (255, 255, 255))
global hint
hint = ""
global hint_text_surface
hint_text_surface = my_font.render(str(hint), False, (255, 255, 255))

# enemy stats display
global current_enemy_name_surface
current_enemy_name_surface = my_font.render(enemy.name, False, (ENEMY_STATS_COLOUR))

def unclick_all_tiles():
    """
    Unclicks all tiles and clears selected word
    """
    for iy, rowOfCells in enumerate(board.board):
        for ix, cell in enumerate(rowOfCells):
            cell.set_unclicked()
    global clicked_letters
    clicked_letters = []
    global current_selected_word
    current_selected_word = ''
    global current_word_score
    current_word_score = 0
    chosen_word_surface = my_font.render(''.join(clicked_letters), False, VALID_WORD_COLOUR)

def generate_new_board():
    """
    Generates a new board object and updates the contents
    """
    global board
    board = Board()
    global clicked_letters
    clicked_letters = []
    global current_score
    current_score = 0

def get_word_score(word):
    score = 0
    if trie.find(word):
        for letter in word:
            score += value_list[letter]
    return score    

def score_word():
    global current_score
    # check if the currently selected word is a valid word
    # if it is, calculate the score as the base value by the multiplier
    global current_selected_word
    current_score += get_word_score(current_selected_word)
    global enemy
    enemy.deal_damage(get_word_score(current_selected_word))
    if enemy.is_dead():
        print(f"Defeated enemy!")
        enemy = factory.create()
    # remove all clicked tiles and repopulate the grid
    row_count = 0
    global board
    board.get_new_clicked_cells()
    unclick_all_tiles()
    clear_hint()

def clear_hint():
    global hint
    hint = ""
    hint_text_surface = my_font.render(str(hint), False, (255, 255, 255))

def update_hint():
    # generate new hint
    global hint
    hint = board.get_new_hints(1)
    hint_text_surface = my_font.render(str(hint), False, (255, 255, 255))
    # clear player's current score
    global current_score
    current_score = 0

# button to reset grid
unselect_all_button = Button(
    window, # surface
    50, #x-coord of top left
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
    50, #x-coord of top left
    750, # y-coord of top left
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
score_word_button = Button(
    window, # surface
    50, #x-coord of top left
    900, # y-coord of top left
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

# button to generate a hint for the given board
generate_hint_button = Button(
    window, # surface
    50, #x-coord of top left
    1050, # y-coord of top left
    200,
    120,
    text='Hint',
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda:(update_hint())
)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:    
            if event.button == 1:
                # checking if any of the Cells have been clicked
                for row in board.board:
                    for cell in row:
                        if cell.check_click(event.pos):
                            cell.update_click_state()

    window.fill((0,0,0))
    # drawing grid of letters
    for iy, rowOfCells in enumerate(board.board):
        for ix, cell in enumerate(rowOfCells):
            window.blit(cell.sprite, (250 + (ix * 120), 600 + (iy * 120)))
    # drawing player sprite
    window.blit(player.sprite, (0,50))
    # drawing enemy
    window.blit(enemy.sprite, (500,50))
    window.blit(chosen_word_surface, (0,480))
    current_score_surface = my_font.render(str(current_score), False, (255, 255, 255))
    # updating label for selected text
    current_selected_word = ''.join(clicked_letters)
    if (trie.find(current_selected_word)):
        chosen_word_surface = my_font.render(current_selected_word, False, VALID_WORD_COLOUR)
    else:
        chosen_word_surface = my_font.render(current_selected_word, False, INVALID_WORD_COLOUR)
    # updating label for selected word score
    current_word_score = get_word_score(current_selected_word)
    current_word_score_surface = my_font.render(f"scores {str(current_word_score)} points", False, (255,255,255))
    hint_text_surface = my_font.render(f"hint {hint}", False, (255,255,255))
    window.blit(current_score_surface, (100, 550))
    window.blit(current_word_score_surface, (200, 550))
    window.blit(hint_text_surface, (500, 550))

    # updating player information UI
    player_name_surface = my_font.render(f"{player.name}", False, (PLAYER_STATS_COLOUR))
    window.blit(player_name_surface, (0,0))
    player_health_surface = my_font.render(f"{player.current_health}/{player.max_health}", False, (PLAYER_STATS_COLOUR))
    window.blit(player_health_surface, (0,20))

    # updating enemy information UI
    current_enemy_name_surface = my_font.render(f"{enemy.name}", False, (ENEMY_STATS_COLOUR))
    window.blit(current_enemy_name_surface, (900,0))
    current_enemy_health_surface = my_font.render(f"{enemy.current_health}/{enemy.max_health}", False, (ENEMY_STATS_COLOUR))
    window.blit(current_enemy_health_surface, (900,20))

    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()
exit()