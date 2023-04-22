import pygame
from enemy import Enemy

class Minotaur(Enemy):
    def __init__(self):
        super().__init__(
            min_possible_health=10,
            max_possible_health=15,
            min_possible_atk=10,
            max_possible_atk=15,
            sprite="assets/enemies/minotaur.png",
            name="Minotaur" 
        )