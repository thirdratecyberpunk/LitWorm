import random
import pygame

class Cell:
    """
    Class representing a Tile the player can select to assemble words
    """
    def __init__(self, x, y, letter, value):
        self.clicked = False
        self.letter = letter
        self.value = value
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
        else:
            self.sprite = pygame.image.load(self.letterName)
        return self

    def set_unclicked(self):
        if self.clicked:
            self.sprite = pygame.image.load(self.letterName)
            self.clicked = False
        return self

    def set_clicked(self):
        if not self.clicked:
            self.sprite = pygame.image.load(self.grayscaleLetterName)
            self.clicked = True
        return self

    def check_click(self, mouse_position):
        """
        Returns whether the current mouse position is colliding with hitbox
        """
        return pygame.Rect.collidepoint(self.rect, mouse_position)

    def __str__(self):
        return str(self.letter)