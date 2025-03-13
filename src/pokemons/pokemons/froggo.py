import pygame.transform

from src.pokemons.classes.pokermon import Pokermon
from src.pokemons.attacks.lick import Lick


class Froggo(Pokermon):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, "assets/Evil_frog.png")

        self.name = "Froggo"
        self.max_hp = 70
        self.hp = self.max_hp
        self.speed = 150
        self.attack = 120

        self.moves = [[Lick(), 10, 10]]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))