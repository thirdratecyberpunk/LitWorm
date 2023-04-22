import pygame
from enemy import Enemy

class RomanSoldier(Enemy):
    def __init__(self):
        super().__init__(
            min_possible_health=10,
            max_possible_health=20,
            min_possible_atk=0,
            max_possible_atk=10,
            sprite="assets/enemies/roman.png",
            name="Roman Soldier" 
        )