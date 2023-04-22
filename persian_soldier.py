import pygame
from enemy import Enemy

class PersianSoldier(Enemy):
    def __init__(self):
        super().__init__(
            min_possible_health=30,
            max_possible_health=60,
            min_possible_atk=5,
            max_possible_atk=8,
            sprite="assets/enemies/persian.png",
            name="Persian Soldier" 
        )