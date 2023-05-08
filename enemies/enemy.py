import pygame
import random

class Enemy:
    def __init__(self, 
                 min_possible_health,
                 max_possible_health, 
                 min_possible_atk, 
                 max_possible_atk,
                 sprite,
                 name):
        self.max_health = random.randint(min_possible_health, max_possible_health)
        self.current_health = self.max_health
        self.max_possible_atk = max_possible_atk
        self.min_possible_atk = min_possible_atk
        self.sprite = pygame.image.load(sprite)
        self.name = name
        print(f"New enemy {self.name} with {self.current_health}/{self.max_health}")

    def deal_damage(self, num_damage):
        self.current_health -= num_damage

    def is_dead(self):
        return self.current_health <= 0
    
    def attack(self):
        return random.rand(self.min_possible_attack, self.max_possible_attack)