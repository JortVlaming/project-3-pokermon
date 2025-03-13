import pygame.transform

from src.pokemons.classes.pokemon import Pokemon
from src.pokemons.attacks.lick import Lick


class Fox(Pokemon):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, "assets/Foxie.png")

        self.name = "Foxie"
        self.max_hp = 70
        self.hp = self.max_hp
        self.speed = 170
        self.attack = 160

        self.moves = [(Lick(), 10, 10)]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))