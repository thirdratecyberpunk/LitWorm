# Recreation of Bookworm Adventures, a turn based word strategy game.

import pygame
import sys
import random
from dataclasses import dataclass, field
from typing import List

# letter tile
@dataclass
class Tile:
    letter: str
    value: int
    scoreMultiplier: float
    sprite: pygame.image
    playable: bool

# generates a default 4 x 4 board
def createDefaultBoard():
    return [createRow(4) for x in range(0,4)]

# board containing player's letters
@dataclass
class Board:
    tileRows: List[List[Tile]] = field(default_factory = createDefaultBoard)

# generates a row of tiles
def createRow(numTiles):
    return [createTile(1.0, True) for x in range(0, numTiles)]

# generates a new random tile 
def createTile(scoreMultiplier, playable):
    value_list = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 
              'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 
              'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 
              'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}
    tile = random.choice(list(value_list.keys()))
    tileName = "assets/letters/" + tile + ".png"
    return Tile(tile, value_list[tile], scoreMultiplier, pygame.image.load(tileName), playable)
 
# define a main function
def main():
    pygame.init()
    # sets font
    global myfont
    myfont = pygame.font.SysFont("monospace", 15)
    logo = pygame.image.load("assets/logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("LitWorm")
     
    screen = pygame.display.set_mode((500,500))
    
    running = True

    WHITE=(255,255,255)

    screen.fill(WHITE)

    playerBoard = Board()
    drawBoard(playerBoard,screen)
    pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
     
# draws an instance of a Board class on the pygame screen
def drawBoard(board, screen):
    y = 0
    for row in board.tileRows:
        x = 0
        for tile in row:
            screen.blit(tile.sprite, (x * 120, y * 120))
            x += 1
        y += 1
     
# run the main function only if this module is executed as the main script
if __name__=="__main__":
    main()