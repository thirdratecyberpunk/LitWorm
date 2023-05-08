import pygame
import random

class Player:
    def __init__(self, 
                 min_possible_health=100,
                 max_possible_health=100, 
                 sprite='assets/not_lex.png',
                 name="Not Lex"):
        self.max_health = random.randint(min_possible_health, max_possible_health)
        self.current_health = self.max_health
        self.sprite = pygame.image.load(sprite)
        self.name = name