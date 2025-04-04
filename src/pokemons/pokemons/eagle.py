import pygame.transform

from src.pokemons.attacks.gun import Gun
from src.pokemons.attacks.peck import Peck
from src.pokemons.attacks.steelWing import SteelWing
from src.pokemons.attacks.windCutter import WindCutter
from src.pokemons.classes.pokermon import Pokermon



class Eagle(Pokermon):
    def __init__(self):
        super().__init__("assets/AREND.png")

        self.name = "'MERICA"
        self.max_hp = 210
        self.hp = self.max_hp
        self.speed = 180
        self.attack = 170
        self.cost =  4

        self.moves = [

            [Gun(), 10, 10],
            [WindCutter(), 10, 10],
            [SteelWing(), 10, 10],
            [Peck(), 10, 10],

        ]

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))