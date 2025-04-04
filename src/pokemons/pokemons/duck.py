import pygame.transform

from src.pokemons.attacks.avadaKadavra import AvadaKadavra
from src.pokemons.attacks.magic import Magic
from src.pokemons.attacks.magicMissile import MagicMissile
from src.pokemons.attacks.peck import Peck
from src.pokemons.classes.pokermon import Pokermon



class Ducky(Pokermon):
    def __init__(self):
        super().__init__("assets/ducky.png")

        self.name = "Ducko"
        self.max_hp = 170
        self.hp = self.max_hp
        self.speed = 140
        self.attack = 140
        self.cost = 2

        self.moves = [

            [MagicMissile(), 10, 10],
            [AvadaKadavra(), 10, 10],
            [Magic(), 10, 10],
            [Peck(), 10, 10],

        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))