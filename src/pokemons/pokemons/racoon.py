import pygame.transform

from src.pokemons.classes.pokemon import Pokemon
from src.pokemons.attacks.lick import Lick


class Racoon(Pokemon):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, "assets/Racoon.png")

        self.name = "Trash Panda"
        self.max_hp = 80
        self.hp = self.max_hp
        self.speed = 110
        self.attack = 130

        self.moves = [(Lick(), 10, 10)]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))