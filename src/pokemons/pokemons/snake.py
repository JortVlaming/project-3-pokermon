﻿import pygame.transform

from src.pokemons.classes.pokemon import Pokemon
from src.pokemons.attacks.lick import Lick
from src.pokemons.attacks.poisonFang import PoisonFang


class Snake(Pokemon):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, "assets/snek.png")

        self.name = "Snek"
        self.max_hp = 100
        self.hp = self.max_hp
        self.speed = 140
        self.attack = 170

        self.moves = [
            [(Lick(), 10, 10)],
            [PoisonFang(), 10, 10],

        ]


        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))