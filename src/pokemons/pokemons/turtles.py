import random

import pygame.transform

from src.pokemons.classes.pokemon import Pokemon
from src.pokemons.attacks.lick import Lick


class Turtles(Pokemon):
    def __init__(self, x:int, y:int):
        naam = random.choice(["Donnatello", "Leonardo", "Michelangelo", "Raphael"])
        super().__init__(x, y, f"assets/{naam}.png")

        self.name = naam
        self.max_hp = 100
        self.hp = self.max_hp
        self.speed = 20
        self.attack = 170

        self.moves = [(Lick(), 10, 10)]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))