import pygame.transform

from src.pokemons.classes.pokermon import Pokermon
from src.pokemons.attacks.lick import Lick


class Spider(Pokermon):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, "assets/spoeder.png")

        self.name = "Spoeder"
        self.max_hp = 90
        self.hp = self.max_hp
        self.speed = 90
        self.attack = 150

        self.moves = [[Lick(), 10, 10]]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))