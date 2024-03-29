import pygame
from enemies.enemy import Enemy

class PersianSoldier(Enemy):
    def __init__(self):
        super().__init__(
            min_possible_health=5,
            max_possible_health=10,
            min_possible_atk=5,
            max_possible_atk=8,
            sprite="assets/enemies/persian.png",
            name="Persian Soldier" 
        )