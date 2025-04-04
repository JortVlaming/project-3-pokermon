import pygame.transform

from src.pokemons.attacks.bugBite import BugBite
from src.pokemons.attacks.firstImpression import FirstImpression
from src.pokemons.attacks.lunge import Lunge
from src.pokemons.attacks.poisonFang import PoisonFang
from src.pokemons.classes.pokermon import Pokermon


class Spider(Pokermon):
    def __init__(self):
        super().__init__("assets/spoeder.png")

        self.name = "Spoeder"
        self.max_hp = 140
        self.hp = self.max_hp
        self.speed = 90
        self.attack = 150
        self.cost = 2

        self.moves = [
            [BugBite(), 10, 10],
            [FirstImpression(), 10, 10],
            [Lunge(), 10, 10],
            [PoisonFang(), 10, 10],

        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))