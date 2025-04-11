import pygame.transform

from src.pokemons.attacks.energyCut import EnergyCut
from src.pokemons.attacks.energyStab import EnergyStab
from src.pokemons.attacks.mudBomb import MudBomb
from src.pokemons.attacks.mudSlap import MudSlap
from src.pokemons.classes.pokermon import Pokermon


class Whooper(Pokermon):
    def __init__(self):
        super().__init__("assets/Energyzwordedwopper.png")

        self.name = "Whooooooooooo"
        self.max_hp = 145
        self.hp = self.max_hp
        self.speed = 90
        self.attack = 150
        self.cost = 3

        self.moves = [
            [MudSlap(), 10, 10],
            [EnergyStab(), 10, 10],
            [MudBomb(), 10, 10],
            [EnergyCut(), 10, 10],

        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))