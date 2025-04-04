import pygame.transform

from src.pokemons.attacks.bite import Bite
from src.pokemons.attacks.feintAttack import FeintAttack
from src.pokemons.attacks.foulPlay import FoulPlay
from src.pokemons.attacks.headbutt import Headbutt
from src.pokemons.classes.pokermon import Pokermon



class Racoon(Pokermon):
    def __init__(self):
        super().__init__("assets/Racoon.png")

        self.name = "Trash Panda"
        self.max_hp = 140
        self.hp = self.max_hp
        self.speed = 110
        self.attack = 130
        self.cost = 2

        self.moves = [
            [Headbutt(), 10, 10],
            [Bite(), 10, 10],
            [FeintAttack(), 10, 10],
            [FoulPlay(), 10, 10],

        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))