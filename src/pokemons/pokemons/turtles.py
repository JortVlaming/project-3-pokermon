import random

import pygame.transform

from src.pokemons.attacks.explosion import Explosion
from src.pokemons.attacks.tackle import Tackle
from src.pokemons.classes.pokermon import Pokermon



class Turtles(Pokermon):
    def __init__(self, x:int, y:int):
        naam = random.choice(["Donnatello", "Leonardo", "Michelangelo", "Raphael"])
        super().__init__(x, y, f"assets/{naam}.png")

        self.name = naam
        self.max_hp = 100
        self.hp = self.max_hp
        self.speed = 20
        self.attack = 170

        self.moves = [
            [Explosion(), 1, 1],
            [Tackle(), 10, 10],
            [Head]
        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))